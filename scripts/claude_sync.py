#!/usr/bin/env python3
"""Sync EngineeringOS into Claude Code. Called by `eng sync-claude` / `eng health`.

`opencode/` stays the single source of truth. This script translates it into
Claude Code's layout:

  opencode/agents/*.md (subagents) -> <claude_dir>/agents/*.md
      permission map -> disallowedTools + PreToolUse hooks (claude/hooks/eos_guard.py)
  opencode/agents/lead.md (primary) -> managed block in <claude_dir>/CLAUDE.md
  opencode/skills/*/                -> <claude_dir>/skills/*/
  opencode/commands/*.md            -> <claude_dir>/commands/*.md
  engineering-memory MCP            -> mcpServers in <claude_json> (user scope)

Names that collide with Claude Code built-ins are prefixed with `eos-`.
Idempotent; files it previously wrote but no longer produces are removed (tracked
in a manifest), user files are never touched. Stdlib only.
"""
import argparse
import json
import os
import re
import shlex
import shutil
import sys
import tempfile
from pathlib import Path

MCP_NAME = "engineering-memory"
MANIFEST = ".engineeringos-manifest.json"
BLOCK_BEGIN = "<!-- BEGIN EngineeringOS (managed by `eng sync-claude`; edits inside this block are overwritten) -->"
BLOCK_END = "<!-- END EngineeringOS -->"

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


# --- minimal frontmatter parser (the subset our definitions use) -------------

def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


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
        elif rest == "":
            if i < len(lines) and lines[i].strip() and _indent(lines[i]) > ind:
                out[key], i = _parse_block(lines, i, _indent(lines[i]))
            else:
                out[key] = ""
        else:
            out[key] = _unquote(rest)
    return out, i


def split_frontmatter(text):
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
        text = re.sub(r"(?<![\w/-])" + re.escape(old) + r"(?![\w-])", new, text)
    for old, new in COMMAND_RENAMES.items():
        text = re.sub(r"(?<![\w-])/" + re.escape(old) + r"(?![\w-])", "/" + new, text)
    return text


# --- translation --------------------------------------------------------------

def _guard_cmd(py, guard, mode, allow=(), deny=()):
    parts = [py, str(guard), mode]
    for p in allow:
        parts += ["--allow", p]
    for p in deny:
        parts += ["--deny", p]
    return " ".join(shlex.quote(p) for p in parts)


def translate_permissions(perm, py, guard):
    """Return (disallowed_tools, [(matcher, command)])."""
    disallowed, hooks = [], []
    if not isinstance(perm, dict):
        return disallowed, hooks

    edit = perm.get("edit", "allow")
    if edit == "deny":
        disallowed += ["Edit", "Write", "NotebookEdit"]
    elif isinstance(edit, dict) and edit.get("*", "allow") == "deny":
        globs = [k for k, v in edit.items() if k != "*" and v == "allow"]
        hooks.append(("Edit|Write|NotebookEdit", _guard_cmd(py, guard, "edit", allow=globs)))

    bash = perm.get("bash", "allow")
    if bash == "deny":
        disallowed.append("Bash")
    elif isinstance(bash, dict):
        rules = {k: v for k, v in bash.items() if k != "*"}
        if bash.get("*", "allow") == "deny":
            allow = [k for k, v in rules.items() if v == "allow"]
            if allow:
                hooks.append(("Bash", _guard_cmd(py, guard, "bash", allow=allow)))
            else:
                disallowed.append("Bash")
        else:
            deny = [k for k, v in rules.items() if v == "deny"]
            if deny:
                hooks.append(("Bash", _guard_cmd(py, guard, "bash", deny=deny)))

    if perm.get("webfetch") == "deny":
        disallowed.append("WebFetch")
    if perm.get("websearch") == "deny":
        disallowed.append("WebSearch")
    if perm.get("task") == "deny":
        disallowed.append("Agent")
    return disallowed, hooks


def render_agent(name, fm, body, source, py, guard):
    disallowed, hooks = translate_permissions(fm.get("permission"), py, guard)
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


def render_claude_block(engine, data, lead_body, agents, commands):
    lines = [
        BLOCK_BEGIN,
        "# EngineeringOS",
        "",
        f"@{engine}/PRINCIPLES.md",
        f"@{data}/USER.md",
        "",
        "## Running EngineeringOS in Claude Code",
        "- This main conversation plays the EngineeringOS **Lead** role (below). Delegate with the Agent tool to the "
        "EngineeringOS subagents: " + ", ".join(f"`{a}`" for a in agents) + ". Prefer them over the built-in "
        "Explore/Plan agents when following EngineeringOS workflows.",
        f"- The `{MCP_NAME}` MCP server (`mcp__{MCP_NAME}__*`) is the system of record for project context, ADRs, "
        "research, tasks and state. Claude Code's built-in auto-memory is only for personal working preferences; "
        "durable project knowledge goes to EngineeringOS.",
        "- Project rules: if a repo has `AGENTS.md` but no `CLAUDE.md`, read `AGENTS.md`.",
        "- Workflows: " + ", ".join(f"`/{c}`" for c in commands) + ".",
        "- " + TOOL_NOTE.lstrip("> "),
        "",
        "## Lead role",
        re.sub(r"^(#{2,5}) ", r"#\1 ", rename_refs(lead_body.strip()), flags=re.M),
        BLOCK_END,
    ]
    return "\n".join(lines) + "\n"


# --- filesystem helpers --------------------------------------------------------

def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def atomic_write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
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


def mcp_entry(py, engine, data):
    return {
        "type": "stdio",
        "command": py,
        "args": [str(engine / "mcp" / MCP_NAME / "server.py")],
        "env": {"ENGINEERING_OS_DATA": str(data)},
    }


def configure_mcp(claude_json, entry):
    cfg = {}
    if claude_json.exists():
        try:
            cfg = json.loads(claude_json.read_text(encoding="utf-8") or "{}")
        except ValueError:
            sys.exit(f"[eng]   FAIL: {claude_json} is not valid JSON; not touching it")
    servers = cfg.setdefault("mcpServers", {})
    if servers.get(MCP_NAME) == entry:
        return False
    if claude_json.exists():
        shutil.copy2(claude_json, claude_json.with_name(claude_json.name + ".engineeringos.bak"))
    servers[MCP_NAME] = entry
    atomic_write_json(claude_json, cfg)
    return True


# --- commands -------------------------------------------------------------------

def sync(a):
    engine, data, cdir = Path(a.engine), Path(a.data), Path(a.claude_dir)
    guard = engine / "claude" / "hooks" / "eos_guard.py"
    oc = engine / "opencode"
    produced, changed = [], 0
    agents, commands, lead_body = [], [], ""

    for src in sorted((oc / "agents").glob("*.md")):
        fm, body = split_frontmatter(src.read_text(encoding="utf-8"))
        name = src.stem
        if fm.get("mode") == "primary":
            if name == "lead":
                lead_body = body
            continue
        dest = cdir / "agents" / f"{name}.md"
        changed += write_if_changed(dest, render_agent(name, fm, body, f"opencode/agents/{src.name}", a.python, guard))
        produced.append(dest)
        agents.append(name)

    for sdir in sorted(p for p in (oc / "skills").iterdir() if p.is_dir()):
        name = SKILL_RENAMES.get(sdir.name, sdir.name)
        for f in sorted(sdir.rglob("*")):
            if not f.is_file():
                continue
            dest = cdir / "skills" / name / f.relative_to(sdir)
            if f.name == "SKILL.md":
                fm, body = split_frontmatter(f.read_text(encoding="utf-8"))
                changed += write_if_changed(dest, render_skill(name, fm, body))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists() or dest.read_bytes() != f.read_bytes():
                    shutil.copy2(f, dest)
                    changed += 1
            produced.append(dest)

    for src in sorted((oc / "commands").glob("*.md")):
        fm, body = split_frontmatter(src.read_text(encoding="utf-8"))
        name = COMMAND_RENAMES.get(src.stem, src.stem)
        dest = cdir / "commands" / f"{name}.md"
        changed += write_if_changed(dest, render_command(fm, body))
        produced.append(dest)
        commands.append(name)

    # Remove files we produced last time but no longer do (never user files).
    manifest = cdir / MANIFEST
    old = []
    if manifest.exists():
        try:
            old = json.loads(manifest.read_text(encoding="utf-8")).get("files", [])
        except ValueError:
            old = []
    now = {str(p) for p in produced}
    for stale in old:
        sp = Path(stale)
        if stale not in now and sp.is_file() and cdir in sp.parents:
            sp.unlink()
            changed += 1
            parent = sp.parent
            while parent != cdir and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    write_if_changed(manifest, json.dumps({"files": sorted(now)}, indent=2) + "\n")

    print(f"[eng]   claude: {len(agents)} agents, {len(commands)} commands, skills synced ({changed} files changed)")

    block = render_claude_block(engine, data, lead_body, agents, commands)
    if merge_claude_md(cdir / "CLAUDE.md", block):
        print(f"[eng]   claude: updated EngineeringOS block in {cdir / 'CLAUDE.md'}")

    if configure_mcp(Path(a.claude_json), mcp_entry(a.python, engine, data)):
        print(f"[eng]   claude: configured {MCP_NAME} MCP (user scope) in {a.claude_json} (backup: *.engineeringos.bak)")
    else:
        print(f"[eng]   claude: {MCP_NAME} MCP already configured")


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
    entry = None
    if cj.exists():
        try:
            entry = json.loads(cj.read_text(encoding="utf-8")).get("mcpServers", {}).get(MCP_NAME)
        except ValueError:
            entry = None
    if entry and entry.get("args") and Path(entry["args"][0]).is_file():
        print(f"[eng]   Claude MCP: ok ({MCP_NAME} -> {entry['args'][0]})")
    else:
        print(f"[eng]   Claude MCP: missing (run 'eng sync-claude')")


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
    a = p.parse_args()
    sync(a) if a.action == "sync" else health(a)


if __name__ == "__main__":
    main()
