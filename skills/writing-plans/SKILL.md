---
name: writing-plans
description: Write a bite-sized, executable implementation plan with exact paths, code and commands for work that already has a spec or requirements. Use when turning a spec into step-by-step tasks before touching code. Not for phase or dependency decomposition, which `project-planning` covers.
metadata:
  audience: lead, builder
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Writing Plans

## When to use
- A spec or requirements exist and the work is multi-step.
- Another agent, or a future session, will execute the plan without your context.

`project-planning` decides the phases, dependencies and ownership. This skill
writes the per-task detail an executor follows.

## Assumptions
Write for a skilled developer who has zero context for this codebase and knows
almost nothing about the toolset or domain. Assume they are weak at test design.
Document everything: which files to touch, the code, the tests, the docs to
check, how to verify.

## Scope check
If the spec covers several independent subsystems, suggest one plan per
subsystem before writing tasks. Each plan must produce working, testable
software on its own.

## File structure first
Map which files are created or modified and what each is responsible for, before
defining tasks; this locks in the decomposition.
- One clear responsibility per file, with clear boundaries and interfaces.
- Prefer smaller focused files; you reason better about code you hold in context
  at once, and edits are more reliable in focused files.
- Files that change together live together: split by responsibility, not layer.
- In existing codebases follow established patterns; do not restructure
  unilaterally, but a split of a file you are already changing is fair.
- Prefactor to make the change easy, then make the easy change.

## Bite-sized steps
Each step is one action, 2 to 5 minutes: write the failing test, run it and see
it fail, write the minimal implementation, run the tests and see them pass,
commit. TDD, DRY, YAGNI, frequent commits.

## Plan header and task shape
Every plan starts with a goal (one sentence), architecture (2 to 3 sentences)
and tech stack, then the tasks. Each task names files as Create / Modify (with
line range) / Test, then numbered checkbox steps. For every step give the exact
command and the expected output, for example "Expected: FAIL with ..." or
"Expected: PASS". Show the code for any step that changes code.

Save the plan to `docs/plans/YYYY-MM-DD-<feature>.md` unless the user prefers
another location.

## No placeholders
Never write "TBD", "TODO", "implement later", "fill in details", "add
appropriate error handling", "handle edge cases", "write tests for the above"
without the test code, "similar to Task N" (repeat the code, the executor may
read tasks out of order), or a step that says what to do without showing how.
Never reference a type, function or method that no task defines.

## Self-review before handing off
1. Spec coverage: point at a task for each requirement; add a task for any gap.
2. Placeholder scan: `grep` the plan for the red flags above and fix them.
3. Name and type consistency: signatures used in later tasks match what earlier
   tasks defined.
Fix inline and move on.

## Handoff
Hand each task to an executor through `task` (a fresh agent per task, with review
between tasks) or execute them in this session in batches with checkpoints.

## Checklist
- [ ] Scope is one subsystem; header has goal, architecture and stack
- [ ] File structure mapped before tasks
- [ ] Every step is one 2 to 5 minute action with exact commands and expected output
- [ ] Complete code in every code-changing step; exact file paths always
- [ ] No placeholder wording anywhere
- [ ] Spec coverage, placeholder scan and name consistency reviewed
