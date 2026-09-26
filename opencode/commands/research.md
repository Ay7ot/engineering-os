---
description: Run a technical research workflow, persist findings to EngineeringOS
agent: lead
subtask: false
---
Run the EngineeringOS research workflow. Research topic: $ARGUMENTS

## Steps
1. Read `~/EngineeringOS/PRINCIPLES.md`, `~/EngineeringOS/data/USER.md`, and the project `AGENTS.md` if present.
2. Search EngineeringOS first: use `engineering-memory` MCP (`search_knowledge`, `search_research`, `search_decisions`, `get_project_context`) to check what is already known. Do not redo prior work.
3. Inspect the current architecture if the question concerns the project (explorer agent, only if not already mapped this session).
4. Research with the researcher agent: official documentation, library/framework docs, GitHub, standards/RFCs, implementation comparisons, benchmarks where useful. Prioritize primary sources.
5. Identify alternatives, operational complexity, cost, scalability, risks and limitations.
6. Recommend an approach with confidence and explicit reasoning.
7. Persist useful research to EngineeringOS via `record_research` (question, findings, recommendation, sources, project when applicable).
8. Report: the question, findings, recommendation, alternatives, confidence, unresolved questions, sources, and what was persisted.

## Output
Concise report with evidence and sources. Flag any decisions that require the user's judgment (e.g., cost, operational, product implications).