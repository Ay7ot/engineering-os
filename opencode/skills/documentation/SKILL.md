---
name: documentation
description: Write clear, accurate, maintainable project and system documentation (README, AGENTS.md, ADRs, runbooks). Use when creating or updating docs.
metadata:
  audience: architect, builder, lead
---
# Documentation

## When to use
- Creating or improving AGENTS.md, README, architecture docs, ADRs, runbooks.
- Documenting decisions and operational procedures.

## Rules
- Document WHAT and WHY; code already says HOW. Avoid duplicating code as prose.
- Keep docs close to the code they describe; stale docs are worse than none.
- ADRs record the decision, context, alternatives considered, and consequences — not an essay.
- README: what it is, quickstart, dev setup, how to run tests, where to find more.
- AGENTS.md: project overview, stack, architecture, conventions, build/test/lint commands, entry points, and how to use EngineeringOS memory tools. Concise; agents read it every session.
- Use links over duplication (single source of truth).
- Dates and owners on operational docs; review periodically.
- Prefer concrete examples over vague instructions.

## Structure sketch — ADR
```
# ADR-NNN: Title
Date / Status / Deciders
## Context
## Decision
## Consequences (positive/negative)
## Alternatives considered
```

## Checklist
- [ ] Why explained, not just what
- [ ] Close to the code (paths cited)
- [ ] No stale or duplicate content
- [ ] README quickstart accurate
- [ ] AGENTS.md concise and current
- [ ] ADRs recorded for significant decisions
- [ ] Examples concrete