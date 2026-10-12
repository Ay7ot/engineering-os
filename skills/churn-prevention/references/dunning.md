# Dunning playbook

Dunning recovers involuntary churn: payment failures that would otherwise end a subscription. The stack runs pre-dunning, smart retry, dunning emails, a grace period, then hard cancel.

## Pre-dunning

- Card expiry alerts 30, 15 and 7 days before the card expires.
- Prompt for a backup payment method at signup.
- Enable card-updater services, which let the networks refresh expired cards and reduce hard declines substantially.
- Send a pre-billing notice 3-5 days before an annual charge.

## Retry by decline type

| Decline type | Examples | Strategy |
|---|---|---|
| Soft (temporary) | Insufficient funds, processor timeout | Retry 3-5 times over 7-10 days |
| Hard (permanent) | Card stolen, account closed | Do not retry; ask for a new card |
| Authentication required | 3D Secure, SCA | Send the customer to update payment |

Retry timing: retry 1 at 24 hours, retry 2 at 3 days, retry 3 at 5 days, retry 4 at 7 days with an escalated email, then hard cancel after four attempts with a clear reactivation path.

Retry on the day of the month the payment previously succeeded: if day 1 worked before, retry on day 1. Most billing providers offer smart retries that handle this automatically.

## Dunning email sequence

| Email | Timing | Tone | Content |
|---|---|---|---|
| 1 | Day 0 | Friendly alert | Payment did not go through; update the card |
| 2 | Day 3 | Helpful reminder | Update payment to keep access |
| 3 | Day 7 | Urgency | Account pauses in 3 days |
| 4 | Day 10 | Final warning | Last chance to keep the account active |

Rules: direct link to the payment update page with no login required where possible, state what they will lose, never blame the customer, include a support contact, and prefer plain text over designed HTML.

## Recovery benchmarks

| Metric | Poor | Average | Good |
|---|---|---|---|
| Soft decline recovery | under 40 percent | 50-60 percent | 70 percent plus |
| Hard decline recovery | under 10 percent | 20-30 percent | 40 percent plus |
| Overall payment recovery | under 30 percent | 40-50 percent | 60 percent plus |
| Pre-dunning prevention | none | 10-15 percent | 20-30 percent |

## Provider capabilities

| Provider | Smart retries | Dunning emails | Card updater |
|---|---|---|---|
| Stripe | Built in | Built in | Automatic |
| Chargebee | Built in | Built in | Via gateway |
| Paddle | Built in | Built in | Managed |
| Recurly | Built in | Built in | Built in |
| Braintree | Manual config | Manual | Via gateway |

## After recovery

- Confirm the update and the next charge date so the customer is not surprised twice.
- If the account was paused, restore access before the next email goes out.
- Log the decline type and recovery outcome so retry rules can be tuned.
