---
name: design-critique
description: Structure a design critique: presentation, clarifying questions, a feedback round and prioritised next steps. Use when reviewing a mockup, prototype or live UI with peers, or receiving feedback on your own design. Not for testing with real users, see `usability-testing`.
metadata:
  audience: lead, builder, reviewer
  upstream: https://github.com/slb2248/ai-ux-skills/tree/main/skills/design-critique
  license: MIT
---
# Design Critique

A critique is a scheduled feedback session with a stated scope, not an open
opinion swap. The presenter owns the questions. Reviewers answer those questions
before adding anything else.

## When to use
- Reviewing a mockup, prototype or live screen with peers.
- Getting direction before committing to build.
- Running a recurring design review.
- Receiving feedback on your own work.

For testing with real users instead of peers, use `usability-testing`. For a
workshop that produces a decision rather than feedback, use
`design-workshop-facilitation`.

## Before the session
The presenter shares, in advance:
- Problem: what problem, for which user, under which constraints.
- Scope: stage of the work, the feedback wanted, what is explicitly out of scope.
- Materials: design files or a prototype, research findings, requirements.
- Two or three specific questions the session must answer.

The facilitator prepares:
- Time boxes per segment and something to keep time with.
- The single feedback format reviewers will use.
- A note taker and the place captured feedback will land.

## Run it
| Segment | Time | Output |
|---|---|---|
| Presentation | 5-10 min | problem, user needs, solution, questions |
| Clarifying questions | 5 min | shared understanding |
| Feedback round | 15-20 min | observations from every reviewer |
| Discussion | 10 min | themes, priorities, next steps |

Enforce the order: questions first, then feedback. A reviewer who starts
solving during the questions segment is guessing at context.

## Feedback formats
Pick one and state it up front.

- Likes, wishes, what-ifs: "I like how onboarding reduces friction", "I wish the
  error states were more helpful", "what if we added a progress indicator".
- Observation, impact, suggestion: "I notice the CTA is below the fold, this
  may reduce conversions, consider testing it above the fold".

Give actionable feedback, not preference: contrast "the button contrast is
2.8:1, below the 4.5:1 WCAG AA floor" beats "I do not like the blue". Give
specific feedback, not vague: "the form has 12 fields, progressive disclosure
would cut load" beats "this feels overwhelming".

## Receiving feedback
- Listen fully before responding, take notes, ask clarifying questions.
- Do not defend every decision or explain feedback away.
- Watch for patterns across reviewers; a repeated note is a real finding.
- Thank reviewers and follow up on the actions you accept.

Stage-specific focus, facilitation tips, remote practice and the follow-up
summary are in `references/session-runbook.md`.

## Checklist
- [ ] Scope, stage and out-of-scope stated in advance
- [ ] Presenter brought specific questions, not "any thoughts?"
- [ ] Questions segment completed before feedback
- [ ] One feedback format used by all reviewers
- [ ] Feedback is actionable and specific, not preference
- [ ] Themes and prioritised next steps captured with owners
