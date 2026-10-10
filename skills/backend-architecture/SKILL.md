---
name: backend-architecture
description: Design maintainable, secure, observable backend services (APIs, services, data, queues, auth, deployment). Use when planning or reviewing backend work.
metadata:
  audience: architect, builder
---
# Backend Architecture

## When to use
- Planning or implementing backend services, APIs, or data layers.
- Reviewing backend code.

## Rules
- Layering: interface/handler -> domain/use case -> data access. Keep domain logic independent of framework and transport.
- API consistency and security per `api-design` and `security-review` skills.
- Configuration: env-based, typed, validated at startup; secrets injected, never in code/repo.
- Errors: typed, handled at the boundary; no leaks of internals; graceful degradation.
- Concurrency: bounded worker pools, backpressure, idempotent consumers, at-least-once + dedupe.
- Data: per `database-design`; repositories abstract storage; transactions at the right scope.
- Queues/jobs: retry with backoff, DLQ, idempotency, dead-letter visibility, monitoring.
- Caching: explicit invalidation strategy; cache-aside with TTL; never trust cache for authz.
- Security: authN/Z at every entry point, tenant isolation, input validation, rate limiting, secrets hygiene.
- Observability per `observability` skill: structured logs with correlation IDs, metrics, health endpoints.
- Testing: unit (domain logic), integration (boundaries/DB/queues), contract tests for APIs; deterministic.
- Deployment: containerized, health checks, graceful shutdown, migration ordering (migrate before deploy where needed), rollback plan.

## Checklist
- [ ] Domain logic decoupled from framework
- [ ] Config validated at startup, secrets injected
- [ ] Errors typed and handled at boundary
- [ ] Idempotent consumers, backpressure
- [ ] Cache with explicit invalidation
- [ ] Security at every entry point
- [ ] Structured logs + metrics + health
- [ ] Unit + integration + contract tests
- [ ] Migration + rollback plan