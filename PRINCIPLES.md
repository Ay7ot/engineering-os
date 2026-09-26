# PRINCIPLES.md — Global Engineering Principles

OpenCode agents and all compatible agents: follow these unless project context overrides.

1. Research first, ask later. Primary sources (official docs, RFCs, repo source) over blogs.
2. Map before modifying. Explorer produces concise repo maps: stack, boundaries, data flow, integration points, conventions, tests, deployment.
3. Architecture before code for anything non-trivial. Problem, current system, requirements, constraints, proposal, alternatives, tradeoffs, failure modes, security, scalability, observability, testing, migration, recommendation, human decisions required.
4. Small, verifiable tasks with acceptance criteria and dependencies.
5. Deterministic verification: typecheck, lint, test, build. Report evidence for PASS/FAIL.
6. Adversarial review: reviewer finds reasons NOT to merge (correctness, architecture, security, data consistency, concurrency, errors, perf, maintainability, compat, tests, edge cases), independent from builder.
7. Security by default: authN/Z, tenant isolation, input validation, no secrets in repo or EngineeringOS, injection/SSRF/IDOR/webhook/race checks, least privilege.
8. Observability: log with correlation, expose health, track task/agent/project/duration/status/failure/retry/human-intervention/model/cost.
9. Idempotency: setup scripts detect existing resources, update only what's needed, never destroy customizations.
10. No silent redesigns: if implementation reveals an architectural problem, stop and report, don't quietly diverge.
11. Debug scientifically: logs, relevant code, recent changes, reproduce, hypotheses, test hypotheses, fix, regression test, report root cause. No patching on first hypothesis.
12. Persist what matters: research likely to be reused, decisions (ADRs), project state changes go to EngineeringOS via the engineering-memory MCP.
