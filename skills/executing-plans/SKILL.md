---
name: executing-plans
description: Execute a written implementation plan task by task in a fresh session, running each task's verification and pausing at review checkpoints. Use when handed a plan to implement in a separate session. See `project-planning` to write a plan, `subagent-driven-development` for same-session dispatch.
metadata:
  audience: builder, lead
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Executing Plans

## When to use
- A written implementation plan exists and you will implement it in this
  session, with a reviewer working separately or checkpoints agreed.
- A fresh session picks up a plan another session wrote.
- Not for writing the plan itself (see `project-planning`), and not for
  dispatching a subagent per task inside one session (see
  `subagent-driven-development`).

## Step 1: Load and review the plan
1. Read the plan file in full, once.
2. Review it critically before starting: does every task have concrete steps and
   a verification? Is a dependency missing, a task too large, a step ambiguous?
3. Raise concerns with the human before starting. Do not start around a known
   gap and hope it resolves.
4. No concerns: create a `todowrite` list with every task and proceed.

## Step 2: Execute
For each task in order:
1. Mark it in progress.
2. Follow the plan's steps exactly; they are deliberately bite-sized. Do not
   merge or reorder steps without telling the human.
3. Run the verification the task names (test, typecheck, lint, build). Use the
   `testing` ladder, and do not claim a step passes without fresh output (see
   `verification-before-completion`).
4. Mark the task complete only once its verification passes.
5. At the checkpoints the plan names, stop and hand off for review before
   continuing. `code-review` is the reviewer's method.
6. When a finished task is passing, run `simplify` on the change before review.

## Step 3: Complete
After the last task and its verification:
- Re-run the full suite and the plan's acceptance criteria.
- Check the plan and the requirements line by line, and report any gap.
- Finish the branch and open the review (see `git-workflow`).

## When to stop and ask
Stop executing immediately and ask when:
- a blocker appears: a missing dependency, an unclear instruction, a failing
  verification you cannot explain;
- the plan has a critical gap that prevents starting;
- verification fails repeatedly after fixes;
- the fundamental approach needs rethinking.

Ask rather than guess. Do not force through a blocker. Never start
implementation on main or master without explicit consent.

## When to revisit the plan
Return to Step 1 when the human updates the plan from your feedback, or when the
approach must change. Record plan changes before executing them.

## Checklist
- [ ] Plan read in full and reviewed critically before any edit
- [ ] Concerns raised and resolved before starting
- [ ] Todowrite holds every task; tasks executed in order with their steps
- [ ] Each task's verification run and passing before it is marked complete
- [ ] Review checkpoints honoured; change simplified before review
- [ ] Full suite and acceptance criteria verified at the end
- [ ] Blockers and plan gaps escalated instead of guessed around
