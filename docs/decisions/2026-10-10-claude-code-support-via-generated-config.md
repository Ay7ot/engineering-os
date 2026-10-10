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
  rejects shell control operators. This preserves the read-only lockdown from
  ADR 2026-09-10 rather than loosening it.
- The `lead` primary agent → a marker-delimited block in `~/.claude/CLAUDE.md`
  that `@`-imports `PRINCIPLES.md` and `USER.md`. User content outside the
  block is preserved.
- Skills and commands copied; names colliding with Claude Code built-ins get an
  `eos-` prefix (`code-review`, `security-review`, `/review`, `/debug`), and
  references are rewritten.
- MCP → user-scope `mcpServers.engineering-memory` in `~/.claude.json`, merged
  (never replaced), atomic write, backup to `*.engineeringos.bak`.
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
- **Run `lead` as the main-thread agent via settings.** Rejected for now: the
  CLAUDE.md block is simpler, visible, and doesn't replace Claude Code's
  default system behavior.

## Consequences

- One edit in `opencode/` + `eng sync-claude` updates both tools.
- The translator must be extended when new permission shapes appear; tests in
  `tests/test_claude_sync.sh` (run in CI) cover the current shapes and the guard.
- `~/.claude.json` is a file Claude Code writes too; the merge is atomic but
  should be run while Claude Code is idle, then Claude Code restarted.
