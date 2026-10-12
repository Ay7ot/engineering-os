---
name: measuring-product-market-fit
description: Assess and reach product-market fit using the Sean Ellis survey, retention curves, reference customers and pull signals, then decide whether to scale or keep iterating. Use when asking if you have PMF, reading retention data, or choosing between scaling and iterating.
metadata:
  audience: lead, researcher
  upstream: https://github.com/RefoundAI/lenny-skills/tree/main/skills/measuring-pmf
  license: MIT
---
# Measuring Product Market Fit

## When to use
- Someone asks whether they have product-market fit.
- Retention data needs interpreting before more spend.
- Deciding whether to scale acquisition or keep iterating.
- A segment looks promising and you want to know if it is real.

## How to work
Ask how many customers exist, what retention looks like at day 7, 30 and 90,
and what signals they are seeing. Then separate three situations: pre-PMF,
PMF in one segment, and genuine fit that is ready to scale. Apply only the
framework that matches.

## Signals, strongest first
- Retention is the ultimate metric. If people come back, you are creating value. A curve that flattens, or a "smile" that rises over time, is the strongest signal. A curve decaying toward zero is not fit, whatever acquisition looks like.
- Sean Ellis survey. Ask users how they would feel if they could no longer use the product: very disappointed, somewhat disappointed, not disappointed. Around 40 percent saying "very disappointed" is the threshold to watch. It is a leading indicator before long retention data exists.
- Reference customers. The holy grail is a customer who loves it enough to tell others. Target roughly 6 to 8 references for B2B and 15 to 25 for B2C before launching publicly.
- Pull. Real intent shows in the questions: "How are you pricing this?", "When can we start?" Buyers drive next steps instead of politely saying it is interesting. See `user-research` for capturing this in interviews.
- Fit is obvious when it is real. If there is genuine doubt, you most likely do not have it. Look for the market pulling the product out of your hands.
- Outage test. If the product goes down and nobody complains, you are not mission critical yet.

## Fit is multi-stage, not binary
Four rough levels by customer count: 3 to 5, 5 to 25, 25 to 100, then 100 plus.
Sequence the focus: satisfaction at the first level, demand at the second,
efficiency at the third. Fit also lives in segments, not universally. Find the
segment with the strongest pull before expanding.

## It can be lost and it needs distribution
Fit is not static. Markets shift, competitors improve and expectations rise, so
keep improving or you can fall out of fit in a year or five. Fit also requires
distribution: strong retention with no way to reach more users is not
product-market fit.

## Questions to ask
- "If users could no longer use the product, what percentage would be very disappointed?"
- "What does retention look like at day 7, 30 and 90?"
- "Do you have customers willing to be references?"
- "Is the market pulling the product from you, or are you pushing it?"
- "Are customers driving next steps, or just being polite?"
- "Which specific segment has the strongest fit?"

## Common mistakes
- Mistaking a launch spike or press coverage for fit; look for sustained organic growth.
- Ignoring retention because acquisition numbers look good.
- Scaling paid growth before fit, which burns cash and can damage the brand.
- Conflating a large market with having fit inside it.
- Optimising for "somewhat disappointed" users instead of what makes "very disappointed" users love the product.

## Where to get the data
Use `analytics` for retention cohorts and activation events, and
`onboarding-cro` when the first-run experience is what is capping retention.

## Checklist
- [ ] Stage classified: pre-PMF, segment fit, or scale ready
- [ ] Retention curve read at day 7, 30 and 90
- [ ] Sean Ellis percentage calculated, not estimated
- [ ] Reference customer count against the B2B or B2C target
- [ ] Pull signals checked in customer questions and next steps
- [ ] Strongest segment identified before any expansion
