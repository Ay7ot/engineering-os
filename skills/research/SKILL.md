---
name: research
description: Investigate a question against primary sources and capture the findings as a Markdown note in the repo. Use when asked to research a topic, gather docs or API facts, or delegate reading legwork to a background agent.
metadata:
  audience: researcher, lead
  upstream: https://github.com/mattpocock/skills/tree/main/skills/engineering/research
  license: MIT
---
# Research

## When to use
- A question must be investigated before you can answer, plan or decide.
- The reading is legwork: docs, API references, source code, specs, changelogs.
- The findings should outlive the session as a file in the repo, not just a chat reply.

This is investigative work captured as a repo Markdown note. For a heavier evaluation that cross-checks several primary sources and cites each claim, use `technical-research`; this note is lighter, faster, and can feed it.

## Procedure
1. Restate the question in one line, and list what a good answer must cover.
2. Check for prior work first: search EngineeringOS (`engineering-memory` MCP) and `grep` the repo for existing notes on the topic. Do not redo what exists.
3. Delegate the reading when it can run alongside other work: spawn a `task` with the question, the primary sources to start from, and where to write the note. Keep working while it reads.
4. Investigate against primary sources: official docs, first-party APIs, source code, specs, changelogs. Follow each claim back to the source that owns it, not a second-hand summary.
5. Capture every claim with its source: title, URL or path, and version or date.
6. Write the findings to a single Markdown file.

## Where to put the note
- Match the convention the repo already uses for such notes. `glob` and `grep` for research, notes or docs directories before choosing a path.
- If there is no convention, pick a sensible path, for example docs/research/<topic>.md, and say where you put it.
- One topic per file; keep each note self-contained.

## Note structure
- Question
- Answer (short, up front)
- Findings, each with its source
- Open questions and anything unverified
- Sources list

## Rules
- Prefer primary over secondary sources. If only secondary ones exist, say so.
- Cite next to the claim. Never cite a source you did not read.
- Mark anything you could not verify as unverified rather than asserting it.
- Separate what the source says from what you infer.
- Do not pad the note; the answer and its evidence are the point.

## Checklist
- [ ] Question restated; prior work checked
- [ ] Reading delegated to a background `task` when it could run in parallel
- [ ] Claims traced to primary sources
- [ ] Every claim carries its source and a version or date
- [ ] Note saved to a conventional path, and its location reported
- [ ] Unverified items marked, not asserted
