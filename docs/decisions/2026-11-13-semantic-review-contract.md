# Semantic review contract and per-PR merge gate

Date: 2026-11-13
Status: accepted, operator-requested 2026-11-13

## Context

The 2026-11-06 review gate made independent review mandatory and gave the
reviewer a verification allowlist. Real sessions showed three gaps that the gate
did not close.

1. **The review checked what the brief asked, not what the product does.** On
   2026-11-05 the reviewer finished a 47-file redesign review at 20:39 with one
   blocker and eleven should-fix items. Between 20:52 and 20:57 Vercel posted
   three findings on PR 130: newly `enrolled` care plans shown as `Active`,
   refills deduped by `orderId` with medications hidden and undercounted, and a
   review screen promising a charge after dispatch when card holds were off. All
   three were fixed before the 21:01 merge. The review brief covered behavior
   preservation, money and safety paths, contract tests, mobile, accessibility
   and tokens. It did not cover state semantics, cardinality or time.
2. **The review gate ran per phase, not per PR.** After the 20:39 review, PRs
   133 through 138 were merged on 2026-11-06 with no further reviewer session.
   PRs 129, 134 and 138 had no reviewer session at all. Vercel caught bugs on
   those PRs, and the lead fixed the threads before merging. In practice Vercel
   was the first semantic reviewer.
3. **The reviewer often did not run the playbook or the verification.** Only 10
   of 60 reviewer sessions loaded `code-review`. 9 of 109 builder sessions loaded
   `test-driven-development`. 1 of 23 tester sessions loaded `testing`. In one
   review, `git -C ...` was rejected by the allowlist, so the reviewer read files
   and accepted author-reported results.

The model was not the bottleneck. A blind replay of PR 138, the double-charge
race Vercel caught, used the current `deepseek-v4.1-flash#max` reviewer on the
buggy commit `5aecdd4`. It found the exact bug Vercel found and two more
blockers, including the missing serialization and the unconditional session-id
write. A generic brief and a `deepseek-v4-pro` reviewer also found it. The
difference was whether the reviewer ran the code-review passes at all.

## Decision

1. Add a seven-row semantic contract to work orders, implementation and review:
   surfaces, data provenance, state matrix, cardinality, time, copy truth, and
   optional-field render, plus money and concurrency where they apply.
2. The builder derives the contract before coding, writes a behavioral test for
   each risky row, and reports rows it could not prove. Source-pin tests are
   allowed only for wiring and security invariants, never as the sole evidence
   for logic, money, time, state or copy.
3. The reviewer independently derives the contract, runs it as mandatory passes,
   and returns a coverage table with the head SHA and the verdict. A review
   without the table is incomplete. Author-reported results are not verified
   evidence.
4. Review each mergeable change at its exact head SHA. If a commit lands after
   the review, re-review the delta. One branch-level review does not cover PRs
   created later from the same branch.
5. Add a merge gate (`/merge`): reviewer verdict with the coverage table for
   the head SHA, raw verification, green CI, no unresolved review threads, and a
   mergeable base. Sensitive changes still stop for human approval. This is a
   process control; GitHub branch protection enforces review, last-push approval
   and thread resolution for non-admin contributors.
6. Expand read-only verification access for the reviewer, tester and security
   agents: common package scripts, local test and build binaries, read-only
   `git -C` inspection, package audits, and no web access for the reviewer or
   security agent. External documentation comes from the lead's packet. Keep the source-edit, install, publish, deploy, merge and
   write-command boundary. The reviewer does not get `gh api` or web access.
7. Close the loop in the lead prompt: end every turn on the next action or a
   concrete decision through the `question` tool, not on a bare status report.

## Alternatives considered

- **Upgrade the reviewer model.** Rejected as the primary fix. The current model
  found the PR 138 bug when the brief asked the right questions and the reviewer
  ran the passes. A stronger model is a margin, not a substitute for the brief.
- **Rely on the Vercel review agent.** Rejected as the primary gate. It is
  post-PR, outside our control, and it reviews after the code is already written
  and CI is green. Keep it as a second gate and a free recall check.
- **Give the reviewer full shell access.** Rejected. It loses the source-edit
  boundary. The expansion is read-only verification, not implementation.
- **Keep one review per branch.** Rejected. The 2026-11-06 evidence shows later
  PRs merged without a review of their own head.
- **Put all procedure in skills.** Rejected as the only mechanism. The playbooks
  are good, but the agents skipped them. Critical passes also go in the agent
  prompt, and the coverage table makes an omission visible.

## Security review of the access expansion

The independent security review of the first cut found four holes in the new
read-only access. A second pass found the remaining write and exfiltration paths.
They are fixed or recorded here:

- `gh api repos/*/pulls/*` was removed from the reviewer. It allowed implicit
  POST with `-f`, `--method=POST` and merge or review endpoints, so the reviewer
  could write to the PR it was gating.
- Reviewer `webfetch` and `websearch` were reverted to deny, and the security
  agent's web access was denied for the same reason. The tool has no
  private-address guard and the agents can read host files, so the pair is an
  SSRF and exfiltration path. External documentation comes from the lead's
  packet.
- The `git -C` allow rules got blanket `*--output*`, `*--ext-diff*`, `git -C * -c *`
  and `git -c *` denies, so the OpenCode map matches the Claude guard for the
  literal forms. Quote-split forms remain a stopgap.
- The security agent got the reviewer's control-operator deny block, plus
  `*--output*`, `*--ext-diff*`, `*--report-path*`, `npm audit fix`,
  `semgrep --config=https/http`, `semgrep -o`, `trivy -o`, `gitleaks -o`,
  `*--fix*`, `* -o*`, `trivy plugin` and `--generate-default-config` denies. It
  had no control denies before, so every wildcard was a chaining anchor.
- The reviewer's local binary allows got write-flag denies: `eslint --fix`,
  `eslint --output-file`, `jest -u`, `vitest -u`, `tsc --outFile`, `tsc --outDir`,
  `playwright --update-snapshots`. The test wildcards got `python3 -m pytest /*`,
  `../*`, `--junitxml`, `go test -toolexec` and `cargo test --manifest-path`
  denies.
- Quoted and escaped flag forms are a stopgap: targeted `git *--out*"*`,
  `git *--ext-*"*`, `git *"-c"*`, `git *\*` and `*$'*` denies. The Claude
  guard also rejects ANSI-C `$'` quoting. A parser-based guard is the durable
  fix and task 738.
- Semgrep `--autofix`, the `--*-output` URL family, `install-semgrep-pro`,
  `publish`, `ci`, `login`, `--remote`, Trivy `repo`/`aws`/`server`/`clean`,
  TruffleHog git URLs, the Go single-dash profile flags, `pip-audit --out`, and
  the scanner URL overrides (`--registry`, `--index-url`, `--db-repository`,
  `govulncheck -db`) are denied.
- The merge gate's thread step now uses GraphQL `reviewThreads` with
  `isResolved`, `id` and `pageInfo`, because the REST comments endpoint has no
  resolution field.
- The semantic contract now carries the optional-field row in the lead,
  work-order and builder documents as well as the reviewer.

## Consequences

- Work orders and reviews take longer to write. The cost moves from the post-PR
  fix loop to the pre-PR contract, where it is cheaper.
- The reviewer and tester can verify more, so fewer reviews are static-only. The
  map denies the configured scanner install/publish subcommands; scanner network
  fetch and code execution through test scripts remain residual.
- The engine gains a `work-order` skill and a `/merge` command, and the
  `code-review` and `testing` skills gain the semantic passes.
- The model tiers and the default model do not change. Cost is roughly flat.
- Vercel findings become a quality metric: the target is no new semantic finding
  on a reviewed PR. A finding becomes a new contract row and a regression test.

## Validation

- `tests/test_adapters.py` covers the seventh command, the `work-order` skill,
  the expanded read-only verification allowlist, the `git -C` read-only rules and
  their write-form denies, the quoted-flag stopgap, the security control-operator
  and scanner write-flag denies, the local binary write-flag denies, and the
  semantic-contract names in the prompts.
- `tests/test_claude_sync.sh` covers the Claude guard for `git -C`, the local
  binary and script-variant allows, the `go test -exec` deny under a wildcard,
  the ANSI-C `$'` rejection, and the generated reviewer output and fix denies.
- The full engine suite runs: `bash tests/test_eng.sh`,
  `python3 tests/test_adapters.py`, `bash tests/test_claude_sync.sh`,
  `bash tests/test_mcp.sh`, `python3 tests/test_ruleset.py`,
  `python3 tests/test_evals.py`.
- The change itself goes through the new review gate.

## Residual risk

- The reviewer can still miss a bug that needs production state, a live database
  or a real browser. The semantic contract reduces the class, it does not
  eliminate it.
- The shell allowlist is a guardrail, not a sandbox. OpenCode matches raw
  strings, so the quoted and escaped flag denies are a stopgap. One-character
  quote shifts still bypass them. A parser-based guard, shared with the Claude
  hook, is the durable fix and task 738. The operator must accept this residual
  explicitly before the reviewer handles external PRs.
- The expanded allowlist still executes project test and build code with the
  reviewer's permissions. The local binary and `node scripts/check-*` prefixes
  bound the command name, not the code. The external-PR fallback remains a
  process control, not a sandbox.
- The merge gate is a process control. The operator's admin role can bypass the
  ruleset, and the reviewer verdict is not a signed artifact. The lead must not
  use `gh pr merge --admin`.
- The read-only agents still have default access to write-capable MCP tools
  because the permission map does not deny them. Closing that is a separate
  security task, and it must be closed before the reviewer is pointed at an
  external PR.
