---
name: product-manager-toolkit
description: Priorise a backlog with RICE, value versus effort and MoSCoW, run discovery interviews, and shape a PRD. Use when scoring or sequencing product work, planning capacity, or sizing a feature portfolio. Not for the delivery spec, see `to-prd`.
metadata:
  audience: lead, planner
  upstream: https://github.com/sickn33/antigravity-awesome-skills
  license: MIT
---
# Product Manager Toolkit

## When to use
- Scoring and sequencing a backlog.
- Planning quarterly capacity and dependencies.
- Running or synthesising customer discovery interviews.
- Choosing the right PRD shape for a feature.

For writing the PRD itself, use `to-prd`. For the interview method, use
`user-research`.

## Prioritisation
**RICE:** score = (reach x impact x confidence) / effort.
- Reach: users affected per quarter.
- Impact: massive 3, high 2, medium 1, low 0.5, minimal 0.25.
- Confidence: high 100 percent, medium 80 percent, low 50 percent.
- Effort: person-months, sized xl, l, m, s, xs.
Record one row per candidate with name, reach, impact, confidence, effort,
compute the score, then sort. Check that the portfolio mixes quick wins with a
few big bets, and that the top items match strategy.

**Value versus effort:** high value plus low effort are quick wins (do first);
high value plus high effort are big bets (plan); low value plus low effort are
fill-ins (maybe); low value plus high effort are time sinks (avoid).

**MoSCoW:** must have (critical for launch), should have (important, not
critical), could have (nice to have), won't have (explicitly out of scope).

Full definitions, weights, and worked examples: `references/frameworks.md`.

## Discovery
1. Run semi-structured interviews on problems, not solutions; on past behaviour,
   not future intentions; record only with permission.
2. Keep the guide timed: context (5 min), problem exploration (15 min), solution
   validation (10 min), wrap-up (5 min).
3. Synthesise: group pain points, rank by severity and frequency, then map them
   to opportunity areas.
4. Write hypotheses: "We believe that changing X for users Y will produce
   outcome Z. We will know we are right when the metric moves."
5. Pick a north star metric that reflects core value and is measurable,
   actionable, and a leading indicator.

Interview script and a fuller guide: `references/discovery.md`.

## PRD shapes
- Standard PRD: complex features, roughly 6 to 8 weeks of work.
- One-page PRD: simple features, roughly 2 to 4 weeks.
- Feature brief: exploration, roughly 1 week.
- Epic: sprint-based delivery.
Every shape states the problem before the solution, success metrics up front,
explicit out of scope, and copy-pasteable acceptance criteria.

## Common pitfalls
- Solution-first thinking before the problem is understood.
- Analysis paralysis: researching without shipping.
- Feature factory: shipping without measuring impact.
- Stakeholder surprise from late communication.
- Metric theatre on vanity metrics; ignoring technical debt.

## Checklist
- [ ] Candidates scored and sorted; portfolio leans on quick wins
- [ ] Team capacity and dependencies checked, with a buffer of about 20 percent
- [ ] Interviews captured problems, not solution requests
- [ ] Each hypothesis has an outcome and a metric
- [ ] North star metric is actionable and leading
- [ ] PRD states problem, success metrics, and out of scope
