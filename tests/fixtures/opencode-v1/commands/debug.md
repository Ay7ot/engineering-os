---
description: Run the EngineeringOS debugging workflow on a reported problem
agent: lead
subtask: false
---
Run the EngineeringOS debug workflow. Problem: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. **Investigate logs.** Locate and inspect application/server/error logs for the problem window. Check configured observability (dashboards, error trackers) if available.
3. **Inspect relevant code.** Map the code path involved using the explorer agent or directly. Read the actual implementations.
4. **Search recent changes.** Check git history (`git log`, `git diff`) for recent commits that could have introduced the problem.
5. **Reproduce where possible.** Attempt to reproduce the issue locally with a test or a controlled command. If not reproducible, document the evidence gap.
6. **Identify hypotheses.** List plausible root causes ranked by likelihood, each tied to evidence.
7. **Test hypotheses.** Gather evidence to support/refute each hypothesis (logs, tests, targeted experiments) BEFORE modifying code.
8. **Implement a fix.** Only after a hypothesis is supported. Smallest correct change; follow conventions.
9. **Add regression tests.** Add a test that would have caught this bug.
10. **Verify the fix.** Run tests, typecheck, lint, build. Confirm the reproduction no longer fails.
11. **Update knowledge.** `update_project_state` with root cause + fix; `record_task` if useful.
12. **Report.** Root cause (with evidence), the fix, verification evidence, regression coverage.

## Discipline
- Do NOT immediately modify code based on the first hypothesis. Investigate, reproduce, and test hypotheses first.
- If the investigation is blocked (no logs, can't reproduce), say so and propose the most likely cause with the evidence that supports it rather than guessing at a fix.