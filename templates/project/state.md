# <project> — State

Append-only log of meaningful project state changes (newest ideas on top or
bottom — be consistent). The `engineering-memory` MCP `update_project_state`
tool appends here and mirrors a row into the DB.

## <ISO timestamp> UTC
What changed, what's in flight, what's blocked, and the next action.
