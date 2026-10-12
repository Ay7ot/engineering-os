---
name: marketing-psychology
description: Apply psychological principles and mental models to marketing decisions such as trust, urgency, pricing and onboarding. Use when asking why people buy, picking a bias such as anchoring or social proof, or designing a nudge; not for page layout (`page-cro`) or copy wording (`copywriting`).
metadata:
  audience: lead, builder
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/marketing-psychology
  license: MIT
---
# Marketing Psychology

## When to use
- Explaining why people buy, or why a campaign is not landing.
- Choosing a specific bias or mental model for a page, price or message.
- Stress testing a tactic for manipulation, fake scarcity or false proof.

## Before applying models
- Read the shared context document (for example `docs/marketing-context.md`, see `product-marketing-context`) first, and ask only for what is missing.
- Name the behaviour you want to change, and where the buyer is: awareness, consideration or decision.
- Find out what the buyer already believes. Fighting an existing belief rarely works.

## How to apply
1. Diagnose before prescribing. Ask what currently prevents the action instead of reaching for a favourite bias.
2. Pick one to three models that fit the diagnosis. A stack of ten is a sign the problem is unclear.
3. Explain the mechanism in one sentence so the tactic can be judged, not just cited.
4. Turn it into a concrete change: the exact line, price, default or nudge.
5. State what would falsify it, and hand the test to `ab-testing` rather than assuming it works.

## Quick reference
| Problem | Models worth checking |
| --- | --- |
| Low conversions | Hick's Law, activation energy, BJ Fogg, friction |
| Price objections | Anchoring, framing, mental accounting, loss aversion |
| Building trust | Authority, social proof, reciprocity, pratfall effect |
| Increasing urgency | Scarcity, loss aversion, Zeigarnik effect |
| Retention or churn | Endowment effect, switching costs, status-quo bias |
| Growth stalling | Theory of constraints, local vs global optima, compounding |
| Decision paralysis | Paradox of choice, default effect, nudge theory |
| Onboarding | Goal-gradient effect, IKEA effect, commitment and consistency |

## The handful that carry most weight
- Loss aversion: losses feel about twice as painful as equivalent gains feel good. Frame what they lose by waiting, only when it is true.
- Anchoring: the first number shown shifts every later judgement. Show the higher reference price before the real one.
- Social proof: counts, logos and named testimonials make an outcome feel reachable. Specific beats vague.
- Default effect: pre-selected options win. Choose the default you would defend in public.
- Paradox of choice: three plans beat seven. Recommend one as best for most.
- Zero-price effect: the jump from $1 to $0 is bigger than $2 to $1. Free tiers and trials are disproportionately attractive.
- Endowment and IKEA effects: people value what they already hold or helped build. Let users own, configure or build something early.
- Goal-gradient effect: effort rises near a goal. Show progress and "almost there" states in flows.

## Ethics
- Use real scarcity, real counts, real deadlines. Inventory, seats and timers must be genuine.
- Never fake testimonials, logos, review scores or stock levels. In many markets it is illegal as well as corrosive.
- Prefer opt-out only where it serves the user, and make leaving as easy as joining.
- Flag any tactic that only works because the user cannot tell what is happening.

## Deep reference
The full catalogue, grouped by thinking models, buyer psychology, persuasion, pricing, delivery and growth, is in `references/mental-models.md`.

## Checklist
- [ ] Behaviour and journey stage named before a model is chosen
- [ ] One to three models, each with a plain-language mechanism
- [ ] Tactic written as a concrete change, not a label such as "add social proof"
- [ ] Ethics checked: no fake scarcity, proof or defaults
- [ ] Measurement handed to `ab-testing`
