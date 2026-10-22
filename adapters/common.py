"""Shared layer for EngineeringOS editor adapters. Stdlib only.

Everything an adapter needs that is not editor-specific lives here:

- load_source(): read + validate the neutral source (agents/, skills/, commands/)
- parse_frontmatter() / emit_yaml(): the small YAML subset our files use. The
  parser fails loudly on anything outside that subset instead of guessing.
- Writer: ownership-tracked file installer (never clobbers files it did not
  write, prunes only what it wrote).
- JSON / JSONC helpers with atomic, backed-up writes.
- grants(): permission semantics (fail closed: only the exact value "allow").
"""
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST = ".engineeringos-manifest.json"
MCP_NAME = "engineering-memory"
ROLES = ("primary", "subagent")
MODEL_TIERS = ("deep", "standard", "fast")
EFFECTS = ("allow", "ask", "deny")

AGENT_KEYS = {"name", "description", "role", "model_tier", "permissions", "targets"}
COMMAND_KEYS = {"description", "targets"}
SKILL_KEYS = {"name", "description", "metadata", "targets"}


class SourceError(ValueError):
    """Raised when a neutral source file is invalid. Message carries file:line."""


def log(adapter, msg):
    print(f"[eng]   {adapter}: {msg}")


# --- YAML subset ----------------------------------------------------------------
# Supported: nested maps by indentation, block lists of scalars or maps, quoted or
# bare keys, plain/quoted scalars, folded (>, >-) and literal (|, |-) blocks,
# comments. Not supported (raises): flow collections, anchors/aliases, tabs,
# multi-document.

def _indent(line):
    return len(line) - len(line.lstrip(" "))


_TYPED = re.compile(r"^(-?\d+)$|^(-?\d+\.\d+)$|^(true|false)$")


def _quoted(s, where):
    """Parse a leading quoted string; return (value, rest-of-line)."""
    q = s[0]
    if q == '"':
        i = 1
        while i < len(s):
            if s[i] == "\\":
                i += 2
                continue
            if s[i] == '"':
                break
            i += 1
        if i >= len(s):
            raise SourceError(f"{where}: unterminated double-quoted string")
        try:
            return json.loads(s[:i + 1]), s[i + 1:]
        except ValueError:
            raise SourceError(f"{where}: unsupported escape in double-quoted string {s[:i + 1]!r}")
    i = 1
    while i < len(s):
        if s[i] == "'":
            if s[i + 1:i + 2] == "'":
                i += 2
                continue
            break
        i += 1
    if i >= len(s):
        raise SourceError(f"{where}: unterminated single-quoted string")
    return s[1:i].replace("''", "'"), s[i + 1:]


def _scalar(s, where, typed=False):
    s = s.strip()
    if s[:1] in "\"'":
        val, rest = _quoted(s, where)
        rest = rest.strip()
        if rest and not rest.startswith("#"):
            raise SourceError(f"{where}: unexpected text after quoted value: {rest!r}")
        return val
    if s[:1] in ("[", "{", "&", "*", "!", "|", ">", "~"):
        raise SourceError(f"{where}: unsupported YAML value {s!r}")
    val = re.sub(r"\s+#.*$", "", s)
    if typed:
        m = _TYPED.match(val)
        if m:
            return int(val) if m.group(1) else float(val) if m.group(2) else val == "true"
    return val


def _key(s, where):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if not s:
        raise SourceError(f"{where}: empty key")
    return s


def _split_key(line, where):
    s = line.strip()
    if s[0] in "\"'":
        q = s[0]
        end = s.find(q, 1)
        if end == -1 or s[end + 1:end + 2] != ":":
            raise SourceError(f"{where}: malformed quoted key")
        return s[:end + 1], s[end + 2:]
    if ":" not in s:
        raise SourceError(f"{where}: expected 'key: value'")
    k, _, rest = s.partition(":")
    return k, rest


def _is_map_item(item, where):
    """True for `- key: value` (including a quoted key), False for `- scalar`."""
    if item[:1] in ("\"", "'"):
        try:
            _, rest = _quoted(item, where)
        except SourceError:
            return False
        return rest.strip().startswith(":")
    return ":" in item


def _parse_list(lines, i, indent, src, base, typed=False):
    """Block sequence at `indent`: `- scalar`, or `- key: value` plus a nested map.

    Items are re-indented to `indent + 2` and handed to _parse_block, so map items
    reuse the whole map grammar (nested maps, quoted values, comments).
    """
    out = []
    while i < len(lines):
        line = lines[i]
        where = f"{src}:{base + i + 1}"
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        ind = _indent(line)
        if ind < indent:
            break
        if ind > indent:
            raise SourceError(f"{where}: unexpected indentation")
        s = line.strip()
        if not s.startswith("- "):
            break
        item = s[2:].strip()
        j = i + 1
        while j < len(lines) and lines[j].strip() and _indent(lines[j]) > indent:
            j += 1
        if _is_map_item(item, where):
            block = [" " * (indent + 2) + item] + lines[i + 1:j]
            val, end = _parse_block(block, 0, indent + 2, src, base + i, typed)
            if end != len(block):
                # A line indented less than the item's map would otherwise vanish.
                raise SourceError(f"{where}: unexpected indentation in this list item")
            out.append(val)
        else:
            if j > i + 1:
                raise SourceError(f"{where}: a scalar list item cannot have nested lines")
            out.append(_scalar(item, where, typed))
        i = j
    return out, i


def _parse_block(lines, i, indent, src, base, typed=False):
    out = {}
    while i < len(lines):
        line = lines[i]
        where = f"{src}:{base + i + 1}"
        if "\t" in line[:_indent(line) + 1]:
            raise SourceError(f"{where}: tabs are not allowed in frontmatter")
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        ind = _indent(line)
        if ind < indent:
            break
        if ind > indent:
            raise SourceError(f"{where}: unexpected indentation")
        if line.lstrip().startswith("- "):
            raise SourceError(f"{where}: a list cannot be a mapping key's sibling; put it under a key")
        rawk, rest = _split_key(line, where)
        key, rest = _key(rawk, where), rest.strip()
        if key in out:
            raise SourceError(f"{where}: duplicate key {key!r}")
        i += 1
        if rest in (">", ">-", "|", "|-"):
            buf = []
            while i < len(lines) and (not lines[i].strip() or _indent(lines[i]) > ind):
                buf.append(lines[i].strip())
                i += 1
            out[key] = " ".join(b for b in buf if b) if rest.startswith(">") else "\n".join(buf).strip()
        elif rest == "" or rest.startswith("#"):
            j = i
            while j < len(lines) and (not lines[j].strip() or lines[j].lstrip().startswith("#")):
                j += 1
            if j < len(lines) and lines[j].strip() and _indent(lines[j]) > ind:
                child = _indent(lines[j])
                nested = _parse_list if lines[j].lstrip().startswith("- ") else _parse_block
                out[key], i = nested(lines, j, child, src, base, typed)
            else:
                out[key] = ""
        else:
            out[key] = _scalar(rest, where, typed)
    return out, i


def parse_frontmatter(text, src="<text>", typed=False):
    """Return (frontmatter dict, body). Body is returned byte-for-byte.

    Scalars are strings. With typed=True, unquoted integers, decimals and
    true/false become int/float/bool (what a real YAML parser would produce);
    tests use this to catch quoting drift.
    """
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 3)
    if end == -1:
        raise SourceError(f"{src}: frontmatter is not closed with '---'")
    fm, _ = _parse_block(text[4:end].splitlines(), 0, 0, src, 1, typed)
    return fm, text[end + 5:]


_BARE_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")
_RAW_SCALAR = re.compile(r"^(-?\d+(\.\d+)?|true|false)$")


def _emit_key(k):
    return k if _BARE_KEY.match(k) else json.dumps(k, ensure_ascii=False)


# Bare words a YAML 1.1/1.2 parser would read as bool/null instead of a string.
_YAML_SPECIAL = {"null", "true", "false", "yes", "no", "on", "off", "y", "n", "nan", "inf"}


def _emit_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    v = str(v)
    if _RAW_SCALAR.match(v):
        # Our sources keep numbers/booleans unquoted, and the parser returns them
        # as strings, so round-tripping must keep them unquoted (temperature: 0.1).
        return v
    if _BARE_KEY.match(v) and v.lower() not in _YAML_SPECIAL:
        return v
    return json.dumps(v, ensure_ascii=False)


def emit_yaml(mapping, indent=0):
    """Order-preserving emitter for the same subset parse_frontmatter reads."""
    pad, out = " " * indent, []
    for k, v in mapping.items():
        if isinstance(v, dict):
            out.append(f"{pad}{_emit_key(k)}:")
            out.append(emit_yaml(v, indent + 2))
        elif isinstance(v, list):
            out.append(f"{pad}{_emit_key(k)}:")
            for item in v:
                if isinstance(item, dict):
                    lines = emit_yaml(item, indent + 4).splitlines()
                    out.append(f"{pad}  - {lines[0].strip()}")
                    out.extend(lines[1:])
                else:
                    out.append(f"{pad}  - {_emit_scalar(item)}")
        else:
            out.append(f"{pad}{_emit_key(k)}: {_emit_scalar(v)}")
    return "\n".join(line for line in out if line != "")


def render_frontmatter(fm, body):
    return "---\n" + emit_yaml(fm) + "\n---\n" + body


# --- neutral source -------------------------------------------------------------

@dataclass
class Item:
    name: str
    fm: dict
    body: str
    path: Path

    def target(self, editor):
        t = self.fm.get("targets", {})
        return t.get(editor, {}) if isinstance(t, dict) else {}


@dataclass
class Skill(Item):
    files: list = field(default_factory=list)  # (relative Path, absolute Path) for non-SKILL.md files


@dataclass
class Source:
    root: Path
    agents: list
    skills: list
    commands: list

    def primary(self):
        return [a for a in self.agents if a.fm.get("role") == "primary"]

    def subagents(self):
        return [a for a in self.agents if a.fm.get("role") == "subagent"]


def _check_keys(fm, allowed, src):
    extra = set(fm) - allowed
    if extra:
        raise SourceError(f"{src}: unknown frontmatter keys {sorted(extra)} (allowed: {sorted(allowed)})")
    if "targets" in fm:
        t = fm["targets"]
        if not isinstance(t, dict) or not all(isinstance(v, dict) for v in t.values()):
            raise SourceError(f"{src}: 'targets' must be a map of editor -> settings map")


def load_source(root):
    root = Path(root)
    agents, skills, commands = [], [], []
    for p in sorted((root / "agents").glob("*.md")):
        rel = p.relative_to(root)
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"), str(rel))
        _check_keys(fm, AGENT_KEYS, rel)
        if fm.get("name") != p.stem:
            raise SourceError(f"{rel}: 'name' must equal the file name ({p.stem!r})")
        if not fm.get("description"):
            raise SourceError(f"{rel}: 'description' is required")
        if fm.get("role") not in ROLES:
            raise SourceError(f"{rel}: 'role' must be one of {ROLES}")
        if "model_tier" in fm and fm["model_tier"] not in MODEL_TIERS:
            raise SourceError(f"{rel}: 'model_tier' must be one of {MODEL_TIERS}")
        if "permissions" in fm and not isinstance(fm["permissions"], dict):
            raise SourceError(f"{rel}: 'permissions' must be a map")
        for cap, rule in fm.get("permissions", {}).items():
            if isinstance(rule, dict):
                if "*" in rule and next(iter(rule)) != "*":
                    # Editors differ on rule precedence (OpenCode: last match wins).
                    # A leading "*" default is the only shape every adapter reads the same way.
                    raise SourceError(f"{rel}: permissions.{cap}: the \"*\" default must be the first rule")
                bad = [k for k, v in rule.items() if v not in EFFECTS]
                if bad:
                    raise SourceError(f"{rel}: permissions.{cap}: effect for {bad} must be one of {EFFECTS}")
            elif rule not in EFFECTS:
                raise SourceError(f"{rel}: permissions.{cap}: must be one of {EFFECTS} "
                                  "or a map of pattern -> effect")
        agents.append(Item(p.stem, fm, body, p))
    sroot = root / "skills"
    for d in sorted(x for x in sroot.iterdir() if x.is_dir()) if sroot.is_dir() else []:
        sk = d / "SKILL.md"
        rel = sk.relative_to(root)
        if not sk.is_file():
            raise SourceError(f"{rel}: missing")
        fm, body = parse_frontmatter(sk.read_text(encoding="utf-8"), str(rel))
        _check_keys(fm, SKILL_KEYS, rel)
        if fm.get("name") != d.name:
            raise SourceError(f"{rel}: 'name' must equal the directory name ({d.name!r})")
        files = [(f.relative_to(d), f) for f in sorted(d.rglob("*")) if f.is_file() and f != sk]
        skills.append(Skill(d.name, fm, body, sk, files))
    for p in sorted((root / "commands").glob("*.md")):
        rel = p.relative_to(root)
        fm, body = parse_frontmatter(p.read_text(encoding="utf-8"), str(rel))
        _check_keys(fm, COMMAND_KEYS, rel)
        if not fm.get("description"):
            raise SourceError(f"{rel}: 'description' is required")
        commands.append(Item(p.stem, fm, body, p))
    if not agents:
        raise SourceError(f"{root}/agents: no agent definitions found")
    return Source(root, agents, skills, commands)


def grants(value):
    """Permission semantics shared by every adapter: fail closed."""
    return value == "allow"


# --- context ----------------------------------------------------------------------

@dataclass
class Context:
    engine: Path
    data: Path
    python: str
    home: Path
    env: dict
    options: dict = field(default_factory=dict)

    @property
    def server(self):
        return self.engine / "mcp" / MCP_NAME / "server.py"


# --- file installer ----------------------------------------------------------------

class Writer:
    """Installs generated files into an editor's config dir.

    A path is owned (may be written) if the previous manifest lists it, if it
    does not exist yet, or if it already holds exactly the bytes we would write.
    adopt_legacy (OpenCode only) additionally takes over existing paths when no
    manifest exists yet, to migrate installs made by the old copy-based sync,
    which overwrote unconditionally. Note this also applies if the manifest is
    deleted later. Ownership is by path: owned files are rewritten even if hand
    edited, because generated files must not be edited. Unowned paths are
    reported as SKIPPED, never touched.
    finish() prunes owned files we no longer produce and saves the manifest.
    """

    def __init__(self, root, adapter, adopt_legacy=False):
        self.root = Path(root)
        self.adapter = adapter
        self.manifest = self.root / MANIFEST
        self.owned = set()
        self.first_run = not self.manifest.exists()
        if not self.first_run:
            try:
                self.owned = set(json.loads(self.manifest.read_text(encoding="utf-8")).get("files", []))
            except ValueError:
                self.owned = set()
        self.adopt_legacy = adopt_legacy and self.first_run
        self.produced, self.skipped, self.changed = [], [], 0

    def _mine(self, path, data):
        if str(path) in self.owned or not path.exists() or self.adopt_legacy:
            return True
        return path.read_bytes() == data

    def write(self, path, content):
        data = content.encode("utf-8") if isinstance(content, str) else content
        if not self._mine(path, data):
            self.skipped.append(path)
            return False
        self.produced.append(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() == data:
            return False
        path.write_bytes(data)
        self.changed += 1
        return True

    def wrote(self, path):
        return path in self.produced

    def finish(self):
        now = {str(p) for p in self.produced}
        for stale in sorted(self.owned - now):
            sp = Path(stale)
            if sp.is_file() and self.root in sp.parents:
                sp.unlink()
                self.changed += 1
                parent = sp.parent
                while parent != self.root and parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent
        write_text_if_changed(self.manifest, json.dumps({"files": sorted(now)}, indent=2) + "\n")
        for p in self.skipped:
            log(self.adapter, f"SKIPPED {p} (exists and was not written by EngineeringOS; rename or remove it to let sync manage it)")


def write_text_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


# --- JSON / JSONC ---------------------------------------------------------------------

def strip_jsonc(s):
    """JSONC -> JSON: remove // and /* */ comments and trailing commas outside strings."""
    return _strip_trailing_commas(_strip_comments(s))


def _strip_trailing_commas(s):
    out, in_str, i, n = [], False, 0, len(s)
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(s[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
        elif c == '"':
            in_str = True
            out.append(c)
        elif c == ",":
            j = i + 1
            while j < n and s[j] in " \t\r\n":
                j += 1
            if j < n and s[j] in "}]":
                i += 1
                continue
            out.append(c)
        else:
            out.append(c)
        i += 1
    return "".join(out)


def _strip_comments(s):
    out, i, n, in_str = [], 0, len(s), False
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(s[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "/":
            while i < n and s[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "*":
            i += 2
            while i + 1 < n and not (s[i] == "*" and s[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def load_json(path, jsonc=False):
    path = Path(path)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(strip_jsonc(text) if jsonc else (text or "{}")) if text.strip() else {}
    except ValueError as exc:
        raise SystemExit(f"[eng]   FAIL: {path} is not valid JSON ({exc}); not touching it")


def atomic_write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = path.with_name(path.name + ".engineeringos.bak")
    if path.exists() and not backup.exists():
        # Keep the FIRST backup: it is the user's original (with any JSONC
        # comments, which are not preserved on write). Later writes do not
        # overwrite it.
        shutil.copy2(path, backup)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2)
            fh.write("\n")
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
