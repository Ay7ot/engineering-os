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
