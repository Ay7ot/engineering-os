---
name: testing
description: Write meaningful tests and verify changes with deterministic tooling. Use when creating tests, running the suite, or verifying acceptance criteria.
metadata:
  audience: tester, builder
---
# Testing

## When to use
- Adding coverage for new behavior.
- Verifying a change or a fix (regression tests).
- Signing off acceptance criteria.

## Rules
- Prefer deterministic tools: test runner, typecheck, lint, build, static analysis. LLM judgment is secondary evidence.
- Test behavior, not implementation. Assert on observable outcomes.
- Cover the risky paths: boundaries, empty input, invalid input, failure injection, concurrency, idempotency, timezones, unicode.
- Each bug fix ships with a regression test that would have failed before the fix.
- Isolation: no shared mutable global state between tests; clean up after each.
- Deterministic tests: no sleeps, no flaky timing; freeze time, inject clocks, use hermetic dependencies.
- Keep tests fast; slow suites get targeted/parallel runs.
- Meaningful assertions: not tautologies, not `expect(true)`.
- If a test requires real infrastructure, prefer hermetic equivalents (testcontainers/in-memory/local), and mark integration tests clearly so CI separates them.

## Verification ladder (use highest available)
1. Typecheck
2. Lint
3. Unit tests
4. Integration tests
5. Build
6. Static analysis / security scanner

## Evidence report sketch
- Command run: `npm test`
- Result: 42 passed, 0 failed
- Acceptance criteria: each criterion -> PASS/FAIL with command evidence
- Coverage gaps: list of risky behaviors untested

## Checklist
- [ ] Deterministic runner used
- [ ] Regression test for each fix
- [ ] Edge cases covered (boundaries, invalid input)
- [ ] Tests isolated and deterministic
- [ ] Acceptance criteria verified with evidence
- [ ] Verification gaps stated explicitly (missing env/command)