---
name: technical-research
description: Research libraries, frameworks, technologies, standards, and implementation options using primary sources. Use when investigating unfamiliar technology, evaluating a tool, or comparing approaches.
metadata:
  audience: researcher, lead
---
# Technical Research

## When to use
- Investigating an unfamiliar library/framework/technology.
- Evaluating tools or approaches for a decision.
- Verifying APIs, versions, or configuration formats against current docs.

## Procedure
1. Search EngineeringOS knowledge/decisions/research first (`engineering-memory` MCP). Do not redo prior work.
2. Prefer primary sources in this order:
   - Official documentation
   - Official source code / first-party repos
   - RFCs / standards documents
   - Well-maintained community references
3. Verify version compatibility: the exact version in use (check package manifests), not the latest docs.
4. Look for: API shape, configuration format, breaking changes, maintenance status, known issues, security posture, license, operational complexity.

## Output structure
- Question
- Findings (evidence-based, cited)
- Recommendation
- Alternatives
- Confidence (high/medium/low + why)
- Unresolved questions
- Sources

## Rules
- Do not invent APIs, versions, or configuration formats. Verify against primary sources.
- Cite sources. Distinguish fact from inference.
- If evidence is weak, say so with low confidence.
- Persist reusable findings via `record_research`.

## Checklist
- [ ] Checked EngineeringOS for prior work
- [ ] Consulted primary sources
- [ ] Version verified against project manifest
- [ ] Risks/limitations identified
- [ ] Sources cited
- [ ] Recommendation with confidence
- [ ] Persisted if reusable