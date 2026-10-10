---
description: Initialize or refresh a project in EngineeringOS
agent: lead
subtask: false
---
Run the project initialization workflow for the current workspace. Works for a git repository OR a non-git folder (including empty folders and workspaces that contain multiple embedded git repos, e.g. a monorepo-of-repos with sibling `*/` subfolders).

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. Use the explorer agent to map the workspace (if not already mapped this session):
   - First determine whether the workspace is itself a git repo (`git status` succeeds) or a non-git folder.
   - If it is a git repo: detect the technology stack, architecture, conventions, testing strategy, deployment setup, external services, build/test/lint commands, CI.
   - If it is NOT a git repo: still proceed. Detect embedded git repos (subfolders containing `.git`, e.g. `*/` at depth 1-2), map them individually (stack, entry points, remotes/branches where available), and record the workspace layout (which subfolders are repos vs working docs). Never fail on a non-git workspace and never emit git errors ("fatal: not a git repository") to the user.
   - For an empty folder: map it as empty, note "no code yet", and proceed with registration.
3. Determine the project name: use the workspace folder name unless context indicates otherwise. Check `engineering-memory` MCP `get_project_context` to see if already registered.
4. Do NOT overwrite existing documentation without inspection. Read existing docs first; merge and improve, keep what is accurate.
5. Generate or improve `AGENTS.md` in the workspace root covering: project overview, stack, architecture, conventions, testing strategy, build/lint/test commands, key entry points, how to use EngineeringOS memory tools, and (for multi-repo workspaces) the repo layout.
6. Register the project in EngineeringOS via `engineering-memory` MCP:
   - `update_project_state` (project name, state = "Registered during /init-project", status = "active") to create `projects/<name>/context.md`, `architecture.md`, `state.md`.
   - `record_task` (title "Project initialized", project, status "done") to mark registration.
   - If significant architecture was discovered, propose an ADR via `record_decision` (project-scoped) — only after confirming it is accurate and worth persisting.
   - In `context.md`, record the workspace layout explicitly: "Workspace root: <path> — git repo" or "Workspace root: <path> — not a git repo; embedded repos: <list>".
7. Identify missing documentation and note it in the project `context.md` under "Missing documentation".
8. Configure relevant skills and note MCP access relevant to the project in `AGENTS.md`.
9. Record initial project state.

## Output
Report to the user: what was created/updated (AGENTS.md, project context, architecture notes, state), detected stack, discovered conventions and test strategy, missing documentation identified, and any open questions requiring the user. Do not modify application code.