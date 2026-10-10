---
description: Review current changes, branch, PR, or specified files
agent: lead
subtask: false
---
Run the EngineeringOS review workflow. Scope: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. Determine the scope of the review from `$ARGUMENTS`:
   - If empty or "current changes": review the uncommitted diff (`git diff`) and staged changes.
   - If "branch" or a branch name: review changes on the current branch vs its base (e.g., `git diff main...HEAD`).
   - If "PR" or a PR URL/number: fetch the PR diff via `gh` if available and review it.
   - If specific files or paths are named: review those files.
3. Invoke the reviewer agent (adversarial) over the scope, with the relevant acceptance criteria and plan.
4. Invoke the security agent when the scope touches auth, payments, data, webhooks, secrets, or infrastructure.
5. Synthesize findings into a report: severity-ranked issues with locations, why each matters, suggested fixes, and a clear verdict (APPROVE / CHANGES REQUESTED).
6. Update `engineering-memory` `update_project_state` with review outcome when meaningful.
7. Report to the user, and ask whether to apply any changes if the user wants fixes.

## Discipline
- Reviewer is adversarial and independent: it finds reasons NOT to merge.
- Prefer deterministic verification: run tests/typecheck/lint/build as part of review evidence when in scope.
- Do not edit code during review unless the user asks for fixes.