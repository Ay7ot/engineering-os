---
name: grilling
description: Grill the user about a plan, decision or idea in rounds until every branch of the design tree is settled. Use when asked to stress-test thinking, harden a plan, or resolve open questions before implementation. Not for a one-question-at-a-time idea intake, see `brainstorming`.
metadata:
  audience: lead, architect
  upstream: https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling
  license: MIT
---
# Grilling

## When to use
- The user asks to be grilled, or to stress-test a plan, decision, or idea.
- A design is agreed in outline but hides unresolved choices.
- Work is about to start and silent assumptions need surfacing.
- A decision needs its prerequisites settled before it can be answered.

For a lighter idea intake that produces a spec, use `brainstorming`. For
evaluating a system design, use `architecture-analysis`.

## The design tree
Model the subject as a tree: each decision branches into the decisions that
hang off it. A decision is settled only when it is stated and the user accepts
it. Keep the tree visible as you go; it is what makes the next round obvious.

## Rounds and the frontier
- The frontier is every decision whose prerequisites are already settled: the
  questions you can ask now without guessing at answers you have not heard.
- Ask the whole frontier in one round. Number each question and give your
  recommended answer.
- Wait for the user's answers before the next round. Their answers reshape the
  tree: settled decisions push the frontier outward and unblock the questions
  behind them. Recompute the frontier and ask the next round.
- A question that depends on another question still open in this round belongs
  to a later round, not this one.

## Question format
```
Q1 <question title>: <body, which may be several paragraphs and may offer
multiple options>

Recommendation: <your recommended answer and why>
```

## Findings are your job, decisions are the user's
- If a frontier question needs a fact (a file, a command output, a library's
  behaviour), find it yourself: dispatch a `task` subagent, or use `grep`,
  `glob`, `bash`, or `webfetch`. Never ask the user for something you could look
  up.
- Do not block the whole round on a running lookup. A lookup is an unsettled
  prerequisite, so only the questions downstream of it wait; ask the rest of the
  frontier now.
- The decisions are the user's. Put each one to them and wait for the answer.

## Done
- The session ends when the frontier is empty: every branch of the tree visited
  and nothing left silently assumed.
- Do not act on the result until the user confirms the shared understanding.
- Write the settled decisions down (a list, a doc, or `engineering-memory`) so
  the answers survive the conversation.

## Checklist
- [ ] Subject modelled as a design tree with separable decisions
- [ ] Frontier computed; only answerable-now questions asked
- [ ] Whole frontier asked in one round, each with a recommendation
- [ ] Facts looked up, not asked of the user; lookups did not block the round
- [ ] Later-round questions held back until their prerequisites settled
- [ ] Frontier empty and the user has confirmed shared understanding
