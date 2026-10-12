---
name: using-git-worktrees
description: Create and prepare an isolated workspace for feature work: detect existing isolation, prefer native worktree tools, fall back to git worktree, then run setup and a clean baseline. Use when starting work that must not disturb the current checkout. See `git-workflow` for branches and commits.
metadata:
  audience: builder, lead
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Using Git Worktrees

## When to use
- Starting feature work that must not disturb the current checkout.
- Before executing an implementation plan.
- Any time two writers would otherwise share one working tree.

`git-workflow` owns branches, commits, and the project's own worktree commands;
this skill owns picking and preparing the isolated workspace.

## Step 0: Detect existing isolation first
Never create a worktree before checking.
```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
git branch --show-current
```
- Submodule guard: `GIT_DIR != GIT_COMMON` is also true inside a git submodule.
  Run `git rev-parse --show-superproject-working-tree`; if it prints a path you
  are in a submodule, treat it as a normal repo.
- Already in a linked worktree, and not a submodule: stop, do not create
  another. Report the path and branch. Detached HEAD means branch creation is
  needed at finish time.
- Normal checkout: honour a worktree preference already stated in the
  instructions. Otherwise ask for consent before creating one; if declined, work
  in place.

## Step 1: Create the workspace
1. **Native tools first.** If the environment offers a worktree tool or command,
   use it: it handles placement, branch creation, and cleanup. Running
   `git worktree add` when a native tool exists creates state the harness cannot
   see or manage. This is the most common mistake.
2. **Git fallback only when no native tool exists.** Directory priority, highest
   first:
   - explicit preference in the instructions;
   - existing `.worktrees/` (preferred) or `worktrees/` at the project root;
     if both exist, `.worktrees` wins;
   - existing global worktree directory, kept for compatibility;
   - otherwise default to `.worktrees/` at the project root.
3. **Safety check for project-local directories:** confirm the directory is
   ignored before creating it, `git check-ignore -q .worktrees`. If it is not
   ignored, add it to `.gitignore`, commit that, then proceed. This is what
   stops worktree contents being committed to the repository.
4. Create and enter it:
   ```bash
   git worktree add "$path" -b "$BRANCH_NAME"
   cd "$path"
   ```
5. **Sandbox fallback:** if creation is denied by the sandbox, tell the human
   and work in the current directory instead, running setup and the baseline
   there.

## Step 2: Project setup
Auto-detect and run the project's install or build step: `package.json` gives
`npm install`; `Cargo.toml` gives `cargo build`; `requirements.txt` gives
`pip install -r requirements.txt`; `pyproject.toml` gives `poetry install`;
`go.mod` gives `go mod download`. None present: skip.

## Step 3: Verify a clean baseline
Run the project's test command (`npm test`, `cargo test`, `pytest`,
`go test ./...`).
- Passes: report ready.
- Fails: report the failures and ask whether to proceed. A dirty baseline makes
  new breakage indistinguishable from pre-existing breakage.

Report shape: worktree path, test count and failures, the feature about to
start.

## Checklist
- [ ] Step 0 detection run; no nested worktree created
- [ ] Native worktree tool used when available; git only as fallback
- [ ] Directory chosen by priority: preference, existing, legacy global, default
- [ ] Project-local directory proven ignored before creation
- [ ] Setup run and baseline tests green, or failures reported and consent asked
