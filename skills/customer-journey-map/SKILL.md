---
name: customer-journey-map
description: Map a customer journey stage by stage with touchpoints, thoughts, emotions, pain points, and opportunities. Use when mapping the customer experience, finding friction or drop-off, or improving onboarding and retention. Not for running the interviews, see `user-research`.
metadata:
  audience: lead, researcher
  upstream: https://github.com/phuryn/pm-skills
  license: MIT
---
# Customer Journey Map

## When to use
- Understanding the end-to-end experience for one specific persona.
- Finding where users drop off, get confused, or churn.
- Improving onboarding, activation, or retention with evidence.
- Turning interview, survey, analytics, or support data into a shared picture.

If the user provides files, `read` them first (transcripts, survey exports,
support tickets, analytics, existing maps). If a product URL is given, use
`websearch` to understand it before mapping. For the interview method itself,
use `user-research`.

## Method
1. **Choose one persona.** A specific persona with a job to be done, not
   "users". Note the segment and the trigger that starts the journey.
2. **Fix the stages.** Start from awareness, consideration, acquisition,
   onboarding, engagement, retention, advocacy, and rename to fit the product.
   Do not skip a stage because data is thin; mark the gap.
3. **Fill each stage.** Record touchpoints, user actions, thoughts and
   questions, emotions, pain points, and opportunities.
4. **Mark the critical moments.** The aha moment (first real value), the moments
   of truth (where they commit or abandon), and the churn triggers.
5. **Build the table.** One row per stage, with a column per dimension.
6. **Prioritise improvements.** Rank pain points by impact on conversion or
   retention; separate quick wins from deeper investments.

| Stage | Touchpoint | User action | Emotion | Pain point | Opportunity |
|---|---|---|---|---|---|

Template and worked example rows: `references/journey-map-template.md`.

## Rules
- Evidence beats opinion: anchor every emotion and pain point to a quote, a
  metric, or an observed behaviour.
- One map per persona. Averaging personas hides the friction that matters.
- Keep actions and emotions separate; "frustrated when the invite expires" is
  two facts, not one.
- Keep the table as the source of truth; for a rendered version, draw it with
  the `diagrams` skill or a whiteboard tool rather than hand-maintaining a
  picture.
- A map is a working document: date it, name an owner, and revisit it when the
  journey changes.

## Common mistakes
- A generic persona, so nothing in the map bites.
- Touchpoints listed without the user's thoughts or feelings.
- Stopping at the current state and skipping the opportunity column.
- A one-off exercise: no owner, no follow-up changes.

## Checklist
- [ ] One specific persona with a job to be done
- [ ] Stages run from awareness through advocacy, gaps marked
- [ ] Touchpoints, actions, thoughts, emotions, and pain points filled
- [ ] Aha moment, moments of truth, and churn triggers named
- [ ] Improvements ranked by impact; quick wins separated
- [ ] Owner and review date set
