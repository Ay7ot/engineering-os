# Agent evals

Phase 0 of the subagent review: a deterministic task-completion harness that
compares agent configurations before and after a routing change.

This is **not** part of CI. It calls real models, costs real tokens, and takes
minutes. CI still runs `tests/`, which covers the engine's mechanics.

## What it measures

For each task it records:

- pass/fail against a deterministic check (tests, imports, file contents, scope)
- wall clock and session duration
- cost, input/output/reasoning tokens
- number of subagent sessions

OpenCode stores those in `session_v2`. The runner reads the root session and its
children, so a handoff-heavy workflow shows up in the numbers.

## Quick start

```sh
python3 evals/run.py --self-check          # every check must fail on the untouched fixture
python3 evals/run.py --config current --tasks typo --runs 1   # smoke one run
python3 evals/run.py --config both --runs 1 --flatten-model opencode-go/mimo-v2.6-flash
python3 evals/run.py --report
```

`--flatten-model` puts every agent on one model. Use it for comparisons: the
model tier is then constant. Always pass `--model` as well. OpenCode's root run
does not reliably apply the agent's `model` field, and without `--model` it falls
back to a free default and retries for minutes on a 503. The first real run costs
money. Start with one task, then widen.

## Isolation

Each config gets its own:

- engine copy: `baseline` is `git archive HEAD`, `current` is the working tree
- `HOME`, with `~/EngineeringOS` pointing at that engine copy
- OpenCode config dir (`XDG_CONFIG_HOME`), synced by `eng sync opencode`
- data dir for `engineering-memory` (`ENGINEERING_OS_DATA`)

The provider auth and session DB are shared through a symlink to the real
`~/.local/share/opencode`, so sessions are recorded in the normal place. Runs
use `--standalone` to avoid the background server. Remote MCP servers are not
installed in the eval config; the sandbox is offline by prompt and by config.

Each run gets a fresh copy of `evals/fixtures/pyapp` in its own git repo, so the
agent's diff and `git status` behave normally.

## Tasks

| id | Complexity | What it checks |
|---|---|---|
| `typo` | simple | exact fix, no collateral change, tests still pass |
| `feature-clamp` | moderate | new export, boundary behaviour, tests |
| `bug-average` | important | failing test fixed, tests untouched |
| `repo-map` | moderate | map file with stack, entry points, test command, conventions |
| `architecture-export` | complex | ADR with alternatives, tradeoffs, failure modes, recommendation |
| `plan-export` | complex | phased plan, 3+ tasks, dependencies, acceptance criteria |
| `security-sql` | important | seeded SQL injection found, scoped report |
| `review-offbyone` | important | seeded off-by-one found, verdict, no fixes |
| `research-retry` | moderate | correct facts from bundled docs, source cited |
| `refactor-rename` | complex | symbol renamed everywhere, tests pass |

`--self-check` proves no check passes on the untouched fixture.

## Results

`/tmp/opencode/eos-evals/results.jsonl` by default, one row per run. Override the
work root with `EOS_EVAL_WORK`. `--report` prints a per-task table with pass
rate, median wall clock, median cost and median subagent count, then lists tasks
where the two configs disagree.

The work root is deliberately outside the engine repo: OpenCode walks up to the
enclosing git repository, so a sandbox nested under the engine would make the
engine the project.

Repeat a differing task before believing it. One run hides flakiness; Anthropic's
own case study saw a regression in one run out of two.

## Adding a task

Add a `Task` to `evals/tasks.py` with a `prompt`, an optional `setup(root)`, and
a `check(root, baseline)`. Keep the check deterministic. Run `--self-check`
before using it for real.
