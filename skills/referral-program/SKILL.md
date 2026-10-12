---
name: referral-program
description: Design, optimise and measure customer referral and affiliate programmes that turn users into an acquisition channel. Use when building a refer-a-friend or affiliate programme, choosing incentives, or diagnosing a low referral rate; not for launch virality (`launch`) or nurture emails (`emails`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/referrals
  license: MIT
---
# Referral and Affiliate Programmes

## When to use
- Designing a referral or affiliate programme from scratch.
- Improving a programme that is not producing referrals or conversions.
- Choosing incentives, trigger moments or a share mechanism.

## Before starting
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Program type: customer referral, affiliate, or both. Note B2B or B2C, average customer lifetime value, and current acquisition cost from other channels.
- Current state: existing programme, current referral rate, and incentives already tried.
- Product fit: how shareable the product is, whether it has network effects, and whether customers already talk about it.
- Resources: tools or platforms in use, and budget for rewards or commissions.

## Referral versus affiliate
- Customer referral: the referrer is an existing customer, rewards are one-time or limited, trust is higher and volume lower. Best for natural word of mouth and self-serve products.
- Affiliate: the affiliate may not be a customer, the commission relationship is ongoing, volume is higher and trust more variable. Best for reaching audiences you do not have and for higher-ticket products.

## The referral loop
Trigger moment, share action, convert referred user, reward, then repeat.

1. Trigger moments: right after the first "aha" moment, after a milestone, after exceptional support, and after renewing or upgrading.
2. Share mechanism, ranked by effectiveness: in-product sharing, then a personalised link, email invitation, social sharing, and finally a referral code for offline.
3. Incentive structure: single-sided (referrer only) is simpler and suits high-value products; double-sided (both parties) converts better with a win-win framing; tiered rewards gamify repeat referral.

## Optimising
- If few customers refer: ask at better moments, simplify sharing to one step, test different incentive types, and make the programme prominent in the product.
- If referrals do not convert: improve the landing experience for the referred user, strengthen the new-user incentive, and keep the referrer's endorsement visible.
- Common problems: low awareness means add in-app prompts; low share rate means reduce to one click; low conversion means fix the referred experience; fraud means add verification and limits; one-time referrers means add tiered rewards.

## Measuring
- Programme health: active referrers in the last 30 days, referral conversion rate, rewards earned and paid.
- Business impact: share of new customers from referrals, acquisition cost via referral versus other channels, lifetime value of referred customers, and programme return.
- Typical findings to validate against your own data: referred customers have roughly 16-25 percent higher lifetime value, 18-37 percent lower churn, and refer others at 2-3 times the rate.

## Before launch
1. Define goals and success metrics.
2. Design the incentive structure.
3. Build or configure the tool.
4. Create the referral landing page.
5. Set up tracking and attribution.
6. Define fraud-prevention rules and terms.
7. Test the complete flow end to end.

## After launch
- Announce to existing customers, add in-app prompts, update the site, and brief support.
- In the first 30 days: review the funnel, identify top referrers, gather feedback, fix friction, and remind non-referrers once.
- Nurture prompts that work: day 7 reminder, day 30 "know anyone who would benefit?", day 60 success story plus prompt, and a prompt after a user milestone. Keep email cadence detail in `emails`.

## Checklist
- [ ] Marketing context read; lifetime value and acquisition cost known
- [ ] Program type chosen (referral, affiliate, or both)
- [ ] Trigger moments identified in the product
- [ ] Share mechanism chosen, ideally in-product and one click
- [ ] Incentive structure chosen and sized
- [ ] Tracking, attribution and fraud rules configured
- [ ] Full flow tested before announcing
- [ ] Programme-health and business-impact metrics tracked
