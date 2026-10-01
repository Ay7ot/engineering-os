---
name: architecture-analysis
description: Produce architecture analysis and proposals with explicit tradeoffs. Use when designing or evaluating a system, component, API, or significant change. Covers requirements, boundaries, alternatives, failure modes, security, scalability, observability, testing, and a recommendation with confidence.
metadata:
  audience: architect, lead
---
# Architecture Analysis

## When to use
- Designing a new system or significant component.
- Evaluating a proposed change with non-trivial tradeoffs.
- Before producing ADRs or implementation strategy.

## Procedure
1. Gather requirements: functional, non-functional (perf, reliability, security, cost, ops), and constraints (team, timeline, existing stack).
2. Map the current system: boundaries, data flow, data ownership, existing integrations, failure modes.
3. Identify alternatives BEFORE picking a recommendation. At least 2-3.
4. Score alternatives against the non-functional requirements, not vibes.

## Deliverable structure
- Problem
- Current system
- Requirements (functional / non-functional / constraints)
- Proposed architecture (components, boundaries, data flow, data ownership, APIs, failure modes) — with Mermaid diagrams (see the `diagrams` skill)
- Alternatives (with reasons rejected)
- Tradeoffs
- Failure modes
- Security considerations
- Scalability considerations
- Observability
- Testing strategy
- Migration strategy (if applicable)
- Recommendation
- Human decisions required (explicit list)

## Rules
- Explain WHY the recommendation fits THIS system. No "best practice" hand-waving.
- State confidence (high/medium/low) and evidence. Do not pretend certainty where evidence is weak.
- Separate fact from inference.
- Flag only decisions that genuinely need human judgment or carry significant consequences — not every technical detail.
- Be conservative: prefer proven patterns over novel ones unless evidence justifies novelty.
- Make structure and flow visible: a context/component diagram plus a sequence or data-flow diagram for the critical path (load the `diagrams` skill). A diagram must reflect the analysis — never invent nodes or edges.

## Example sketch
Bad: "Use Postgres because it's a best practice."
Good: "Use Postgres because we need transactional multi-row consistency across billing and inventory writes, already operate Postgres in prod, and the write volume (~50 rps) is far below its ceiling. SQLite would be simpler but can't give us row-level locking across a pool of API instances. Expected tradeoff: schema migrations become a review gate."

## Checklist
- [ ] Requirements explicit (functional + non-functional)
- [ ] Alternatives listed with reasons rejected
- [ ] Tradeoffs called out
- [ ] Failure modes identified
- [ ] Security reviewed (authN/Z, injection, exposure, least privilege)
- [ ] Scalability considered
- [ ] Observability planned
- [ ] Testing strategy defined
- [ ] Recommendation with reasoning + confidence
- [ ] Human decisions clearly separated from routine decisions