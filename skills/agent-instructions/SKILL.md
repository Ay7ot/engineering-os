---
name: agent-instructions
description: Audit and improve a project's agent-instruction file (AGENTS.md or an editor's equivalent) so agents get accurate, actionable context. Use when asked to check, audit, update or fix AGENTS.md, or when project context has gone stale. Writing project docs generally is `documentation`.
metadata:
  audience: lead, builder
  upstream: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-md-management/skills/claude-md-improver
  license: Apache-2.0
---
# Agent Instructions

## When to use
- A repository has an agent-instruction file and it may be stale, thin, or
  wrong.
- An agent behaves oddly because a command, path, or convention changed.
- Onboarding a repository that has no instruction file yet.
- A periodic pass to keep project context accurate.

This covers the agent-instruction file only. For documentation in general
(README, ADRs, runbooks), use `documentation`.

## Which files to audit
The same rules apply to every kind:

| Kind | Typical location | Purpose |
|---|---|---|
| Project instruction file | repository root, for example AGENTS.md | Shared context every agent reads, checked in |
| Local override | an untracked per-developer file alongside it | Personal settings, never committed |
| Nested file | a package or subdirectory | Module or domain-specific context |

Treat an editor's own file name for the shared file as the same artefact and
keep the content portable. Find candidates with `glob` (`**/AGENTS.md`) or
`grep`, then confirm which file is authoritative before editing.

## Phase 1: discovery
- Find every instruction file, root first then nested packages (`glob`).
- Record each file's kind, path, and last change (`bash`:
  `git log -1 --format=%cs -- <path>`), and note tracked versus local overrides.

## Phase 2: assess against the rubric
100 points total; detail in `references/quality-criteria.md`.
- Commands and workflows (20): build, test, dev, lint, deploy present and
  correct.
- Architecture clarity (20): structure, entry points, config an agent can find.
- Non-obvious patterns (15): gotchas and quirks captured.
- Conciseness (15): no verbose explanation, no restating obvious code.
- Currency (15): matches the current codebase.
- Actionability (15): executable instructions, not vague ones.

Grades: A 90 to 100 comprehensive and current; B 70 to 89 good with gaps;
C 50 to 69 basic, missing key sections; D 30 to 49 sparse or outdated;
F 0 to 29 missing or severely outdated.

## Phase 3: report before editing
Always present the report first, then wait for approval.
- Summary: files found, average score, files needing work.
- Per file: path and kind, score and grade, per-criterion notes, specific
  issues, recommended additions.
- Verify while assessing: run the documented commands, confirm cited paths.

## Phase 4: targeted updates
- Propose additions only: a command found during analysis, a gotcha in the code,
  an unclear package relationship, a working test approach, a config quirk.
- Avoid restating the obvious, generic best practice, one-off fixes, and long
  prose where a line will do.
- Show each change as a diff, with the file and a one-line reason (for example
  "build command was missing").
- Apply with `edit` only after approval, preserving the existing structure.

## What a good file contains
Concise and human-readable, with copy-pasteable commands, project-specific
patterns rather than generic advice, and non-obvious gotchas.
Sections where relevant: commands, architecture, key files, code style,
environment, testing, gotchas, workflow. Templates: `references/templates.md`.

## Common issues to flag
- Stale build or test commands that no longer work.
- Missing required tools, environment variables, or setup steps.
- Architecture or directory structure that has changed.
- Undocumented gotchas that agents keep tripping on.
- Two instruction files that contradict each other.

## Checklist
- [ ] All instruction files located, kinds and owners known
- [ ] Each scored against the rubric, with claims checked by running commands
- [ ] Report presented and approval obtained before any edit
- [ ] Changes are targeted additions, shown as diffs with a reason
- [ ] No editor-specific names or paths introduced; content stays portable
- [ ] Existing structure preserved; the file stays concise and current
