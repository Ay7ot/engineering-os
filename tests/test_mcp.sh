#!/usr/bin/env bash
# Tests for the engineering-memory MCP server. Hermetic: uses a temp data dir.
# Run: bash tests/test_mcp.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER="$REPO_ROOT/mcp/engineering-memory/server.py"

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

echo "test_mcp: syntax"
if python3 -m py_compile "$SERVER"; then ok "server.py compiles"; else no "server.py compiles"; fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export ENGINEERING_OS_DATA="$TMP/data"

# Send a sequence of newline-delimited JSON-RPC requests, collect the responses.
rpc() { # stdin lines -> stdout
  ENGINEERING_OS_DATA="$TMP/data" python3 "$SERVER"
}

out="$(
  {
    printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0"}}}'
    printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
  } | rpc
)"

expect_contains "initialize returns serverInfo" '"serverInfo"' "$out"
expect_contains "initialize names the server" '"engineering-memory"' "$out"
expect_contains "tools/list returns search_knowledge" '"search_knowledge"' "$out"
expect_contains "tools/list returns record_decision" '"record_decision"' "$out"
expect_contains "tools/list returns update_project_state" '"update_project_state"' "$out"

# record_decision -> get_decision round trip
out="$(
  {
    printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
    printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"record_decision","arguments":{"title":"Test ADR","decision":"Do the thing","context":"ctx"}}}'
  } | rpc
)"
expect_contains "record_decision returns an id" '"id"' "$out"
expect_contains "record_decision writes a path" 'decisions/' "$out"

if [ -f "$TMP/data/memory/engineering_memory.db" ]; then
  ok "SQLite db auto-created"
else
  no "SQLite db auto-created"
fi

# record_task -> get_active_tasks round trip
out="$(
  {
    printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
    printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"record_task","arguments":{"title":"Test task","project":"demo"}}}'
    printf '%s\n' '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_active_tasks","arguments":{"project":"demo"}}}'
  } | rpc
)"
expect_contains "record_task returns a task id" '"id": 1' "$out"
expect_contains "record_task persists the title" 'Test task' "$out"

# update_project_state creates project files
out="$(
  {
    printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
    printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"update_project_state","arguments":{"project":"demo","state":"hello","status":"active"}}}'
  } | rpc
)"
expect_contains "update_project_state succeeds" 'state.md' "$out"
for f in context.md architecture.md state.md; do
  if [ -f "$TMP/data/projects/demo/$f" ]; then ok "project file created: $f"; else no "project file created: $f"; fi
done

# `tool_json <id>` reads rpc output on stdin and prints the decoded tool result
# of the response with that id (or the raw response if it is an error).
tool_json() {
  python3 -c 'import json,sys
for line in sys.stdin:
    r = json.loads(line)
    if r.get("id") == int(sys.argv[1]):
        try:
            print(json.dumps(json.loads(r["result"]["content"][0]["text"]) if "result" in r else r))
        except ValueError:
            print("{}")  # truncated/invalid payload: the check that follows fails' "$1"
}
call() { # $1 id, $2 tool, $3 arguments JSON
  printf '{"jsonrpc":"2.0","id":%s,"method":"tools/call","params":{"name":"%s","arguments":%s}}\n' "$1" "$2" "$3"
}
check_py() { # $1 desc, $2 python expression over `d`, $3 JSON (not piped: counters must survive)
  if python3 -c 'import json,sys; d=json.loads(sys.argv[2]); sys.exit(0 if eval(sys.argv[1]) else 1)' "$2" "$3" 2>/dev/null
  then ok "$1"; else no "$1"; fi
}

echo "test_mcp: cancelled tasks are not open"
mkdir -p "$TMP/data-tasks/projects/demo"
in="$(
  call 1 record_task '{"title":"Keep me","project":"demo"}'
  call 2 record_task '{"title":"Cancel me","project":"demo"}'
  call 3 record_task '{"title":"Finish me","project":"demo"}'
  call 4 update_task '{"id":2,"status":"cancelled"}'
  call 5 update_task '{"id":3,"status":"done"}'
)"
printf '%s\n' "$in" | ENGINEERING_OS_DATA="$TMP/data-tasks" python3 "$SERVER" >/dev/null
for tool in get_project_context get_project_state get_active_tasks; do
  key=open_tasks; [ "$tool" = get_active_tasks ] && key=tasks
  j="$(call 9 "$tool" '{"project":"demo"}' | ENGINEERING_OS_DATA="$TMP/data-tasks" python3 "$SERVER" | tool_json 9)"
  check_py "$tool lists only the open task" "[t['title'] for t in d['$key']] == ['Keep me']" "$j"
done

echo "test_mcp: update_task details (replace vs append)"
out="$(
  {
    call 1 record_task '{"title":"T","project":"demo","details":"line one"}'
    call 2 update_task '{"id":1,"status":"open","append_details":"line two"}'
    call 3 update_task '{"id":1,"status":"done","append_details":"Closed: shipped"}'
  } | ENGINEERING_OS_DATA="$TMP/data-append" python3 "$SERVER"
)"
j="$(printf '%s\n' "$out" | tool_json 3)"
check_py "append_details appends on new lines" \
  "d['task']['details'] == 'line one\nline two\nClosed: shipped' and d['task']['status'] == 'done'" "$j"
out="$(
  {
    call 1 record_task '{"title":"Empty","project":"demo"}'
    call 2 update_task '{"id":1,"status":"open","append_details":"first"}'
    call 3 update_task '{"id":1,"status":"open","details":"replaced"}'
    call 4 update_task '{"id":1,"status":"open"}'
    call 5 update_task '{"id":1,"status":"open","details":"x","append_details":"y"}'
  } | ENGINEERING_OS_DATA="$TMP/data-append2" python3 "$SERVER" 2>/dev/null
)"
j="$(printf '%s\n' "$out" | tool_json 2)"
check_py "append_details on empty details adds no blank line" "d['task']['details'] == 'first'" "$j"
j="$(printf '%s\n' "$out" | tool_json 3)"
check_py "details still replaces (backward compatible)" "d['task']['details'] == 'replaced'" "$j"
j="$(printf '%s\n' "$out" | tool_json 4)"
check_py "no details keeps existing details" "d['task']['details'] == 'replaced'" "$j"
j="$(printf '%s\n' "$out" | tool_json 5)"
check_py "details + append_details together is rejected" "'error' in d" "$j"
j="$(call 1 update_task '{"id":1,"status":"open"}' | ENGINEERING_OS_DATA="$TMP/data-append2" python3 "$SERVER" | tool_json 1)"
check_py "rejected call changed nothing" "d['task']['details'] == 'replaced'" "$j"
j="$(printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | ENGINEERING_OS_DATA="$TMP/data-append2" python3 "$SERVER")"
check_py "update_task schema declares append_details" \
    "'append_details' in [t for t in d['result']['tools'] if t['name']=='update_task'][0]['inputSchema']['properties']" "$j"

echo "test_mcp: update_project_state keeps status when omitted"
out="$(
  {
    call 1 update_project_state '{"project":"demo","state":"one","status":"active"}'
    call 2 update_project_state '{"project":"demo","state":"two"}'
    call 3 get_project_state '{"project":"demo"}'
    call 4 update_project_state '{"project":"demo","state":"three","status":"paused"}'
    call 5 get_project_state '{"project":"demo"}'
  } | ENGINEERING_OS_DATA="$TMP/data-status" python3 "$SERVER"
)"
j="$(printf '%s\n' "$out" | tool_json 3)"
check_py "omitted status keeps previous status" "d['db']['status'] == 'active' and 'two' in d['db']['state']" "$j"
j="$(printf '%s\n' "$out" | tool_json 5)"
check_py "explicit status still updates" "d['db']['status'] == 'paused'" "$j"
call 1 update_project_state '{"project":"fresh","state":"hi"}' | ENGINEERING_OS_DATA="$TMP/data-status" python3 "$SERVER" >/dev/null
j="$(call 1 get_project_state '{"project":"fresh"}' | ENGINEERING_OS_DATA="$TMP/data-status" python3 "$SERVER" | tool_json 1)"
check_py "new project without status stores empty status" "d['db']['status'] == ''" "$j"

echo "test_mcp: long state.md returns the newest entries"
D="$TMP/data-long"
mkdir -p "$D/projects/demo"
python3 - "$D/projects/demo/state.md" <<'PY'
import sys
parts = ["# demo — State\n"]
for i in range(400):
    parts.append(f'\n## 2026-01-01T00:00:{i:03d} UTC\nentry {i:03d} "quoted" detail text padding padding padding\n')
open(sys.argv[1], "w", encoding="utf-8").write("".join(parts))
PY
echo "# demo — Context" > "$D/projects/demo/context.md"
for tool in get_project_state get_project_context; do
  key=state_file; [ "$tool" = get_project_context ] && key=state
  raw="$(call 1 "$tool" '{"project":"demo"}' | ENGINEERING_OS_DATA="$D" python3 "$SERVER")"
  printf '%s\n' "$raw" | python3 -c 'import json,sys; t=json.loads(sys.stdin.readline())["result"]["content"][0]["text"]; json.loads(t); assert len(t) <= 12000' \
    && ok "$tool: response is complete JSON within the limit" || no "$tool: response is complete JSON within the limit"
  j="$(printf '%s\n' "$raw" | tool_json 1)"
  check_py "$tool: newest entry kept, oldest dropped, flagged" \
    "'entry 399' in d['$key'] and 'entry 000' not in d['$key'] and d['state_truncated'] is True and d['state_omitted_chars'] > 0" "$j"
  check_py "$tool: cut lands on an entry boundary" \
    "d['$key'].split(chr(10), 1)[1].startswith('## ')" "$j"
done
j="$(call 1 get_project_state '{"project":"demo"}' | ENGINEERING_OS_DATA="$TMP/data-status" python3 "$SERVER" | tool_json 1)"
check_py "short state.md is returned untouched" "'state_truncated' not in d and d['state_file'].startswith('# demo')" "$j"

# Unknown tool must return an error, not crash the process.
out="$(
  {
    printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
    printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"does_not_exist","arguments":{}}}'
  } | rpc 2>&1 || true
)"
expect_contains "unknown tool returns an error" '"error"' "$out"

echo
echo "test_mcp: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
