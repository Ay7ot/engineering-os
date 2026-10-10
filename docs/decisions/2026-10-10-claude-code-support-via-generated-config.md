# ADR: Claude Code support via config generated from `opencode/`

- **Date:** 2026-10-10
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Project:** engineering-os

## Context

EngineeringOS was wired only into OpenCode (`eng setup` / `sync-opencode`), even
though the engine itself (MCP server, data dir, principles) is tool-agnostic.
The operator also uses Claude Code (desktop app, so `claude` is not on PATH) and
wants both tools to share the same memory and agent roster.

Claude Code's formats differ: subagents take `name`/`description`/`model`/
`disallowedTools`/`hooks` instead of OpenCode's `mode` + `permission` map, MCP
servers live in `~/.claude.json`, and there is no "default primary agent" — the
main conversation plays that role, steered by `~/.claude/CLAUDE.md`.

## Decision

Keep `opencode/` as the **single source of truth** and add `eng sync-claude`
(`scripts/claude_sync.py`, stdlib only) that generates Claude Code config:

- Subagents → `~/.claude/agents/`. `permission` is translated: blanket denies
  become `disallowedTools`; per-command bash maps and path-scoped edit maps
  (e.g. explorer's git-only bash, architect's `*.md`-only edits) become a
  `PreToolUse` hook running `claude/hooks/eos_guard.py`, which fails closed and
  rejects shell control operators and mutating git forms (push, reset,
  branch -D, remote set-url, --output, -c) for allowlisted agents, even under a
  wildcard like `git *`. Translation fails closed: anything other than an exact
  `allow` (including OpenCode's `ask`) removes the capability. This preserves the read-only lockdown from
  ADR 2026-09-10 rather than loosening it.
- The `lead` primary agent → the **EngineeringOS Lead** output style
  (`~/.claude/output-styles/eos-lead.md`, `keep-coding-instructions: true`),
  made the default `outputStyle` in `~/.claude/settings.json` (operator choice:
  default everywhere, mirroring OpenCode's `default_agent: lead`). An existing
  non-default style choice is respected. An output style is Claude Code's
  switchable "mode", the closest match to an OpenCode primary agent.
- Always-on context → a marker-delimited block in `~/.claude/CLAUDE.md` that
  `@`-imports `PRINCIPLES.md` and `USER.md`. User content outside the block is
  preserved.
- Skills and commands copied; names colliding with Claude Code built-ins get an
  `eos-` prefix (`code-review`, `security-review`, `/review`, `/debug`), and
  references are rewritten.
- MCP → user scope via `claude mcp add-json` when the CLI exists (Claude Code
  owns its file, no lost-update race); otherwise merged into `~/.claude.json`
  with an atomic write, backup and read-back verification.
- Sync never overwrites a file it did not write (prints SKIPPED instead).
- Generated files tracked in a manifest so re-syncs prune stale output without
  touching user files. Models mapped by role (opus for architect/reviewer/
  security, haiku for explorer, sonnet otherwise).

`eng setup` now requires only git + python3 and syncs whichever of OpenCode /
Claude Code is present.

## Alternatives

- **Maintain a parallel `claude/agents/` tree by hand.** Rejected: two copies
  drift; every prompt fix would need doing twice.
- **Approximate bash allowlists by dropping Bash from read-only agents.**
  Rejected: weaker than OpenCode for explorer/reviewer (they need git reads),
  and silently changes agent behavior across tools.
- **Lead role in the global CLAUDE.md block.** First iteration; rejected
  because it cannot be switched off per session and loads into every session
  with no visible mode.
- **Run `lead` as the main-thread agent.** Would allow pinning model/tools, but
  is not switchable from the desktop app the way an output style is.

## Consequences

- One edit in `opencode/` + `eng sync-claude` updates both tools.
- The translator must be extended when new permission shapes appear; tests in
  `tests/test_claude_sync.sh` (run in CI) cover the current shapes and the guard.
- Without the CLI (desktop app only), `~/.claude.json` is edited directly; run
  sync while Claude Code is idle and confirm with `eng health` after restart.
- Claude Code read-only agents are now stricter than OpenCode for git (the
  OpenCode permission maps still allow e.g. `git branch -D` and, for researcher,
  `git push`). Tightening the OpenCode sources is a separate change.
