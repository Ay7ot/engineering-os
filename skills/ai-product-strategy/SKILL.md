---
name: ai-product-strategy
description: Design where AI belongs in a product: the human-AI boundary, build versus buy, model choice, and imperfect accuracy. Use when planning an AI feature or roadmap, or when AI is being added without a clear user problem. For implementation see `ai-product`, for measurement `ai-evals`.
metadata:
  audience: lead, architect
  upstream: https://github.com/RefoundAI/lenny-skills/tree/main/skills/ai-product-strategy
  license: MIT
---
# AI Product Strategy

## When to use
- Deciding whether and where AI belongs in a product or roadmap.
- Setting the boundary between what the model decides and what people decide.
- Choosing to build, buy, or fine-tune, and picking models.
- A team is adding AI without a clear user problem behind it.

For shipping the feature, use `ai-product`. For measuring quality, use
`ai-evals`. For the system shape, use `architecture-analysis`.

## Principles
- **Start with the problem, not the AI.** Begin from a minimal-impact use case a
  real user problem justifies, and gauge current capability on it before
  widening.
- **Define the human-AI boundary deliberately.** State what the model is
  responsible for, what people are responsible for, and how disagreements are
  resolved. This is the core product decision.
- **Design for squishiness.** At 99 percent accuracy the model is wrong one time
  in a hundred; design the experience for that case instead of assuming it away.
- **Build for the slope, not the snapshot.** Capability and price move quickly;
  keep model choice behind your own interface so it can be swapped.
- **Flywheels beat first-mover advantage.** Log human decisions so the system
  improves with use; the improvement loop matters more than being first.
- **Use a society of models.** Match each task to a specialised model (reasoning,
  speed, code) and use deterministic algorithms where they already win. Keep the
  model where it adds judgement, not where a rule is exact.
- **Assume the human is the bottleneck.** Prefer systems that are useful without
  constant prompting, and make interaction natural and often asynchronous.
- **Respect non-determinism.** Neither user behaviour nor model output is
  predictable; test across both, and expect inputs you did not anticipate.

## Questions to ask the user
- What specific user problem does the AI solve?
- What should the AI decide, and what should people decide?
- How will the product behave in the cases where the model fails?
- What feedback loop will improve the system over time?
- Are you building for today's capability, or anticipating the next model?
- Are evals and observability in place (`ai-evals`, `observability`)?

## Common mistakes
- AI for its own sake, with no user problem behind it.
- Single-model thinking: no specialised models, no deterministic fallbacks.
- No designed experience for when the model is wrong.
- An architecture that cannot swap models as they improve.
- No measurement or observability from day one.
- Over-automation that removes people where they add value.

## Deep detail
- Practitioner insights and quotes: `references/guest-insights.md`

## Checklist
- [ ] User problem stated before the AI approach
- [ ] Human-AI boundary written down, including conflict handling
- [ ] Failure experience designed for the imperfect cases
- [ ] Model choice abstracted so it can be swapped
- [ ] Feedback loop that logs human decisions
- [ ] Evals and observability planned (`ai-evals`, `observability`)
