---
name: database-design
description: Design schemas, migrations, and data access that are consistent, performant, and evolvable. Use when creating or modifying tables, collections, or data models.
metadata:
  audience: architect, builder
---
# Database Design

## When to use
- Defining new tables/collections or changing existing ones.
- Planning migrations.
- Designing queries that must stay fast.

## Rules
- Model real entities and relationships; avoid premature denormalization. Denormalize only when there is measured read need.
- Use constraints: NOT NULL, UNIQUE, FK, CHECK, type-specific columns. Reject garbage at the DB, not just in app.
- Choose types carefully (money as integer cents or NUMERIC; timestamps in UTC; fixed-length where bounded).
- Primary keys: stable, immutable, not business data. UUID/ULID for externally visible IDs; auto-increment only for internal.
- Indexes for the query patterns that exist, not speculative ones. Composite indexes: leftmost-prefix rules.
- Avoid SELECT * in production paths. Limit and page large reads.
- Migrations: forward-only, additive when possible; destructive changes (drops, column type changes) are approval-gated.
- Backfill large tables in batches; respect locks and replication lag.
- Idempotency of writes: unique keys for natural dedupe; idempotency keys for retries.
- Transactions: wrap multi-row invariants; keep scope small.
- Soft deletes only when there's a real need (audit, referential integrity) — they add query complexity.

## Migration sketch
```
-- additive
ALTER TABLE charges ADD COLUMN capture_id uuid NULL;
CREATE INDEX charges_capture_id_idx ON charges(capture_id);
```

## Checklist
- [ ] Constraints defined (not null, unique, FK, check)
- [ ] Money/timestamps types correct
- [ ] IDs stable + external-safe
- [ ] Indexes match real query patterns
- [ ] Migrations forward-only; destructive = approval gate
- [ ] Idempotency/dedupe handled
- [ ] Backfill batching planned
- [ ] Sensitive data handling (encryption at rest, redaction)