---
name: opportunity-solution-tree
description: Build an Opportunity Solution Tree that maps one desired outcome to customer opportunities, candidate solutions and validation experiments. Use when structuring product discovery, prioritising what to build next, or comparing solutions before committing.
metadata:
  audience: lead
  upstream: https://github.com/phuryn/pm-skills/tree/main/pm-product-discovery/skills/opportunity-solution-tree
  license: MIT
---
# Opportunity Solution Tree

A tree that connects one desired outcome to customer opportunities, possible
solutions, and the experiments that validate them. Based on Teresa Torres,
Continuous Discovery Habits. It stops teams jumping to solutions by forcing the
opportunity space to be mapped first.

## When to use
- Structuring discovery for one product outcome.
- Deciding what to build next, or comparing several solutions.
- Organising existing research into a coherent picture.

## The four levels
1. **Desired Outcome** (top): one measurable business or product metric, taken
   from the OKRs or product strategy, for example "increase 7-day retention to
   40%".
2. **Opportunities**: customer needs, pains and desires found through research.
   These are problems worth solving, not features, framed from the customer's
   perspective ("I struggle to...", "I wish I could..."). Prioritise with the
   Opportunity Score, `Importance x (1 - Satisfaction)`, with Importance and
   Satisfaction normalised to 0-1 (Dan Olsen, The Lean Product Playbook).
3. **Solutions**: possible ways to address each opportunity. Generate several per
   opportunity rather than committing to the first idea; the product trio (PM,
   designer, engineer) ideates together, since good ideas often come from
   engineers.
4. **Experiments** (bottom): fast, cheap tests of whether a solution actually
   addresses the opportunity, covering Value, Usability, Viability and
   Feasibility risks. Prefer experiments with skin in the game (Alberto Savoia)
   over opinion-based validation.

## Principles
- One outcome at a time. Do not try to solve everything in one tree.
- Prioritise opportunities, not features. Never let customers design solutions.
- Compare and contrast: generate at least 3 solutions per opportunity before
  choosing, to avoid the first-idea trap.
- Discovery is not linear: loop back when experiments fail, kill solutions that
  do not validate, and explore new branches.
- Continuous, not periodic: update the tree weekly as interviews, analytics and
  experiments teach you more.

## Process
1. Confirm or help articulate the single measurable outcome at the top.
2. Map 3 to 7 opportunities from the research, group related ones, and frame each
   from the customer's perspective.
3. Prioritise with the Opportunity Score or a qualitative ranking; focus on the
   top 2 to 3.
4. Generate 3 or more solutions per prioritised opportunity, from PM, designer
   and engineer perspectives.
5. Design 1 or 2 fast experiments for the most promising solutions. Specify the
   hypothesis, method, metric and success threshold for each.
6. Present the full tree as a clear hierarchy, and save it as markdown when it is
   substantial; use `diagrams` when the user reads diagrams better than lists.

## Checklist
- [ ] One measurable outcome at the top
- [ ] Opportunities framed as customer problems, not features
- [ ] Each prioritised opportunity has at least 3 candidate solutions
- [ ] Every experiment states hypothesis, method, metric and threshold
- [ ] Failing branches killed and the tree updated with new learning
