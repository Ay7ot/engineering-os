---
description: Run the full EngineeringOS feature workflow
agent: lead
subtask: false
---
Run the EngineeringOS feature workflow. Request: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. **Understand the request.** Clarify only genuine ambiguities (one question max); otherwise proceed.
3. **Explore the project** with the explorer agent if unfamiliar: map stack, structure, relevant files, conventions, tests, integration points.
4. **Search EngineeringOS**: use `engineering-memory` MCP (`get_project_context`, `search_knowledge`, `search_research`, `search_decisions`) for prior context, decisions, and research on this feature area.
5. **Research unfamiliar technology** with the researcher agent (context7 / websearch / webfetch; primary sources; persist via `record_research` if reusable).
6. **Produce architecture proposal** when the change is non-trivial (architect agent), including: problem, current system, requirements, proposed architecture, alternatives, tradeoffs, failure modes, security/scalability/observability, testing strategy, recommendation, human decisions required.
7. **Ask only necessary human questions.** For significant architecture, present the proposal and require approval per the human approval gate.
8. **Wait for approval** when required (major architecture, destructive migrations, production deploy, security-sensitive, irreversible, significant infra, major product behavior, substantial cost).
9. **Create implementation plan** (planner agent): phases, tasks, dependencies, acceptance criteria, testing/migration/documentation requirements; register tasks via `record_task`.
10. **Delegate implementation** to builder agent(s). Use `eng worktree new` per builder task for isolated git worktrees; never two writers in one tree.
11. **Run verification** with the tester agent: tests, typecheck, lint, build; evidence-based PASS/FAIL.
12. **Run review** with the reviewer agent (adversarial). Run security review when relevant (auth, payments, data, webhooks, etc.).
13. **Update project knowledge**: `update_project_state`, `record_task` statuses, `record_decision` for significant decisions, `record_research` for reusable findings.
14. **Produce a final report**: what was done, key decisions, verification evidence, outstanding risks, any human decisions still required.

## Discipline
- Choose the simplest workflow that safely accomplishes the task. Do NOT invoke every agent for every feature.
- Trivial changes: implement directly with verification. Moderate: builder -> tester. Important: explorer -> builder -> reviewer -> tester. Complex: full pipeline above.
- Do not modify code based on first impressions. Map before modifying.
- If implementation reveals an architectural problem, stop and report instead of silently redesigning.