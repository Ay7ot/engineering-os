---
name: subagent-driven-development
description: Execute an implementation plan in the current session by dispatching a fresh subagent per task, with a spec compliance review then a code quality review after each. Use when a plan has mostly independent tasks. Not for a separate session: see `executing-plans`.
metadata:
  audience: lead, builder
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Subagent-Driven Development

## When to use
- A written implementation plan has mostly independent tasks and you will
  execute it in this session.
- You want fresh context per task and automatic review checkpoints.
- Not when tasks are tightly coupled (execute them manually), and not for a
  parallel session (use `executing-plans`).

## Setup
1. Read the plan once. Extract every task with its full text and the context
   each one needs.
2. Create a `todowrite` list holding all tasks.
3. Confirm the workspace is isolated before the first dispatch (see
   `using-git-worktrees`).

## Per task
1. **Dispatch one implementer subagent.** Give it the full task text, the
   surrounding context, the workspace path, and the constraint to follow
   `test-driven-development`. Never make it read the plan file itself.
2. **Answer its questions before it starts.** If it asks, supply the missing
   context and re-dispatch rather than rushing it into implementing.
3. **It implements, tests, commits, and self-reviews**, returning one status:
   - DONE: go to review.
   - DONE_WITH_CONCERNS: read the concerns first; resolve correctness or scope
     ones before review, note observations and continue.
   - NEEDS_CONTEXT: supply the missing context and re-dispatch.
   - BLOCKED: diagnose. Needs context -> re-dispatch same tier. Needs more
     reasoning -> re-dispatch a stronger tier. Too large -> split it. Plan is
     wrong -> escalate to the human.
   Never force the same setup to retry unchanged.
4. **Spec compliance review.** A fresh reviewer confirms the code matches the
   spec: all requirements met, nothing extra added. Fixes go back to the same
   implementer, then re-review.
5. **Code quality review.** Only once spec review is clear. A fresh reviewer
   applies `code-review`. Fix, then re-review, until approved.
6. **Mark the task complete**, then move to the next.

## Model selection
Use the least capable model that can do the role.
- 1 to 2 files, complete spec, mechanical work: fast tier.
- Multiple files, integration or debugging judgement: standard tier.
- Architecture, design, and review: strongest tier.

## Prompt shapes
Write prompts from `references/prompt-templates.md`: focused on one task,
self-contained, with the spec, the commits or diff under review, the output
format, and what to return.

## Red flags
- Dispatching two implementers in parallel (they conflict; parallel write work
  needs separate worktrees).
- Skipping either review, or starting quality review before spec is clear.
- Accepting "close enough" on spec compliance, or a self-review in place of a
  real review.
- Moving on while a review has open issues.
- Fixing a failed task yourself instead of via a fix subagent.
- Starting on main or master without explicit consent.
- Pausing between tasks to check in. Execute the plan; stop only when blocked,
  when there is a genuine ambiguity, or when all tasks are done.

## Finish
After the last task, dispatch a fresh reviewer over the whole implementation,
then complete the branch (see `git-workflow`).

## Checklist
- [ ] Plan read once, all tasks extracted with full text, todowrite created
- [ ] One fresh implementer per task; its questions answered first
- [ ] Each implementer status handled per its meaning
- [ ] Spec review passed before quality review starts
- [ ] Each finding fixed by the implementer and re-reviewed
- [ ] Final whole-implementation review before finishing
