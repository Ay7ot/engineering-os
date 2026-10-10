---
name: memory-hygiene
description: Audit and tidy EngineeringOS memory, finding duplicate or contradictory ADRs, superseded decisions, stale project state and dead tasks, then correct the record through the engineering-memory tools. Use periodically, after a big refactor, or when memory search returns conflicting answers.
metadata:
  audience: lead
---
# Memory Hygiene

## When to use
- Periodically (for example monthly) or after a large refactor or migration.
- When `search_decisions` / `search_knowledge` return answers that contradict
  each other or the code.
- Before a new contributor or agent relies on a project's memory.

## What the tools can and cannot do
- **Append only.** The `engineering-memory` server can add ADRs, research,
  state entries and tasks, and change a task's status. It cannot delete or edit
  existing ADRs, research or state history, and there is no "superseded" flag.
  Correct the record by adding to it.
- **Partial reads.** Every tool response is truncated (about 12,000 characters).
  `get_project_state` and `get_project_context` return `state.md` oldest-first,
  so on a long-lived project the newest entries are the part that gets cut.
  `get_project_context` lists only the 10 most recent decisions, and
  `search_decisions` is a plain text match without a project filter. For a full
  audit, also **read** the data directory directly (read-only). It is
  `$ENGINEERING_OS_DATA`, or `data/` inside the engine checkout if unset:
  `projects/<project>/state.md` (newest entries at the end) and
  `projects/<project>/decisions/`, plus `decisions/` for global ADRs.
- **Task details are replaced, not appended.** `update_task` with non-empty
  `details` overwrites the existing details.
- **Task status.** Use `done` to close a task. Some tools still list `cancelled`
  tasks as open, so do not rely on `cancelled` to hide one.
- **State status.** Always pass `status` to `update_project_state`; omitting it
  clears the stored status.
- **ADR titles.** `record_decision` names the file from the date and the first
  50 characters of the title, and overwrites an existing file with that name.
  Make the start of each title distinct (for example "Consolidated <topic>:
  ..."), not just the end.

Never hand-edit files under the data directory unless the operator asks for that
specific edit.

## Procedure
1. **Scope.** One project at a time, plus global decisions if asked.
2. **Gather.** `get_project_context`, `get_active_tasks` for the project, and the
   data-directory files above. Note your coverage (how many ADRs and state
   entries you actually read).
3. **Find problems:**
   - **Duplicates:** two ADRs deciding the same thing.
   - **Superseded:** an older ADR overruled by a newer one that does not say so.
   - **Contradicted by reality:** an ADR or state entry the current code, config
     or docs no longer match. Check the repo; do not assume.
   - **Stale state:** the newest state entry no longer describes the project.
   - **Dead tasks:** open tasks that are finished, abandoned or duplicated.
4. **Report first.** A table: item (id or path), problem, evidence, proposed
   fix, plus your coverage. Wait for the operator's OK before changing anything.
5. **Apply (after approval):**
   - Superseded or duplicate ADRs: `record_decision` one consolidating ADR with a
     distinct title that names each superseded ADR by id or path and states what
     is current.
   - Stale state: `update_project_state` with one consolidated "current state"
     entry and an explicit `status`.
   - Dead tasks: read the task's existing details first (`get_active_tasks`
     filtered to the project returns them; for long lists check the
     `tasks/` folder in the data directory), then `update_task` to `done` with
     `details` = existing details + a "Closed: <reason>" line.
6. **Verify.** Search again and confirm the consolidating ADR appears and names
   the superseded items (it may not rank first; file results are ranked by term
   matches). Confirm closed tasks no longer appear in `get_active_tasks`.

## Rules
- Evidence over memory: confirm against the repo before calling something stale.
- Append and close; never delete, never overwrite task details blindly.
- One consolidated entry beats many small corrections.
- No secrets or personal data in anything you record.
- If the same cleanup keeps being needed, record a follow-up for the engine (a
  supersede flag, a reindex, a project filter), not a workaround.

## Checklist
- [ ] Scope chosen; tools and data-directory files read; coverage noted
- [ ] Duplicates, superseded, contradicted, stale and dead items listed with evidence
- [ ] Report shown; approval obtained before changes
- [ ] Consolidating ADR (distinct title), state entry (with status), task closures (details preserved) applied
- [ ] Re-checked: consolidating ADR found, closed tasks gone from active list
