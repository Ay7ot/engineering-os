---
name: git-workflow
description: Safe git operations: worktrees for parallel work, clean branches, conventional commits, safe diffs. Use whenever git commands are run.
metadata:
  audience: builder, lead
---
# Git Workflow

## When to use
- Making commits, branches, worktrees, merges, or rebases.
- Parallel work across agents.

## Rules
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`.
- Short subject line + body explaining WHY when non-obvious.
- Commit logical units; never bundle unrelated changes.
- Never commit secrets, credentials, `.env`, or build artifacts.
- Inspect before commit: `git status`, `git diff`, `git log --oneline -10`. Stage only intended files.
- Parallel write work: one agent per worktree; never two writers in the same tree.
- Create a worktree for each feature/bug: `~/EngineeringOS/scripts/eng worktree new <name> --repo <path> [--type fix]` (sibling `../<repo>-<slug>-wt`, branch `feat/<slug>` or `fix/<slug>`, base auto-detected, registered in `projects/<project>/worktrees.md`).
- List: `eng worktree list --repo <path>` · Close: `eng worktree close <name> [--force] [--delete-branch]`.
- Closing refuses on uncommitted changes unless `--force` (commit or stash first).
- Merge strategy: prefer rebase for feature branches onto main; keep history linear when the project prefers it.
- Destructive operations (force push, rebase of shared branches, reset) require human approval.

## Approval gates (git)
- Force-push / history rewrite: ask.
- Merge to a protected branch / production: ask.
- Tagging releases: ask.

## Checklist
- [ ] Status/diff inspected before commit
- [ ] Conventional commit message
- [ ] No secrets or artifacts staged
- [ ] Worktree isolation for parallel agents
- [ ] No destructive ops without approval