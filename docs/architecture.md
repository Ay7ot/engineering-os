# EngineeringOS — Architecture

> Generic architecture of the engine. Your project- and client-specific
> architecture lives under the private data directory, not here.

## Purpose

EngineeringOS is a persistent, local-first **context, memory, and state layer**
shared by AI coding agents across projects. Coding tools (OpenCode, Claude Code, Codex, etc.)
are interchangeable execution surfaces; EngineeringOS is the system of record.

## Components

| Component | Path | Role |
|---|---|---|
| Principles | `PRINCIPLES.md` | Global engineering rules agents must follow |
| Operator profile | `<data>/USER.md` | Who the operator is, how they work, approval gates |
| Agent definitions | `agents/*.md` | Editor-neutral specialized agents (lead, architect, builder, …) |
| Skills | `skills/*/SKILL.md` | Reusable task playbooks |
| Commands | `commands/*.md` | Slash-command workflows |
| Editor adapters | `adapters/<editor>/` | Render the neutral source into each editor and register MCP (OpenCode, Claude Code) |
| Memory MCP server | `mcp/engineering-memory/server.py` | Exposes data + SQLite/FTS5 over MCP stdio |
| CLI | `scripts/eng` + `scripts/eos_sync.py` | Idempotent setup, health, per-editor sync, git worktrees, repo protection |
| Tests | `tests/` | Hermetic CLI, adapter (incl. OpenCode golden fixtures), Claude adapter + guard, MCP, and ruleset tests; run by CI |
| Templates | `templates/` | Seed files for a new data directory |
| CI | `.github/workflows/ci.yml` | Syntax checks, tests, ruleset guard |
| Branch protection | `.github/ruleset.json` | Source of truth for the `main` ruleset |

## Data model

All durable knowledge lives in the **data directory** (default
`~/EngineeringOS/data`, override with `$ENGINEERING_OS_DATA`):

```
data/
  USER.md            operator profile
  knowledge/         durable cross-project knowledge (markdown)
  decisions/         global ADRs (markdown)
  research/          persisted technical research (markdown)
  projects/<name>/   context.md, architecture.md, state.md, worktrees.md, decisions/
  tasks/  state/     blackboard scratch space
  memory/engineering_memory.db   SQLite + FTS5 index
```

Markdown is the source of truth; the SQLite DB is a search/index layer.
`search_knowledge` also greps the markdown directly, so search degrades
gracefully if the DB is lost.

## Engine / data split

The engine repo contains **no personal data**. Data is version-controlled
separately (recommended: a **private** Git repo) so it can be restored after a
machine reset without ever being published. `$ENGINEERING_OS_DATA` is the only
coupling point; each editor adapter wires it into that editor's MCP config
(`eng setup` / `eng sync`).

## Editor integration

Agents, skills and commands are written once in an editor-neutral format and
rendered per editor by adapters (`adapters/<editor>/adapter.py`, contract:
`detect`, `sync`, `health`). The shared layer (`adapters/common.py`) validates
the source, never overwrites files it did not write, and fails closed on
permissions. Supported today: OpenCode and Claude Code. See
[adapters.md](adapters.md) for the format and how to add an editor, and
[design/editor-neutral-engine.md](design/editor-neutral-engine.md) for the
design and its tradeoffs.

## Flows

1. **Intent** → lead agent clarifies only what needs human judgment.
2. **Research** → researcher + explorer inspect repo, EngineeringOS memory, and
   primary sources; findings persisted via `record_research`.
3. **Architecture** → architect proposes options/tradeoffs; human gate for
   consequential decisions (ADRs via `record_decision`).
4. **Plan** → planner decomposes into small, verifiable tasks with acceptance
   criteria.
5. **Implement** → builder works in isolated git worktrees (`eng worktree`).
6. **Verify** → tester runs typecheck/lint/test/build and reports evidence.
7. **Review** → reviewer and security review adversarially before merge.
8. **State** → project state and knowledge updated via MCP.

## Security posture

- No secrets in the engine repo or in EngineeringOS data, by rule
  (`PRINCIPLES.md` §7).
- Privileged operations (prod deploy, destructive migrations, irreversible data
  ops) require explicit human approval.
- The data repo is expected to be private; treat it as sensitive by default.

## Repository governance

`main` is protected by a repository ruleset defined in `.github/ruleset.json`
and applied with `eng repo-protect`. Contributors cannot push to `main`; they
open a PR that must pass CI (`tests/`). A single admin bypass actor keeps the
solo maintainer unblocked. See `CONTRIBUTING.md` and ADR
`docs/decisions/2026-10-02-open-source-contributor-workflow-and-branch-protection.md`.

CI (`.github/workflows/ci.yml`) runs the same tests a contributor can run
locally: `tests/test_eng.sh`, `tests/test_adapters.py`,
`tests/test_claude_sync.sh`, `tests/test_mcp.sh`, `tests/test_ruleset.py`, plus
syntax checks. The job is named `ci` and is the required status check.
