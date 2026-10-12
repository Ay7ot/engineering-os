---
name: to-prd
description: Turn the current conversation and codebase knowledge into a PRD, then publish it to the issue tracker. Use when asked to create a PRD from context already in the session. Not for architecture proposals or implementation plans.
metadata:
  audience: planner, lead
  upstream: https://github.com/mattpocock/skills
  license: MIT
---
# To PRD

## When to use
- The session already holds enough context (conversation, codebase, prototype)
  to write a PRD, and the user asks for one.
- The PRD should be published to the issue tracker, not just drafted locally.

If the idea is still being shaped, use `brainstorming` first. A PRD states the
problem, solution and decisions; it is not an architecture proposal nor a task
plan (`project-planning` covers the plan).

## Rules
- Do NOT interview the user. Synthesise what is already known; ask only when a
  blocking decision is unresolved.
- Explore the repo first if you have not: `glob` and `grep` the area, `read` the
  module entry points, and respect ADRs in the area you touch.
- Use the project's domain glossary vocabulary throughout. Sketch the seams where
  the feature will be tested: prefer existing seams, use the highest seam
  possible, and propose new seams at the highest point you can. Confirm the
  seams with the user before publishing.
- Include no file paths or code snippets: they go stale. Exception: a prototype
  snippet that encodes a decision more precisely than prose (state machine,
  reducer, schema, type shape) may be inlined, noted as coming from a prototype,
  and trimmed to the decision-rich parts rather than a working demo.

## PRD template
- **Problem Statement**: the problem from the user's perspective.
- **Solution**: the solution from the user's perspective.
- **User Stories**: a long numbered list, "As an <actor>, I want a <feature>, so
  that <benefit>", covering all aspects of the feature.
- **Implementation Decisions**: modules built or modified, their interfaces,
  technical clarifications, architectural decisions, schema changes, API
  contracts, specific interactions.
- **Testing Decisions**: what makes a good test (external behaviour only, not
  implementation details), which modules are tested, prior art in the codebase.
- **Out of Scope**, then **Further Notes**.

## Publish
Publish to the issue tracker, then apply the ready-for-agent triage label: no
further triage is needed. Anything not agent-ready goes through `triage` first.

## Checklist
- [ ] Repo explored; domain glossary and ADRs honoured
- [ ] Test seams chosen at the highest point and confirmed with the user
- [ ] Problem, solution and user stories cover the whole feature
- [ ] Implementation and testing decisions recorded, with no stale file paths
- [ ] Out of scope listed
- [ ] Published to the issue tracker with the ready-for-agent label
