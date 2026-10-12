---
name: brainstorming
description: Turn a raw idea into an approved design through one question at a time, then a spec the user reviews. Use when starting a feature, component or behaviour change, before any code or scaffolding is written.
metadata:
  audience: lead, architect
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Brainstorming

Turn ideas into fully formed designs and specs through dialogue: read the
context, ask questions one at a time, propose approaches, present the design, get
approval, then write it down.

## When to use
- Starting a feature, a component, or a behaviour change.
- A request arrives vague or under-specified.

Not for a bug fix or a one-line change to already agreed behaviour. For a
throwaway answer to one question use `prototype`; for the step-by-step task list
use `writing-plans`.

## Hard gate
Do NOT write code, scaffold a project, or take any implementation action until a
design has been presented and the user has approved it. This applies to every
project, however simple. "This is too simple to need a design" is the most common
way unexamined assumptions waste work. Simple projects get a short design, a few
sentences, that is still presented and approved.

## Process
Work in order, tracking the steps with `todowrite`:
1. **Explore project context**: `read` the files and docs, `grep` the area, look
   at recent commits.
2. **Offer a visual companion once** if upcoming questions will be visual
   (mockups, layouts, diagrams). The offer must be its own message, with nothing
   else in it, and you wait for the answer. Accepting does not make every
   question visual: decide per question whether the user understands it better by
   seeing it than by reading it. Text, requirements and trade-off questions stay
   in the terminal.
3. **Ask clarifying questions one at a time**, never several in one message.
   Prefer multiple choice where it fits; open-ended is fine too. Focus on purpose,
   constraints and success criteria.
4. **Propose 2 to 3 approaches** with trade-offs, leading with your
   recommendation and the reasoning.
5. **Present the design** in sections scaled to their complexity (a few sentences
   when straightforward, up to 200 to 300 words when nuanced), covering
   architecture, components, data flow, error handling and testing. Ask after
   each section whether it looks right so far, and be ready to go back and
   clarify.
6. **Write the spec** to `docs/specs/YYYY-MM-DD-<topic>-design.md` unless the user
   prefers another location, and commit it.
7. **Self-review the spec**: scan for placeholders ("TBD", "TODO", vague
   requirements), internal contradictions, scope that needs decomposition, and
   requirements that could be read two ways. Pick one reading, make it explicit,
   and fix inline.
8. **Ask the user to review** the written spec and wait. If they request changes,
   edit and re-run the review loop.
9. **Hand off to `writing-plans`** to produce the implementation plan. Nothing
   else is invoked at this point.

## Scope check
If the request describes several independent subsystems, for example chat, file
storage, billing and analytics, say so before refining details, then decompose
into sub-projects: the independent pieces, how they relate, and the order to
build them. Brainstorm the first sub-project through the normal flow; each
sub-project gets its own spec, plan and implementation cycle.

## Design for isolation
Break the system into units that each have one clear purpose, communicate through
well-defined interfaces, and can be understood and tested independently. For each
unit answer: what does it do, how is it used, what do you depend on? Can someone
understand it without reading its internals, and can internals change without
breaking consumers? If not, the boundaries need work.

In an existing codebase, explore the structure and follow existing patterns
first. Where existing code directly obstructs this work, include targeted
improvements in the design. Do not propose unrelated refactoring.

## Principles
- One question at a time; multiple choice preferred where possible.
- YAGNI ruthlessly: remove unnecessary features from the design.
- Explore 2 to 3 alternatives before settling on one.
- Validate incrementally; get approval before moving on.

## Checklist
- [ ] Project context read before the first question
- [ ] One question at a time; visual companion offered once if relevant
- [ ] 2 to 3 approaches presented with a clear recommendation
- [ ] Design presented in sections and approved by the user
- [ ] Spec written, self-reviewed, reviewed by the user, committed
- [ ] Handed to `writing-plans`; no implementation started
