---
name: prototype
description: Build throwaway code that answers one design question, capture the answer, then delete or absorb it. Use when sanity-checking whether a state model or logic feels right, or exploring what a UI should look like before committing to a design.
metadata:
  audience: builder, architect
  upstream: https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype
  license: MIT
---
# Prototype

A prototype is throwaway code that answers a question. The question decides the
shape. It is not a spike to ship: it is deleted or absorbed.

## When to use
- "Does this logic or state model feel right?"
- "What should this look like?"
- The user wants a quick sanity check before committing to a design.

For a durable design artefact use `brainstorming`; for the implementation plan
use `writing-plans`.

## Pick the branch first
Getting this wrong wastes the whole prototype.
- **Logic / state model**: build a tiny interactive terminal app that pushes the
  state machine through the cases hard to reason about on paper. One command
  runs it, and cases are replayable from a scripted list.
- **UI**: generate several radically different variations on a single route,
  switchable through a URL search param and a floating bottom bar.

If the question is genuinely ambiguous and the user is unreachable, default to
the branch matching the surrounding code (backend module goes logic, page or
component goes UI) and state the assumption at the top of the prototype.

## Rules for both branches
1. Throwaway from day one and clearly marked. Put the code near the module or
   page it prototypes for, name it so a casual reader sees it is a prototype, and
   follow the project's existing routing convention for throwaway routes.
2. One command to run, using the project's existing task runner
   (`pnpm <name>`, `python <path>`, `bun <path>`): starting it must need no
   thought.
3. No persistence by default. State lives in memory, since persistence is the
   thing being checked, not a dependency. If the question involves a database,
   hit a scratch database or a file named to be wiped, for example one containing
   "PROTOTYPE, wipe me".
4. Skip the polish. No tests, no error handling beyond what makes it runnable,
   no abstractions.
5. Surface the state. After every action (logic) or variant switch (UI), print or
   render the full relevant state so the user sees what changed.
6. Delete or absorb when done. Fold the validated decision into the real code, or
   delete the prototype. Do not leave it rotting in the repo.

## Capture the answer
The answer is the only thing worth keeping. Record it durably (commit message,
ADR, issue, or a notes file next to the prototype) with the question it answered.
If the user is unavailable, leave a placeholder verdict to be filled in before
the prototype is deleted.

## Checklist
- [ ] Branch chosen from the question; assumption stated if it was ambiguous
- [ ] Marked throwaway, placed next to the code it prototypes for
- [ ] Runs with one command; no persistence unless the question is the database
- [ ] Full state surfaced after each action or variant switch
- [ ] Answer captured durably; prototype deleted or absorbed
