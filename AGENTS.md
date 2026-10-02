# AGENTS.md — EngineeringOS engine repository

Orientation for any AI agent working **on** this repository. For what
EngineeringOS is and how to install it, read `README.md`.

## What this repo is

The public **engine**: rules, agent/skill/command definitions, a stdlib-only MCP
server, and a bash CLI. It contains **no personal data**. User knowledge lives in
a separate data directory (`$ENGINEERING_OS_DATA`, default `~/EngineeringOS/data`).

## Layout

| Path | Role |
|---|---|
| `PRINCIPLES.md` | Global engineering principles agents must follow |
| `USER.example.md` | Template for the private operator profile (`<data>/USER.md`) |
| `opencode/agents/*.md` | Agent definitions (lead + 8 subagents) |
| `opencode/skills/*/SKILL.md` | Reusable task playbooks |
| `opencode/commands/*.md` | Slash-command workflows |
| `mcp/engineering-memory/server.py` | Stdlib-only MCP server over stdio |
| `scripts/eng` | Bootstrap / health / sync / worktree / repo-protect CLI |
| `tests/` | Hermetic tests. These are what CI runs |
| `templates/` | Seed files copied into a fresh data directory |
| `docs/` | Architecture notes and framework ADRs |
| `.github/ruleset.json` | Branch-protection source of truth for `main` |
| `.github/workflows/ci.yml` | CI: syntax checks, tests, ruleset guard |

## Commands

```sh
bash tests/test_eng.sh          # CLI tests
bash tests/test_mcp.sh          # MCP server tests
python3 tests/test_ruleset.py   # ruleset config guard
bash -n scripts/eng             # shell syntax
eng health                      # verify a local install
eng sync-opencode               # push agents/skills/commands into ~/.config/opencode
```

There is no build step and no package manager. Nothing to install.

## Conventions

- **Markdown + frontmatter** for agents (description, mode, permission), skills
  (name, description), and commands (description, agent).
- **Conventional commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`,
  `chore:`, `perf:`, `ci:`.
- **Shell**: `set -euo pipefail`, no dependencies beyond `git`, `python3`,
  coreutils. Keep every command idempotent and non-destructive.
- **Python**: stdlib only. The MCP server must never require a pip install.
- **Read-only agents stay read-only**: deny `edit`, allow `bash` only for the
  specific read-only git commands needed.
- Match surrounding style; do not reformat unrelated code.

## Rules for agents in this repo

1. Read `PRINCIPLES.md` first. It applies here too.
2. Never commit secrets or personal data (§7). The engine is public.
3. Change behavior → update docs (`README.md`, `docs/`). Change protection →
   update `.github/ruleset.json`.
4. Run the tests before proposing a change. CI runs the syntax checks plus
   everything in `tests/`.
5. Do not push directly to `main` unless you are acting as the repository admin.
   Contributors open a PR; CI must pass.
6. Persist significant decisions as ADRs in `docs/decisions/`.

## Memory

When a compatible MCP client is configured, use the `engineering-memory` tools
(`get_project_context`, `search_decisions`, `record_decision`, `record_task`, …)
to read and update project memory. The engine repo itself is registered in
EngineeringOS as the `engineering-os` project.
