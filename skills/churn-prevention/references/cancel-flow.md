# Cancel flow detail

## Exit survey reasons

| Reason | What it tells you |
|---|---|
| Too expensive | Price sensitivity; may respond to a discount or downgrade |
| Not using it enough | Low engagement; may respond to a pause or onboarding help |
| Missing a feature | Product gap; show roadmap or a workaround |
| Switching to a competitor | Competitive pressure; learn what they offer |
| Technical issues or bugs | Product quality; escalate to support |
| Temporary or seasonal need | Usage pattern; offer a pause |
| Business closed or changed | Unavoidable; learn and let go gracefully |
| Other | Catch-all; include a free text field |

Survey rules: one question, single-select with optional free text, 5-8 options, most common first, reviewed quarterly, and never framed as a guilt trip.

## Offer-to-reason mapping

| Cancel reason | Primary offer | Fallback |
|---|---|---|
| Too expensive | Discount, 20-30 percent for 2-3 months | Downgrade to a lower plan |
| Not using it enough | Pause, 1-3 months | Free onboarding session |
| Missing a feature | Roadmap preview with timeline | Workaround guide |
| Switching to a competitor | Comparison plus discount | Feedback session |
| Technical issues | Escalate to support immediately | Credit plus priority fix |
| Temporary or seasonal | Pause | Temporary downgrade |
| Business closed | Skip the offer and respect the situation | none |

## Save offer sizing

- Discount: 20-30 percent for 2-3 months. Show the dollar amount, time-limit it, and never exceed 50 percent.
- Pause: 1-3 months, auto-reactivate with advance notice, keep data and settings, and cap the length.
- Downgrade: show what is kept versus lost, call it right-sizing, and keep the path back up short.
- Feature unlock or trial extension: best for "not getting enough value".
- Personal outreach: top 10-20 percent of accounts by revenue.

## Cancel flow UI principles

- Keep "continue cancelling" visible; do not bury it.
- One primary offer plus one fallback, not a wall of choices.
- Show specific money saved rather than an abstract percentage.
- Use the customer's name and account data.
- Optimise for mobile, where many cancellations happen.
- After cancellation, confirm the end date, keep reactivation one click away, and hand off to the win-back sequence in `emails`.

## Risk signals

| Signal | Risk | Lead time before cancel |
|---|---|---|
| Login frequency drops by half or more | High | 2-4 weeks |
| Key feature usage stops | High | 1-3 weeks |
| Support tickets spike then stop | High | 1-2 weeks |
| Email open rates decline | Medium | 2-6 weeks |
| Repeated billing-page visits | High | days |
| Team seats removed | High | 1-2 weeks |
| Data export initiated | Critical | days |
| Detractor score | Medium | 1-3 months |

## Health score

Combine weighted signals into a 0-100 score: login frequency 0.30, feature usage 0.25, support sentiment 0.15, billing health 0.15, engagement 0.15.

| Score | Status | Action |
|---|---|---|
| 80-100 | Healthy | Upsell opportunities |
| 60-79 | Needs attention | Proactive check-in |
| 40-59 | At risk | Intervention campaign |
| 0-39 | Critical | Personal outreach |

## Cancel flow experiments

Test one change at a time and measure save rate and downstream retention, not saves alone.

| Test | Metric |
|---|---|
| Discount 20 percent versus 30 percent | Save rate, retention effect |
| Pause 1 versus 3 months | Reactivation rate |
| Survey before versus after the offer | Save rate |
| Modal versus full page | Save rate |
| Empathetic versus direct copy | Save rate |

Design the test with `ab-testing`; use funnel analytics to watch each step of the flow.
