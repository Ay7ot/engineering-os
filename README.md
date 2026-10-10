# EngineeringOS

A local-first **engineering operating system** for AI coding agents: a shared
context, memory, and state layer that sits under tools like OpenCode, Codex, or
Claude Code. The coding tool is the execution surface; EngineeringOS is the
system of record, so your agents stop forgetting everything between sessions.

It keeps durable, searchable memory across projects, architecture docs, ADRs,
technical research, and task state, and exposes it to agents through a small
local MCP server.

- **Public engine, private data.** This repository is the engine and contains no
  personal data. Everything you know lives in a separate data directory you
  version-control privately.
- **No dependencies.** The MCP server is stdlib-only Python. The CLI is one
  `bash` script. Nothing to `pip install`, no daemon, no cloud.
- **Agents with defined jobs.** A lead orchestrator delegates to specialized
  read-only and write agents instead of one super-agent doing everything.

---

## Contents

- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Everyday usage](#everyday-usage)
- [The agents](#the-agents)
- [The skills](#the-skills)
- [The commands](#the-commands)
- [The MCP server](#the-mcp-server)
- [The `eng` CLI](#the-eng-cli)
- [Split: public engine vs private data](#split-public-engine-vs-private-data)
- [Branch protection and contributing](#branch-protection-and-contributing)
- [Uninstall](#uninstall)
- [License](#license)

---

## How it works

Two directories, one environment variable between them:

```mermaid
flowchart LR
    subgraph tool["Your coding tool (OpenCode, Codex, ...)"]
        A[Lead agent] --> B[Subagents]
        A --> C[Skills + commands]
    end
    B <-->|MCP stdio| M[MCP server<br/>engineering-memory]
    M --> D[(data/)]
    subgraph repo["~/EngineeringOS (this repo, public)"]
        E[PRINCIPLES.md]
        F[agents / skills / commands]
        G[scripts/eng]
        H[mcp/]
    end
    D ---|ENGINEERING_OS_DATA| M
```

The engine ships the rules, agent definitions, skills, commands, the MCP server,
and the CLI. Your data directory holds everything specific to you. Agents, skills
and commands are written once in an **editor-neutral** format (`agents/`,
`skills/`, `commands/`). Per-editor **adapters** (`adapters/<editor>/`) render
them into each tool's own format and register the MCP server there with
`$ENGINEERING_OS_DATA` pointing at your data. `eng setup` runs every adapter
whose editor is installed. Today: OpenCode and Claude Code. See
[docs/adapters.md](docs/adapters.md) to add another.

Markdown is the source of truth. The SQLite database is a search index (FTS5
where available) and can be rebuilt. If the DB is lost, search falls back to
grepping the markdown.

---

## Quick start

**Requirements:** `git`, `python3` 3.9+ (with the `sqlite3` module), `bash`, and
[OpenCode](https://opencode.ai) and/or [Claude Code](https://claude.com/claude-code)
(CLI or desktop app). `eng setup` wires up whichever it finds. `gh` is optional, only needed for the
`repo-protect` command.

```sh
# 1. Clone the engine
git clone https://github.com/Ay7ot/engineering-os.git ~/EngineeringOS

# 2. Bootstrap everything (idempotent, safe to re-run)
~/EngineeringOS/scripts/eng setup

# 3. Restart OpenCode so it loads the new agents, skills, commands, and MCP
```

`eng setup` does all of this for you:

- checks `git` and `python3`, detects which editors you have, and verifies `sqlite3` is importable
- creates `~/EngineeringOS/data` with the standard layout
- seeds your `USER.md` from `USER.example.md` if you do not have one
- runs each installed editor's adapter: installs agents, skills, and commands
  in that editor's format, registers the `engineering-memory` MCP server, and
  makes the `lead` role the default (only if you have not chosen your own)
- adds an `eng` shell alias to your `.zshrc` or `.bashrc`
- runs health checks and prints what it found

Then make it yours:

```sh
$EDITOR ~/EngineeringOS/data/USER.md    # who you are, how you work, approval gates
```

Optionally, put your data under version control in a **private** repo so you can
restore everything after a machine reset:

```sh
cd ~/EngineeringOS/data
git init && git add -A && git commit -m "chore: initial EngineeringOS data"
gh repo create engineering-os-data --private --source=. --push
```

### Restore after a machine reset

```sh
git clone https://github.com/Ay7ot/engineering-os.git ~/EngineeringOS
git clone <your-private-data-repo> ~/EngineeringOS/data
~/EngineeringOS/scripts/eng setup
```

---

## Everyday usage

Open OpenCode in a project and use the lead agent, either directly or through a
command. You provide intent and approve consequential decisions; the agents do
research, exploration, architecture, implementation, testing, review, and
bookkeeping.

```mermaid
flowchart LR
    I[Your intent] --> L[Lead agent]
    L --> R1[Research + explore]
    R1 --> AR[Architecture]
    AR --> HG{Human gate}
    HG -->|approved| P[Plan]
    P --> IMP[Implement in worktrees]
    IMP --> T[Test]
    T --> RV[Review + security]
    RV --> M[Merge]
```

A typical first run on an existing project:

```sh
cd /path/to/your/project
opencode
> /init-project
```

That maps the workspace, writes an `AGENTS.md`, and registers the project in
EngineeringOS memory.

---

## The agents

The lead agent classifies each task and picks the smallest safe workflow, so a
typo fix does not spin up nine agents.

| Agent | Mode | What it does | Can write code? |
|---|---|---|---|
| **lead** | primary | Orchestrates; classifies complexity; delegates; manages approval gates; final report | yes |
| **researcher** | subagent | Technical research from primary sources; persists reusable findings | no (writes research only) |
| **explorer** | subagent | Maps repositories and non-git workspaces; produces repo maps, not dumps | no |
| **architect** | subagent | Architecture proposals, alternatives, tradeoffs, ADRs, diagrams | markdown only |
| **planner** | subagent | Turns approved architecture into small, verifiable tasks | no |
| **builder** | subagent | Implements the approved plan; stops and reports on architectural problems | yes |
| **tester** | subagent | Writes tests, runs typecheck/lint/test/build, reports PASS/FAIL evidence | tests only |
| **reviewer** | subagent | Adversarial review; finds reasons NOT to merge | no |
| **security** | subagent | Security review of auth, data, secrets, injection, dependencies | no |

Read-only agents are locked down at the permission level: their `edit` and
`bash` access is denied except for the specific read-only commands they need.

**Workflows by complexity:**

| Complexity | Workflow |
|---|---|
| Simple | Do it directly, verify |
| Moderate | builder → tester |
| Important | explorer → builder → reviewer → tester |
| Complex | researcher + explorer → architect → **human gate** → planner → builders (parallel worktrees) → tester → reviewer → security → **human gate** if needed |

The human gate always stops for: major architecture decisions, destructive DB
migrations, production deploys, security-sensitive changes, irreversible data
operations, significant infrastructure changes, major product behavior, and
substantial cost. Everything else is inferred autonomously.

---

## The skills

Skills are playbooks loaded by agents when a task matches. They are plain
markdown, easy to read and copy.

| Skill | Use when |
|---|---|
| `api-design` | Designing HTTP/REST, GraphQL, RPC, or internal APIs |
| `architecture-analysis` | Analyzing or proposing a system, component, or significant change |
| `backend-architecture` | Planning or reviewing backend services |
| `code-review` | Reviewing a diff, branch, PR, or file adversarially |
| `database-design` | Designing schemas, migrations, or data access |
| `debugging` | Investigating a reported bug |
| `diagrams` | Authoring Mermaid diagrams for docs, plans, architecture |
| `documentation` | Writing README, AGENTS.md, ADRs, runbooks |
| `frontend-architecture` | Planning or reviewing frontend work |
| `git-workflow` | Any git operation: worktrees, branches, commits |
| `observability` | Adding logging, metrics, tracing, alerting |
| `payments` | Building or reviewing billing and payment flows |
| `project-planning` | Turning approved architecture into tasks |
| `repository-exploration` | Mapping an unfamiliar repository |
| `security-review` | Reviewing auth, payments, data, webhooks, secrets, infra |
| `technical-research` | Investigating unfamiliar technology or comparing options |
| `testing` | Writing tests or verifying acceptance criteria |

---

## The commands

Slash commands in OpenCode that run a full workflow through the lead agent.

| Command | What it does |
|---|---|
| `/init-project` | Map the workspace, write `AGENTS.md`, register the project |
| `/feature` | Full feature workflow: explore, research, architect, plan, build, test, review |
| `/research` | Technical research, persisted to EngineeringOS |
| `/debug` | Investigate, reproduce, test hypotheses, fix, regression-test |
| `/review` | Review current changes, a branch, a PR, or specific files |
| `/worktree` | Create, list, or close git worktrees for features and bug fixes |

---

## The MCP server

`mcp/engineering-memory/server.py` is a stdlib-only MCP server over stdio. It
exposes 13 tools:

| Tool | Purpose |
|---|---|
| `search_knowledge` | Full-text search across knowledge, decisions, research, project docs |
| `get_project_context` | Full project context: context, architecture, state, recent activity |
| `get_project_state` | Current state plus open tasks |
| `update_project_state` | Append a state entry; creates the project if missing |
| `search_decisions` / `get_decision` / `record_decision` | Architecture Decision Records |
| `search_research` / `get_research` / `record_research` | Persisted technical research |
| `get_active_tasks` / `record_task` / `update_task` | The task blackboard |

Test it directly:

```sh
printf '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}\n' \
  | ENGINEERING_OS_DATA=~/EngineeringOS/data python3 mcp/engineering-memory/server.py
```

---

## The `eng` CLI

One bash script, idempotent, no side effects on re-run.

```sh
eng setup                            # bootstrap deps, data, config, MCP, health
eng health                           # verify engine, data, MCP, agents, skills
eng sync [all|<editor>]              # render + install for installed editors (default all)
eng sync-opencode                    # alias: eng sync opencode
eng sync-claude                      # alias: eng sync claude
eng targets                          # list known editors and whether each is installed
eng worktree new <name> [--type fix] # isolated worktree per feature/bug
eng worktree list                    # show active and closed worktrees
eng worktree close <name>            # remove it (refuses if dirty)
eng repo-protect --check             # show branch-protection drift vs GitHub
eng repo-protect                     # apply .github/ruleset.json
```

Worktrees use a sibling path (`../<repo>-<slug>-wt`), auto-detect the base
branch, register themselves in `projects/<name>/worktrees.md`, and refuse to
close over uncommitted changes unless you pass `--force`. One writer per
worktree, never two.

### Claude Code

The Claude Code adapter (`adapters/claude/`, run by `eng sync claude` and by
`eng setup` when `~/.claude` or the `claude` CLI exists) renders the same
neutral sources, so every editor shares one engine and one memory:

| EngineeringOS | Claude Code |
|---|---|
| `agents/*.md` (`role: subagent`) | `~/.claude/agents/*.md`. `permissions:` becomes `disallowedTools` plus a `PreToolUse` hook (`adapters/claude/hooks/eos_guard.py`) that enforces bash/edit allowlists, so read-only agents stay read-only. Translation fails closed: only an exact `allow` grants a capability (`ask` becomes deny). The guard also keeps git read-only for allowlisted agents (no push/reset/branch -D/--output, even under `git *`) and blocks edits to Claude Code config. Models come from `model_tier` (deep → opus, standard → sonnet, fast → haiku) unless `targets.claude.model` overrides |
| `agents/lead.md` (`role: primary`) | The **EngineeringOS Lead** output style (`~/.claude/output-styles/eos-lead.md`, keeps Claude Code's coding instructions), set as the default `outputStyle` in `~/.claude/settings.json` unless you already chose another style. Switch per session in the app or with `/output-style` |
| always-on context | A managed block in `~/.claude/CLAUDE.md` importing `PRINCIPLES.md` and `USER.md`, plus the memory and `AGENTS.md` rules. Your own CLAUDE.md content is kept |
| `skills/` | `~/.claude/skills/` |
| `commands/` | `~/.claude/commands/` |
| `engineering-memory` MCP | user-scope server, registered with `claude mcp add-json` when the CLI is on PATH; otherwise merged into `~/.claude.json` (backup at `~/.claude.json.engineeringos.bak`; restart Claude Code and re-run `eng health` if it was open) |

Names that collide with Claude Code built-ins get an `eos-` prefix:
`/eos-review`, `/eos-debug`, and the `eos-code-review` / `eos-security-review`
skills. Generated files are tracked in `~/.claude/.engineeringos-manifest.json`;
re-syncing prunes files it no longer produces. A file it did not write is never
overwritten: sync prints `SKIPPED` and leaves it alone.
Respects `CLAUDE_CONFIG_DIR`. Edit the neutral sources, never the generated
files, then re-run `eng sync` and restart your editors.

### OpenCode

The OpenCode adapter (`adapters/opencode/`) writes `~/.config/opencode/`
(respects `XDG_CONFIG_HOME`). It renders `role` as `mode`, `permissions` as
`permission`, and passes `targets.opencode.*` (model, temperature, command
`agent`/`subtask`) through. It registers the MCP server in the shape your
OpenCode reads: `mcp.servers.<name>` for v2, `mcp.<name>` for v1. It also removes
the stale v1 entry older `eng` versions wrote. Ownership works like the Claude
adapter (manifest, `SKIPPED` for files it did not write). On the first run it
adopts files the old copy-based sync installed.

---

## Split: public engine vs private data

```
~/EngineeringOS/         ← this public engine repo (no personal data)
~/EngineeringOS/data/    ← your private data (gitignored here)
```

Your data layout:

```
data/
  USER.md            operator profile (from USER.example.md)
  knowledge/         durable cross-project knowledge
  decisions/         global ADRs
  research/          persisted technical research
  projects/<name>/   context.md, architecture.md, state.md, decisions/, worktrees.md
  tasks/  state/     blackboard scratch space
  memory/engineering_memory.db   SQLite + FTS5 index
```

Override the data location with `$ENGINEERING_OS_DATA`. That environment
variable is the only coupling point between the engine and your data.

**Rule (`PRINCIPLES.md` §7): never commit secrets or personal data.** Keep your
data repo private by default.

---

## Branch protection and contributing

`main` is protected: contributors can only land changes through a pull request
that passes CI **and** is approved by a reviewer with write access. The only
account with write access is the maintainer, so the maintainer reviews every
contribution before it merges. No force-push, no deletion, and CI must pass. The
policy lives in [`.github/ruleset.json`](.github/ruleset.json) so it is readable
and reviewable like any other change.

```mermaid
flowchart LR
    C[Contributor] -->|fork + PR| PR[Pull Request]
    PR --> CI["CI: syntax checks, tests, ruleset guard"]
    CI -->|green| RV["Maintainer review<br/>(1 approval required)"]
    RV -->|approved| M[main]
    CI -->|red| X[blocked]
    RV -->|changes or no review| X
    A[Maintainer / admin] -.->|bypass| M
```

Contributor flow:

```sh
git checkout -b feat/short-description
# ... change ...
git commit -m "feat(scope): short description"
git push -u origin feat/short-description
gh pr create --fill
```

A maintainer reviews and approves. On approval, any new push dismisses the
approval, so what is reviewed is exactly what merges. Then it is squash-merged.

CI runs `bash -n scripts/eng`, `python3 -m py_compile`, `tests/test_eng.sh`, `tests/test_adapters.py`, `tests/test_claude_sync.sh`,
`tests/test_mcp.sh`, and `tests/test_ruleset.py`. Run the same tests locally
before you push and CI should be green.

Maintainers apply protection changes with:

```sh
eng repo-protect --check   # read-only drift report
eng repo-protect           # apply
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before your first PR. This project
follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Security issues go
through [SECURITY.md](SECURITY.md), never a public issue.

---

## Uninstall

```sh
# Remove the engine sync (agents, skills, commands, MCP config) then delete the repos.
# OpenCode: delete the files listed in ~/.config/opencode/.engineeringos-manifest.json.
# Claude Code: delete the files listed in ~/.claude/.engineeringos-manifest.json, the
# EngineeringOS block in ~/.claude/CLAUDE.md, "outputStyle" in ~/.claude/settings.json,
# and mcpServers."engineering-memory" in ~/.claude.json.
# Edit ~/.config/opencode/opencode.jsonc and remove mcp.servers."engineering-memory".
rm -rf ~/EngineeringOS
```

Your data lives at `~/EngineeringOS/data` (or `$ENGINEERING_OS_DATA`). Back it up
first if you want to keep it; deleting the engine does not delete your private
data repo.

---

## License

MIT, see [LICENSE](LICENSE).
