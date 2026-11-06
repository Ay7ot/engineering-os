---
description: "Review current changes, branch, PR, or specified files"
targets:
  opencode:
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
3. Build the review packet: the diff and changed-file list, the plan and acceptance criteria, the project rules, the sensitive-path flags, and raw verification output (tests, typecheck, lint, clean build, CI status).
4. Run or collect deterministic verification. The reviewer may run its allowlisted commands; otherwise have the tester run them and pass the raw output. For an external or untrusted change, run verification in a disposable environment and pass the raw output to the reviewer.
5. Invoke the reviewer agent (adversarial) with the packet. Require the `code-review` skill, including the cross-boundary pass.
6. Invoke the security agent when the scope touches auth, payments, PII or PHI, data or migrations, concurrency, build config, public APIs, dependencies, secrets, infrastructure, or deployment.
7. Synthesize findings into a report: severity-ranked issues with locations, why each matters, suggested fixes, verification evidence, and a clear verdict (APPROVE / CHANGES REQUESTED).
8. Update `engineering-memory` `update_project_state` with review outcome when meaningful.
9. Report to the user, and ask whether to apply any changes if the user wants fixes.

## Discipline
- Reviewer is adversarial and independent: it finds reasons NOT to merge.
- The review is not complete without verification evidence or an explicit statement of what could not be verified.
- Prefer deterministic verification: tests, typecheck, lint, clean build, and CI status. Report the command and result.
- Do not edit code during review unless the user asks for fixes.