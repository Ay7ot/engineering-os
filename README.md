# EngineeringOS

A personal, local-first **engineering operating system**: a shared context,
memory, and state layer that sits under your AI coding tools. OpenCode (or any
compatible agent surface) is the execution environment; EngineeringOS is the
system of record.

It keeps durable, searchable memory across projects — architecture docs, ADRs,
technical research, task state — and exposes it to agents through a small local
MCP server, so your agents stop forgetting everything between sessions.

## Engine vs. your data (important)

This repository is the **engine** and contains **no personal data**. All of your
knowledge, projects, research, decisions, and memory live in a separate **data
directory** that you version-control privately:

```
~/EngineeringOS/         ← this public engine repo
~/EngineeringOS/data/    ← your private data (gitignored here; put your own private repo here)
```

Override the data location with `$ENGINEERING_OS_DATA`. The only coupling point
is that environment variable.

## Layout (engine)

- `README.md` — this file
- `LICENSE` — MIT
- `PRINCIPLES.md` — global engineering principles (agents consume this)
- `USER.example.md` — template for your private operator profile (`<data>/USER.md`)
- `opencode/` — canonical agents, skills, commands (synced into `~/.config/opencode/`)
- `mcp/engineering-memory/` — stdlib-only MCP server exposing memory over stdio
- `scripts/eng` — bootstrap / health / sync / worktree CLI
- `templates/` — seed files copied into a fresh data directory
- `docs/` — architecture notes and framework ADRs

## Layout (your data, private)

```
data/
  USER.md            operator profile (from USER.example.md)
  knowledge/         durable cross-project knowledge
  decisions/         global ADRs
  research/          persisted technical research
  projects/<name>/   context.md, architecture.md, state.md, decisions/, worktrees.md
  tasks/  state/     blackboard scratch space
  memory/engineering_memory.db   SQLite + FTS5 index over the markdown
```

Markdown is the source of truth; the DB is a search index and can be rebuilt by
re-running record operations.

## Install

Requirements: `git`, `python3` (with `sqlite3`), and OpenCode.

```sh
git clone https://github.com/<you>/engineering-os.git ~/EngineeringOS
~/EngineeringOS/scripts/eng setup
```

`eng setup` is idempotent. It creates the data directory, seeds `USER.md` from
`USER.example.md`, syncs agents/skills/commands into `~/.config/opencode/`,
wires the `engineering-memory` MCP (with `ENGINEERING_OS_DATA`), and runs health
checks. Restart OpenCode afterwards to load changes.

## Usage

- `eng setup` — bootstrap everything (deps, data, config, MCP, agents, health)
- `eng health` — verify engine, data, MCP, agents/skills/commands
- `eng sync-opencode` — re-sync agents/skills/commands + MCP config
- `eng worktree new|list|close` — per-feature/bug git worktrees (sibling
  `../<repo>-<slug>-wt`), tracked in `<data>/projects/<name>/worktrees.md`
- In OpenCode: `/init-project`, `/feature`, `/research`, `/debug`, `/review`,
  `/worktree`. The `@lead` agent orchestrates; you give intent, approve
  architecture, approve consequential changes.

## Restore after a machine reset

```sh
git clone https://github.com/<you>/engineering-os.git ~/EngineeringOS
git clone <private-data-repo> ~/EngineeringOS/data
~/EngineeringOS/scripts/eng setup
```

## Philosophy

An orchestrated team of specialized agents, not a single super-agent. High agent
autonomy with human control over consequential decisions. Agents research first
(repo, docs, EngineeringOS memory, official sources) and ask only when
human/product judgment or significant consequences require it.

Lifecycle: intent → research → exploration → requirements → architecture →
human gate → plan → implementation → verification → review → approval.

## Security

- No secrets in the engine repo or in EngineeringOS data — by rule
  (`PRINCIPLES.md` §7).
- Keep your data repo **private**. Treat it as sensitive by default.
- Privileged operations (production deploys, destructive migrations,
  irreversible data ops) require explicit human approval.

## License

MIT — see `LICENSE`.
