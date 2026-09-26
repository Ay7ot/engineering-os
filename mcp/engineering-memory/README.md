# engineering-memory MCP server

Stdlib-only Python MCP server over stdio (newline-delimited JSON-RPC). No pip dependencies.

Exposes the EngineeringOS **data** directory (knowledge, decisions, research,
projects, tasks) and a SQLite + FTS5 index over it.

## Data directory resolution (first match wins)

1. `$ENGINEERING_OS_DATA`
2. `<repo>/data` — i.e. next to this server's repo root (default)

Your data is intentionally kept out of this public repo. See the top-level
`README.md` for the public-engine / private-data split.

## Run

```sh
python3 server.py
```

## Test

```sh
printf '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}\n' | ENGINEERING_OS_DATA=~/EngineeringOS/data python3 server.py
```

## Tools

`search_knowledge`, `get_project_context`, `get_project_state`, `update_project_state`,
`search_decisions`, `get_decision`, `record_decision`, `search_research`,
`get_research`, `record_research`, `get_active_tasks`, `record_task`, `update_task`.

DB: `<data>/memory/engineering_memory.db` (auto-created; FTS5 when available,
falls back to `LIKE`).
