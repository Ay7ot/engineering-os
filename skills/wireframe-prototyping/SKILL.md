---
name: wireframe-prototyping
description: Pick the right wireframe or prototype fidelity, lay out the screens and flows, then test them with users before development. Use when sketching a new screen or flow, building an interactive prototype for feedback, or deciding how much fidelity a concept needs.
metadata:
  audience: lead, builder
  upstream: https://github.com/aj-geddes/useful-ai-prompts
  license: MIT
---
# Wireframe Prototyping

Wireframes and prototypes bridge an idea and an implementation: cheap enough to
throw away, concrete enough to test and disagree with.

## When to use
- Validating a concept or a flow before writing production code.
- Aligning stakeholders or a team on structure and scope.
- Preparing developer handoff.
- Exploring several solutions to the same problem.

For throwaway code that answers a design question, use `prototype`. For the
session format that starts the exploration, use `brainstorming`. For running the
test itself, use `usability-testing`.

## Step 1: pick the fidelity
The lowest fidelity that answers the open question wins. Full tiers are in
`references/fidelity-and-tools.md`.

| Fidelity | Typical time | Carries | Best for |
|---|---|---|---|
| Low (sketch, paper, whiteboard) | 30 min to 2 h | layout only, no colour or type | brainstorming, exploration |
| Medium (design tool) | 2 to 8 h | layout, content, basic interaction | team alignment, feedback |
| High (design tool or code) | 8 h and up | visual design, interactions, motion | developer handoff, user testing |

Do not jump straight to high fidelity: every unresolved structural question
costs more to change once it looks finished.

## Step 2: lay it out
- Work mobile first, then widen; check 375, 768, 1024 and 1440 px.
- Use a consistent grid and spacing scale, not ad hoc gaps.
- One primary action per screen. Everything else is secondary.
- Design the real content: long names, empty lists, zero results, errors.
- Mark each interactive element with its trigger and action so the flow is not
  left implicit.

A screen skeleton example (e-commerce product page) is in
`references/fidelity-and-tools.md`.

## Step 3: define the flows
Write screens and transitions as data before building anything clickable:

```text
screens: Login (email, password, submit), Dashboard (list, create, search)
flows:   Login -> Dashboard on valid credentials
         Dashboard -> Detail on clicking a project
```

Every screen needs at least one exit, and every flow needs its failure branch
(invalid input, no permission, empty state).

## Step 4: test it
Run a small unmoderated test: 5 representative users, roughly 30 minutes each,
tasks drawn from the primary flows. Success bar and the full plan template are
in `references/prototype-testing.md`. Record the top three friction points with
quotes, then change the prototype and retest.

## Rules
- Iterate: get feedback early and often, then change the prototype.
- Keep the prototype focused on the flows under test, not every screen.
- Do not test only with teammates; they know the intended path.
- Include accessibility from the start: labels, focus order, contrast.
- Do not lock a design before it has passed a user test.

## Checklist
- [ ] Fidelity matches the open question and stage
- [ ] Mobile, tablet and desktop layouts checked
- [ ] Content is realistic; empty, error and edge states designed
- [ ] Every interaction has a trigger and an action defined
- [ ] Test plan written with tasks and success criteria
- [ ] Tested with representative users, not only the team
- [ ] Top friction points captured with evidence and acted on
