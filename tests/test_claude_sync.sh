#!/usr/bin/env bash
# Tests for `eng sync-claude` (scripts/claude_sync.py) and claude/hooks/eos_guard.py.
# Hermetic: HOME points at a temp dir, no network, no real Claude config touched.
# Run: bash tests/test_claude_sync.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENG="$REPO_ROOT/scripts/eng"
GUARD="$REPO_ROOT/claude/hooks/eos_guard.py"

pass=0
fail=0
ok() { printf '  PASS: %s\n' "$1"; pass=$((pass + 1)); }
no() { printf '  FAIL: %s\n' "$1"; fail=$((fail + 1)); }

expect_contains() { # $1 desc, $2 needle, $3 haystack
  case "$3" in
    *"$2"*) ok "$1" ;;
    *) no "$1 (missing [$2])" ;;
  esac
}
expect_missing() { # $1 desc, $2 needle, $3 haystack
  case "$3" in
    *"$2"*) no "$1 (unexpected [$2])" ;;
    *) ok "$1" ;;
  esac
}
expect_file() { if [ -f "$2" ]; then ok "$1"; else no "$1 ($2 missing)"; fi; }
expect_nofile() { if [ ! -e "$2" ]; then ok "$1"; else no "$1 ($2 exists)"; fi; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export HOME="$TMP/home"
unset CLAUDE_CONFIG_DIR
export ENGINEERING_OS_DATA="$TMP/data"
C="$HOME/.claude"
mkdir -p "$C/agents"
printf '{"numStartups": 3, "mcpServers": {"other": {"command": "x"}}}\n' > "$HOME/.claude.json"
printf '# my prefs\nbe terse\n' > "$C/CLAUDE.md"
printf -- '---\nname: mine\ndescription: user agent\n---\nkeep me\n' > "$C/agents/mine.md"

echo "test_claude_sync: syntax"
if python3 -m py_compile "$REPO_ROOT/scripts/claude_sync.py" "$GUARD"; then ok "python compiles"; else no "python compiles"; fi

echo "test_claude_sync: first sync"
out="$("$ENG" sync-claude 2>&1 || true)"
expect_contains "sync reports agents" "8 agents" "$out"
expect_contains "sync configures MCP" "configured engineering-memory MCP" "$out"

for a in architect builder explorer planner researcher reviewer security tester; do
  expect_file "agent $a generated" "$C/agents/$a.md"
done
expect_nofile "lead is not a subagent (it lives in CLAUDE.md)" "$C/agents/lead.md"
expect_file "user agent untouched" "$C/agents/mine.md"

explorer="$(cat "$C/agents/explorer.md")"
expect_contains "explorer has name" "name: explorer" "$explorer"
expect_contains "explorer cannot edit" "disallowedTools: Edit, Write, NotebookEdit" "$explorer"
expect_contains "explorer bash guarded" "eos_guard.py bash --allow 'git status *'" "$explorer"
expect_contains "explorer model mapped" "model: haiku" "$explorer"
expect_missing "opencode permission map not leaked" "permission:" "$explorer"

builder="$(cat "$C/agents/builder.md")"
expect_missing "builder unrestricted" "disallowedTools" "$builder"
expect_missing "builder has no guard" "eos_guard" "$builder"

architect="$(cat "$C/agents/architect.md")"
expect_contains "architect edits limited to markdown" "edit --allow '*.md'" "$architect"
planner="$(cat "$C/agents/planner.md")"
expect_contains "planner bash denied" "Bash" "$(grep '^disallowedTools' "$C/agents/planner.md")"

expect_file "renamed skill eos-security-review" "$C/skills/eos-security-review/SKILL.md"
expect_file "renamed skill eos-code-review" "$C/skills/eos-code-review/SKILL.md"
expect_nofile "built-in skill name not shadowed" "$C/skills/security-review"
expect_contains "skill name rewritten" "name: eos-security-review" "$(cat "$C/skills/eos-security-review/SKILL.md")"
expect_contains "cross-skill refs rewritten" "eos-security-review" "$(cat "$C/skills/backend-architecture/SKILL.md")"
expect_file "renamed command eos-review" "$C/commands/eos-review.md"
expect_nofile "built-in command name not shadowed" "$C/commands/review.md"
feature="$(cat "$C/commands/feature.md")"
expect_contains "command keeps \$ARGUMENTS" '$ARGUMENTS' "$feature"
expect_missing "command drops opencode agent key" "agent: lead" "$feature"

md="$(cat "$C/CLAUDE.md")"
expect_contains "CLAUDE.md keeps user content" "be terse" "$md"
expect_contains "CLAUDE.md imports principles" "@$REPO_ROOT/PRINCIPLES.md" "$md"
expect_contains "CLAUDE.md carries lead role" "Lead Agent of EngineeringOS" "$md"

cj="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=d["mcpServers"]; print(d["numStartups"], "other" in m, m["engineering-memory"]["env"]["ENGINEERING_OS_DATA"])' "$HOME/.claude.json")"
expect_contains ".claude.json preserves keys and sets data dir" "3 True $TMP/data" "$cj"
expect_file ".claude.json backup written" "$HOME/.claude.json.engineeringos.bak"

echo "test_claude_sync: idempotent"
out="$("$ENG" sync-claude 2>&1 || true)"
expect_contains "second sync changes nothing" "(0 files changed)" "$out"
expect_contains "second sync leaves MCP" "already configured" "$out"
blocks="$(grep -c 'BEGIN EngineeringOS' "$C/CLAUDE.md")"
if [ "$blocks" = "1" ]; then ok "single managed block"; else no "single managed block (got $blocks)"; fi

echo "test_claude_sync: stale managed files removed, user files kept"
python3 - "$C/.engineeringos-manifest.json" "$C/agents/ghost.md" <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); m["files"].append(sys.argv[2])
json.dump(m, open(sys.argv[1], "w"))
open(sys.argv[2], "w").write("old generated agent\n")
PY
"$ENG" sync-claude >/dev/null 2>&1 || true
expect_nofile "stale generated agent pruned" "$C/agents/ghost.md"
expect_file "user agent still untouched" "$C/agents/mine.md"

echo "test_claude_sync: health"
out="$("$ENG" health 2>&1 || true)"
expect_contains "health shows Claude MCP ok" "Claude MCP: ok" "$out"
expect_contains "health shows CLAUDE.md block" "Claude CLAUDE.md block: present" "$out"

echo "test_claude_sync: guard"
guard() { # $1 json input, rest guard args -> prints exit code
  printf '%s' "$1" | python3 "$GUARD" "${@:2}" >/dev/null 2>&1 && echo 0 || echo $?
}
B=(bash --allow 'git log *' --allow 'git status *')
[ "$(guard '{"tool_input":{"command":"git log --oneline -5"}}' "${B[@]}")" = 0 ] && ok "allowed command passes" || no "allowed command passes"
[ "$(guard '{"tool_input":{"command":"git status"}}' "${B[@]}")" = 0 ] && ok "bare command matches 'x *'" || no "bare command matches 'x *'"
[ "$(guard '{"tool_input":{"command":"git -C /repo log -3"}}' "${B[@]}")" = 0 ] && ok "git -C path normalized" || no "git -C path normalized"
[ "$(guard '{"tool_input":{"command":"rm -rf /"}}' "${B[@]}")" = 2 ] && ok "unlisted command blocked" || no "unlisted command blocked"
[ "$(guard '{"tool_input":{"command":"git log && rm -rf x"}}' "${B[@]}")" = 2 ] && ok "chained command blocked" || no "chained command blocked"
[ "$(guard '{"tool_input":{"command":"git log $(rm x)"}}' "${B[@]}")" = 2 ] && ok "substitution blocked" || no "substitution blocked"
[ "$(guard '{"tool_input":{"command":"git log > out"}}' "${B[@]}")" = 2 ] && ok "redirect blocked" || no "redirect blocked"
[ "$(guard 'not json' "${B[@]}")" = 2 ] && ok "bad input fails closed" || no "bad input fails closed"
[ "$(guard '{"tool_input":{"command":"git push"}}' bash --deny 'git push *')" = 2 ] && ok "deny pattern blocks" || no "deny pattern blocks"
[ "$(guard '{"tool_input":{"command":"ls"}}' bash --deny 'git push *')" = 0 ] && ok "deny-only allows others" || no "deny-only allows others"
[ "$(guard '{"tool_input":{"file_path":"/x/docs/adr.md"}}' edit --allow '*.md')" = 0 ] && ok "markdown edit allowed" || no "markdown edit allowed"
[ "$(guard '{"tool_input":{"file_path":"/x/src/app.ts"}}' edit --allow '*.md')" = 2 ] && ok "code edit blocked" || no "code edit blocked"

echo
echo "test_claude_sync: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
