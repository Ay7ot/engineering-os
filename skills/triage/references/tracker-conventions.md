# Tracker conventions for triage

Reference detail for the `triage` skill: how to pick the work, how to write the
briefs and notes, and how to resume.

## Show what needs attention

Query the issue tracker and present three buckets, oldest first, each with a
count and a one-line summary per item:

1. **Unlabeled**: never triaged.
2. **needs-triage**: evaluation in progress.
3. **needs-info with reporter activity since the last triage notes**: needs
   re-evaluation.

When PRs are in scope, include external PRs in these buckets and tag each line
`[PR]` or `[issue]`. Discovery surfaces only external PRs (the tracker config
defines who counts as external); a collaborator's in-flight PR is not triage
work. The filter is discovery-only: an explicitly named PR is always triaged
regardless of author.

Let the maintainer pick from the list.

## Agent brief

A brief must fully specify the work for an unattended agent: the behaviour to
build, acceptance criteria, dependencies, and the decisions already made. Keep it
in the issue, so it stays durable; update the issue rather than commenting beside
it. A `ready-for-human` brief uses the same structure, plus why the work cannot
be delegated: judgment calls, external access, design decisions, or manual
testing.

## Needs-info notes

```markdown
## Triage Notes

**What we've established so far:**

- point 1
- point 2

**What we still need from you (@reporter):**

- question 1
- question 2
```

Capture everything resolved during grilling under "established so far", so the
work is not lost. Questions must be specific and actionable, never "please
provide more info".

## Resuming a session

If prior triage notes exist on the issue or PR, read them, check whether the
reporter has answered any outstanding questions, and present an updated picture
before continuing. Do not re-ask resolved questions.
