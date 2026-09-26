# Keep read-only agent lockdown, fix prompts instead of permissions

Date: 2026-09-10T02:05:46+00:00
Project: global

## Context
Architect subagent was failing with Shell/permission-denied errors: its frontmatter sets bash *: deny except git log *, edit: deny, task: deny — but its prompt told it to write architecture docs and models defaulted to bash for exploration. Same class of contradiction existed in planner (bash deny + eng worktree new instruction) and explorer (narrow git-only bash allowlist, no guidance to prefer glob/read/grep).

## Decision
Keep strict lockdown (Option A): leave all permission blocks unchanged; add explicit TOOL RESTRICTIONS discipline sections to architect.md (use read/glob/grep/list, never bash except git log; never Write/Edit, return doc as response + persist via record_decision MCP; no task delegation), planner.md (never run shell incl. eng worktree new — specify commands for lead/builder), explorer.md (bash only for listed git read-only cmds; use native tools otherwise).

## Alternatives
B: loosen architect bash to allow safe read-only commands (ls/cat/find/git *). C: both prompt fix + loosened bash + docs-path writes.
