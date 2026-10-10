#!/usr/bin/env bash
# Tests for the Claude Code adapter (adapters/claude) and its guard hook.
# Hermetic: HOME points at a temp dir, no network, no real Claude config touched.
# Run: bash tests/test_claude_sync.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENG="$REPO_ROOT/scripts/eng"
GUARD="$REPO_ROOT/adapters/claude/hooks/eos_guard.py"

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
# Hermetic: never pick up a real `claude` CLI from PATH.
export PATH="$TMP/bin:$PATH"; mkdir -p "$TMP/bin"
printf '#!/bin/sh\nexit 127\n' > "$TMP/bin/claude"; chmod +x "$TMP/bin/claude"
export ENGINEERING_OS_DATA="$TMP/data"
C="$HOME/.claude"
mkdir -p "$C/agents"
printf '{"numStartups": 3, "mcpServers": {"other": {"command": "x"}}}\n' > "$HOME/.claude.json"
printf '# my prefs\nbe terse\n' > "$C/CLAUDE.md"
printf -- '---\nname: mine\ndescription: user agent\n---\nkeep me\n' > "$C/agents/mine.md"
# A user-owned file at a path sync would generate must survive.
mkdir -p "$C/skills/testing"
printf -- '---\nname: testing\ndescription: my own\n---\nmine\n' > "$C/skills/testing/SKILL.md"

echo "test_claude_sync: syntax"
if python3 -m py_compile "$REPO_ROOT/adapters/claude/adapter.py" "$REPO_ROOT/scripts/eos_sync.py" "$GUARD"; then ok "python compiles"; else no "python compiles"; fi

echo "test_claude_sync: first sync"
out="$("$ENG" sync-claude 2>&1 || true)"
expect_contains "sync reports agents" "8 agents" "$out"
expect_contains "sync configures MCP" "configured engineering-memory MCP" "$out"
expect_contains "sync reports skipped user file" "SKIPPED $C/skills/testing/SKILL.md" "$out"
expect_contains "user skill not clobbered" "mine" "$(cat "$C/skills/testing/SKILL.md")"
expect_contains "sets default output style" "set default outputStyle" "$out"

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
expect_missing "source permission map not leaked" "permissions:" "$explorer"

builder="$(cat "$C/agents/builder.md")"
expect_missing "builder unrestricted" "disallowedTools" "$builder"
expect_missing "builder has no guard" "eos_guard" "$builder"

architect="$(cat "$C/agents/architect.md")"
expect_contains "architect edits limited to markdown" "edit --allow '*.md'" "$architect"
planner="$(cat "$C/agents/planner.md")"
expect_contains "planner bash denied" "Bash" "$(grep '^disallowedTools' "$C/agents/planner.md")"

expect_file "renamed skill eos-security-review" "$C/skills/eos-security-review/SKILL.md"
expect_file "renamed skill eos-code-review" "$C/skills/eos-code-review/SKILL.md"
expect_file "renamed skill eos-simplify" "$C/skills/eos-simplify/SKILL.md"
expect_file "renamed skill eos-dataviz" "$C/skills/eos-dataviz/SKILL.md"
expect_nofile "built-in simplify not shadowed" "$C/skills/simplify"
expect_file "memory-hygiene installed" "$C/skills/memory-hygiene/SKILL.md"
expect_file "skill-authoring installed" "$C/skills/skill-authoring/SKILL.md"
expect_missing "skill-authoring never teaches renamed names" "eos-" "$(cat "$C/skills/skill-authoring/SKILL.md")"
expect_contains "code-review points at renamed security skill" '`eos-security-review`' "$(cat "$C/skills/eos-code-review/SKILL.md")"
expect_contains "simplify points at renamed review skill" '`eos-code-review`' "$(cat "$C/skills/eos-simplify/SKILL.md")"
expect_nofile "built-in skill name not shadowed" "$C/skills/security-review"
expect_contains "skill name rewritten" "name: eos-security-review" "$(cat "$C/skills/eos-security-review/SKILL.md")"
expect_contains "cross-skill refs rewritten" "eos-security-review" "$(cat "$C/skills/backend-architecture/SKILL.md")"
expect_file "renamed command eos-review" "$C/commands/eos-review.md"
expect_nofile "built-in command name not shadowed" "$C/commands/review.md"
feature="$(cat "$C/commands/feature.md")"
expect_contains "command keeps \$ARGUMENTS" '$ARGUMENTS' "$feature"
expect_missing "command drops opencode-only keys" "agent: lead" "$feature"

md="$(cat "$C/CLAUDE.md")"
expect_contains "CLAUDE.md keeps user content" "be terse" "$md"
expect_contains "CLAUDE.md imports principles" "@$REPO_ROOT/PRINCIPLES.md" "$md"
expect_missing "CLAUDE.md no longer carries lead role" "Lead Agent of EngineeringOS" "$md"
expect_contains "CLAUDE.md points at the style" "EngineeringOS Lead" "$md"

style="$(cat "$C/output-styles/eos-lead.md")"
expect_contains "style named" 'name: "EngineeringOS Lead"' "$style"
expect_contains "style keeps coding instructions" "keep-coding-instructions: true" "$style"
expect_contains "style carries lead role" "Lead Agent of EngineeringOS" "$style"
expect_contains "style lists subagents" '`explorer`' "$style"
expect_contains "settings default style" '"outputStyle": "EngineeringOS Lead"' "$(cat "$C/settings.json")"
expect_contains "architect edit guard protects claude dir" "--protect $C" "$architect"
expect_contains "architect cannot edit PRINCIPLES.md" "--protect $REPO_ROOT/PRINCIPLES.md" "$architect"
expect_contains "architect cannot edit the data dir" "--protect $TMP/data" "$architect"
expect_contains "architect cannot edit agent sources" "--protect $REPO_ROOT/agents" "$architect"

cj="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=d["mcpServers"]; print(d["numStartups"], "other" in m, m["engineering-memory"]["env"]["ENGINEERING_OS_DATA"])' "$HOME/.claude.json")"
expect_contains ".claude.json preserves keys and sets data dir" "3 True $TMP/data" "$cj"
expect_file ".claude.json backup written" "$HOME/.claude.json.engineeringos.bak"

echo "test_claude_sync: idempotent"
out="$("$ENG" sync-claude 2>&1 || true)"
expect_contains "second sync changes nothing" "(0 files changed)" "$out"
expect_contains "second sync leaves MCP" "already configured" "$out"
blocks="$(grep -c 'BEGIN EngineeringOS' "$C/CLAUDE.md")"
if [ "$blocks" = "1" ]; then ok "single managed block"; else no "single managed block (got $blocks)"; fi

echo "test_claude_sync: existing outputStyle is respected"
printf '{"outputStyle": "Concise", "theme": "dark"}\n' > "$C/settings.json"
out="$("$ENG" sync-claude 2>&1 || true)"
expect_contains "user style left in place" "left your outputStyle 'Concise'" "$out"
expect_contains "settings untouched" '"Concise"' "$(cat "$C/settings.json")"
printf '{"theme": "dark"}\n' > "$C/settings.json"
"$ENG" sync-claude >/dev/null 2>&1 || true
st="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["theme"], d["outputStyle"])' "$C/settings.json")"
expect_contains "settings merge keeps other keys" "dark EngineeringOS Lead" "$st"

echo "test_claude_sync: MCP via claude CLI when present"
rm -f "$HOME/.claude.json"
printf '#!/bin/sh\necho "$@" >> "%s/cli.log"\nexit 0\n' "$TMP" > "$TMP/fakeclaude"; chmod +x "$TMP/fakeclaude"
out="$(python3 "$REPO_ROOT/scripts/eos_sync.py" sync --target claude --engine "$REPO_ROOT" --data "$TMP/data" --claude-cli "$TMP/fakeclaude" 2>&1 || true)"
expect_contains "uses claude mcp add-json" "via \`claude mcp add-json\`" "$out"
expect_contains "CLI called with user scope" "mcp add-json --scope user engineering-memory" "$(cat "$TMP/cli.log")"
expect_nofile "CLI path does not hand-edit .claude.json" "$HOME/.claude.json"
"$ENG" sync-claude >/dev/null 2>&1 || true

echo "test_claude_sync: permission translation fails closed"
python3 - "$REPO_ROOT" <<'PY' && ok "ask/unknown/commented values deny" || no "ask/unknown/commented values deny"
import sys; sys.path.insert(0, sys.argv[1])
from adapters.claude import adapter as cs
from adapters.common import parse_frontmatter
fm, _ = parse_frontmatter("---\npermission:\n  edit: ask\n  bash: deny  # read-only\n  webfetch: maybe\n---\nbody\n")
dis, hooks = cs.translate_permissions(fm["permission"], "py")
assert {"Edit", "Write", "NotebookEdit", "Bash", "WebFetch"} <= set(dis), dis
assert not hooks, hooks
fm, _ = parse_frontmatter("---\r\npermission:\r\n  edit: deny\r\n---\r\nbody\r\n")
assert "Edit" in cs.translate_permissions(fm["permission"], "py")[0], "CRLF"
assert "eos-code-review" in cs.rename_refs("see ~/.claude/skills/code-review/SKILL.md")
assert "skills/code-review/SKILL.md" == cs.rename_refs("skills/code-review/SKILL.md")
r = cs.rename_refs
assert r("simplify the code") == "simplify the code", "prose untouched"
assert r("use `simplify` now") == "use `eos-simplify` now", "backticked one-word renamed"
assert r("see skills/simplify/SKILL.md") == "see skills/simplify/SKILL.md", "source path untouched"
assert r("~/.claude/skills/dataviz/") == "~/.claude/skills/eos-dataviz/", "installed path renamed"
assert r("`eos-simplify`") == "`eos-simplify`", "no double rename"
assert r("`code-review` and code-review") == "`eos-code-review` and eos-code-review", "hyphenated as before"
assert r("`eos-code-review`") == "`eos-code-review`", "no double rename (hyphenated)"
dis, hooks = cs.translate_permissions({"bash": {"*": "deny", "npm *": "allow", "npm publish *": "deny"}}, "py")
assert "--deny 'npm publish *'" in hooks[0][1], hooks
dis, hooks = cs.translate_permissions({"edit": {"*": "allow", "*.env": "ask"}}, "py")
assert hooks and "--deny '*.env'" in hooks[0][1], hooks
PY

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
[ "$(guard '{"tool_input":{"file_path":"/p/agents/explorer.md"}}' edit --allow '*.md' --protect /p)" = 2 ] && ok "protected dir edit blocked" || no "protected dir edit blocked"
[ "$(guard 'null' "${B[@]}")" = 2 ] && ok "non-object input fails closed" || no "non-object input fails closed"
[ "$(guard '{"tool_input":"x"}' "${B[@]}")" = 2 ] && ok "bad tool_input fails closed" || no "bad tool_input fails closed"
[ "$(guard '{"tool_input":{"command":"git log"}}' bogus)" = 2 ] && ok "misconfigured guard fails closed" || no "misconfigured guard fails closed"
[ "$(guard '{"tool_input":{"command":"git log --output=/tmp/x"}}' "${B[@]}")" = 2 ] && ok "git log --output blocked" || no "git log --output blocked"
R=(bash --allow 'git branch *' --allow 'git remote *' --allow 'git *')
[ "$(guard '{"tool_input":{"command":"git branch -a"}}' "${R[@]}")" = 0 ] && ok "git branch -a allowed" || no "git branch -a allowed"
[ "$(guard '{"tool_input":{"command":"git branch -D main"}}' "${R[@]}")" = 2 ] && ok "git branch -D blocked" || no "git branch -D blocked"
[ "$(guard '{"tool_input":{"command":"git branch newb"}}' "${R[@]}")" = 2 ] && ok "git branch create blocked" || no "git branch create blocked"
[ "$(guard '{"tool_input":{"command":"git remote -v"}}' "${R[@]}")" = 0 ] && ok "git remote -v allowed" || no "git remote -v allowed"
[ "$(guard '{"tool_input":{"command":"git remote set-url origin x"}}' "${R[@]}")" = 2 ] && ok "git remote set-url blocked" || no "git remote set-url blocked"
[ "$(guard '{"tool_input":{"command":"git push origin main"}}' "${R[@]}")" = 2 ] && ok "git push blocked under git *" || no "git push blocked under git *"
[ "$(guard '{"tool_input":{"command":"git reset --hard"}}' "${R[@]}")" = 2 ] && ok "git reset blocked under git *" || no "git reset blocked under git *"
[ "$(guard '{"tool_input":{"command":"git -c alias.x=!sh x"}}' "${R[@]}")" = 2 ] && ok "git -c blocked" || no "git -c blocked"
[ "$(guard '{"tool_input":{"command":"git show HEAD"}}' "${R[@]}")" = 0 ] && ok "git show allowed under git *" || no "git show allowed under git *"
N=(bash --allow 'npm *' --deny 'npm publish *')
[ "$(guard '{"tool_input":{"command":"npm publish x"}}' "${N[@]}")" = 2 ] && ok "deny inside allowlist blocks" || no "deny inside allowlist blocks"
[ "$(guard '{"tool_input":{"command":"npm test"}}' "${N[@]}")" = 0 ] && ok "allowlist still allows" || no "allowlist still allows"
[ "$(guard '{"tool_input":{"file_path":"/x/.env"}}' edit --allow '*' --deny '.env' --deny '*.env')" = 2 ] && ok "edit deny glob blocks" || no "edit deny glob blocks"

echo "test_claude_sync: legacy guard shim removed"
if [ ! -e "$REPO_ROOT/claude/hooks/eos_guard.py" ]; then ok "old guard path is gone"; else no "old guard path is gone"; fi
expect_missing "agents never reference the old guard path" "EngineeringOS/claude/hooks" "$(cat "$C"/agents/*.md)"

echo "test_claude_sync: health when Claude Code is not installed"
out="$(HOME="$TMP/nohome" PATH="/usr/bin:/bin" python3 "$REPO_ROOT/scripts/eos_sync.py" health --target claude --engine "$REPO_ROOT" --data "$TMP/data" 2>&1 || true)"
expect_contains "reports not installed" "Claude Code: not installed" "$out"

echo
echo "test_claude_sync: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
