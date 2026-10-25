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
11. **Run verification**: builder runs tests inline for Moderate work; use the tester agent for Important and Complex changes. Tests, typecheck, lint, build; evidence-based PASS/FAIL.
12. **Run review** with the reviewer agent (adversarial). Run security review when relevant (auth, payments, data, webhooks, etc.).
13. **Update project knowledge**: `update_project_state`, `record_task` statuses, `record_decision` for significant decisions, `record_research` for reusable findings.
14. **Produce a final report**: what was done, key decisions, verification evidence, outstanding risks, any human decisions still required.

## Discipline
- Choose the simplest workflow that safely accomplishes the task. Do NOT invoke every agent for every feature.
- Trivial changes: implement directly with verification. Moderate: implement (lead or builder) with tests inline. Important: explorer (if unmapped) -> builder -> tester -> reviewer. Complex: full pipeline above.
- Do not modify code based on first impressions. Map before modifying.
- If implementation reveals an architectural problem, stop and report instead of silently redesigning.