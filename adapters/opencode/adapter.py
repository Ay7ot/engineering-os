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

# Neutral model tiers -> OpenCode `provider/model[#variant]` selectors. The
# variant is the model's effort setting, so a tier can buy more thinking without
# buying a different vendor. It is emitted only for V2 agents: V1 parses agents
# through a compatibility loader that silently drops `#variant` (measured with
# `opencode debug agents`, 2026-10-21), so render_agent strips it there. Override
# per agent with `targets.opencode.model`; an agent with no tier and no override
# inherits the parent session's model, which is OpenCode's own default.
TIER_MODELS = {
    "deep": "opencode-go/deepseek-v4.1-flash#max",
    "standard": "opencode-go/deepseek-v4.1-flash#high",
    "fast": "opencode-go/mimo-v2.6-flash",
}


def config_dir(ctx):
    xdg = ctx.env.get("XDG_CONFIG_HOME")
    return Path(xdg) / "opencode" if xdg else ctx.home / ".config" / "opencode"


def detect(ctx):
    return bool(shutil.which("opencode")) or config_dir(ctx).is_dir()


# --- rendering ------------------------------------------------------------------

# V2 renamed two permission actions. Everything else keeps its name.
V2_ACTIONS = {"bash": "shell", "task": "subagent"}
# Actions V2 has no tool for: emitting them would be rules that can never match.
V2_RETIRED_ACTIONS = {"todowrite", "list"}
# OpenCode prepends a base policy that asks before reading `.env` files. Agent
# rules are appended after it and win, so a blanket `read: allow` would silently
# remove that prompt. Re-state the policy last, in the editor's own shape.
ENV_POLICY = (("*.env", "ask"), ("*.env.*", "ask"), ("*.env.example", "allow"))


def env_policy(permissions):
    """Rules that keep OpenCode's `.env` prompt after a blanket read allow.

    Only for the scalar `read: allow` case. An explicit read map is the author's
    decision about which paths to read, and is left alone.
    """
    return list(ENV_POLICY) if permissions.get("read") == "allow" else []


def model_for(agent):
    """Model selector for an agent: explicit target first, then its tier."""
    return agent.target(NAME).get("model") or TIER_MODELS.get(agent.fm.get("model_tier"))


def permission_rules(permissions, v2):
    """Render the source permission map in the dialect the editor reads.

    v1 keeps the `permission` map (OpenCode resolves it last-match-wins).
    v2 wants an ordered `permissions` list; our maps already put the `"*"`
    default first, so iteration order is the same precedence.
    """
    if v2:
        rules = []
        for cap, rule in permissions.items():
            action = V2_ACTIONS.get(cap, cap)
            if action in V2_RETIRED_ACTIONS:
                effects = set(rule.values()) if isinstance(rule, dict) else {rule}
                if effects - {"allow"}:
                    # Dropping a deny would silently widen access; refuse instead.
                    raise SystemExit(f"[eng]   FAIL: '{cap}' is not a V2 action, so its "
                                     f"{sorted(effects - {'allow'})} rule cannot be expressed")
                continue
            if isinstance(rule, dict):
                rules.extend({"action": action, "resource": res, "effect": eff}
                             for res, eff in rule.items())
            else:
                rules.append({"action": action, "resource": "*", "effect": rule})
        rules.extend({"action": "read", "resource": res, "effect": eff}
                     for res, eff in env_policy(permissions))
        if not rules:
            raise SystemExit("[eng]   FAIL: every permission is a retired V2 action; nothing left to emit")
        return rules

    out = {}
    for cap, rule in permissions.items():
        if cap == "read" and isinstance(rule, str):
            out[cap] = {"*": rule, **dict(env_policy(permissions))} if env_policy(permissions) else rule
        else:
            out[cap] = rule
    return out


def render_agent(agent, v2):
    target = dict(agent.target(NAME))
    fm = {"description": agent.fm["description"], "mode": agent.fm["role"]}
    if v2 and "temperature" in target:
        # V2 shapes this as a request overlay (its runner does not send it yet).
        fm["request"] = {"body": {"temperature": target.pop("temperature")}}
    fm.update(target)
    model = model_for(agent)
    if model:
        # v1's compatibility loader drops `#variant`, so do not ship one there.
        fm["model"] = model if v2 else model.split("#", 1)[0]
    if "permissions" in agent.fm:
        fm["permissions" if v2 else "permission"] = permission_rules(agent.fm["permissions"], v2)
    return render_frontmatter(fm, agent.body)


def render_command(cmd, v2):
    target = dict(cmd.target(NAME))
    if v2 and "subtask" in target:
        # `subtask` is the deprecated V1 alias; V2 wins if both are present.
        target.setdefault("subagent", target.pop("subtask"))
    fm = {"description": cmd.fm["description"]}
    fm.update(target)
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


def _config(ctx):
    """The OpenCode config, validating the shapes we merge into.

    Runs before anything is written, so a broken config aborts the sync instead
    of leaving agents updated and the config untouched.
    """
    path = config_dir(ctx) / CONFIG_FILE
    cfg = load_json(path, jsonc=True)
    mcp = cfg.setdefault("mcp", {})
    if not isinstance(mcp, dict) or not isinstance(mcp.get("servers", {}), dict):
        raise SystemExit(f"[eng]   FAIL: {path}: 'mcp' (or 'mcp.servers') is not an object; not touching it")
    return cfg, mcp


def agent_dialect(ctx, cfg, mcp):
    """'v2' when the installed OpenCode reads V2 agents, else 'v1'.

    Compatibility is one-way: V2 reads V1 agents, V1 cannot read V2
    `permissions` lists. So the detected version wins when known, config shape is
    only a hint, and the unknown case falls back to V1 — the dialect both
    readers understand.
    """
    version = _major_version()
    if version is not None:
        return "v2" if version >= 2 else "v1"
    return "v2" if isinstance(mcp.get("servers"), dict) else "v1"


def configure(ctx, source, cfg, mcp):
    cfg_path = config_dir(ctx) / CONFIG_FILE
    original = repr(cfg)
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
    cfg, mcp = _config(ctx)
    v2 = agent_dialect(ctx, cfg, mcp) == "v2"
    log(NAME, f"agents/commands in {'v2' if v2 else 'v1'} dialect")
    w = Writer(root, NAME, adopt_legacy=True)
    for a in source.agents:
        w.write(root / "agents" / f"{a.name}.md", render_agent(a, v2))
    for c in source.commands:
        w.write(root / "commands" / f"{c.name}.md", render_command(c, v2))
    for s in source.skills:
        w.write(root / "skills" / s.name / "SKILL.md", render_skill(s))
        for rel, f in s.files:
            w.write(root / "skills" / s.name / rel, f.read_bytes())
    w.finish()
    log(NAME, f"{len(source.agents)} agents, {len(source.commands)} commands, {len(source.skills)} skills synced ({w.changed} files changed)")
    log(NAME, configure(ctx, source, cfg, mcp))


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
