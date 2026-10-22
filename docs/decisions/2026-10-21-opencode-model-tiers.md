# ADR: Map `model_tier` to OpenCode models

- **Date:** 2026-10-21
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Project:** engineering-os
- **Builds on:** [Editor-neutral source and adapters](2026-10-10-editor-neutral-source-and-adapters.md),
  [Claude Code support via generated config](2026-10-10-claude-code-support-via-generated-config.md)

## Context

`model_tier` (`deep` / `standard` / `fast`) is the neutral source's way of
expressing "how much model this agent needs". The Claude adapter maps it
(`deep → opus`, `standard → sonnet`, `fast → haiku`). The OpenCode adapter did
not: it passed `targets.opencode.*` through and ignored the tier entirely.

That made the tier decorative on the editor the operator actually uses. Only
`lead` carried an explicit `model:` line, so OpenCode's inheritance rule made
every other agent — builder, tester, explorer, reviewer, security — run on the
parent session's model. Nine agents, one model, no way to see it from the
sources.

OpenCode V2 has no tier concept of its own (verified against
`opencode.ai/v2/docs/agents`, `/models`): an agent takes one
`provider/model[#variant]` selector, or inherits. So the mapping has to live in
the adapter, exactly as it does for Claude.

## Decision

- Add `TIER_MODELS` and `model_for()` to `adapters/opencode/adapter.py`,
  mirroring the Claude adapter's shape:
  - `deep → opencode-go/deepseek-v4.1-flash`
  - `standard → opencode-go/deepseek-v4.1-flash`
  - `fast → opencode-go/mimo-v2.6-flash`
- Precedence: `targets.opencode.model` > `model_tier` > inherit. No tier and no
  override keeps OpenCode's own default rather than inventing one.
- Remove the now-redundant `targets.opencode.model` from `agents/lead.md` so the
  tier map is the single source; the override mechanism stays for future use.

### Effort variants: measured, then dropped

> **Superseded 2026-10-22** by
> [Render OpenCode agents in the V2 dialect](2026-10-22-opencode-v2-agent-dialect.md).
> The variants below were restored once generated agents moved to V2
> frontmatter; the measurement stands, the conclusion no longer applies.

The first attempt used `#variant` to make `deep` think harder
(`…#max`) than `standard` (`…#high`) on the same vendor. Verification with
`opencode debug agents` showed it does not work here: agents that carry the
legacy `permission:` map or `temperature:` get `model: null`, i.e. OpenCode
silently discards the selector. Isolated with scratch agents:

| Frontmatter | Resolved model |
|---|---|
| `model: "…#high"` alone | variant kept |
| `model: "…#high"` + `temperature:` | **null** |
| `model: "…#high"` + `permission:` map | **null** |
| `model: "…#max"` + V2 `request:` / `permissions:` list | variant kept |
| nested `model:` map | agent not loaded at all |

So the suffix is honoured only on the pure-V2 path. Our generated agents use the
legacy shapes (V1 compatibility), where the variant is dropped. Rather than ship
a mapping that lies, the tier map stays variant-free and `deep`/`standard`
converge on the same model. Restoring the distinction is a follow-up: migrate
generated agents to the V2 `permissions:` list and `request:` body, which also
requires teaching the shared YAML subset to emit lists and reworking the golden
fixtures. That is a separate, safety-relevant change (permission ordering), not
part of this one.

### Why these models

Benchmark evidence gathered 2026-10-21 (Vals AI, Artificial Analysis, vendor
cards; persisted as research #114/#115):

- **DeepSeek V4.1 Flash (1017)** is the strongest *scoped* coder in its price
  class — SkillsBench 69.80% (#1/35, the benchmark that supplies task + context,
  which is what our subagents get), Vibe Code Bench v1.1 87.73%, and the lowest
  cost per finished task ($0.58 vs $1.35 GPT-6 Luna, $2.35 GLM-5.3-Flash). It
  also carries the largest OpenCode Go allowance ($80/month, ~173k requests).
- **MiMo-V2.6-Flash** is the cheap tier that holds up: DeepSWE 67.9, VCB 78.96,
  $0.22/test, and a $60/month Go allowance (~150k requests) versus GPT-6 Luna's
  $15 cap (~21k requests).
- Rejected: **GLM-5.3-Flash** (bimodal — 30.76 VCB, 0.00 ProgramBench — and
  3–10× slower), **GPT-6 Luna** (strong scoped, but its allowance is 8× smaller
  than DeepSeek's), **Qwen3.8 Flash** (no independent coding eval), **MiniMax M3**
  (TB4 collapse), **Kimi K2.7 Code** (72% failure on trap tasks), and
  **Muse Spark / Gemini 4 Argon Contributor** (their terms allow training on
  prompts — a privacy decision, not a routing tweak).

## Verification

- `tests/test_adapters.py`: new "OpenCode model tiers" block pins the map
  independently of the adapter (`TIER_MODEL`), asserts every agent renders its
  tier's selector, checks the selector shape, that a `#variant` would round-trip
  if we emitted one, and the precedence rules (target beats tier, no tier
  renders no `model:` line).
- The golden comparison applies a per-agent `MODEL_DELTAS` entry, so any
  unintended model drift still fails, and a stale delta fails too.
- `eng sync opencode` then `opencode debug agents`: all nine agents resolve a
  model (previously eight of nine resolved `null`), explorer to
  `mimo-v2.6-flash`, the rest to `deepseek-v4.1-flash`. A second sync reports
  `0 files changed`.

## Alternatives

- **Leave it unmapped** (status quo): every agent inherits DeepSeek. Simple, but
  the tier vocabulary becomes a lie and a cheap agent can never be cheap.
- **Per-agent `targets.opencode.model` on all nine files**: works today, but
  duplicates the mapping nine times and drifts the moment a model changes.
- **Map tier to vendor only, no `#variant`**: loses the ability to make `deep`
  think harder without switching models, which is the cheapest upgrade we have.

## Consequences

- Changing a model is now a three-line edit (adapter map, pinned `TIER_MODEL` in
  the test, the table in `docs/adapters.md`), not nine hand-edited generated
  files that `eng sync` overwrites.
- `deep` and `standard` routed to the same model until the V2 dialect landed
  (2026-10-22); they now differ by effort variant. The tier vocabulary stays
  honest about intent (lead, architect, reviewer and security are the
  expensive-to-get-wrong roles).
- The model choice is constrained by OpenCode Go's per-model monthly allowance,
  not just token price. DeepSeek V4.1 Flash carries $80/month (~173k requests);
  MiMo-V2.6-Flash $60 (~150k). Revisit the map if the plan changes or an
  allowance is exhausted.
- Out of scope, now tracked: (1) V2 agent frontmatter migration, which unblocks
  effort variants and removes the last legacy field from generated agents;
  (2) DeepSeek's zero-data-retention agreement is renewed monthly (valid through
  2026-10-31 at the time of writing) — if it lapses that is a data-handling
  change, not a config change, and needs its own decision.
