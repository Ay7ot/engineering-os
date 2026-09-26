---
name: api-design
description: Design consistent, secure, evolvable APIs. Use when creating or extending HTTP/REST, GraphQL, RPC, or internal service APIs.
metadata:
  audience: architect, builder
---
# API Design

## When to use
- Creating a new endpoint, service API, or SDK surface.
- Reviewing an existing API for consistency and security.

## Rules
- Prefer resource-oriented REST for CRUD (nouns, HTTP verbs, status codes); RPC-style only where actions dominate (e.g., operations that aren't CRUD).
- Version explicitly (URL or header) when breaking changes are possible; prefer additive evolution.
- Consistent naming (kebab-case paths, snake_case or camelCase fields — pick one, document it).
- Pagination for list endpoints (cursor preferred over offset for large/skewed sets).
- Idempotency keys for non-idempotent write operations (payments, webhooks).
- Idempotent methods (PUT/DELETE) behave correctly on retry.
- Validation server-side always; error shape consistent (e.g., `{"error": {"code", "message", "details"}}`).
- Authentication on every endpoint by default; authorization checked per-resource (tenant isolation, ownership).
- Never return secrets, internal stack traces, or internal IDs in errors.
- Rate limiting on expensive/abused endpoints.
- Backwards compatibility: never remove or repurpose fields silently; deprecate first.

## Request/response sketch
```
POST /api/v1/orgs/{org_id}/billing/charges
Authorization: Bearer <token>
Idempotency-Key: <uuid>

200 {"charge_id":"...","amount_cents":1200,"status":"succeeded"}
409 {"error":{"code":"idempotency_conflict","message":"...","details":{}}}
```

## Checklist
- [ ] Resource naming consistent
- [ ] Pagination defined
- [ ] Idempotency for non-idempotent writes
- [ ] Error shape consistent
- [ ] AuthN on all endpoints; authZ per resource
- [ ] No secrets/stack traces in errors
- [ ] Versioning considered
- [ ] Deprecation policy for breaking changes