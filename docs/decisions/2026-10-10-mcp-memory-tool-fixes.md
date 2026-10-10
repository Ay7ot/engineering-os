# ADR: engineering-memory tool fixes for open tasks, task details, state status and long state

- **Date:** 2026-10-10
- **Status:** Accepted
- **Deciders:** Operator (Ay7ot)
- **Project:** engineering-os
- **Builds on:** the `memory-hygiene` skill (PR #8), whose review found these
  rough edges and documented workarounds for them

## Context

Four behaviours in `mcp/engineering-memory/server.py` made memory upkeep
error-prone:

1. `get_project_context` and `get_project_state` listed tasks with
   `status != 'done'`, so `cancelled` tasks showed as open, while
   `get_active_tasks` already excluded both.
2. `update_task` replaced `details` whenever a non-empty value was passed. The
   only way to add a closing note was to read the old details and resend them.
3. `update_project_state` without `status` wrote an empty status to the DB,
   silently clearing the previous one.
4. Every response is cut at 12,000 characters of JSON. `state.md` is
   append-only (newest last), so on a long project the newest entries, the
   ones that matter, were cut, and the JSON itself was left invalid.

## Decision

1. Both tools use the same open-task filter as `get_active_tasks`:
   `status NOT IN ('done','cancelled')`.
2. `update_task` gains an optional `append_details` input that adds a newline
   plus the text to the existing details (no leading blank line when details
   are empty). `details` keeps its replace behaviour. Passing both is an error
   so the caller's intent is never guessed.
3. `update_project_state` keeps the stored status when `status` is omitted or
   empty (`COALESCE(NULLIF(excluded.status,''), project_state.status)`). A new
   project without a status still stores an empty status.
4. When the whole result would exceed the cap, `get_project_state` and
   `get_project_context` trim `state.md` from the front at an entry boundary
   (`## <timestamp>` heading), prefix a note pointing at the full file, and add
   `state_truncated: true` and `state_omitted_chars`. The response stays valid
   JSON within the cap. Short state is returned unchanged with no new fields.

No file formats or DB schema change. Existing callers see the same fields;
the new fields only appear on truncation.

## Verification

`tests/test_mcp.sh` adds checks for each fix (cancelled hidden in all three
task lists; append, replace, no-op and both-at-once for `update_task`; status
kept, updated and empty-for-new for `update_project_state`; newest entries kept,
entry boundary, valid JSON within the cap, and short state untouched). The same
checks fail against the previous server (14 failures), so they detect the old
behaviour.

## Alternatives

- `details_mode: "append"` flag on `update_task`: works, but one field with two
  meanings is easier to misuse than a separately named input.
- Raising the 12,000-character cap: postpones the problem and grows every
  response in the client's context.
- Returning state newest-first: changes the file's meaning and breaks readers
  that expect chronological order.

## Consequences

- Passing `status: ""` no longer clears a project's status. There is no way to
  clear it through the tool now; set a meaningful status instead.
- Older state history is only in the file once truncation kicks in; audits
  still read `projects/<project>/state.md` directly.
