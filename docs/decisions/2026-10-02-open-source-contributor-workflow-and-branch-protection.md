# ADR: Open-source contributor workflow and branch protection on `main`

- **Date:** 2026-10-02
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Project:** engineering-os

## Context

EngineeringOS is now a public repository. It was already public and MIT-licensed,
but it had **no branch protection, no rulesets, and no `.github/` directory at
all**. Anyone with write access could push straight to `main`, and there was no
CI to catch a broken `scripts/eng` or MCP server.

We want the repo to be genuinely open to contributors (a clear way in, automated
checks, readable policy) without locking the solo maintainer out of their own
repository. A branch protection policy is only meaningful if there is a status
check to require, so CI had to come first.

## Decision

Protect `main` with a repository ruleset, and define it as data:

1. **CI (`.github/workflows/ci.yml`)** runs, in a single job named `ci`:
   `bash -n scripts/eng`, `python3 -m py_compile` on the MCP server,
   `tests/test_eng.sh`, `tests/test_mcp.sh`, and `tests/test_ruleset.py`.
2. **`.github/ruleset.json`** is the source of truth for the ruleset. It is read
   and applied by `eng repo-protect`, and it is guarded by
   `tests/test_ruleset.py` so a bad edit fails CI.
3. **Rules on `main`:** pull request required, **0 required approvals**,
   required status check `ci` (pinned to the GitHub Actions app via
   `integration_id`, branch must be up to date), review threads must be
   resolved, linear history, no force-push, no deletion.
4. **Bypass:** a single actor, the repository admin role (`RepositoryRole`,
   id 5), with `bypass_mode: "always"`.

The resulting policy: contributors can only land on `main` through a PR that
passes CI; the maintainer retains direct push.

## Why these choices

- **0 approvals, not 1.** GitHub bypass modes cannot express "everyone else must
  get an approval, but I can push directly". `always` skips every rule for the
  admin, including the review count, so requiring 1 approval would not actually
  bind the maintainer and would block contributors until a second reviewer
  exists (there is currently one maintainer). Zero approvals is the honest
  setting; the review culture is stated in `CONTRIBUTING.md` and can be raised
  the day a second maintainer appears.
  - GitHub's API *requires* all five review-related keys on the `pull_request`
    rule: `required_approving_review_count`, `dismiss_stale_reviews_on_push`,
    `require_last_push_approval`, `require_code_owner_review`, and
    `required_review_thread_resolution`. With 0 approvals the review-dependent
    ones are set to `false` (there is nothing to dismiss or re-approve).
    `tests/test_ruleset.py` asserts both their presence and their values.
- **`always`, not `pull_request`.** With `always` the admin can also
  rename/change the default branch, which is otherwise blocked by the ruleset.
  `pull_request` would force even the maintainer through a PR and would break
  default-branch operations.
- **`~DEFAULT_BRANCH` instead of `refs/heads/main`.** Protection follows the
  default branch if it is ever renamed, rather than silently detaching.
- **Ruleset as a checked-in JSON file.** It is readable and reviewable like any
  other change, and `eng repo-protect --check` gives a read-only drift report.
  This beat Terraform, which would add a large dependency to a deliberately
  dependency-free repo.
- **Required status check is exactly `ci`, pinned to the Actions app.** A
  required context that does not exist blocks every merge forever, so the
  context is pinned to the CI job name and asserted in `tests/test_ruleset.py`.
  `integration_id` (15368, the GitHub Actions app) ensures only the real
  workflow can satisfy the check, so a future app or integration cannot spoof a
  passing `ci` status.

## Consequences

**Positive**

- Contributors have a clear, enforced path: branch, PR, green CI, merge.
- Broken `eng` or MCP changes cannot reach `main`.
- The protection policy is versioned, reviewable, and testable.
- The maintainer is never locked out; emergency changes remain possible.

**Negative**

- The maintainer's own direct pushes to `main` are not CI-gated. This is a
  deliberate tradeoff for a solo-maintainer repo; the same tests are available
  locally and run on PRs from contributors.
- Adding a required approval later is a one-line change to `ruleset.json`,
  but until then no human review is machine-enforced for the maintainer.

## Alternatives considered

- **Classic branch protection API** instead of rulesets. Rejected: rulesets are
  the current mechanism, support bypass actors and ref conditions cleanly, and
  surface rule insights.
- **`pull_request` bypass + 1 required approval.** Rejected: forces the
  maintainer through a PR for every change and blocks default-branch operations.
- **Terraform / Pulumi for repo config.** Rejected: disproportionate dependency
  for one ruleset on a stdlib-only repo.
- **No protection, convention only.** Rejected: the point of the exercise is
  that contributions cannot land on `main` unchecked.

## References

- GitHub REST API, repository rulesets: https://docs.github.com/en/rest/repos/rules
- GitHub ruleset rules and bypass modes:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- EngineeringOS research record: `research/2026-10-02-github-rulesets-api-for-branch-protection-on-a-per.md`
