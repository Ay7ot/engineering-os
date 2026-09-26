---
description: Create, list, or close git worktrees for features/bugs
agent: lead
subtask: false
---
Run the EngineeringOS worktree workflow. Request: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. Determine intent from $ARGUMENTS: `new` (default if a feature/bug name is given), `list`, or `close`.
3. **new**: run `~/EngineeringOS/scripts/eng worktree new <name> [--repo <path>] [--type fix] [--base <branch>] [--project <name>]`. For bugs, use `--type fix`. If the repo is not the cwd, pass `--repo`. If the EngineeringOS project name differs from the repo basename, pass `--project`.
4. Register the worktree on the blackboard: `engineering-memory` MCP `record_task` (title = feature/bug name, project = project name, owner = "worktree:<branch>", status = "open", details = "type, branch, path, base, repo"). Record the returned task id.
5. Report: branch, worktree path, base branch, how to start (cd into the worktree, run the project's verification), and the task id.
6. **list**: run `eng worktree list [--repo <path>]`; summarize active vs closed worktrees from the registry and `git worktree list`.
7. **close**: run `eng worktree close <name> [--repo <path>] [--force] [--delete-branch]`; if a task was registered for it, mark it `done` (or `cancelled`) via `update_task`; report what was removed and what was left behind.
8. Update project state via `engineering-memory` `update_project_state` when a worktree lifecycle changed meaningfully.

## Discipline
- `eng worktree` is idempotent: never create a duplicate worktree; never clobber existing branches.
- Closing refuses on uncommitted changes unless the user approves `--force`.
- One writer per worktree, never two.