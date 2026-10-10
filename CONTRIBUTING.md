# Contributing to EngineeringOS

Thanks for wanting to help. This is a small, local-first project, so the process
is deliberately light. Read this once and you are good to go.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## The one rule that matters

**Never commit personal data or secrets.** This repository is the public engine.
Your knowledge, projects, decisions, and research live in a **separate private
data directory** (`~/EngineeringOS/data`, or `$ENGINEERING_OS_DATA`). That
directory is gitignored here and must never be pushed to this repo. If your
change needs example data, put it under `templates/` as a clearly fake template.

See `PRINCIPLES.md` §7.

## Setup for development

You need `git`, `python3` (3.9+, with `sqlite3`), `bash`, and `gh` (optional, for
repo tooling). No pip installs: the MCP server is stdlib only.

```sh
git clone https://github.com/Ay7ot/engineering-os.git ~/EngineeringOS
cd ~/EngineeringOS
bash tests/test_eng.sh
python3 tests/test_adapters.py
bash tests/test_claude_sync.sh
bash tests/test_mcp.sh
```

Those four suites are the bulk of what CI runs. CI also runs syntax checks and
`python3 tests/test_ruleset.py`. If they pass locally, CI should pass. All tests
are hermetic: they use a temporary `HOME` and never touch your real editor
config.

## Branching and pull requests

`main` is protected. You cannot push to it directly. Work like this:

```sh
git checkout -b feat/short-description   # or fix/, docs/, chore/, ci/
# ... make your change ...
git add -A
git commit -m "feat(scope): short description"
git push -u origin feat/short-description
gh pr create --fill
```

A maintainer reviews, CI must be green, and then it is squash-merged. The
maintainer's approval is required before a contribution can merge, and any push
after approval dismisses it. Keep pull requests small and scoped: one idea per
PR.

### Commit messages

Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`,
`perf:`, `ci:`. A short subject line, plus a body explaining **why** when it is
not obvious. Commit logical units; do not bundle unrelated changes.

## What CI checks

The `ci` workflow runs on every push and PR:

| Step | Command |
|---|---|
| Bash syntax | `bash -n scripts/eng` |
| Python syntax | `python3 -m py_compile` on the MCP server, `scripts/eos_sync.py`, and every adapter (see `ci.yml`) |
| CLI tests | `bash tests/test_eng.sh` |
| Adapter tests | `python3 tests/test_adapters.py` |
| Claude Code adapter tests | `bash tests/test_claude_sync.sh` |
| MCP tests | `bash tests/test_mcp.sh` |
| Ruleset guard | `python3 tests/test_ruleset.py` |

All of these are required to pass before a PR can merge.

## Adding an agent, skill, or command

These are plain Markdown with editor-neutral YAML frontmatter. Adapters render
them for each editor (`eng sync`). Frontmatter supports nested maps and scalars
only (no lists); the loader rejects anything else with `file:line`.

- **Agent** → `agents/<name>.md` with `name` (= file name), `description`,
  `role` (`primary` or `subagent`), optional `model_tier` (`deep`, `standard`,
  `fast`), a `permissions` map, and editor-only settings under
  `targets.<editor>` (e.g. `targets.opencode.temperature`). Keep read-only
  agents read-only: deny `edit`, and deny `bash` except an explicit list of
  read-only commands, with the `"*"` default first and no git wildcards. Do not
  give an agent a tool its job does not require. If you change an agent's
  permissions, update the golden fixtures in `tests/fixtures/opencode-v1/` in
  the same PR so the change is visible in review.
- **Skill** → `skills/<name>/SKILL.md` with `name` (= directory) and
  `description`. One skill, one playbook.
- **Command** → `commands/<name>.md` with `description`, plus e.g.
  `targets.opencode.agent`. Use `$ARGUMENTS` for user input.
- **Editor** → `adapters/<editor>/adapter.py`; see `docs/adapters.md`. If you
  add a permission shape an adapter does not handle, extend the adapter and its
  tests in the same PR.

Update the tables in `README.md` when you add or rename any of these.

## Style

- Shell: `scripts/eng` is deliberately POSIX-ish `bash` with `set -euo pipefail`,
  no external dependencies beyond `git`, `python3`, and coreutils. Prefer
  readable functions over clever one-liners. Keep it idempotent: running a
  command twice must not break anything or destroy user customizations.
- Python: stdlib only. No third-party packages, ever, for the MCP server or the
  adapters.
- Match the surrounding style. Do not reformat unrelated code.

## Changing branch protection

The `main` ruleset is defined in [`.github/ruleset.json`](.github/ruleset.json)
and applied with the `eng` CLI. To change protection, edit that file and open a
PR; a maintainer applies it after merge.

```sh
eng repo-protect --check    # show what differs from GitHub (read-only)
eng repo-protect            # apply the JSON to the repo
```

`--check` never modifies anything, so it is safe to run anywhere. Applying
requires admin access and `gh` authenticated.

## Documentation

Docs are part of the change. If you alter behavior, update `README.md` and
anything under `docs/`. If you make a significant decision, it deserves an ADR
in `docs/decisions/`.

## Reporting security issues

Do **not** open a public issue. See [SECURITY.md](SECURITY.md).
