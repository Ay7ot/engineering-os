#!/usr/bin/env python3
"""Guard for .github/ruleset.json.

CI must keep running even if a contributor edits the ruleset config, so this
test validates the JSON structurally instead of trusting it. It also asserts the
protection invariants the project has committed to.

Run: python3 tests/test_ruleset.py
"""
import json
import sys
from pathlib import Path

RULESET = Path(__file__).resolve().parents[1] / ".github" / "ruleset.json"

failures = []


def check(cond, msg):
    if cond:
        print(f"  PASS: {msg}")
    else:
        print(f"  FAIL: {msg}")
        failures.append(msg)


def main():
    check(RULESET.is_file(), "ruleset.json exists")
    if not RULESET.is_file():
        return 1

    raw = RULESET.read_text(encoding="utf-8")
    try:
        rs = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  FAIL: ruleset.json is valid JSON ({e})")
        failures.append("json")
        return 1
    check(True, "ruleset.json is valid JSON")

    check(rs.get("target") == "branch", "target is branch")
    check(rs.get("enforcement") == "active", "enforcement is active")
    check(rs.get("name"), "ruleset has a name")

    include = rs.get("conditions", {}).get("ref_name", {}).get("include", [])
    check(bool(include), "conditions include at least one ref")
    check(
        any(x in ("~DEFAULT_BRANCH", "refs/heads/main") for x in include),
        "conditions protect the default branch (main)",
    )

    types = {r.get("type") for r in rs.get("rules", []) if isinstance(r, dict)}

    for required in (
        "deletion",
        "non_fast_forward",
        "required_linear_history",
        "pull_request",
        "required_status_checks",
    ):
        check(required in types, f"rule present: {required}")

    pr = next(
        (r for r in rs.get("rules", []) if r.get("type") == "pull_request"),
        {},
    ).get("parameters", {})
    check(
        pr.get("required_approving_review_count", None) == 0,
        "required approvals is 0 (solo maintainer model)",
    )
    check(
        pr.get("required_review_thread_resolution") is True,
        "review threads must be resolved",
    )
    check(
        sorted(pr.get("allowed_merge_methods", [])) == ["rebase", "squash"],
        "only squash and rebase merges are allowed",
    )
    # These settings imply required reviewers; with 0 approvals they are
    # contradictory and must not be present.
    check(
        "require_last_push_approval" not in pr,
        "no require_last_push_approval while approvals is 0",
    )
    check(
        "dismiss_stale_reviews_on_push" not in pr,
        "no dismiss_stale_reviews_on_push while approvals is 0",
    )

    sc = next(
        (r for r in rs.get("rules", []) if r.get("type") == "required_status_checks"),
        {},
    ).get("parameters", {})
    checks = sc.get("required_status_checks", [])
    contexts = [c.get("context") for c in checks]
    check(contexts == ["ci"], "required status check is exactly 'ci'")
    check(
        bool(checks) and checks[0].get("integration_id") == 15368,
        "status check is pinned to the GitHub Actions app (integration_id 15368)",
    )
    check(
        sc.get("strict_required_status_checks_policy") is True,
        "branches must be up to date before merge",
    )

    bypass = rs.get("bypass_actors", [])
    check(len(bypass) == 1, "exactly one bypass actor")
    if bypass:
        check(
            bypass[0].get("actor_type") == "RepositoryRole"
            and bypass[0].get("actor_id") == 5,
            "bypass actor is the repository admin role (id 5)",
        )
        check(
            bypass[0].get("bypass_mode") in ("always", "pull_request"),
            "bypass_mode is always or pull_request",
        )

    print()
    if failures:
        print(f"test_ruleset: {len(failures)} check(s) failed")
        return 1
    print("test_ruleset: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
