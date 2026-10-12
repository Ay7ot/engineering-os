# Prototype testing

Test the flow, not the art. Five users find most of the friction in a single
flow; more users mostly repeat the same findings.

## Plan template

```text
Objective:  validate primary user flows and UX clarity
Method:     unmoderated remote test
Participants: 5 representative users, mixed experience, close to persona
Tasks:
  1. Register a new account
  2. Create the first project
  3. Invite a team member
  4. Edit project settings
Success criteria:
  - 80 percent or more task completion
  - average time under 5 minutes per task
  - system usability score above 70
  - no critical usability blockers
```

## What to watch

- Navigation clarity: can the user say where they are and what is next?
- Button and link placement: are primary actions where the eye lands?
- Form fields: labels, hints, required markers, validation feedback.
- Visual hierarchy: does the layout say what matters most?
- Error handling: are failures explained and recoverable?

## Analysis and reporting

Report in three parts:
1. Top three friction points, each with the task and the observed behaviour.
2. Representative user quotes, verbatim, next to the step they came from.
3. Design recommendations, each tied to a friction point and a priority.

Prefer observing what people did over asking what they would want. A user who
completes a task while frowning has reported a problem the questionnaire will
miss.

## Between rounds

Change only what the test implicated. Retesting a fixed prototype on the same
tasks is the fastest way to see whether a fix worked, and a prototype that
never changes is not a test, it is a demo.
