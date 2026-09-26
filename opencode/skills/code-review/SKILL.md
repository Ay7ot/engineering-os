---
name: code-review
description: Adversarial code review that finds reasons NOT to merge. Use for reviewing diffs, branches, PRs, or files. Independent from the author.
metadata:
  audience: reviewer, lead
---
# Code Review

## When to use
- Reviewing changes before merge (diff, branch, PR, files).
- Independent verification of another agent's work.

## Review dimensions
- **Correctness** — satisfies requirements and acceptance criteria.
- **Architecture** — matches approved architecture; no silent redesigns.
- **Security** — authN/Z, tenant isolation, input validation, secrets, injection, SSRF, IDOR, webhooks, race conditions, sensitive data exposure, logging, permissions, dependencies.
- **Data consistency** — writes, transactions, migrations, idempotency.
- **Concurrency** — races, locking, atomicity.
- **Error handling** — failures, partial states, retries, observability.
- **Performance** — hot paths, N+1, unbounded growth.
- **Maintainability** — clarity, duplication, naming, misleading comments.
- **Backwards compatibility** — API/schema/binary changes.
- **Tests** — coverage of risky paths, meaningful assertions.
- **Edge cases** — empty inputs, boundaries, failure injection, timezones, unicode.

## Output format
Per issue: **Severity** (blocker / major / minor / nit), **Location** (path:line), **Issue**, **Why it matters**, **Suggested fix**. End with **Verdict**: APPROVE / CHANGES REQUESTED + blocker summary.

## Rules
- Be adversarial: your job is to find reasons NOT to merge.
- Cite specific code. Distinguish fact from opinion.
- Blockers first. Be thorough but concise.
- Report only; never fix during review.
- Prefer deterministic verification (tests, typecheck, lint, build) as evidence when in scope.

## Checklist
- [ ] Correctness vs requirements
- [ ] No silent architecture divergence
- [ ] Security reviewed
- [ ] Error handling and failure modes
- [ ] Edge cases considered
- [ ] Tests cover risky paths
- [ ] Backwards compatibility checked
- [ ] Verdict: APPROVE / CHANGES REQUESTED