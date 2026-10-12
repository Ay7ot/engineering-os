---
name: to-issues
description: Break a plan, spec or PRD into independently grabbable issues that each cut a complete vertical slice end to end. Use when turning approved scope into tracker issues. Not for the phase and dependency breakdown, which `project-planning` covers.
metadata:
  audience: planner, lead
  upstream: https://github.com/mattpocock/skills/tree/main/skills/engineering/to-tickets
  license: MIT
---
# To Issues

Break a plan into independently grabbable issues using vertical slices (tracer
bullets), and publish them to the issue tracker.

## When to use
- A plan, spec or PRD is approved and must become tracker issues.
- The work should be grabbable by several agents at once.

## Process
### 1. Gather context
Work from what is already in the session. If an issue reference (number, URL or
path) was passed, fetch it and `read` the full body and comments.

### 2. Explore the codebase if not already done
Understand the current state so titles and descriptions use the domain glossary
and respect ADRs in the area. Look for prefactoring that makes the change easier:
make the change easy, then make the easy change.

### 3. Draft vertical slices
Each issue is a thin vertical slice through ALL integration layers end to end
(schema, API, UI, tests), never a horizontal slice of one layer.
- Each slice delivers a narrow but COMPLETE path through every layer.
- A completed slice is demoable or verifiable on its own.
- Any prefactoring is done first.

### 4. Quiz the user
Present the breakdown as a numbered list. For each slice show the title, what
blocks it, and the user stories it covers (if the source has them). Ask whether
the granularity is right (too coarse or too fine), whether dependency
relationships are correct, and whether any slice should be merged or split.
Iterate until the user approves.

### 5. Publish in dependency order
Publish each approved slice as a new issue, blockers first so you can reference
real issue identifiers, with the ready-for-agent triage label unless told
otherwise. Where the tracker supports it, link each slice to its parent as a
native sub-issue and wire each blocker as a native blocking edge; the body
sections below are the fallback. Do not close or modify the parent issue.

## Issue template
- **Parent**: a reference to the parent issue, omitted when the source was not
  itself an issue.
- **What to build**: the end-to-end behaviour of this slice, not layer-by-layer
  implementation. Avoid file paths and code snippets, which go stale. Exception:
  point at where prototype code lives when it encodes a decision more precisely
  than prose can (state machine, reducer, schema, type shape).
- **Acceptance criteria**: a checklist of verifiable criteria.
- **Blocked by**: the blocking ticket, or "None - can start immediately".

## Checklist
- [ ] Each slice cuts every layer and is verifiable on its own
- [ ] Prefactoring slices ordered first
- [ ] Breakdown, granularity and dependencies approved by the user
- [ ] Issues published in dependency order with correct labels
- [ ] Parent issue left untouched
