---
name: project-planning
description: Turn approved architecture into small, verifiable implementation tasks with dependencies and acceptance criteria. Use before delegating implementation.
metadata:
  audience: planner, lead
---
# Project Planning

## When to use
- Breaking an approved architecture/feature into implementable work.
- Decomposing a large change for parallel execution.

## Rules
- Tasks small enough for independent implementation and verification when practical.
- Explicit dependencies between tasks; no silent coupling.
- Acceptance criteria per task, verifiable deterministically (tests, typecheck, lint, build).
- Phases ordered by dependency and risk; de-risk early (build the risky/thin slice first).
- Identify parallelizable tasks; create each worktree with `eng worktree new` (branch/worktree naming stays as-is) and track explicit ownership/branch/worktree/dependencies/merge state.
- Register tasks on the blackboard (`engineering-memory` `record_task`) with owner + status.
- Keep IN/OUT of scope explicit.

## Output: implementation plan
- **Phases** (ordered, each with a goal)
- **Tasks** (id, title, description, dependencies, acceptance criteria)
- **Testing requirements**
- **Migration requirements** (if applicable)
- **Documentation requirements**
- **Parallelization** (worktree/ownership per task)

## Task sketch
- id: T-3
- title: Add idempotency key handling to charge creation
- depends_on: T-2 (charge endpoint scaffold)
- acceptance: POST with duplicate key returns existing charge, no double charge; covered by unit test
- worktree: feat-billing-charges (builder-alpha)

## Checklist
- [ ] Phases with goals
- [ ] Tasks small + independently verifiable
- [ ] Dependencies explicit
- [ ] Acceptance criteria deterministic
- [ ] Parallelization/worktree plan
- [ ] Registered on blackboard