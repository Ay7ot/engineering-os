---
name: churn-prevention
description: Reduce voluntary and involuntary churn with cancel flows, targeted save offers, proactive retention and failed-payment recovery. Use when customers keep cancelling, designing an exit survey and save offers, or setting up dunning; not for win-back emails (`emails`) or churn tests (`ab-testing`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/churn-prevention
  license: MIT
---
# Churn Prevention

## When to use
- Monthly churn is too high, or customers keep cancelling.
- Building or optimising a cancellation flow and its save offers.
- Recovering involuntary churn from failed payments (dunning).
- Adding proactive retention before customers reach the cancel button.

## Before starting
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Current situation: monthly churn rate (voluntary versus involuntary if known), active subscribers, average revenue per customer, and whether cancel is instant today.
- Product and usage: whether per-user feature usage is tracked, whether engagement drop-offs are visible, past cancellation reasons, and the activation metric that retained users hit and churned users do not.
- Billing and constraints: provider, billing interval, whether pausing or downgrade exists, any retention tooling already in place, B2B or B2C, whether self-serve cancellation is required by regulation, and the brand tone for offboarding.

## Two types of churn
| Type | Cause | Solution |
|---|---|---|
| Voluntary | Customer chooses to cancel | Cancel flows, save offers, exit surveys |
| Involuntary | Payment fails | Dunning emails, smart retries, card updaters |

Voluntary churn is typically 50-70 percent of total churn. Involuntary is 30-50 percent and is usually the easier of the two to fix.

## Cancel flow
Every cancel flow follows the same sequence: trigger, exit survey, dynamic offer, confirmation, post-cancel.

1. Trigger: the customer clicks cancel in account settings.
2. Exit survey: ask why they are cancelling; the answer selects the save offer.
3. Dynamic save offer: present a targeted offer for that reason.
4. Confirmation: if they still cancel, confirm clearly and state the end-of-billing-period timing.
5. Post-cancel: set expectations, keep reactivation easy, and trigger a win-back sequence. Sequence copy belongs to `emails`.

Survey design: one single-select question with optional free text, 5-8 reason options maximum, most common reasons first, and "help us improve" framing rather than "why are you leaving?". Full reason list and offer-to-reason mapping: `references/cancel-flow.md`.

## Save offers
Match the offer to the reason. A discount will not save someone who is not using the product, and a roadmap will not save someone who cannot afford it.

- Discount: 20-30 percent for 2-3 months is the sweet spot. Avoid 50 percent or more, which trains customers to cancel for deals. Time-limit the offer and show the money saved, not just the percentage.
- Pause: 1-3 months maximum, because longer pauses rarely reactivate. Most pausers return when reactivation is automatic with advance notice and data kept intact.
- Downgrade: offer a lower tier with what they keep versus lose, framed as right-sizing the plan, with an easy path back up.
- Feature unlock or trial extension: for "not getting enough value" reasons.
- Personal outreach: for the top 10-20 percent of accounts by revenue, routed to customer success or a founder email.

UI principles: keep "continue cancelling" visible rather than relying on dark patterns, show one primary offer plus one fallback, show dollar amounts, use the customer's own data, and make it work on mobile.

## Proactive retention
The best save happens before the customer clicks cancel. Track leading signals such as login frequency dropping by half, key feature usage stopping, support tickets spiking then stopping, declining email opens, repeated billing-page visits, removed team seats, a data export, or a detractor score. Intervene on a trigger rather than a hunch, for example a usage drop over two weeks gets a "need help with [feature]?" message, and a detractor score gets personal follow-up within 24 hours. Signals, weights and health-score bands: `references/cancel-flow.md`.

## Involuntary churn
Failed payments are the most recoverable churn. The stack is: pre-dunning, smart retry, dunning emails, grace period, hard cancel.

- Pre-dunning: card-expiry alerts at 30, 15 and 7 days, a backup payment method prompt at signup, card-updater services, and a pre-billing notice 3-5 days ahead for annual plans.
- Retry by decline type: soft declines retry 3-5 times over 7-10 days; hard declines do not retry and instead ask for a new card; authentication failures send the customer to update payment.
- Retry timing: 24 hours, then 3, 5 and 7 days, escalating with dunning email; after four retries, hard cancel with a reactivation path.
- Dunning emails: friendly alert on day 0, helpful reminder on day 3, urgency on day 7, final warning on day 10. Link straight to payment update, say what they will lose, avoid blame, and prefer plain text.
- Benchmarks, provider capabilities and the full retry playbook: `references/dunning.md`.

## Metrics
| Metric | Formula | Target |
|---|---|---|
| Monthly churn | Churned / start-of-month customers | under 5 percent B2C, under 2 percent B2B |
| Net revenue churn | (Lost MRR minus expansion MRR) / start MRR | negative (net expansion) |
| Cancel flow save rate | Saved / total cancel sessions | 25-35 percent |
| Offer acceptance rate | Accepted / shown offers | 15-25 percent |
| Pause reactivation | Reactivated / total paused | 60-80 percent |
| Dunning recovery | Recovered / failed payments | 50-60 percent |

Segment churn by acquisition channel, plan, tenure, cancel reason and save-offer type. Test one variable at a time; design the experiment with `ab-testing`.

## Common mistakes
- No cancel flow at all; even a survey plus one offer saves 10-15 percent.
- Hiding cancellation, which breeds resentment, bad reviews and regulatory risk.
- The same offer for every reason, or discounts that are too deep.
- Ignoring involuntary churn, so failures silently cancel accounts.
- Guilt-trip copy, pauses longer than three months, or no post-cancel path.
- Not checking whether a "saved" customer churns again within 30 days.

## Checklist
- [ ] Marketing context read; churn split into voluntary and involuntary
- [ ] Cancel flow has survey, targeted offer, confirmation and post-cancel step
- [ ] Survey has 5-8 reasons with the most common first
- [ ] Save offers mapped to reasons, each with a fallback
- [ ] Cancel option visible and easy to find, no dark patterns
- [ ] Proactive risk signals tracked and tied to interventions
- [ ] Dunning covers pre-dunning, retries, emails and a grace period
- [ ] Metrics baselined; one variable tested at a time
