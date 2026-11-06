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
2. **Research** → the lead searches EngineeringOS memory and primary sources;
   the researcher or explorer is used when the work needs an isolated context.
   Findings persisted via `record_research`.
3. **Architecture** → the lead loads the `architecture-analysis` skill, or the
   architect for complex or novel design; human gate for consequential decisions
   (ADRs via `record_decision`).
4. **Plan** → the lead writes the plan with the `project-planning` skill: small,
   verifiable tasks with acceptance criteria.
5. **Implement** → the lead or a builder works in an isolated git worktree
   (`eng worktree`).
6. **Verify** → builder runs tests inline for Moderate work; the tester verifies
   independently for Important, Complex, and review-gated Moderate work, and
   reports raw evidence.
7. **Review gate** → independent reviewer for every non-trivial change and every
   sensitive path; security too for auth, payments, PII or PHI, data or
   migrations, concurrency, build config, public APIs, dependencies, secrets,
   infrastructure, or deployment. The reviewer gets a packet: diff and changed
   files, plan and acceptance criteria, raw verification output, CI status,
   project rules, and sensitive-path flags. It may run its allowlisted
   verification commands; otherwise the tester runs them and passes the raw
   output. For an external or untrusted change, the tester or CI runs
   verification in a disposable environment and the reviewer judges the raw
   output. The `code-review` skill includes a cross-boundary pass for DB type
   against parameter, timestamp precision, client/server boundary, bundle
   boundary, serialization, and concurrency token precision.
8. **State** → project state and knowledge updated via MCP.

## Subagent policy

A subagent gets its own context window only when one of three conditions holds:

- **Isolation** — the work would flood the main context (large repo map, long
  research, noisy verification).
- **Independence** — the check must not share the main context or write access
  (adversarial review, security review, final verification).
- **Parallelism** — independent tasks with separate write scopes.

Every other responsibility is a skill loaded on demand. Design is not a fourth
reason: the lead loads `architecture-analysis` and spawns the architect only
when the design is large enough to isolate or needs an independent read. The
read-only agents keep no source-edit rights at the permission level, and that
boundary is the reason they exist as separate agents rather than as prompts in
the main loop.

The review gate is the independence condition in practice: it is why
independence is one of the three delegation conditions. A non-trivial change is
not merged on the lead's own judgment. The reviewer is a separate context with no edit rights, a review
packet, and a narrow verification allowlist. It can run tests, typecheck, lint,
a clean build, and read CI status. The allowlist constrains the command string,
not the code it runs: test and build code executes with the reviewer's
permissions. For an external or untrusted change, the tester or CI runs
verification in a disposable environment and passes the raw output, so the
reviewer still judges evidence rather than a summary.

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
