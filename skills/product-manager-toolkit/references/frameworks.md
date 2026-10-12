# Prioritisation frameworks

## RICE

Score = (reach x impact x confidence) / effort.

| Factor | Definition | Values |
|---|---|---|
| Reach | Users affected per quarter | a number of users |
| Impact | Effect on each user | massive 3, high 2, medium 1, low 0.5, minimal 0.25 |
| Confidence | How sure you are of reach and impact | high 100 percent, medium 80 percent, low 50 percent |
| Effort | Total person-months | xl, l, m, s, xs |

Procedure:
1. Collect candidates from customer feedback, sales requests, technical debt, and
   strategic initiatives.
2. Write one row per candidate: name, reach, impact, confidence, effort.
3. Compute the score and sort descending.
4. Analyse the portfolio: how many quick wins (high score, small effort) versus
   big bets (high score, large effort); check the effort distribution.
5. Compare the top items against strategy before committing them.
6. Plan the quarter against capacity, map dependencies, and leave a buffer of
   roughly 20 percent for unexpected work.

Worked example. A feature reaching 400 users a quarter, impact high (2),
confidence medium (80 percent), effort m (about 2 person-months) scores
400 x 2 x 0.8 / 2 = 320. A feature reaching 2000 users, impact medium (1),
confidence high (100 percent), effort xl (about 6 person-months) scores
2000 x 1 x 1.0 / 6 = 333, so it ranks slightly higher despite costing more.

RICE is a conversation aid, not a verdict. If a low-scoring item is a
prerequisite for a high-scoring one, the dependency wins.

## Value versus effort

|  | Low effort | High effort |
|---|---|---|
| High value | Quick wins: prioritise | Big bets: plan and staff |
| Low value | Fill-ins: do if capacity allows | Time sinks: avoid |

## MoSCoW

- Must have: critical for launch; without it the release does not work.
- Should have: important but not critical; a workaround exists.
- Could have: nice to have; include only with spare capacity.
- Won't have: explicitly out of scope for this release; state it so the
  decision is visible.

## Opportunity cost and re-review

Every item taken is an item not taken. Account for dependencies and shared
work, communicate the ranking and the reason, and revisit the ranking quarterly
rather than treating it as fixed.
