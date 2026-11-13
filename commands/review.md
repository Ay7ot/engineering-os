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
   Pin the exact head SHA before reviewing. The verdict is valid only for that SHA. For uncommitted work, review the tree but state that the verdict cannot satisfy the merge gate; commit and re-review the SHA before merge.
3. Build the review packet: the head SHA, the diff and changed-file list, the work order and acceptance criteria, the project rules, the sensitive-path flags, and raw verification output (tests, typecheck, lint, clean build, CI status). If the raw output is missing, mark the review conditional.
4. Run or collect deterministic verification. The reviewer may run its allowlisted commands; otherwise have the tester run them and pass the raw output. For an external or untrusted change, run verification in a disposable environment and pass the raw output to the reviewer.
5. Invoke the reviewer agent (adversarial) with the packet. Require the `code-review` skill, including the semantic passes and the cross-boundary pass. Require the coverage table and a verdict that names the head SHA.
6. Invoke the security agent when the scope touches auth, payments, PII or PHI, data or migrations, concurrency, build config, public APIs, dependencies, secrets, infrastructure, or deployment.
7. If the PR is open, fetch the review threads and count unresolved ones with GraphQL:
   `gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$pr){reviewThreads(first:100){nodes{isResolved path comments(first:1){nodes{author{login} body}}}}}}}' -F owner=<owner> -F repo=<repo> -F pr=<number>`
   Resolve every thread or record why it is a false positive. Do not treat an unresolved thread as a pass.
8. If any commit lands after the review, re-review the delta and issue a new verdict for the new head SHA.
9. Synthesize findings into a report: severity-ranked issues with locations, why each matters, suggested fixes, verification evidence, the head SHA, and a clear verdict (APPROVE / CHANGES REQUESTED).
10. Update `engineering-memory` `update_project_state` with the review outcome, the head SHA and the Vercel thread count when meaningful.
11. Report to the user, and use the `question` tool for the next decision instead of ending on the report.

## Discipline
- Reviewer is adversarial and independent: it finds reasons NOT to merge.
- The verdict is valid only for the head SHA. A moving branch is not reviewed.
- The review is not complete without verification evidence or an explicit statement of what could not be verified. Author-reported results are not verified.
- The semantic passes and the coverage table are mandatory. No coverage table, no verdict.
- Vercel review threads are a second gate, not a replacement for the reviewer. Resolve them before merge.
- Prefer deterministic verification: tests, typecheck, lint, clean build, and CI status. Report the command and result.
- Do not edit code during review unless the user asks for fixes.