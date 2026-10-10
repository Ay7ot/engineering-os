#!/usr/bin/env python3
"""Sync EngineeringOS into Claude Code. Called by `eng sync-claude` / `eng health`.

`opencode/` stays the single source of truth. This script translates it into
Claude Code's layout:

  opencode/agents/*.md (subagents) -> <claude_dir>/agents/*.md
      permission map -> disallowedTools + PreToolUse hooks (claude/hooks/eos_guard.py)
  opencode/agents/lead.md (primary) -> <claude_dir>/output-styles/eos-lead.md
      ("EngineeringOS Lead" output style, set as the default outputStyle in
      <claude_dir>/settings.json unless the user already picked another style)
  opencode/skills/*/                -> <claude_dir>/skills/*/
  opencode/commands/*.md            -> <claude_dir>/commands/*.md
  always-on context                 -> managed block in <claude_dir>/CLAUDE.md
  engineering-memory MCP            -> user-scope mcpServers (via `claude mcp` when
                                       the CLI exists, else merged into <claude_json>)

Names that collide with Claude Code built-ins are prefixed with `eos-`.
Idempotent. Files it wrote before but no longer produces are removed (tracked in
a manifest). Files it did not write are never overwritten or deleted. Stdlib only.
"""
import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MCP_NAME = "engineering-memory"
MANIFEST = ".engineeringos-manifest.json"
BLOCK_BEGIN = "<!-- BEGIN EngineeringOS (managed by `eng sync-claude`; edits inside this block are overwritten) -->"
BLOCK_END = "<!-- END EngineeringOS -->"
STYLE_FILE = "eos-lead.md"
STYLE_NAME = "EngineeringOS Lead"

# Avoid shadowing Claude Code built-in skills/commands.
SKILL_RENAMES = {"code-review": "eos-code-review", "security-review": "eos-security-review"}
COMMAND_RENAMES = {"review": "eos-review", "debug": "eos-debug"}

# OpenCode models are not Claude models; pick by role.
AGENT_MODELS = {
    "architect": "opus",
    "reviewer": "opus",
    "security": "opus",
    "researcher": "sonnet",
    "planner": "sonnet",
    "builder": "sonnet",
    "tester": "sonnet",
    "explorer": "haiku",
}

TOOL_NOTE = (
    "> Claude Code tool names: read -> Read, glob/list -> Glob, grep -> Grep, "
    "edit -> Edit/Write, bash -> Bash, webfetch -> WebFetch, websearch -> WebSearch, "
    "todowrite -> TodoWrite, task -> Agent, skill -> Skill. "
    "EngineeringOS memory tools are `mcp__engineering-memory__*`."
)


def log(msg):
    print(f"[eng]   claude: {msg}")


# --- minimal frontmatter parser (the subset our definitions use) -------------

def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    # Unquoted scalar: drop a trailing YAML comment ("deny  # read-only").
    return re.sub(r"\s+#.*$", "", s)


def _parse_block(lines, i, indent):
    out = {}
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        ind = _indent(line)
        if ind < indent:
            break
        key, _, rest = line.strip().partition(":")
        key, rest = _unquote(key), rest.strip()
        i += 1
        if rest in (">", ">-", "|", "|-"):
            buf = []
            while i < len(lines) and (not lines[i].strip() or _indent(lines[i]) > ind):
                buf.append(lines[i].strip())
                i += 1
            out[key] = " ".join(b for b in buf if b) if rest.startswith(">") else "\n".join(buf).strip()
        elif rest == "" or rest.startswith("#"):
            if i < len(lines) and lines[i].strip() and _indent(lines[i]) > ind:
                out[key], i = _parse_block(lines, i, _indent(lines[i]))
            else:
                out[key] = ""
        else:
            out[key] = _unquote(rest)
    return out, i


def split_frontmatter(text):
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 3)
    if end == -1:
        return {}, text
    fm, _ = _parse_block(text[4:end].splitlines(), 0, 0)
    return fm, text[end + 5:]


def q(s):
    """YAML-safe double-quoted scalar (JSON strings are valid YAML)."""
    return json.dumps(s, ensure_ascii=False)


def rename_refs(text):
    for old, new in SKILL_RENAMES.items():
        # Bare names ("the `code-review` skill") and installed paths
        # ("~/.claude/skills/code-review/"). opencode/skills/<old> source paths stay.
        text = re.sub(r"(?<![\w/-])" + re.escape(old) + r"(?![\w-])", new, text)
        text = re.sub(r"(\.claude/skills/)" + re.escape(old) + r"(?![\w-])", r"\g<1>" + new, text)
    for old, new in COMMAND_RENAMES.items():
        text = re.sub(r"(?<![\w-])/" + re.escape(old) + r"(?![\w-])", "/" + new, text)
    return text


# --- translation --------------------------------------------------------------

def _guard_cmd(py, guard, mode, allow=(), deny=(), protect=()):
    parts = [py, str(guard), mode]
    for p in allow:
        parts += ["--allow", p]
    for p in deny:
        parts += ["--deny", p]
    for p in protect:
        parts += ["--protect", str(p)]
    return " ".join(shlex.quote(p) for p in parts)


def translate_permissions(perm, py, guard, protect=()):
    """Return (disallowed_tools, [(matcher, command)]).

    Fails closed: only the exact value "allow" grants a capability. Anything
    else ("deny", OpenCode's "ask", typos) removes it, because Claude Code
    subagents have no interactive "ask" equivalent we can rely on here.
    """
    disallowed, hooks = [], []
    if not isinstance(perm, dict):
        return disallowed, hooks

    edit = perm.get("edit", "allow")
    if isinstance(edit, dict):
        if edit.get("*", "allow") != "allow":
            globs = [k for k, v in edit.items() if k != "*" and v == "allow"]
            if globs:
                hooks.append(("Edit|Write|NotebookEdit", _guard_cmd(py, guard, "edit", allow=globs, protect=protect)))
            else:
                disallowed += ["Edit", "Write", "NotebookEdit"]
    elif edit != "allow":
        disallowed += ["Edit", "Write", "NotebookEdit"]

    bash = perm.get("bash", "allow")
    if isinstance(bash, dict):
        rules = {k: v for k, v in bash.items() if k != "*"}
        if bash.get("*", "allow") != "allow":
            allow = [k for k, v in rules.items() if v == "allow"]
            if allow:
                hooks.append(("Bash", _guard_cmd(py, guard, "bash", allow=allow)))
            else:
                disallowed.append("Bash")
        else:
            deny = [k for k, v in rules.items() if v != "allow"]
            if deny:
                hooks.append(("Bash", _guard_cmd(py, guard, "bash", deny=deny)))
    elif bash != "allow":
        disallowed.append("Bash")

    for key, tool in (("webfetch", "WebFetch"), ("websearch", "WebSearch"), ("task", "Agent")):
        if key in perm and perm[key] != "allow":
            disallowed.append(tool)
    return disallowed, hooks


def render_agent(name, fm, body, source, py, guard, protect):
    disallowed, hooks = translate_permissions(fm.get("permission"), py, guard, protect)
    out = ["---", f"name: {name}", f"description: {q(fm.get('description', name))}"]
    out.append(f"model: {AGENT_MODELS.get(name, 'inherit')}")
    if disallowed:
        out.append("disallowedTools: " + ", ".join(disallowed))
    if hooks:
        out += ["hooks:", "  PreToolUse:"]
        for matcher, cmd in hooks:
            out += [
                f"    - matcher: {q(matcher)}",
                "      hooks:",
                "        - type: command",
                f"          command: {q(cmd)}",
            ]
    out.append("---")
    out.append(f"<!-- Generated by `eng sync-claude` from {source}. Edit the source, not this file. -->")
    out.append("")
    out.append(TOOL_NOTE)
    out.append("")
    return "\n".join(out) + "\n" + rename_refs(body.lstrip("\n"))


def render_skill(name, fm, body):
    out = ["---", f"name: {name}", f"description: {q(rename_refs(fm.get('description', name)))}", "---"]
    return "\n".join(out) + "\n" + rename_refs(body)


def render_command(fm, body):
    out = ["---", f"description: {q(fm.get('description', ''))}", "---"]
    return "\n".join(out) + "\n" + rename_refs(body)


def render_style(fm, body, agents):
    out = [
        "---",
        f"name: {q(STYLE_NAME)}",
        f"description: {q('EngineeringOS Lead: orchestrate specialist subagents, approval gates, persistent engineering memory')}",
        "keep-coding-instructions: true",
        "---",
        "<!-- Generated by `eng sync-claude` from opencode/agents/lead.md. Edit the source, not this file. -->",
        "",
        "You are running in the EngineeringOS Lead mode. Delegate with the Agent tool to the EngineeringOS "
        "subagents: " + ", ".join(f"`{a}`" for a in agents) + ". Prefer them over the built-in Explore/Plan "
        "agents when following EngineeringOS workflows.",
        "",
        TOOL_NOTE,
        "",
    ]
    return "\n".join(out) + "\n" + rename_refs(body.strip()) + "\n"


def render_claude_block(engine, data, agents, commands):
    lines = [
        BLOCK_BEGIN,
        "# EngineeringOS",
        "",
        f"@{engine}/PRINCIPLES.md",
        f"@{data}/USER.md",
        "",
        f"- The `{MCP_NAME}` MCP server (`mcp__{MCP_NAME}__*`) is the system of record for project context, ADRs, "
        "research, tasks and state. Claude Code's built-in auto-memory is only for personal working preferences; "
        "durable project knowledge goes to EngineeringOS.",
        "- Project rules: if a repo has `AGENTS.md` but no `CLAUDE.md`, read `AGENTS.md`.",
        "- EngineeringOS subagents: " + ", ".join(f"`{a}`" for a in agents) + ".",
        "- Workflows: " + ", ".join(f"`/{c}`" for c in commands) + ".",
        f"- The orchestration role lives in the `{STYLE_NAME}` output style.",
        BLOCK_END,
    ]
    return "\n".join(lines) + "\n"


# --- filesystem helpers --------------------------------------------------------

class Writer:
    """Writes generated files, never clobbering files it does not own.

    A path is owned if the previous manifest lists it, if it does not exist yet,
    or if it already has exactly the content we would write.
    """

    def __init__(self, cdir):
        self.cdir = cdir
        self.manifest = cdir / MANIFEST
        self.owned = set()
        if self.manifest.exists():
            try:
                self.owned = set(json.loads(self.manifest.read_text(encoding="utf-8")).get("files", []))
            except ValueError:
                self.owned = set()
        self.produced, self.skipped, self.changed = [], [], 0

    def mine(self, path, content=None):
        if str(path) in self.owned or not path.exists():
            return True
        return content is not None and path.read_bytes() == content

    def write(self, path, content):
        data = content.encode("utf-8") if isinstance(content, str) else content
        if not self.mine(path, data):
            self.skipped.append(path)
            return False
        self.produced.append(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() == data:
            return False
        path.write_bytes(data)
        self.changed += 1
        return True

    def finish(self):
        now = {str(p) for p in self.produced}
        for stale in sorted(self.owned - now):
            sp = Path(stale)
            if sp.is_file() and self.cdir in sp.parents:
                sp.unlink()
                self.changed += 1
                parent = sp.parent
                while parent != self.cdir and parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent
        write_if_changed(self.manifest, json.dumps({"files": sorted(now)}, indent=2) + "\n")
        for p in self.skipped:
            log(f"SKIPPED {p} (exists and was not written by EngineeringOS; rename or remove it to let sync manage it)")


def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8") or "{}")
    except ValueError:
        sys.exit(f"[eng]   FAIL: {path} is not valid JSON; not touching it")


def atomic_write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_name(path.name + ".engineeringos.bak"))
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


def merge_claude_md(path, block):
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    pattern = re.compile(re.escape(BLOCK_BEGIN) + r".*?" + re.escape(BLOCK_END) + r"\n?", re.S)
    if pattern.search(text):
        new = pattern.sub(lambda _: block, text, count=1)
    else:
        new = (text.rstrip("\n") + "\n\n" if text.strip() else "") + block
    return write_if_changed(path, new)


def set_default_style(settings_path):
    """Make the Lead style the default unless the user already chose another."""
    cfg = load_json(settings_path)
    current = cfg.get("outputStyle")
    if current == STYLE_NAME:
        return "already default"
    if current not in (None, "", "default"):
        return f"left your outputStyle {current!r} in place (set it to {STYLE_NAME!r} to use the Lead mode)"
    cfg["outputStyle"] = STYLE_NAME
    atomic_write_json(settings_path, cfg)
    return f"set default outputStyle to {STYLE_NAME!r} in {settings_path}"


def mcp_entry(py, engine, data):
    return {
        "type": "stdio",
        "command": py,
        "args": [str(engine / "mcp" / MCP_NAME / "server.py")],
        "env": {"ENGINEERING_OS_DATA": str(data)},
    }


def read_mcp(claude_json):
    return load_json(claude_json).get("mcpServers", {}).get(MCP_NAME)


def configure_mcp(claude_json, entry, claude_cli):
    if read_mcp(claude_json) == entry:
        return f"{MCP_NAME} MCP already configured"
    if claude_cli:
        # Let Claude Code write its own config file: no lost-update race with a
        # running instance.
        subprocess.run([claude_cli, "mcp", "remove", "--scope", "user", MCP_NAME],
                       capture_output=True, text=True)
        res = subprocess.run([claude_cli, "mcp", "add-json", "--scope", "user", MCP_NAME, json.dumps(entry)],
                             capture_output=True, text=True)
        if res.returncode == 0:
            return f"configured {MCP_NAME} MCP via `claude mcp add-json` (user scope)"
        log(f"`claude mcp add-json` failed ({res.stderr.strip() or res.returncode}); editing {claude_json} directly")
    cfg = load_json(claude_json)
    cfg.setdefault("mcpServers", {})[MCP_NAME] = entry
    atomic_write_json(claude_json, cfg)
    if read_mcp(claude_json) != entry:
        sys.exit(f"[eng]   FAIL: {MCP_NAME} entry did not persist in {claude_json}")
    return (f"configured {MCP_NAME} MCP in {claude_json} (backup: *.engineeringos.bak). "
            "If Claude Code was running, restart it, then run 'eng health' to confirm the entry survived")


# --- commands -------------------------------------------------------------------

def sync(a):
    engine, data, cdir = Path(a.engine), Path(a.data), Path(a.claude_dir)
    guard = engine / "claude" / "hooks" / "eos_guard.py"
    protect = [cdir, engine / "claude", engine / "opencode"]
    oc = engine / "opencode"
    w = Writer(cdir)
    agents, commands, lead = [], [], None

    for src in sorted((oc / "agents").glob("*.md")):
        fm, body = split_frontmatter(src.read_text(encoding="utf-8"))
        name = src.stem
        if fm.get("mode") == "primary":
            if name == "lead":
                lead = (fm, body)
            continue
        dest = cdir / "agents" / f"{name}.md"
        w.write(dest, render_agent(name, fm, body, f"opencode/agents/{src.name}", a.python, guard, protect))
        if dest in w.produced:
            agents.append(name)

    skills_dir = oc / "skills"
    for sdir in sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []:
        name = SKILL_RENAMES.get(sdir.name, sdir.name)
        for f in sorted(sdir.rglob("*")):
            if not f.is_file():
                continue
            dest = cdir / "skills" / name / f.relative_to(sdir)
            if f.name == "SKILL.md":
                fm, body = split_frontmatter(f.read_text(encoding="utf-8"))
                w.write(dest, render_skill(name, fm, body))
            else:
                w.write(dest, f.read_bytes())

    for src in sorted((oc / "commands").glob("*.md")):
        fm, body = split_frontmatter(src.read_text(encoding="utf-8"))
        name = COMMAND_RENAMES.get(src.stem, src.stem)
        dest = cdir / "commands" / f"{name}.md"
        w.write(dest, render_command(fm, body))
        if dest in w.produced:
            commands.append(name)

    if lead:
        w.write(cdir / "output-styles" / STYLE_FILE, render_style(lead[0], lead[1], agents))

    w.finish()
    log(f"{len(agents)} agents, {len(commands)} commands, skills, output style synced ({w.changed} files changed)")

    if merge_claude_md(cdir / "CLAUDE.md", render_claude_block(engine, data, agents, commands)):
        log(f"updated EngineeringOS block in {cdir / 'CLAUDE.md'}")

    if lead:
        log(set_default_style(cdir / "settings.json"))

    claude_cli = a.claude_cli if a.claude_cli is not None else shutil.which("claude")
    log(configure_mcp(Path(a.claude_json), mcp_entry(a.python, engine, data), claude_cli or ""))


def health(a):
    cdir, cj = Path(a.claude_dir), Path(a.claude_json)
    agents = sorted(p.stem for p in (cdir / "agents").glob("*.md")
                    if "Generated by `eng sync-claude`" in p.read_text(encoding="utf-8"))
    print(f"[eng]   Claude agents synced: {' '.join(agents) or '(none)'}")
    commands = sorted(p.stem for p in (cdir / "commands").glob("*.md"))
    print(f"[eng]   Claude commands: {' '.join(commands) or '(none)'}")
    md = cdir / "CLAUDE.md"
    has_block = md.exists() and BLOCK_BEGIN in md.read_text(encoding="utf-8")
    print(f"[eng]   Claude CLAUDE.md block: {'present' if has_block else 'missing'}")
    style = (cdir / "output-styles" / STYLE_FILE).is_file()
    try:
        current = load_json(cdir / "settings.json").get("outputStyle") or "default"
    except SystemExit:
        current = "(settings.json unreadable)"
    print(f"[eng]   Claude Lead style: {'present' if style else 'missing'}, default outputStyle: {current}")
    try:
        entry = read_mcp(cj)
    except SystemExit:
        entry = None
    if isinstance(entry, dict) and entry.get("args") and Path(entry["args"][0]).is_file():
        print(f"[eng]   Claude MCP: ok ({MCP_NAME} -> {entry['args'][0]})")
    else:
        print("[eng]   Claude MCP: missing (run 'eng sync-claude')")


def main():
    home = Path.home()
    cfg_dir = os.environ.get("CLAUDE_CONFIG_DIR")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("action", choices=["sync", "health"])
    p.add_argument("--engine", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--python", default=sys.executable)
    p.add_argument("--claude-dir", default=cfg_dir or str(home / ".claude"))
    p.add_argument("--claude-json", default=str(Path(cfg_dir) / ".claude.json") if cfg_dir else str(home / ".claude.json"))
    p.add_argument("--claude-cli", default=None,
                   help="path to the claude CLI for MCP registration ('' to force direct file edit)")
    a = p.parse_args()
    sync(a) if a.action == "sync" else health(a)


if __name__ == "__main__":
    main()
