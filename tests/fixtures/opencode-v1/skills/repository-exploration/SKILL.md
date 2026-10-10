---
name: repository-exploration
description: Map an unfamiliar repository quickly: stack, structure, data flow, key files, conventions, tests, integration points. Produce a concise map, not a source dump.
metadata:
  audience: explorer, lead
---
# Repository Exploration

## When to use
- Entering a new repository.
- Locating code for a specific task.
- Understanding conventions, tests, and integration points before modifying.

## Procedure
1. Check for context: `AGENTS.md`, `README.md`, and `~/EngineeringOS/data/projects/<name>/` (via `engineering-memory` `get_project_context`).
2. Inventory: manifests (package.json, pyproject.toml, Cargo.toml, go.mod, etc.), config files, CI, top-level dirs.
3. Read entry points and key modules. Trace the main data flow for the task area.
4. Identify: conventions (naming, error handling, patterns), test framework + how to run tests, deployment setup, external services.

## Output: repository map
- Overview (1 paragraph)
- Stack (languages, frameworks, key deps with versions)
- Structure (top-level layout + where relevant code lives)
- Data flow / architecture
- Key files (for the task, with paths)
- Existing implementations (patterns already in codebase)
- Tests (framework, location, how to run)
- Conventions
- Integration points (APIs, DBs, queues, auth, services)
- Deployment
- Risks / observations

## Rules
- Produce maps, not dumps. Summarize; quote only essential signatures.
- Cite file paths. State what you did NOT verify.
- If something is ambiguous, report as unresolved rather than guessing.
- You are read-only. Never modify code.

## Checklist
- [ ] Read AGENTS.md / README / prior context
- [ ] Inventory manifests + config + CI
- [ ] Traced main data flow
- [ ] Identified test runner command
- [ ] Noted conventions and integration points
- [ ] Reported unresolved items explicitly