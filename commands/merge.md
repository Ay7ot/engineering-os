---
description: "Run the merge gate for the current branch or PR: head SHA, reviewer verdict, raw verification, CI, and Vercel threads"
targets:
  opencode:
    agent: lead
    subtask: false
---
Run the EngineeringOS merge gate. Scope: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. Resolve the PR and pin its head SHA: `gh pr view --json number,headRefOid,baseRefOid,mergeable,reviewDecision,statusCheckRollup,url`.
3. Confirm the independent reviewer verdict covers that exact head SHA. A verdict for an earlier SHA is not a pass. If the head moved, re-review the delta first.
4. Confirm raw verification evidence for that SHA: the test, typecheck, lint and build commands and their output. Author-reported results are not evidence.
5. Confirm CI is green for that SHA: `gh pr checks`.
6. Fetch the Vercel review comments and count unresolved threads: `gh api repos/<owner>/<repo>/pulls/<number>/comments`. Every finding is either fixed or recorded as a false positive with a reason. An unresolved thread is a blocker.
7. Confirm the PR is mergeable and the base is current.
8. If any gate fails, stop. List exactly what is missing and do not merge.
9. If all gates pass, present the evidence: PR, head SHA, reviewer verdict, verification commands and results, CI, Vercel thread counts.
10. Ask with the `question` tool before merging when the change is sensitive: auth, payments, PII or PHI, data or migrations, concurrency, build config, public APIs, dependencies, secrets, infrastructure, deployment or production. For a routine change, merge with the project's convention.
11. Confirm the merge commit, the CI run on the base branch, and any deploy. Record the verdict, head SHA and Vercel thread count in project state.

## Discipline
- No reviewer verdict for the head SHA means no merge. A review by the author or by the same session that wrote the code does not count.
- No raw verification evidence means no merge.
- An unresolved Vercel finding means no merge.
- A red or pending CI check means no merge.
- Do not force-push, bypass checks or merge over a blocker. Escalate instead.
