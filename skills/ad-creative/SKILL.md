---
name: ad-creative
description: Generate and iterate ad copy and static creative at scale for Google, Meta, LinkedIn, TikTok and X. Use when asked for headlines, descriptions or RSA copy, or iterating on winning and losing ads; not for campaign setup and targeting (`ads`) or post-click page copy (`copywriting`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/ad-creative
  license: MIT
---
# Ad Creative

## When to use
- Producing ad headlines, descriptions or primary text, from scratch or at volume.
- Writing Google responsive search ads under strict character limits.
- Iterating on ads from performance data: scaling what wins, retiring what does not.

## Before starting
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Platform and format: Google search, Meta feed or stories, LinkedIn, TikTok, X; static, carousel or video.
- Product, offer and audience: what is promoted, the core value, what differs from competitors, who it is for, and their awareness stage.
- Constraints: brand voice, words to avoid, compliance rules, and mandatory disclaimers.

## Modes
1. Generate from scratch, using product context, audience insight and platform rules.
2. Iterate from performance data: identify winning patterns, then generate variations that extend them.
3. Scaled static batches: many concepts per batch, from a grounded inputs corpus and a reusable set of templates.
The loop: pull performance data, identify winning patterns, generate variations, validate specs, deliver.

## Grounded inputs
Ungrounded generation produces ads that sound plausible and look like every other ad in the feed. Before scaling, keep a durable corpus: `inputs/winning-ads/` with 10-20 screenshots of the highest performers from the last 90 days; `inputs/reviews/` with 50-100 customer reviews as text; `inputs/comments/` with top campaign comments, where objections and unprompted praise surface angles; `inputs/brand/` with voice notes, colours and assets; and `outputs/` with dated batch folders.

Rules: every concept cites the source it traces to, no invented claims, statistics or testimonials, and if the winners or reviews folders are empty, stop and ask the user to populate them rather than generating ungrounded work. Refresh winners as new ads scale, and reviews and comments monthly.

## Platform limits
Check every element against the limit before delivering; platforms truncate without warning.

- Google responsive search ads: 15 headlines at 30 characters, 4 descriptions at 90 characters, 2 paths at 15 characters.
- Meta: primary text 125 characters visible (up to 2,200), headline 40, description 30.
- LinkedIn: intro text 150 recommended (600 max), headline 70 recommended (200 max), description 100 recommended (300 max).
- TikTok: ad text 80 recommended (100 max), display name 40.
- X: post text 280, card headline 70, card description 200.
- Responsive search ads must read correctly alone and in any combination, pinned only when necessary, with at least one keyword, one benefit and one call to action headline.
- Full table: `references/platform-specs.md`.

## Angles before headlines
Define 3-5 distinct angles first, each a different reason someone would click: pain point, outcome, social proof, curiosity, comparison, urgency, identity, contrarian.

Then generate variations per angle, varying word choice, specificity (numbers over general claims), tone (statement, question, command) and structure (short punch versus full benefit statement).

## Iterating from data
1. Analyse winners: which themes, structures, word patterns and character lengths recur.
2. Analyse losers: which angles fall flat, and whether they are too generic, too long, or the wrong tone.
3. Generate: double down on winning themes with fresh phrasing, extend winning angles, test 1-2 new angles, and avoid the patterns found in underperformers.
4. Log the iteration: round, date, top performers with metrics, winning patterns, variation counts, angles being tested, and angles retired.

## Quality standards
- Headlines: specific over vague ("Cut reporting time 75%" not "Save time"), benefits over features, active voice, numbers where possible. Avoid jargon, unsupported superlatives, all caps, excessive punctuation, and clickbait the page cannot deliver.
- Descriptions complement the headline rather than repeating it: add proof, handle objections ("No credit card required"), reinforce the call to action, or add genuine urgency.
- Change one variable per test cycle, and let an ad reach at least 1,000 impressions before judging it.

## Output
Organise by angle with character counts, for example:

```
## Angle: Pain point, manual reporting
Headlines (30 max): "Stop Building Reports by Hand" (29)
Descriptions (90 max): "Marketing teams save 10+ hours weekly with automated reporting." (65)
```

Flag anything over limit and give a trimmed alternative immediately. For 10 or more variations, also offer CSV for direct upload. For static batches, save to a dated folder with an index naming each concept's template and grounding source.

## Batch workflow
- Split into sub-tasks: headlines for click-through, descriptions for conversion, primary text for engagement.
- Generate in waves: core angles first, extended variations on the top two angles, then wild-card angles.
- Quality filter: remove anything over limit, remove duplicates, flag possible policy violations, and check that headline and description combinations make sense together.

## Common mistakes
- Headlines that only work together, which responsive search ads then combine randomly.
- Ignoring character limits, or variations that only change wording, not angle.
- No call to action headline, or a generic description that wastes the slot.
- Iterating without performance data, or generating without grounding.
- Testing too many things at once, or retiring creative before it has enough impressions.

## Checklist
- [ ] Marketing context read; platform, offer and audience confirmed
- [ ] Angles defined before headlines
- [ ] Grounded inputs populated for scaled batches
- [ ] Every element within the platform character limit, counts printed
- [ ] Responsive search ads include keyword, benefit and call to action headlines
- [ ] Descriptions add proof or handle objections, not repeat the headline
- [ ] Iteration log records winners, patterns and new angles
- [ ] CSV or dated batch output supplied when generating at volume
