# Prompt templates

Fill these in per task. Keep each prompt self-contained: the subagent starts
with fresh context, so anything it needs must be in the prompt. Never point it
at the plan file; paste the task text instead.

## Implementer

```
Task: <task title from the plan>

Context: <where this fits, the module, the related tasks already done,
the approved architecture decisions that constrain it>

Full task text:
<verbatim steps and acceptance criteria from the plan>

Workspace: <path>

Rules:
- Follow `test-driven-development` for each behavior.
- Stay inside this task's scope; do not touch unrelated code.
- Do not read the plan file; this prompt is the plan for you.
- If anything is unclear, ask before implementing.
- Commit the work when the task's tests pass.

Return: status (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED), the
commits created, the test evidence, and anything you flagged in self review.
```

## Spec compliance reviewer

```
Review these commits for spec compliance only:
<commit SHAs or diff>

The spec:
<verbatim requirements and acceptance criteria from the plan>

Check, and report:
- Missing: requirements not implemented.
- Extra: behavior, flags, or files added that the spec did not ask for.
- Wrong: requirements implemented differently from the spec.

Do not review code quality here. Report findings as a checklist with file
references, each marked met, missing, extra, or wrong.
```

## Code quality reviewer

```
Review these commits for quality, given that they already passed spec review:
<commit SHAs or diff, plus the spec for intent>

Apply the `code-review` method. Look for concrete defects with a failure
scenario: correctness, error handling, data and concurrency, compatibility,
security, duplication, weight, and tests that would not catch the bug coming
back.

Output per issue: severity, location (path:line), issue, failure scenario,
suggested fix. End with APPROVE or CHANGES REQUESTED and a blocker summary.
```
