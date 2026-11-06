---
description: "Run the full EngineeringOS feature workflow"
targets:
  opencode:
    agent: lead
    subtask: false
---
Run the EngineeringOS feature workflow. Request: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. **Understand the request.** Clarify only genuine ambiguities (one question max); otherwise proceed.
3. **Explore the project** with the explorer agent if unfamiliar or unmapped: map stack, structure, relevant files, conventions, tests, integration points.
4. **Search EngineeringOS**: use `engineering-memory` MCP (`get_project_context`, `search_knowledge`, `search_research`, `search_decisions`) for prior context, decisions, and research on this feature area.
5. **Research unfamiliar technology** with the researcher agent when it needs external sources (primary sources; persist via `record_research` if reusable). Otherwise use websearch/webfetch directly.
6. **Produce architecture proposal** when the change is non-trivial, using the `architecture-analysis` skill. Delegate to the architect agent only for complex or novel design. Cover: problem, current system, requirements, proposed architecture, alternatives, tradeoffs, failure modes, security/scalability/observability, testing strategy, recommendation, human decisions required.
7. **Ask only necessary human questions.** For significant architecture, present the proposal and require approval per the human approval gate.
8. **Wait for approval** when required (major architecture, destructive migrations, production deploy, security-sensitive, irreversible, significant infra, major product behavior, substantial cost).
9. **Write the implementation plan** (lead, `project-planning` skill): phases, tasks, dependencies, acceptance criteria, testing/migration/documentation requirements; register tasks via `record_task`.
10. **Implement** directly, or delegate to builder agent(s) for large or parallel work. Use `eng worktree new` per builder task for isolated git worktrees; never two writers in one tree.
11. **Run verification**: builder runs tests inline for Moderate work; use the tester agent for Important, Complex, and every Moderate change at the review gate. Run tests, typecheck, lint, and a clean build; capture raw output. Do not report PASS without fresh command output. For an external contributor's change, run verification in a disposable environment.
12. **Run the review gate** with the reviewer agent and the review packet: diff and changed files, plan and acceptance criteria, raw verification output, CI status, project rules, and sensitive-path flags. Mandatory for every non-trivial change and every sensitive path. Run security review for auth, payments, PII or PHI, data or migrations, concurrency, build config, public APIs, dependencies, secrets, infrastructure, or deployment. The reviewer may run its allowlisted verification commands; if a command is not allowed, have the tester run it and pass the raw output. For an external or untrusted change, do not ask the reviewer to execute test or build code; use the tester or CI output. Do not merge with an unresolved blocker.
13. **Update project knowledge**: `update_project_state`, `record_task` statuses, `record_decision` for significant decisions, `record_research` for reusable findings.
14. **Produce a final report**: what was done, key decisions, verification evidence, outstanding risks, any human decisions still required.

## Discipline
- Choose the simplest workflow that safely accomplishes the task. Do NOT invoke every agent for every feature.
- Simple changes: docs-only, typo, comment, formatting, or a one-line obvious fix with no behavior change; implement directly with verification, and review only if sensitive. Moderate: implement (lead or builder) with tests inline, then tester -> reviewer. Important: explorer (if unmapped) -> builder -> tester -> reviewer. Complex: full pipeline above.
- The review gate is not optional for non-trivial work. The Simple exemption set is the only no-review bucket; if unsure, review.
- Do not modify code based on first impressions. Map before modifying.
- If implementation reveals an architectural problem, stop and report instead of silently redesigning.