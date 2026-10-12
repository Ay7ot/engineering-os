---
name: loop-me
description: Grill the user one round of questions at a time to turn a recurring loop in their life or work into a written workflow spec an implementer can build. Use when asked to design or spec a repeating workflow, or to find loops worth delegating.
metadata:
  audience: lead, architect
  upstream: https://github.com/mattpocock/skills/tree/main/skills/in-progress/loop-me
  license: MIT
---
# Loop Me

Run a grilling session whose only output is workflow specs. Relentless, a round
of questions at a time, with a recommended answer attached to every question.
Create, edit and delete specs as the grilling resolves things.

## When to use
- The user wants to design a recurring workflow.
- The user asks which parts of their week could be delegated.
- A workflow exists but its spec has open questions an implementer would trip on.

For exploring an unfamiliar problem before committing, use `brainstorming`. For
sequencing the work once the spec is settled, use `project-planning`.

## The loop lens
A loop is a recurring pattern in the user's life: their career, their week,
their morning, one repeated activity. Seeing a life as loops within loops shows
how predictable its activities are, which is exactly what makes them worth
delegating. Use the lens to find loops worth specifying, and propose loops the
user has not noticed.

A workflow is the spec of one loop made real. The user runs a workflow on a
loop; the loop is its running instance.

## Vocabulary
A shared language, reached for only when a workflow calls for it. Mandate
nothing structural: a workflow needs no AI, no checkpoint and no schedule
unless the grilling shows it does.

- Trigger: what fires each run, an event (a new email, a new issue) or a
  schedule (every morning). Event triggers are usually more efficient.
- Checkpoint: the point where the user is asked to verify or decide. Some
  workflows have none and run autonomously; some use no AI at all.
- Push right: defer the checkpoint as far as it will go, so the human is asked
  once, late, with all the work already prepared.
- Brief: what a checkpoint presents. A tight, decision-ready summary of what was
  produced, why, and a link down to the asset itself. Never the raw output. The
  user reads a brief, not a draft; review speed is the point.

## The workspace
- `workflows/*.md`: one spec per workflow, and the source of truth.
- `NOTES.md`: raw notes on the user's world, the tools and channels they
  process, and their own terminology for both. When it is empty or thin,
  interview them about their world before specifying anything. Sharpen fuzzy
  terms into canonical ones as they surface and record them here.

## The grilling method
1. Ask one round of questions, not one question at a time and not a wall.
2. Attach a recommended answer to each question so the user can agree fast.
3. When an answer settles something, write it into the spec immediately.
4. If two answers conflict, surface the conflict before moving on.
5. Keep going while any question remains. A question the user cannot answer is
   either out of scope (delete it) or research (answer it, then continue).

## Definition of done
A workflow spec is done when an implementer agent could build it without asking
a single question. Nothing is done while a question remains.

## Checklist
- [ ] The loop is named and its recurrence stated
- [ ] Trigger defined: event or schedule
- [ ] Checkpoints listed, each pushed as far right as it will go
- [ ] Each checkpoint has a brief format, not raw output
- [ ] No structural element added that the grilling did not justify
- [ ] `workflows/*.md` updated, and `NOTES.md` holds the shared terms
- [ ] No open question remains
