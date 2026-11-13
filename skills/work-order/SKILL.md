---
name: work-order
description: Write a complete work order before delegating to a builder, tester or reviewer. Use when a task needs more than one step, when a subagent needs context, or when a change touches a user flow, data, time, money or permissions.
metadata:
  audience: lead, builder
---
# Work Order

## When to use
- Delegating implementation, testing or review to a subagent.
- Writing a plan task that someone else will execute.
- A change touches a user flow, a query, a status, a date, a count or a money path and the brief is still a sentence.

A work order is not a summary. It is the contract the builder implements and the reviewer checks.

## The contract
| Row | What to write |
|---|---|
| **Goal** | The user-visible outcome and the problem it solves. |
| **Non-goals** | What is deliberately out of scope. |
| **Surfaces** | Every screen, route, handler, component and entry point the change touches, and every other entry point that reaches it. |
| **States** | Every status, enum, access state and permission. For each: label, visibility, CTA, copy and gate. |
| **Data** | Every value shown or sent: source field, unit, format, null/empty behavior, default, and whether a hardcoded value shadows real data. |
| **Cardinality** | Every join, group-by, dedupe and count. Can a one-to-many collapse? Does a total count every row? |
| **Time** | Every date comparison, date-only vs timestamp, local vs UTC, day/month boundary, DST, preset and clamp. |
| **Copy truth** | Every user-facing promise against the code path that actually runs. |
| **Money and concurrency** | Every event ordering, retry, double submit, webhook delay, partial failure and idempotency key. |
| **Acceptance tests** | The behavioral test for each risky row. A source-pin test is not enough for logic, money, time, state or copy. |
| **Verification** | The exact commands for tests, typecheck, lint and build, plus what cannot run here. |
| **Definition of done** | Every contract row proven or marked as a gap. The flow run end to end, or the gap stated. |

If a row does not apply, write `n/a` and the reason. Do not leave it blank.

## Template
```
Goal:
Non-goals:
Surfaces:
States:
Data:
Cardinality:
Time:
Copy:
Money/concurrency:
Acceptance tests:
Verification:
Definition of done:
Stop conditions:
```

## Stop conditions
The builder infers implementation details from the repo, docs and tests. It returns one question only when a product, architecture, scope or security decision is genuinely missing and would change the outcome. A missing test command or a naming choice is not a stop condition.

## Delegation notes
- One writer per worktree. Name the worktree and the branch.
- Give the builder the base SHA and the diff base.
- Give the reviewer the head SHA, the work order and the raw verification output.
- Give the tester the risk matrix and the environment constraints.
- If the work order changes after work starts, record the change and re-review the delta.

## Checklist
- [ ] Goal, non-goals and user-visible outcome
- [ ] Surfaces and every entry point
- [ ] State matrix, data map, cardinality, time and copy truth
- [ ] Money and concurrency rows, or `n/a`
- [ ] Behavioral acceptance test per risky row
- [ ] Verification commands and definition of done
- [ ] Stop conditions limited to real decisions
- [ ] Worktree, branch and base SHA named
