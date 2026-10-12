# Journey map template and example

## Stage definitions

| Stage | What it covers |
|---|---|
| Awareness | how they first learn the product exists |
| Consideration | what they evaluate and which alternatives they compare |
| Acquisition | how they sign up or purchase |
| Onboarding | first experience, time to first value |
| Engagement | regular usage, habit forming |
| Retention | what keeps them coming back, what would cause churn |
| Advocacy | when and why they recommend the product |

Rename stages to fit the product, but keep their order and keep the first mile
and the exit both visible.

## Per-stage columns

| Column | Question to answer |
|---|---|
| Touchpoint | where the user meets the product, brand, or team (site, email, in-app, support, social) |
| User action | what they actually do |
| Thoughts and questions | what is on their mind ("Is this worth my time?", "How do I import data?") |
| Emotion | how they feel, rated or labelled (excited, confused, frustrated, delighted) |
| Pain point | friction, confusion, drop-off risk, with the evidence behind it |
| Opportunity | how the experience could be improved here |

## Filled example

Persona: a solo developer evaluating an API product, triggered by a failing
integration in their current tool.

| Stage | Touchpoint | User action | Thoughts | Emotion | Pain point | Opportunity |
|---|---|---|---|---|---|---|
| Awareness | search result, blog post | skims the quickstart | "Will this work with my stack?" | curious | code samples in the wrong language | show a tabbed quickstart per language |
| Consideration | pricing page | compares free tiers | "What happens when I hit the limit?" | sceptical | limit is buried in the FAQ | state the limit next to the price |
| Acquisition | signup form | creates an account | "Why do you need a card now?" | annoyed | card required before any call | allow a key-first trial |
| Onboarding | dashboard | runs the first request | "It returned data, good" | relieved | first call needs an env var it does not mention | make the first call copy-paste runnable |
| Engagement | docs, SDK | wires it into the app | "Now what breaks in prod?" | focused | no guidance on retries and rate limits | add a reliability page |
| Retention | invoice, changelog | keeps using it | "Is my traffic growing?" | comfortable | usage is hard to find | surface usage on the dashboard |
| Advocacy | review site | writes a review | "Worth recommending if limits were clearer" | willing | past friction colours the review | fix the earlier stages first |

## Critical moments

- Aha moment: the first successful call returning useful data.
- Moments of truth: hitting the free-tier limit; deciding whether to add a card.
- Churn triggers: a first call that fails on setup; an unexplained usage spike.

## Prioritising improvements

1. List the pain points that sit on the path to the aha moment. Fix these first;
   they move conversion most.
2. Separate quick wins (copy, ordering, defaults) from deeper investments
   (pricing, onboarding rework).
3. For each improvement, name the metric that should move (activation rate, time
   to first value, churn) so the change is testable.
