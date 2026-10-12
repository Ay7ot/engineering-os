---
name: ab-testing
description: Design, run and analyse A/B tests and growth experiments that produce statistically valid results. Use when comparing two versions, deciding whether a change is worth testing, or building an experimentation programme; not for implementing the tracking itself (`analytics`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/ab-testing
  license: MIT
---
# A/B Testing

## When to use
- Comparing two versions of a page, flow or message and wanting to measure which is better.
- Deciding whether a proposed change is worth testing.
- Building or running a continuous experimentation programme.

## Before designing
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Establish what you are trying to improve and the change under consideration; the baseline conversion rate and traffic volume; and the constraints (technical complexity, timeline, tools).

## Principles
- Start with a hypothesis, not "let's see what happens": a specific prediction grounded in data or reasoning.
- Test one thing. Multiple changes at once and you cannot tell what worked.
- Statistical rigour: set the sample size in advance, do not peek and stop early, and commit to the method.
- Measure what matters: one primary metric tied to business value, secondary metrics for context, and guardrail metrics to catch harm.

## Hypothesis
- Template: "Because [observation or data], we believe [change] will cause [expected outcome] for [audience]. We will know this is true when [metrics]."
- Weak: "Changing the button colour might increase clicks."
- Strong: "Because heatmaps and feedback show users struggle to find the CTA, making the button larger with a contrasting colour will lift CTA clicks by 15%+ for new visitors, measured as click-through from page view to signup start."

## Test types and sample size
- Types: A/B (two versions, one change, moderate traffic), A/B/n (several variants, higher traffic), multivariate (combinations, very high traffic), split URL (variants on different URLs).
- Sample size per variant at 95% confidence: at a 1% baseline, a 10% lift needs about 150k, 20% about 39k, 50% about 6k; at 3%: 47k / 12k / 2k; at 5%: 27k / 7k / 1.2k; at 10%: 12k / 3k / 550.
- Use a sample-size calculator and divide by daily eligible traffic to get the duration.

## Metrics
- Primary: the single metric the hypothesis targets and the one you call the test on.
- Secondary: metrics that explain why or how the change worked.
- Guardrail: metrics that must not get worse; stop the test if they are significantly negative.
- Example on a pricing page: primary plan selection rate; secondary time on page and plan distribution; guardrail support tickets and refund rate.

## Variants and allocation
- Vary one meaningful thing, bold enough to detect: headline or copy angle, visual design, CTA copy or placement, or the amount and order of content.
- Allocation: 50/50 by default; 90/10 or 80/20 to limit the risk of a bad variant; ramp up gradually for technical risk. Keep a returning user on the same variant and balance exposure across time of day and week.
- Client-side tests are quick to ship but can flicker; server-side assigns the variant before render and needs engineering work.

## Running the test
- Pre-launch: hypothesis documented, primary metric defined, sample size calculated, variants implemented correctly, tracking verified, QA done on every variant.
- During: monitor technical issues, check segment quality, and log external factors. Do not peek and stop early, change variants mid-test, or add traffic from new sources.
- Peeking problem: stopping before the pre-committed sample size produces false positives and wrong calls.

## Analysing results
- 95% confidence means p under 0.05, under a 5% chance the result is random. It is a threshold, not a guarantee.
- Work through: did you reach sample size; is it statistically significant (check confidence intervals); is the effect larger than the minimum detectable effect; do secondary metrics agree; any guardrail harm; any segment differences (mobile versus desktop, new versus returning)?
- Call the result: a significant winner ships; a significant loser means keep control and learn why; no difference means you need more traffic or a bolder test; mixed signals means dig deeper, possibly by segment.

## Programme and documentation
- Record every test: hypothesis, variants with screenshots, results (sample, metrics, significance), decision and learnings.
- Experiment loop: generate hypotheses (analytics drop-offs, customer research, competitors, support tickets, heatmaps, past losers), prioritise with ICE, design and run, analyse, promote winners to a playbook, then generate new hypotheses.
- ICE: score Impact, Confidence and Ease from 1 to 10; ICE = (Impact + Confidence + Ease) / 3. Run the highest first and re-score monthly.
- Velocity targets: 4-8 experiments per month for most teams, a 20-30% win rate for mature programmes, a 2-4 week average duration, 20+ queued hypotheses; track cumulative lift.
- Cadence: weekly, review running tests and guardrails (stop on significant harm, do not call winners early); bi-weekly, conclude tests, update the playbook and launch the next; monthly, review velocity, win rate and backlog and re-prioritise with ICE; quarterly, audit which winning patterns are not yet scaled and which funnel areas are under-tested.
- Playbook entry per winner: date, hypothesis, sample size, result with lift and confidence interval and p-value, guardrails, segment deltas, why it worked, the reusable pattern, where else to apply it, and status.

## Common mistakes
- Design: too small a change to detect, too many changes at once, no clear hypothesis.
- Execution: stopping early, changing things mid-test, not checking the implementation.
- Analysis: ignoring confidence intervals, cherry-picking segments, over-reading inconclusive results.

## Checklist
- [ ] Hypothesis written in the Because / we believe / we will know form
- [ ] One primary metric plus secondary and guardrail metrics
- [ ] Sample size and duration pre-committed; no peeking
- [ ] Variants QA'd and tracking verified on every variant
- [ ] Result judged on sample size, significance, effect size and segments
- [ ] Test and its reusable pattern documented in the playbook
