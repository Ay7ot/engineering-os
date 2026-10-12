---
name: pricing-strategy
description: Design and revise software pricing using willingness to pay, packaging, free-tier sampling and the self-serve ceiling. Use when setting a price for the first time, moving between freemium and paid, or testing monetisation changes; for the pricing page itself see `page-cro`.
metadata:
  audience: lead, builder
  upstream: https://github.com/RefoundAI/lenny-skills/tree/main/skills/pricing-strategy
  license: MIT
---
# Pricing Strategy

## When to use
- Setting a price for the first time.
- Choosing between freemium, free trial and paid-only.
- Pricing has not been revisited as the product changed.
- Deciding when to move from self-serve to sales-assisted.

## Work
1. Establish the business model, segments and what value is delivered to whom.
2. Run willingness to pay conversations early, before the roadmap is fixed.
3. Look for technical, market and competitive constraints on the price.
4. Design pricing that can change, then set a review cadence rather than a final number.

## Principles
- Price is a measure of value, the way a litre measures volume. Willingness to pay is the proxy for whether people actually want the product.
- Never set it and forget it. Pricing is part of the roadmap; revisit it every 6 to 12 months as new value ships. Companies labour over features and pick the price from thin air.
- Self-serve has a ceiling. Card processing and individual spending authority cap self-serve at roughly $10,000. Move contracts of about $10,000 to $15,000 and above to a sales-assisted motion.
- Sample premium features in the free experience. Interspersing real paid value for free users converts better than hiding everything behind a hard paywall.
- Reduce early monetary friction. Lowering the barrier buys users more runway to find value, which causally improves their odds of success.
- Prioritise the roadmap by willingness to pay. The 20 percent of features that drive 80 percent of willingness to pay come first.
- Pricing changes are two-way doors. Move fast on reversible changes, and grandfather existing users so the change stays reversible and safe.
- Anchoring, decoy and mental accounting effects apply. See `marketing-psychology` before choosing tier structure or numbers.

## Packaging
- Three tiers, with a clearly recommended one for most buyers.
- Package by the value metric customers already track, not by arbitrary feature counts.
- Make the difference between tiers obvious; avoid a cheap tier that cannibalises the middle.
- Show annual pricing where it improves retention, with the monthly equivalent stated.

## Questions to ask
- "What would customers pay if they had to pay today? Have you asked them directly?"
- "What value does the product create, and for which segment is it highest?"
- "When was pricing last revisited, and what has changed in the product since?"
- "What is stopping a higher price: competition, value delivery, or an assumption?"
- "How do free users experience paid value today?"
- "At what price does the motion need to change from self-serve to sales-assisted?"

## Common mistakes
- Pricing on gut feel rather than willingness to pay research.
- Launching a price and never revisiting it.
- A hard paywall that hides all premium value.
- Trying to close $50K deals through card checkout.
- Racing to the bottom on price instead of differentiating on value.

## Verify changes
Test packaging and price presentation with `ab-testing`, measure impact through
`analytics`, and check the buying experience on `page-cro`.

## Checklist
- [ ] Willingness to pay evidence gathered, not assumed
- [ ] Value metric and tier structure chosen deliberately
- [ ] Premium value sampled inside the free experience
- [ ] Self-serve ceiling respected, sales-assisted path defined above it
- [ ] Existing users grandfathered on any change
- [ ] Review cadence set, within 6 to 12 months
