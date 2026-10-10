---
name: testing
description: Write meaningful tests and verify changes with deterministic tooling, up to running the real app to see the change work. Use when creating tests, running the suite, verifying acceptance criteria, or confirming a change works end to end.
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
7. Run it for real (below)

## Run it for real
Tests prove what they assert; they do not prove the feature works. When a change
affects something a user or another system sees, run the real thing once:

1. **Find how the project runs.** README, `AGENTS.md`, package scripts,
   Makefile, existing launch configs. Reuse them; do not invent a new way.
2. **Prove the environment is safe before starting anything.** Inspect the
   environment the app will load (env files, config) and confirm:
   - databases point at a local, dev or branch database, not production or a
     database shared with other apps;
   - payment keys are test-mode, and email, SMS and other outbound messaging are
     sandboxed or disabled;
   - no real user or patient data will be read or written.
   If you cannot confirm all of this, **stop and report**; do not run it.
3. **Start it the way users do**, in that disposable environment: local dev
   server, CLI on a temp directory, a test/sandbox account, the simulator.
4. **Drive the changed path** end to end: the request, the click, the command,
   the webhook. Include one failure path (bad input, missing permission).
5. **Observe, do not assume:** response bodies and status codes, logs, screenshots
   or page text, files written, rows changed.
6. **Compare against a baseline** when the claim is "nothing changed": capture
   the same observation from the base commit in a **separate worktree** (never
   by stashing or switching branches in the tree someone is working in), then
   diff it against the change.
7. **Clean up** what you started (servers, temp data, test accounts you created).

Report it like any other evidence: what you ran, what you observed, PASS/FAIL.
If the app cannot be run here (missing env, secrets, devices), say exactly what
is missing instead of claiming it works.

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
- [ ] Environment proven safe (no production/shared data, test-mode keys, messaging off) before running the app
- [ ] User-visible changes exercised in the running app, or the gap stated
- [ ] Verification gaps stated explicitly (missing env/command)