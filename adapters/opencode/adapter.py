"""OpenCode adapter: neutral source -> ~/.config/opencode.

Renders agents/commands/skills in OpenCode's frontmatter dialect and registers
the engineering-memory MCP in the config shape the installed OpenCode reads
(v2: mcp.servers.<name>; v1: mcp.<name>).
"""
import re
import shutil
import subprocess
from pathlib import Path

from adapters.common import (MCP_NAME, Writer, atomic_write_json, load_json, log,
                             render_frontmatter)

NAME = "opencode"
CONFIG_FILE = "opencode.jsonc"


def config_dir(ctx):
    xdg = ctx.env.get("XDG_CONFIG_HOME")
    return Path(xdg) / "opencode" if xdg else ctx.home / ".config" / "opencode"


def detect(ctx):
    return bool(shutil.which("opencode")) or config_dir(ctx).is_dir()


# --- rendering ------------------------------------------------------------------

def render_agent(agent):
    fm = {"description": agent.fm["description"], "mode": agent.fm["role"]}
    fm.update(agent.target(NAME))
    if "permissions" in agent.fm:
        fm["permission"] = agent.fm["permissions"]
    return render_frontmatter(fm, agent.body)


def render_command(cmd):
    fm = {"description": cmd.fm["description"]}
    fm.update(cmd.target(NAME))
    return render_frontmatter(fm, cmd.body)


def render_skill(skill):
    if "targets" not in skill.fm:
        return skill.path.read_bytes()  # byte-identical pass-through
    fm = {k: v for k, v in skill.fm.items() if k != "targets"}
    fm.update(skill.target(NAME))
    return render_frontmatter(fm, skill.body)


# --- MCP --------------------------------------------------------------------------

def _major_version():
    """Major version of the opencode CLI on PATH, or None if unknown.

    Reads only the first non-empty output line (stdout, else stderr) and only a
    full x.y.z version token, so update notices further down cannot mislead it.
    """
    exe = shutil.which("opencode")
    if not exe:
        return None
    try:
        res = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    for stream in (res.stdout, res.stderr):
        lines = [ln for ln in stream.splitlines() if ln.strip()]
        if lines:
            m = re.search(r"(?<![\d.])v?(\d+)\.(\d+)\.(\d+)(?![\d.])", lines[0])
            return int(m.group(1)) if m else None
    return None


def choose_shape(mcp, ctx, version):
    """Return ("v1"|"v2", reason). Prefer what the config already uses."""
    if isinstance(mcp.get("servers"), dict):
        return "v2", "config already uses mcp.servers"
    if version is not None:
        return ("v2" if version >= 2 else "v1"), f"opencode --version major {version}"
    if _ours(mcp.get(MCP_NAME), ctx):
        return "v1", "existing v1 entry and opencode version unknown"
    return "v2", "opencode version unknown (CLI not on PATH); defaulting to current v2 format"


def _ours(entry, ctx):
    return isinstance(entry, dict) and str(ctx.server) in " ".join(map(str, entry.get("command", [])))


def configure(ctx, source):
    cfg_path = config_dir(ctx) / CONFIG_FILE
    cfg = load_json(cfg_path, jsonc=True)
    original = repr(cfg)
    mcp = cfg.setdefault("mcp", {})
    if not isinstance(mcp, dict) or not isinstance(mcp.get("servers", {}), dict):
        raise SystemExit(f"[eng]   FAIL: {cfg_path}: 'mcp' (or 'mcp.servers') is not an object; not touching it")
    shape, reason = choose_shape(mcp, ctx, _major_version())
    log(NAME, f"MCP config shape {shape} ({reason})")
    v2 = shape == "v2"
    command = [ctx.python, str(ctx.server)]
    env = {"ENGINEERING_OS_DATA": str(ctx.data)}
    if v2:
        servers = mcp.setdefault("servers", {})
        current = servers.get(MCP_NAME, {})
        entry = dict(current) if isinstance(current, dict) else {}
        entry.update({"type": "local", "command": command, "environment": env})
        entry.setdefault("timeout", {"catalog": 10000, "execution": 10000})
        servers[MCP_NAME] = entry
        if _ours(mcp.get(MCP_NAME), ctx):  # stale v1 entry written by an older eng
            del mcp[MCP_NAME]
    else:
        mcp[MCP_NAME] = {"type": "local", "command": command, "environment": env, "timeout": 10000}
    primaries = [a.name for a in source.primary()]
    if primaries:
        cfg.setdefault("default_agent", "lead" if "lead" in primaries else primaries[0])
    if repr(cfg) == original:
        return f"{MCP_NAME} MCP already configured ({'v2' if v2 else 'v1'} shape)"
    atomic_write_json(cfg_path, cfg)
    return f"configured {MCP_NAME} MCP in {cfg_path} ({'v2' if v2 else 'v1'} shape; backup: *.engineeringos.bak)"


# --- contract ---------------------------------------------------------------------

def sync(ctx, source):
    root = config_dir(ctx)
    w = Writer(root, NAME, adopt_legacy=True)
    for a in source.agents:
        w.write(root / "agents" / f"{a.name}.md", render_agent(a))
    for c in source.commands:
        w.write(root / "commands" / f"{c.name}.md", render_command(c))
    for s in source.skills:
        w.write(root / "skills" / s.name / "SKILL.md", render_skill(s))
        for rel, f in s.files:
            w.write(root / "skills" / s.name / rel, f.read_bytes())
    w.finish()
    log(NAME, f"{len(source.agents)} agents, {len(source.commands)} commands, {len(source.skills)} skills synced ({w.changed} files changed)")
    log(NAME, configure(ctx, source))


def health(ctx, source):
    root = config_dir(ctx)
    if not detect(ctx):
        print("[eng]   OpenCode: not installed")
    names = [a.name for a in source.agents]
    print(f"[eng]   Agents synced:{''.join(' ' + n for n in names if (root / 'agents' / f'{n}.md').is_file())}")
    cfg = {}
    try:
        cfg = load_json(root / CONFIG_FILE, jsonc=True)
    except SystemExit:
        pass
    print(f"[eng]   Default agent: {cfg.get('default_agent') or '(unset)'}")
    cmds = [c.name for c in source.commands]
    print(f"[eng]   Commands synced:{''.join(' ' + n for n in cmds if (root / 'commands' / f'{n}.md').is_file())}")
    print(f"[eng]   Skills dir: {'present' if (root / 'skills').is_dir() else 'missing'}")
    mcp = cfg.get("mcp", {}) if isinstance(cfg.get("mcp"), dict) else {}
    entry = (mcp.get("servers") or {}).get(MCP_NAME) if isinstance(mcp.get("servers"), dict) else None
    shape = "v2"
    if entry is None and isinstance(mcp.get(MCP_NAME), dict):
        entry, shape = mcp[MCP_NAME], "v1"
    stale = isinstance(mcp.get("servers"), dict) and isinstance(mcp.get(MCP_NAME), dict)
    version = _major_version()
    mismatch = version is not None and ((version >= 2) != (shape == "v2"))
    if _ours(entry, ctx):
        note = " (stale v1 entry present; run eng sync opencode)" if stale else ""
        if mismatch:
            note += f" (WARNING: installed opencode is v{version}; re-run eng sync opencode)"
        print(f"[eng]   OpenCode MCP: ok ({shape} shape){note}")
    else:
        print("[eng]   OpenCode MCP: missing (run 'eng sync opencode')")
