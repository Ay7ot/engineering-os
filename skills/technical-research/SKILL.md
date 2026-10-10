---
name: technical-research
description: Research libraries, frameworks, technologies, standards, and implementation options using primary sources, cross-checked across several of them and cited. Use when investigating unfamiliar technology, evaluating a tool, comparing approaches, or writing a research report.
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
5. **Split broad questions.** Break the question into 3 to 6 sub-questions
   (capabilities, limits, cost, security, migration, alternatives) and research
   each separately. Independent sub-questions can be researched in parallel.
6. **Cross-check.** Every important claim needs either one primary source or two
   independent secondary ones. When sources disagree, record both, prefer the
   newer and more authoritative one, and say why.
7. **Check freshness.** Note each source's date or version. Treat anything older
   than the version in use, or older than about a year for fast-moving tools, as
   suspect until confirmed.
8. **Synthesize, do not stack.** Write findings per sub-question, then one
   recommendation that weighs them. Do not paste source text; summarize in your
   own words and quote only short fragments when the exact wording matters.

## Output structure
- Question
- Findings (evidence-based, cited)
- Recommendation
- Alternatives
- Confidence (high/medium/low + why)
- Unresolved questions
- Sources (title, URL or path, date/version, what it supported)

## Rules
- Do not invent APIs, versions, or configuration formats. Verify against primary sources.
- Cite sources next to the claims they support. Distinguish fact from inference.
- Never cite a source you did not actually read.
- If evidence is weak, say so with low confidence.
- Persist reusable findings via `record_research`.

## Checklist
- [ ] Checked EngineeringOS for prior work
- [ ] Consulted primary sources
- [ ] Version verified against project manifest
- [ ] Risks/limitations identified
- [ ] Broad question split into sub-questions
- [ ] Key claims cross-checked; disagreements recorded
- [ ] Source dates/versions noted
- [ ] Sources cited next to claims
- [ ] Recommendation with confidence
- [ ] Persisted if reusable