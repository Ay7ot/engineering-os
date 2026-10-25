# Fold the planner and move agent procedure into skills

Date: 2026-10-25
Status: accepted, validated by the Phase 0 eval

## Context

Anthropic's [agent design guidance](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)
(2026-10-22) reports that a single agent loop with skills frequently matches or
beats a subagent architecture on quality, often at lower cost and latency. This
is vendor-reported, measured on enterprise agents on Claude Platform, not a
general deprecation of subagents. It keeps subagents for three cases:
measurable context bloat, parallel work in fresh contexts, and tool-selection
overload or conflicting system-prompt instructions. It also names verification
and modular permissioning as legitimate isolation.

An audit of this engine found the same failure mode in miniature:

- 9 agents, 4,092 words of prompt text, 130 skills.
- Every procedural agent already had a matching skill with the same procedure in
  more detail. The architect's 14-item deliverable list was essentially a copy of
  `architecture-analysis`; planner duplicated `project-planning`, reviewer
  `code-review`, security `security-review`, tester `testing`, explorer
  `repository-exploration`, researcher `technical-research`.
- Every spawn re-read `PRINCIPLES.md`, `USER.md` and the project `AGENTS.md`,
  roughly 1.5k tokens of identical rules before any work.
- CI had no behavioural evals, so the routing could not be measured.

## Decision

Keep the main loop in the lead and delegate only for isolation, independence or
parallelism.

- **Fold `planner`.** The lead writes the plan with the `project-planning` skill.
  The agent had no isolation value: it was a procedure in a prompt.
- **Make `architect` conditional.** The lead uses the `architecture-analysis`
  skill by default and spawns the architect for complex or novel design, where a
  clean context and the deep model earn the handoff.
- **Tier verification.** Moderate work runs tests inline in the builder (or the
  lead). The tester verifies independently for Important and Complex work.
- **Keep the read-only agents.** `reviewer`, `security`, `explorer` and
  `researcher` earn their context windows through permission isolation,
  black-box verification, discardable context and independent research paths.
  Folding them into a lead with `edit: allow` would delete an enforced control.
- **Deduplicate every agent prompt.** Each body is now role, context, tool
  contract, handoff expectations and skill pointers. Procedure lives only in the
  skill it already duplicated.

## Alternatives considered

- **Status quo.** Two copies of every procedure drift apart, and every spawn
  pays for rules it already has.
- **Full consolidation into one agent.** Cheapest to maintain, but loses the
  enforced read-only boundary on review and security, and risks the
  "Frankenprompt" failure with 130 skills.
- **Remove only the planner.** Leaves the duplication and the context tax in
  six other agents.

## Consequences

- Agent prompt text drops from 4,092 to 2,612 words (36% less, measured with
  `wc -w agents/*.md` before and after) and there is one fewer handoff in the
  Complex path.
- Permission blocks, read-only enforcement and model tiers are unchanged, so the
  security properties and cost routing hold.
- The OpenCode golden test now compares agent frontmatter to the frozen fixture
  and asserts the body passes through verbatim. Agent bodies are no longer
  pinned to the pre-migration fixture, because the fixture cannot represent a
  deliberate rewrite.
- Behavioural detail that lived only in an agent prompt is now in a skill, so a
  skill edit can change agent behaviour. That is intended; the harness covers
  routing, and a skill edit still needs a targeted rerun.
- `evals/` holds a 10-task deterministic harness, and `tests/test_evals.py` keeps
  it honest in CI by asserting every check fails on the untouched fixture.

## Validation (Phase 0, 2026-10-25)

Ten tasks, one run per task per config, every agent on
`opencode-go/deepseek-v4.1-flash#max`, in a small sandbox. Baseline is
`git archive HEAD`; current is the working tree. Raw results are in
`/tmp/opencode/eos-evals/results.jsonl`, not committed.

| Metric | Baseline | Current | Delta |
|---|---|---|---|
| Pass | 10/10 | 10/10 | no regression |
| Cost | $0.2827 | $0.1416 | 50% less |
| Wall clock | 2254s | 1195s | 47% faster |
| Input tokens | 599,184 | 254,415 | 58% less |
| Output tokens | 71,558 | 49,410 | 31% less |
| Subagent sessions | 2 | 0 | 2 fewer |

- Current is cheaper on 9 of 10 tasks. `plan-export` is the exception (+32% cost,
  +20% wall), but the current plan is 670 lines against 411, with more explicit
  assumptions, security treatment and acceptance criteria. Both pass the check.
- Architecture: baseline 1445s, $0.164, 1 subagent; current 646s, $0.068, 0
  subagents. Both ADRs contain alternatives, recommendation, design, security and
  failure modes (678 and 527 lines). The lead plus the skill was 2.2x faster.
- Security: baseline 376s, $0.050, 1 subagent, 179-line report; current 115s,
  $0.018, 0 subagents, 305-line report with more findings. The skill-backed loop
  was faster and more thorough on this seeded case.

## Limits of the validation

- One run per task. Repeat a differing task before treating a delta as real.
- The sandbox is one small Python repo. It under-represents the isolation benefit
  of the explorer and researcher on large codebases.
- Every agent ran on the same model, so the numbers measure context and handoff
  overhead, not the production model-tier savings.
- The ADR and plan checks are structural (sections, counts, scope), not a judgment
  of quality. The ADRs were read to confirm they are substantive.
- Most tasks were completed by the lead directly in both configs, so the eval did
  not isolate the planner and architect agents. Security and architecture are the
  only runs where the baseline delegated. The fold is supported by the audit plus
  the absence of regression, not by a head-to-head on those two agents.

## Rollback trigger

- A task the baseline passes and the current fails, traceable to the folded
  routing.
- A review finding that a removed procedure would have caught.
- Rerun `evals/run.py --config both` with the same flags before reverting. Do not
  revert on one run.
