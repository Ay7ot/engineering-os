# ADR: Editor-neutral source and per-editor adapters

- **Date:** 2026-10-10
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Project:** engineering-os
- **Design:** [docs/design/editor-neutral-engine.md](../design/editor-neutral-engine.md)
- **Supersedes (layout only):** [Claude Code support via generated config](2026-10-10-claude-code-support-via-generated-config.md)

## Context

Agents, skills and commands lived in `opencode/` in OpenCode's frontmatter
dialect. Claude Code support had to translate from that dialect, and we plan to
support many more editors. OpenCode had become the de facto spec. While
auditing we also found that `eng sync-opencode` wrote the MCP entry in the
OpenCode v1 shape, while the installed OpenCode is v2 (`mcp.servers.*`), so
every sync re-added a stale key.

## Decision

- Move the source of truth to root-level `agents/`, `skills/`, `commands/`
  (via `git mv`, history kept) with **neutral frontmatter**: `name`,
  `description`, `role`, `model_tier`, `permissions`, and editor-only settings
  under `targets.<editor>`.
- One **adapter per editor** in `adapters/<editor>/adapter.py` with a fixed
  contract (`detect`, `sync`, `health`), registered in `adapters/__init__.py`.
  Shared concerns (validated loader, YAML subset that fails loudly, ownership
  manifest `Writer`, JSON helpers, fail-closed `grants()`) live in
  `adapters/common.py`.
- `eng sync [all|<editor>]` runs adapters; `eng sync-opencode` and
  `eng sync-claude` stay as aliases. `eng setup` / `eng health` loop over all
  adapters.
- OpenCode adapter writes the MCP entry in the shape the installed OpenCode
  reads (v2 when `mcp.servers` exists or `opencode --version` >= 2), and removes
  the stale v1 entry only when it points at our server.
- Zero behaviour change is enforced by tests: OpenCode output is compared
  (order-sensitive, parsed) against frozen pre-migration fixtures in
  `tests/fixtures/opencode-v1/`; the Claude suite is unchanged apart from paths.

## Alternatives

- Keep `opencode/` and add converters per editor: least churn, but OpenCode's
  quirks leak into every adapter. Rejected.
- Fully abstract schema without `targets`: breaks on the first editor-specific
  setting. Rejected.
- A real YAML parser: violates stdlib-only. The subset parser plus loud
  validation covers our own files.

## Consequences

- Adding an editor is additive: one adapter, its tests, docs (`docs/adapters.md`).
- Frontmatter cannot use YAML lists; the loader rejects them with `file:line`.
- Generated OpenCode files are reformatted (quoted descriptions instead of
  folded blocks) but resolve to identical agents (`opencode debug agents`).
- Claude hook commands now point at `adapters/claude/hooks/eos_guard.py` and
  protect `adapters/`, `agents/`, `skills/`, `commands/` from markdown edits.
- OpenCode's own permission maps still allow some git writes (e.g. researcher
  `git *`); tightening them is a separate change.
