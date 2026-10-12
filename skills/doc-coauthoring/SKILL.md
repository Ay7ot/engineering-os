---
name: doc-coauthoring
description: Guide a structured co-authoring workflow for a document: gather context, build it section by section, then test it on a fresh reader. Use when writing a proposal, spec, PRD or decision doc with the user; not for README or AGENTS.md upkeep (`documentation`).
metadata:
  audience: lead, architect
  upstream: https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring
  license: Apache-2.0
---
# Doc Co-Authoring

## When to use
- The user wants to write a substantial document and will iterate on it: proposal, technical spec, PRD, RFC, decision doc.
- The user says "write a doc", "draft a proposal" or "create a spec".
- The document must land with readers who have none of this session's context.

Not for README, AGENTS.md, ADR or runbook upkeep, which follow house structure (`documentation`). Offer this workflow for open-ended docs; if the user declines, work freeform.

## Stage 1: Gather context
Goal: close the gap between what the user knows and what you know.
1. Ask five meta questions: document type, primary audience, intended impact on the reader, any template or format, other constraints.
2. If they name a template or doc type, ask for it and `read` the file or fetch the link.
3. For an existing shared doc, `read` its current state and check images for alt text; report anything missing so the user can supply a description.
4. Ask for a free-form dump: background, related discussions, rejected alternatives, org context, timeline pressure, architecture, stakeholder concerns. Tell them not to organise it.
5. `read` anything they point at (channels, threads, docs) and pull it in.
6. When the dump ends, ask 5 to 10 numbered clarifying questions from the gaps. Short answers and shorthand are fine.
Exit when you can ask about edge cases and trade-offs without re-explaining basics. Ask whether to add more context or start drafting.

## Stage 2: Build it section by section
1. Agree the structure. If the user does not know it, propose 3 to 5 sections for the doc type and confirm.
2. `write` the file with every section header and a placeholder such as "[To be written]". Name it for the doc, for example decision-doc.md or technical-spec.md.
3. Start with the section with the most unknowns (the core proposal for a decision doc, the technical approach for a spec). Leave any summary for last.
4. For each section, run five steps:
   - ask 5 to 10 clarifying questions about what belongs in it;
   - brainstorm 5 to 20 candidate points, including forgotten context and angles the user missed;
   - ask what to keep, remove or combine, each with a short reason, to learn their priorities;
   - gap check: what is still missing;
   - `edit` the placeholder into the drafted section.
5. Ask the user to describe changes rather than edit the file themselves, so you learn their style ("make the third paragraph more concise").
6. Iterate with `edit` on the specific passage; never reprint the whole document. If the user edits the file directly, `read` it back and keep their choices in mind.
7. After 3 iterations with no substantial change, ask what can be removed without losing information.

## Stage 3: Test on a fresh reader
Goal: catch what makes sense to the author but confuses others.
1. Predict 5 to 10 questions a reader would ask while trying to find or use the document.
2. Answer them with a context-free reader: spawn a `task` that sees only the document and one question, or ask the user to paste the doc into a fresh session.
3. Also ask the reader: what is ambiguous, what context the doc assumes, and whether anything contradicts itself.
4. Record what the reader got right and wrong, fix the sections that failed, then re-test those questions.
Exit when the reader answers consistently and surfaces no new ambiguity. See references/reader-testing.md.

## Near completion
At about 80% of sections, `read` the whole document and check flow, redundancy, contradictions, filler, and whether every sentence carries weight.

## Final review
- Ask the user for their own final read: they own the document.
- Ask them to re-check facts, links and technical details.
- Suggest appendices for depth without bloating the body, and updating the doc as real readers respond.

## Checklist
- [ ] Document type, audience and intended impact stated
- [ ] Context gathered; 5 to 10 clarifying questions asked
- [ ] Structure agreed; scaffold written with placeholders
- [ ] Section with the most unknowns drafted first
- [ ] Each section brainstormed, curated and iterated
- [ ] Tested with a context-free reader; failing sections fixed
- [ ] Facts, links and technical details verified by the user
