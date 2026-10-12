---
name: scoping-cutting
description: Scope and cut a version to fit a fixed time budget, using appetite, an MVP as a hypothesis test, and aggressive cutting. Use when defining an MVP, fighting scope creep, or deciding what to drop to ship sooner. Not for sequencing the build, see `project-planning`.
metadata:
  audience: lead, planner
  upstream: https://aiuxplayground.com/skills/scoping-cutting
  license: MIT
---
# Scoping and Cutting

## When to use
- Defining an MVP or a first version of a feature.
- Scope keeps growing and a deadline is at risk.
- Deciding what to drop, defer, or kill.
- A team is estimating effort instead of choosing a budget.

For putting the surviving work in order, use `project-planning`.

## Method
1. **State the hypothesis.** Write the single thing this version must validate,
   before any feature list. If you cannot, the scope is not ready.
2. **Set the appetite.** Fix the maximum time you are willing to spend, and the
   team size, then design a version that fits inside it. Vary scope, not the
   deadline.
3. **Find the essential core.** List the features assumed necessary, cut the
   list in half, then cut it in half again. Build that.
4. **Cut vertically, not horizontally.** Ship a smaller complete value
   proposition (the scooter), not an incomplete piece of the bigger one (the
   wheels and the axle).
5. **Prefer manual validation.** Where a person can play the role of the feature
   (a concierge or Wizard of Oz test), do that before building automation.
6. **Design for learning.** Optimise how fast you learn whether the hypothesis
   is true, not only how fast you ship.
7. **Kill on time.** If the work is still unsolved at the appetite limit, let it
   die, unless the user consciously re-decides at that moment.

## Rules
- Appetite over estimates: never ask "how long will this take", ask "what can we
  do within this budget".
- An MVP tests a hypothesis. It is not a low-quality version of the whole
  product, and it is not the most you can build in the time.
- Make cutting a normal step: roadmap items can be cut or pivoted without
  signalling failure.
- Keep the team small. Constraints force the simplest effective solution.

## Questions to ask the user
- What is the single hypothesis this version validates?
- What is the maximum time you will invest before shipping?
- What would you cut if you had to ship in half the time?
- Can this value proposition be tested manually first?
- If it misses the budget, do you kill it or consciously re-decide?
- What is the smallest thing that still delivers complete value?

## Common mistakes
- Estimating effort instead of time-boxing.
- Building the axle: an incomplete part of a larger feature.
- Extending deadlines instead of cutting scope, so nothing ever dies.
- Over-building the MVP before testing the core hypothesis.
- Defaulting to build when a manual test would validate faster.

## Deep detail
- Cutting tactics and quotes: `references/guest-insights.md`

## Checklist
- [ ] Hypothesis written before the feature list
- [ ] Appetite fixed in time and team size
- [ ] Feature list halved twice
- [ ] Vertical slice chosen, not a horizontal fragment
- [ ] Manual test considered before automation
- [ ] Kill or re-decide rule stated for the budget limit
