# ADR: Render OpenCode agents in the V2 dialect (version-gated)

- **Date:** 2026-10-22
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Supersedes in part:** [Map `model_tier` to OpenCode models](2026-10-21-opencode-model-tiers.md)
  (the "effort variants: measured, then dropped" section)
- **Builds on:** [Editor-neutral source and adapters](2026-10-10-editor-neutral-source-and-adapters.md)

## Context

The tier map shipped without `#variant` because OpenCode silently discards the
suffix on agents carrying legacy fields. Measured on v2.0.27: an agent with
`permission:` or `temperature:` **together with a `#variant`** resolves
`model: null`; the same model string on a pure-V2 agent resolves with the variant
intact, and without a variant both dialects resolve the model. `deep` and `standard` therefore
had to converge on one model, and every generated file carried fields that V2
inherits only through a compatibility loader.

OpenCode V2 renamed the agent surface:

| V1 | V2 |
|---|---|
| `permission:` map | `permissions:` ordered list |
| `temperature:` | `request.body.temperature` |
| action `bash` | action `shell` |
| action `task` | action `subagent` |
| command `subtask` | command `subagent` (`subtask` = deprecated alias) |
| — | `todowrite`, `list` are not actions |

## Decision

Render both dialects and pick by installed version — but on its own
precedence, because agent frontmatter has a one-way compatibility the MCP shape
does not.

- `agent_dialect(ctx, cfg, mcp)`: the detected CLI major wins when known. The
  config's MCP shape is only a hint when the CLI is absent, and the unknown case
  falls back to **v1**. Compatibility is one-way — V2 reads V1 agents, V1 cannot
  read `permissions:` lists — so the safe default is the dialect both readers
  understand. This deliberately does *not* reuse `choose_shape`'s precedence,
  which prefers `mcp.servers` over the version and would write V2 agents into a
  downgraded v1 install, silently dropping every rule.
- V2 rendering: `permissions` as an ordered list of
  `{action, resource, effect}`; `bash`→`shell`, `task`→`subagent`; `todowrite`
  and `list` dropped (they can never match); `temperature` moved into
  `request.body`; commands emit `subagent`.
- Rule order is preserved. Our source maps already put the `"*"` default first,
  and both dialects resolve last-match-wins, so precedence is unchanged by
  construction rather than by convention.
- `TIER_MODELS` regains `#max` (deep) and `#high` (standard). `render_agent`
  strips the suffix on the v1 path, because that loader drops it anyway and a
  silent drop is worse than an explicit one.
- The YAML subset gains block lists (`- scalar` and `- key: value` with a nested
  map). Flow collections, anchors, tabs and multi-document remain rejected.

## Verification

- `tests/test_adapters.py` (86 checks): list parse/emit round-trip including a
  nested map and the rejection cases; every agent renders a V2 list with no
  legacy field, three-key rules, and `temperature` inside `request.body`; and a
  **differential** check — for every agent, the v1 map and the v2 list must
  resolve the same effect for 35 shell probes (30 mutating git commands plus
  shell/pytest/rm/ls/secret-read) and for three read paths. The read-only agent
  guarantees are asserted directly against the v2 list too.
- Sandbox installs pin the gate: v2 CLI → `permissions:`/`request:`; v1 CLI →
  `permission:`/`temperature:`; **v1 CLI + v2-shaped config → v1** (the
  downgrade fail-open); v2 CLI + v1-shaped config → v2; no CLI + no config → v1.
- Source validation now rejects an unknown effect (`maybe`), a list-valued
  permission rule, and a non-map `targets.<editor>` at load time, so a malformed
  deny cannot degrade into an inert rule. A `deny` on a retired V2 action raises
  instead of being dropped.
- Live: `eng sync opencode` then `opencode debug agents` on v2.0.27 — all nine
  agents resolve a model, `deep` agents carry `variant: max`, `standard`
  `variant: high`, explorer `mimo-v2.6-flash`. Builder's resolved list went
  17 → 15 rules (OpenCode's 5-rule base policy plus our 12 capabilities, minus
  the two retired actions) with `subagent`/`shell` in place of `task`/`bash`;
  the generated file itself carries 10 rules, and `request.body.temperature`
  is `0.2`.
- A generated file also parses under PyYAML, so the emitted YAML is not merely
  valid for our own reader.
- Full suite: 86 + 24 + 103 + 36 checks, ruleset guard, `eng health` clean,
  second `eng sync` reports `0 files changed`.

## Alternatives

- **V2 only.** Simplest, but a v1 install cannot read `permissions:` lists, so
  its agents would lose every rule. Rejected: the adapter already promises to
  match the installed editor.
- **Keep the V1 dialect.** Status quo; costs the effort tiers and keeps
  deprecated fields.
- **Build the permission list by string concatenation.** Avoids touching the
  shared YAML subset, but leaves the emitter unable to represent what the
  adapter produces, and keeps tests parsing a shape the emitter cannot write.
  Rejected.

## Consequences

- `deep` and `standard` are now genuinely different (max vs high effort) at the
  same token price per token class, which is the cheapest capability upgrade
  available to us.
- Two renderings to maintain. The v1 path's *field shape* is frozen: it exists for installs that
  cannot read V2 and should be deleted when OpenCode V1 is no longer supported.
- `todowrite` and `list` disappear from generated V2 agents. They were rules for
  actions that do not exist; no tool behaviour changes.
- `request.body` is written but V2's session runner does not send request
  overlays yet, so per-agent `temperature` is stored and inert. That matches
  what V2 already did with the legacy top-level field, so behaviour does not
  change — but do not read the field as proof the setting takes effect.
- **Secret files prompt again.** OpenCode's base policy asks before reading
  `*.env`, but agent rules are appended after it, so our blanket
  `read: * → allow` removed the prompt on every agent — true in the V1 dialect
  since the beginning, not introduced by this migration. Both dialects now
  re-state the policy *last* (`*.env` and `*.env.*` → ask, `*.env.example` →
  allow) whenever the source says `read: allow`. An explicit read map is left
  alone: that is the author deciding which paths to read.
- Claude Code has no equivalent base policy, so there is nothing to restore
  there. Its adapter translates `read` into `allowedTools` and has no `ask`
  effect; a parity rule would be a new restriction on reading secrets, which is
  a policy decision tracked separately rather than smuggled into this change.
