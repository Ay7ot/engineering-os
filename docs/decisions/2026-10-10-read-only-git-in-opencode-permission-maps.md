# ADR: Read-only git in the source permission maps

- **Date:** 2026-10-10
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Project:** engineering-os
- **Builds on:** [Keep read-only agent lockdown](2026-09-10-keep-read-only-agent-lockdown-fix-prompts-instead-.md),
  [Editor-neutral source and adapters](2026-10-10-editor-neutral-source-and-adapters.md)

## Context

The read-only agents (explorer, reviewer, security, researcher, architect) are
meant to inspect, never change, repositories. The Claude Code guard
(`adapters/claude/hooks/eos_guard.py`) already enforces that for git, but
OpenCode consumes the source `permissions.bash` maps as-is, and they were
looser:

- researcher allowed `git *` (push, `reset --hard`, `clean`, `clone`, ...);
- explorer and reviewer allowed `git branch *` / `git remote *`, which admit
  `git branch -D`, `git remote set-url`, and branch creation;
- every `git log *` / `git show *` / `git diff *` admitted `--output=FILE`
  (writes a file) and `--ext-diff` (runs an external diff program).

So the same agent was read-only in Claude Code and writable in OpenCode.

## Decision

- Replace the wildcards with explicit read-only forms. Branch and tag are
  allowed only bare or in list mode (`git branch`, `-a`, `-r`, `-v`, `-vv`,
  `--show-current`, `--list *`, `--contains *`, `--merged *`, `--no-merged *`;
  `git tag`, `--list *`, `-l *`). Remotes only `git remote`, `git remote -v`,
  `git remote get-url *`.
- Where an allow wildcard remains (`git log|show|diff *`), carve out the write
  forms with deny rules placed after it: `git <sub> *--output*` and
  `git <sub> *--ext-diff*`. OpenCode applies the last matching rule and the
  Claude guard checks denies first, so both editors read this the same way.
  The `"*": deny` default stays first.
- **researcher loses `git clone`.** Cloning writes to disk and fetches
  untrusted content (clone-time RCE bugs have hit case-insensitive filesystems
  such as macOS). The Claude guard already blocks clone, and the researcher can
  read upstream source through `webfetch`. Its prompt now says so. Its local
  git access is the explorer set plus `show`, `diff`, `describe`, tag listing.
- Prompts that named removed commands (explorer's TOOL RESTRICTIONS) are
  updated. The 2026-09-10 lockdown ADR is unchanged: this only narrows it.

Why list mode is safe under a trailing `*`: git rejects mutating flags in list
mode (`git branch --list -D x`, `--merged HEAD -c a b`, `git tag --list -d v1`
all fail with a usage error) and ignores `-f`/`-t` there. Checked on the local
git before choosing these patterns.

## Verification

- `tests/test_adapters.py`: the OpenCode golden now compares each rendered agent
  with its pre-migration fixture **after applying a declared delta** (rules
  removed, rules appended, exact prompt edits). Any other drift still fails, and
  a stale delta fails too. A new check simulates OpenCode's last-match wildcard
  rules against 30 mutating git commands for every read-only agent, confirms it
  flags the old maps, and confirms the intended read commands stay allowed.
- `opencode debug agents` before/after `eng sync`: only the listed shell rules
  changed (plus explorer/researcher prompt text); no other permission, model,
  or field changed, and the relative order of untouched rules is kept.

## Alternatives

- Keep the wildcards and rely on the Claude guard: rejected, OpenCode has no
  such guard.
- Port the guard's git logic into an OpenCode plugin: more code to keep in sync
  for a problem that static patterns solve.
- Keep `git clone` for the researcher: rejected for the reasons above.

## Consequences

- Agents that need a git form not listed here get a denial and must ask the
  lead or builder. Add the form to the source map deliberately.
- Out of scope, worth a follow-up: researcher's `opencode mcp *` also matches
  `opencode mcp add/remove`, and security's `npm audit *` also matches
  `npm audit fix` (which installs packages and runs their scripts).
