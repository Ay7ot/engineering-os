#!/usr/bin/env bash
# Tests for scripts/eng. Fast, hermetic, no network.
# Run: bash tests/test_eng.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENG="$REPO_ROOT/scripts/eng"

pass=0
fail=0
ok() { printf '  PASS: %s\n' "$1"; pass=$((pass + 1)); }
no() { printf '  FAIL: %s\n' "$1"; fail=$((fail + 1)); }

expect_eq() { # $1 desc, $2 expected, $3 actual
  if [ "$2" = "$3" ]; then ok "$1"; else no "$1 (expected [$2], got [$3])"; fi
}

expect_contains() { # $1 desc, $2 needle, $3 haystack
  case "$3" in
    *"$2"*) ok "$1" ;;
    *) no "$1 (missing [$2] in [$3])" ;;
  esac
}

echo "test_eng: syntax"
if bash -n "$ENG"; then ok "scripts/eng parses"; else no "scripts/eng parses"; fi

echo "test_eng: usage"
out="$("$ENG" bogus-command 2>&1 || true)"
expect_contains "unknown command prints usage" "usage: eng" "$out"

echo "test_eng: health (isolated data dir)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export ENGINEERING_OS_DATA="$TMP/data"
out="$("$ENG" health 2>&1 || true)"
expect_contains "health reports engine path" "Engine:" "$out"
expect_contains "health reports data path" "Data:" "$out"
expect_contains "health MCP responds" "ok: engineering-memory MCP responds" "$out"
# These lines come after the last possible early abort, so they catch truncation.
expect_contains "health reaches default agent line" "Default agent:" "$out"
expect_contains "health reaches commands line" "Commands synced:" "$out"
expect_contains "health lists worktree command" "worktree" "$out"

echo "test_eng: worktree new/list/close in a scratch repo"
SCRATCH="$TMP/scratch"
mkdir -p "$SCRATCH"
git -C "$SCRATCH" init -q -b main
git -C "$SCRATCH" config user.email "test@example.com"
git -C "$SCRATCH" config user.name "Test"
printf 'hello\n' > "$SCRATCH/README.md"
git -C "$SCRATCH" add -A
git -C "$SCRATCH" commit -qm "init"

out="$("$ENG" worktree new demo --repo "$SCRATCH" --base main 2>&1 || true)"
expect_contains "worktree new reports branch" "branch: feat/demo" "$out"
wt="$TMP/scratch-demo-wt"
if [ -d "$wt" ]; then ok "worktree directory created"; else no "worktree directory created"; fi
if git -C "$SCRATCH" show-ref --verify --quiet refs/heads/feat/demo; then
  ok "feature branch created"
else
  no "feature branch created"
fi

out="$("$ENG" worktree list --repo "$SCRATCH" 2>&1 || true)"
expect_contains "worktree list shows git worktrees" "git worktree list" "$out"

# Idempotency: a second run must not duplicate or crash. The first guard hit is
# the branch-exists guard, which is the correct behavior for a re-run.
out="$("$ENG" worktree new demo --repo "$SCRATCH" --base main 2>&1 || true)"
expect_contains "worktree new is idempotent" "branch already exists" "$out"

# Type collision: same slug, different type must be refused.
out="$("$ENG" worktree new demo --repo "$SCRATCH" --type fix --base main 2>&1 || true)"
expect_contains "type collision refused" "refusing to reuse" "$out"

# Dirty worktree close must be refused.
printf 'dirty\n' > "$wt/dirty.txt"
out="$("$ENG" worktree close demo --repo "$SCRATCH" 2>&1 || true)"
expect_contains "dirty close refused" "uncommitted changes" "$out"

out="$("$ENG" worktree close demo --repo "$SCRATCH" --force --delete-branch 2>&1 || true)"
expect_contains "forced close succeeds" "closed demo" "$out"
if [ -d "$wt" ]; then no "worktree directory removed"; else ok "worktree directory removed"; fi

# Not a git repo must fail clearly, not silently.
out="$("$ENG" worktree list --repo "$TMP" 2>&1 || true)"
expect_contains "non-git repo reports clearly" "not a git repo" "$out"

echo "test_eng: repo-protect (stubbed gh, no network)"
# Stub gh so we exercise the CLI logic without touching GitHub. It parses the
# real `gh api [-X METHOD] PATH [--input FILE]` shape, so the CLI's own arg
# construction is what is under test.
STUB="$TMP/bin"
mkdir -p "$STUB"
cat > "$STUB/gh" <<'STUBEOF'
#!/usr/bin/env bash
# Minimal gh stub. Driven by $GH_STUB_MODE: empty | create | update | drift.
method="GET"; path=""; input=""
while [ $# -gt 0 ]; do
  case "$1" in
    api) shift ;;
    -X) method="$2"; shift 2 ;;
    --input) input="$2"; shift 2 ;;
    -*) shift ;;
    *) path="$1"; shift ;;
  esac
done
mode="${GH_STUB_MODE:-empty}"
case "$mode" in
  empty)
    # GET list -> no rulesets yet; any write -> created.
    if [ "$method" = "GET" ] && [ "$path" = "repos/x/y/rulesets" ]; then echo '[]'; else echo '{"id":1}'; fi
    ;;
  update)
    if [ "$method" = "GET" ] && [ "$path" = "repos/x/y/rulesets" ]; then echo '[{"id":1,"name":"protect-main"}]'; else echo '{"id":1}'; fi
    ;;
  drift)
    case "$path" in
      repos/x/y/rulesets) echo '[{"id":1,"name":"protect-main"}]' ;;
      repos/x/y/rulesets/1)
        # Same policy the file declares, plus an extra field GitHub adds.
        echo '{"name":"protect-main","enforcement":"active","conditions":{"ref_name":{"include":["~DEFAULT_BRANCH"],"exclude":[]}},"bypass_actors":[{"actor_type":"RepositoryRole","actor_id":5,"bypass_mode":"always"}],"rules":[{"type":"deletion"},{"type":"non_fast_forward"},{"type":"required_linear_history"},{"type":"pull_request","parameters":{"required_approving_review_count":0,"require_code_owner_review":false,"required_review_thread_resolution":true,"allowed_merge_methods":["squash","rebase"],"extra_github_field":true}},{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":true,"do_not_enforce_on_create":true,"required_status_checks":[{"context":"ci","integration_id":15368}]}}]}' ;;
      *) echo '{}' ;;
    esac
    ;;
  *) echo '[]' ;;
esac
STUBEOF
chmod +x "$STUB/gh"
export PATH="$STUB:$PATH"

out="$(GH_STUB_MODE=empty "$ENG" repo-protect --repo x/y --file "$REPO_ROOT/.github/ruleset.json" 2>&1 || true)"
expect_contains "repo-protect creates when absent" "created" "$out"

out="$(GH_STUB_MODE=update "$ENG" repo-protect --repo x/y --file "$REPO_ROOT/.github/ruleset.json" 2>&1 || true)"
expect_contains "repo-protect updates when present" "updated" "$out"

# Extra fields in the GitHub response must NOT read as drift.
out="$(GH_STUB_MODE=drift "$ENG" repo-protect --check --repo x/y --file "$REPO_ROOT/.github/ruleset.json" 2>&1 || true)"
expect_contains "repo-protect --check tolerates extra server fields" "IN SYNC" "$out"

# Missing origin remote must produce the friendly error, not a silent abort.
# Point the CLI's engine home at a scratch repo that has no origin remote.
FAKE_ENG="$TMP/engine"
mkdir -p "$FAKE_ENG/.github"
cp "$REPO_ROOT/.github/ruleset.json" "$FAKE_ENG/.github/ruleset.json"
git -C "$FAKE_ENG" init -q -b main
out="$(GH_STUB_MODE=empty ENGINEERING_OS_HOME="$FAKE_ENG" "$ENG" repo-protect 2>&1 || true)"
expect_contains "repo-protect without origin errors clearly" "pass --repo" "$out"

# Invalid --repo must be rejected.
out="$(GH_STUB_MODE=empty "$ENG" repo-protect --repo 'evil;rm' --file "$REPO_ROOT/.github/ruleset.json" 2>&1 || true)"
expect_contains "repo-protect rejects invalid repo" "pass --repo" "$out"

# Missing gh binary must be reported clearly (PATH without the stub).
out="$(PATH="/usr/bin:/bin" "$ENG" repo-protect --repo x/y --file "$REPO_ROOT/.github/ruleset.json" 2>&1 || true)"
expect_contains "repo-protect reports missing gh" "gh" "$out"

echo
echo "test_eng: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
