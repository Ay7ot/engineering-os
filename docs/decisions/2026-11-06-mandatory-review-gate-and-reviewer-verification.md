# Mandatory review gate and reviewer verification

Date: 2026-11-06
Status: accepted, operator-requested 2026-11-06

## Context

The subagent fold kept `reviewer` and `security`, but the lead routing still
allowed Moderate work to merge after an inline test run and a spot-check of the
diff. Real misses showed the gap:

- A Postgres enum column compared against a `text[]` parameter raised
  `operator does not exist` and 500'd a cron. The same review also caught invalid
  enum values and a missing terminal status.
- A microsecond-precision `updated_at` compared against a millisecond-truncated
  concurrency token made every edit return `not_found` on a fresh read.
- A client-bundle build breaker, a rollup scope issue, and a measurement trigger
  needed a clean build, not a diff read.

These are cross-boundary bugs. They need the schema, the query, the
serialization, and the build in the same view. The reviewer had a diff and
read-only git, and Moderate work did not always reach it.

## Decision

1. Make independent review mandatory for every non-trivial change and every
   sensitive path. The complexity label does not waive it. The only exemptions
   are docs-only, typo, comment, formatting, or a one-line obvious fix with no
   behavior change.
2. Always run reviewer plus security for auth, payments, PII or PHI, data or
   migrations, concurrency, build config, public APIs, dependencies, secrets,
   infrastructure, and deployment.
3. Give the reviewer a review packet: the diff and changed files, the plan and
   acceptance criteria, raw test/typecheck/lint/clean-build/CI output, the
   project rules, and the sensitive-path flags.
4. Give the reviewer a narrow verification allowlist:
   - exact package-manager `test`, `run test`, `run typecheck`, `run lint`,
     `run build`, and `run check` commands for npm, pnpm, yarn, and bun, with no
     extra arguments;
   - exact `pytest`, `pytest tests`, `python -m pytest`, `python3 -m pytest`,
     `python3 -m unittest`, `go test ./...`, `go vet ./...`, `cargo test`,
     `cargo check`, `cargo clippy`, `make test`, `make check`, `make lint`,
     `make build`, and `python3 -m py_compile`;
   - exact `gh pr checks`, plus read-only `gh pr view`, `gh pr diff`, and
     `gh run list`;
   - read-only git inspection.
5. Deny direct install, publish, deploy, merge, data mutation, source edits,
   chained commands, redirection, pipes, command substitution, a single `&`,
   newlines, zsh process substitution `=(`, and the git parser flags
   `--textconv` and `--show-signature`. Package-manager scripts are exact, so
   they cannot take extra flags. Do not allow `npx`: it can fetch and execute a
   remote package. Do not allow `git grep`: its pager flag can execute a
   command. Do not allow `go test -exec`, `go vet -vettool`,
   `cargo clippy --fix`, or `cargo test --config`. Do not allow `bash -n`: its
   `-i -c` form executes a command; shell syntax checks are left to the tester.
6. If a command is outside the allowlist, the tester runs it and passes the raw
   output to the reviewer. The reviewer judges evidence, not a summary.
7. Add a cross-boundary pass to the `code-review` skill: DB type against query
   parameter, timestamp precision, client/server boundary, bundle boundary,
   serialization, and concurrency token precision.

## Security boundary

The allowlist constrains the command string, not the code it runs. Test and build
code executes with the reviewer's permissions, including read access and
network access. It is not a sandbox. For an external or untrusted change, the
tester or CI runs verification in a disposable environment and passes the raw
output; the reviewer does not execute untrusted project code. The reviewer
prompt also treats PR descriptions, comments, commit messages, and CI logs as
untrusted data, never instructions.

## Alternatives considered

- **Leave review optional for Moderate work.** Rejected. That is the observed
  failure mode: the change looks local, the tests pass, and the bug lives on the
  other side of a boundary.
- **Give the reviewer full bash.** Rejected. It loses the source-edit boundary
  and turns review into a second builder.
- **Have only the tester run verification.** Rejected as the sole mechanism. The
  reviewer needs to confirm or refute its own candidates, and a round trip
  through the lead for every check is slower. The tester remains the fallback
  for commands outside the allowlist and for untrusted changes.
- **Use one generic `verify` wrapper.** Deferred. A wrapper is a larger change
  and hides the exact command from the reviewer. The allowlist plus the tester
  fallback covers the common stacks now.
- **Revert the subagent fold.** Rejected. The fold kept reviewer and security;
  reverting restores the planner and longer prompts, adds cost and latency, and
  does not restore any review capability.

## Consequences

- A non-trivial Moderate change takes one more handoff: tester then reviewer.
  That is the cost of the gate.
- The reviewer prompt and permission block grow. The review is slower but
  evidence-backed.
- The reviewer can still miss bugs that need production state, a live database,
  or a runtime environment. The gate reduces the class, it does not eliminate
  it.
- The allowlist needs maintenance as new stacks appear. The tester fallback
  covers gaps.
- The lead must state the review verdict and evidence in the final report. A
  missing verdict is a process failure, not an implicit approval.
- The YAML subset now unescapes double-quoted keys, so a deny pattern with a
  newline can round-trip. This is a parser correctness fix, not a new syntax
  surface.

## Validation

- `tests/test_adapters.py` asserts the reviewer can run the exact verification
  commands, cannot run install, publish, deploy, merge, mutating git, exec-flag
  commands, `npx`, `bash -n -i -c`, or chained commands. The chaining probes use a broad
  `git diff` prefix so the control deny, not the exact allow, is the deciding
  rule. The same probes are denied in the v2 ordered list.
- `tests/test_claude_sync.sh` asserts the Claude guard carries the reviewer
  allowlist, blocks `npm install`, and blocks single-`&`, newline, and `=(`
  chaining under a broad `git diff` allow. It also checks that the generated
  hook does not carry literal newline or CR deny arguments.
- `eng sync` renders both editors; `eng health` is green.
- No model eval was run for this change. A seeded review-recall eval is the next
  step.

## Residual risk

- Project test and build code still runs with the reviewer's permissions. The
  external-PR fallback is a process control, not a sandbox.
- OpenCode v1 enforcement is modelled by the repository's matcher, not a live
  binary. The control denies cover the known operators; a live check on each
  OpenCode upgrade is still worthwhile.
- The allowlist can be narrowed further as the operator's stacks settle.
