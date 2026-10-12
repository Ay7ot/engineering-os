---
name: usability-testing
description: Plan and run usability tests that validate a concept or find friction before building: choose fidelity, recruit unbiased users, and compare options. Use when planning user tests, validating a prototype, or investigating why users struggle with a product.
metadata:
  audience: lead, builder
  upstream: https://aiuxplayground.com/skills/usability-testing
  license: MIT
---
# Usability Testing

## When to use
- Validating a concept before building it, or optimising an existing flow.
- A prototype needs user validation before more is written.
- Users struggle with something and the cause is not yet clear.

For research planning and synthesis, see `user-research`.

## Start by clarifying the goal
1. What is being validated: a concept, a friction point, or conversion?
2. Which fidelity: Wizard of Oz, fake door, prototype, or production?
3. Who to recruit, what scenario to set, and what to observe?
4. How findings flow back into development, and who iterates on them?

## Core principles
- **Fake it before you build it.** Fake door, smoke and Wizard of Oz tests
  validate the core value proposition before production code, with a human
  performing the "automated" task behind a facade.
- **Small samples reveal big friction.** Around 10 random people give feedback
  representative of a much larger group.
- **Watch users, do not just ask them.** Observe without intervening; when a user
  deviates from the expected path, ask why.
- **Test multiple options, not one.** Present several designs and compare which
  one drives the intended behaviour; a single design tells you little.
- **Overcome creator bias.** Builders overrate how well their product works; give
  the product to someone else and watch them interact with it.
- **Micro-level testing drives millions.** Small copy and button changes can move
  conversion: look for scary or confusing calls to action.
- **Progress through stages.** Fish fooding (your team), then dogfooding (your
  company), then alphas and longitudinal studies, raising confidence iteratively.
- **Make it a team sport.** Have PMs, engineers, designers and the researcher
  react live to sessions in a shared thread.

## Run the test
1. Recruit prospective users with zero skin in the game, so feedback is honest.
2. Write a short scenario and scripted tasks; do not lead the participant.
3. Have the team observe live and note pain points, hesitations and questions.
   Scripted simulations work well when real conditions are hard to stage.
4. Record where users deviate, ask why at that moment, and capture quotes.
5. Review findings together the same day, then fix and re-test.

## Common mistakes
- Testing only one design instead of comparing multiple options.
- Building before validating, skipping Wizard of Oz or fake door tests.
- Relying on internal intuition; employees are too familiar with the product.
- Ignoring micro-level issues such as copy and button labels.
- Testing in isolation, without engineers and designers present.

Deep dive: `references/guest-insights.md` holds the insights from the 11 product
leaders behind these principles.

## Checklist
- [ ] Goal and fidelity chosen deliberately
- [ ] Users recruited who have no stake in the outcome
- [ ] Multiple options tested, not a single design
- [ ] Sessions observed live by cross-functional team members
- [ ] Findings prioritised with users, not by internal opinion alone
- [ ] Fixes re-tested before launch
