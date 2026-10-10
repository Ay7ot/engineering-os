---
name: payments
description: Design and review payment flows (charges, subscriptions, refunds, webhooks, reconciliation) safely. Use when building or reviewing billing/payments code.
metadata:
  audience: architect, builder, security
---
# Payments

## When to use
- Building or modifying charges, subscriptions, refunds, payouts, or payment webhooks.
- Reviewing payment-related code.

## Rules
- Money as integer minor units (cents) or NUMERIC — never floats.
- Idempotency keys on every external charge call and write.
- NEVER process payments without explicit user authorization + confirmation screen for direct charges.
- Webhooks: verify signature, handle replays idempotently, process async, acknowledge quickly (return 2xx even if processing continues; retry on failure).
- Store only what you need: last4, card brand, expiry month/year — never full PAN or CVV.
- Handle declined cards, 3DS/fraud challenges, expired cards, insufficient funds with clear UX.
- Refunds: full/partial, original payment method, idempotent, audit trail.
- Subscription lifecycle: trial -> active -> past_due -> canceled; grace periods; proration rules.
- Reconciliation: provider events vs your records; detect mismatches; dead-letter queue for unprocessable events.
- Currency: never mix currencies in one charge; store currency per transaction.
- Audit trail: every payment state transition logged with actor, amount, idempotency key.

## Checklist
- [ ] Money as integer minor units
- [ ] Idempotency keys everywhere
- [ ] Explicit authorization before charging
- [ ] Webhook signature verification + idempotent replay handling
- [ ] No full PAN/CVV stored
- [ ] Refunds idempotent + audited
- [ ] Decline/fraud paths handled
- [ ] Reconciliation + DLQ for events
- [ ] Payment changes flagged for security review + human gate