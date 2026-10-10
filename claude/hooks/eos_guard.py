#!/usr/bin/env python3
"""PreToolUse guard for EngineeringOS subagents in Claude Code.

Claude Code subagents cannot express OpenCode's per-command permission maps
(e.g. bash: {"*": deny, "git log *": allow}) in frontmatter, so `eng
sync-claude` attaches this script as a PreToolUse hook. It reads the hook JSON
on stdin and exits 2 (block, reason on stderr) unless the call is allowed.
Any error inside the guard also exits 2: it fails closed, never open.

Usage:
  eos_guard.py bash [--allow PATTERN]... [--deny PATTERN]...
  eos_guard.py edit [--allow GLOB]... [--protect DIR]...

Semantics mirror OpenCode wildcards:
  - With any --allow, the default is deny.
  - "git log *" also matches the bare "git log".
  - Under an allowlist, commands containing shell control operators
    (; & | ` $( > < newline) are blocked, so "git log && rm -rf x" cannot ride
    along, and git is held read-only: mutating subcommands, write flags
    (--output) and config injection (-c) are blocked even when a wildcard such
    as "git *" or "git branch *" would match.
  - "git -C <path> <sub>" is matched as "git <sub>" so agents can inspect other
    repos without cd.
  - edit --protect DIR blocks any edit inside DIR even if the glob matches
    (keeps agents from rewriting their own definitions or Claude Code config).

Stdlib only.
"""
import fnmatch
import json
import os
import shlex
import sys

CONTROL = (";", "&", "|", "`", "$(", ">", "<", "\n", "\r")

# git subcommands that change refs, the index, the worktree, remotes or config.
GIT_MUTATING = {
    "add", "am", "apply", "checkout", "cherry-pick", "clean", "clone", "commit",
    "config", "fetch", "filter-branch", "gc", "init", "merge", "mv", "notes",
    "prune", "pull", "push", "rebase", "reflog", "replace", "reset", "restore",
    "revert", "rm", "stash", "submodule", "switch", "update-index", "update-ref",
    "worktree",
}
# Flags that make otherwise read-only subcommands write.
GIT_WRITE_FLAGS = {
    "branch": {"-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy",
               "-f", "--force", "-u", "--set-upstream-to", "--unset-upstream",
               "--edit-description", "-t", "--track"},
    "tag": {"-d", "--delete", "-a", "-s", "-u", "-f", "--force", "-m", "-F"},
}
REMOTE_READ = {"-v", "--verbose", "show", "get-url"}


class Blocked(Exception):
    pass


def parse_args(argv):
    if not argv or argv[0] not in ("bash", "edit"):
        raise Blocked("misconfigured hook (expected 'bash' or 'edit')")
    mode, opts = argv[0], {"--allow": [], "--deny": [], "--protect": []}
    i = 1
    while i < len(argv):
        flag = argv[i]
        if flag in opts and i + 1 < len(argv):
            opts[flag].append(argv[i + 1])
            i += 2
        else:
            raise Blocked(f"misconfigured hook (bad argument {flag!r})")
    return mode, opts["--allow"], opts["--deny"], opts["--protect"]


def matches(text, pattern):
    if fnmatch.fnmatchcase(text, pattern):
        return True
    return pattern.endswith(" *") and text == pattern[:-2]


def tokenize(cmd):
    try:
        return shlex.split(cmd)
    except ValueError:
        return cmd.split()


def normalize(tokens):
    if len(tokens) >= 3 and tokens[0] == "git" and tokens[1] == "-C":
        tokens = ["git"] + tokens[3:]
    return tokens


def check_git_read_only(tokens):
    if not tokens or tokens[0] != "git":
        return
    if len(tokens) < 2:
        return
    sub, args = tokens[1], tokens[2:]
    if sub.startswith("-"):
        raise Blocked(f"git global option {sub!r} is not allowed for this agent")
    if sub in GIT_MUTATING:
        raise Blocked(f"'git {sub}' modifies the repository; this agent is read-only")
    if any(a == "--output" or a.startswith("--output=") or a == "--ext-diff" for a in args):
        raise Blocked("git write/exec flags (--output, --ext-diff) are not allowed for this agent")
    bad = GIT_WRITE_FLAGS.get(sub, set())
    if any(a in bad or a.split("=", 1)[0] in bad for a in args):
        raise Blocked(f"'git {sub}' with those flags modifies the repository; this agent is read-only")
    if sub == "tag" and [a for a in args if not a.startswith("-")] and not ({"-l", "--list"} & set(args)):
        raise Blocked("creating tags is not allowed for this agent")
    if sub == "branch" and [a for a in args if not a.startswith("-")] and not (
            {"-l", "--list", "--contains", "--merged", "--no-merged", "--points-at", "-a", "-r"} & set(args)):
        raise Blocked("creating branches is not allowed for this agent")
    if sub == "remote" and args and not (set(args) <= REMOTE_READ or args[0] in ("show", "get-url")):
        raise Blocked("changing remotes is not allowed for this agent")


def check_bash(tool_input, allow, deny):
    raw = str(tool_input.get("command", "")).strip()
    if not raw:
        raise Blocked("empty command")
    tokens = normalize(tokenize(raw))
    cmd = " ".join(tokens)
    for pat in deny:
        if matches(cmd, pat):
            raise Blocked(f"command matches denied pattern {pat!r}")
    if not allow:
        return
    if any(op in raw for op in CONTROL):
        raise Blocked("shell operators are not allowed for this agent; run one allowed command at a time")
    if not any(matches(cmd, pat) for pat in allow):
        raise Blocked("this agent may only run: " + ", ".join(allow) + ". Use Read/Glob/Grep for everything else.")
    check_git_read_only(tokens)


def _inside(path, root):
    path, root = os.path.realpath(path), os.path.realpath(os.path.expanduser(root))
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def check_edit(tool_input, allow, protect):
    path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
    if not path:
        raise Blocked("edit without a file path")
    for root in protect:
        if _inside(path, root):
            raise Blocked(f"{path} is inside a protected directory ({root})")
    name = path.rsplit("/", 1)[-1]
    if not any(fnmatch.fnmatchcase(name, g) or fnmatch.fnmatchcase(path, g) for g in allow):
        raise Blocked("this agent may only edit files matching: " + ", ".join(allow or ["(none)"]))


def main():
    mode, allow, deny, protect = parse_args(sys.argv[1:])
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        raise Blocked("unexpected hook input")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise Blocked("unexpected hook input (no tool_input)")
    if mode == "bash":
        check_bash(tool_input, allow, deny)
    else:
        check_edit(tool_input, allow, protect)


if __name__ == "__main__":
    try:
        main()
    except Blocked as exc:
        sys.stderr.write(f"EngineeringOS guard: {exc}\n")
        sys.exit(2)
    except BaseException as exc:  # noqa: BLE001 - fail closed on anything unexpected
        if isinstance(exc, SystemExit) and exc.code in (0, None):
            sys.exit(0)
        sys.stderr.write(f"EngineeringOS guard: blocked (guard error: {type(exc).__name__})\n")
        sys.exit(2)
    sys.exit(0)
