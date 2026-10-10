#!/usr/bin/env python3
"""PreToolUse guard for EngineeringOS subagents in Claude Code.

Claude Code subagents cannot express OpenCode's per-command permission maps
(e.g. bash: {"*": deny, "git log *": allow}) in frontmatter, so `eng
sync-claude` attaches this script as a PreToolUse hook. It reads the hook JSON
on stdin and exits 2 (block, reason on stderr) unless the call is allowed.

Usage:
  eos_guard.py bash [--allow PATTERN]... [--deny PATTERN]...
  eos_guard.py edit [--allow GLOB]...

Semantics mirror OpenCode wildcards:
  - With any --allow, the default is deny (fail closed).
  - "git log *" also matches the bare "git log".
  - Commands containing shell control operators (; & | ` $( > < newline) are
    blocked under an allowlist, so "git log && rm -rf x" cannot ride along.
  - "git -C <path> <sub>" is matched as "git <sub>" so agents can inspect other
    repos without cd.

Stdlib only.
"""
import fnmatch
import json
import shlex
import sys

CONTROL = (";", "&", "|", "`", "$(", ">", "<", "\n")


def block(reason):
    sys.stderr.write(f"EngineeringOS guard: {reason}\n")
    sys.exit(2)


def parse_args(argv):
    if not argv or argv[0] not in ("bash", "edit"):
        block("misconfigured hook (expected 'bash' or 'edit')")
    mode, allow, deny = argv[0], [], []
    i = 1
    while i < len(argv):
        flag = argv[i]
        if flag in ("--allow", "--deny") and i + 1 < len(argv):
            (allow if flag == "--allow" else deny).append(argv[i + 1])
            i += 2
        else:
            block(f"misconfigured hook (bad argument {flag!r})")
    return mode, allow, deny


def matches(text, pattern):
    if fnmatch.fnmatchcase(text, pattern):
        return True
    return pattern.endswith(" *") and text == pattern[:-2]


def normalize_command(cmd):
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return " ".join(cmd.split())
    if len(tokens) >= 3 and tokens[0] == "git" and tokens[1] == "-C":
        tokens = ["git"] + tokens[3:]
    return " ".join(tokens)


def check_bash(tool_input, allow, deny):
    raw = str(tool_input.get("command", "")).strip()
    if not raw:
        block("empty command")
    cmd = normalize_command(raw)
    for pat in deny:
        if matches(cmd, pat):
            block(f"command matches denied pattern {pat!r}")
    if not allow:
        return
    if any(op in raw for op in CONTROL):
        block("shell operators are not allowed for this agent; run one allowed command at a time")
    if not any(matches(cmd, pat) for pat in allow):
        block(
            "this agent may only run: " + ", ".join(allow)
            + ". Use Read/Glob/Grep for everything else."
        )


def check_edit(tool_input, allow):
    path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
    if not path:
        block("edit without a file path")
    name = path.rsplit("/", 1)[-1]
    if not any(fnmatch.fnmatchcase(name, g) or fnmatch.fnmatchcase(path, g) for g in allow):
        block("this agent may only edit files matching: " + ", ".join(allow or ["(none)"]))


def main():
    mode, allow, deny = parse_args(sys.argv[1:])
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        block("could not parse hook input")
    tool_input = payload.get("tool_input") or {}
    if mode == "bash":
        check_bash(tool_input, allow, deny)
    else:
        check_edit(tool_input, allow)
    sys.exit(0)


if __name__ == "__main__":
    main()
