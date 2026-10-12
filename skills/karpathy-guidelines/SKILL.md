---
name: karpathy-guidelines
description: Behavioural guidelines that reduce common LLM coding mistakes: surface assumptions, keep changes minimal and surgical, and turn tasks into verifiable goals. Use when writing, reviewing, or refactoring code, before adding features or abstractions. For tidying a finished change, see `simplify`.
metadata:
  audience: builder, reviewer, lead
  upstream: https://github.com/multica-ai/andrej-karpathy-skills
  license: MIT
---
# Karpathy Guidelines

## When to use
- Before writing code for a task whose requirements have gaps or more than one
  reading.
- When a change starts drifting beyond what was asked.
- When reviewing code that looks overcomplicated or touches unrelated lines.

These bias toward caution over speed; use judgement on trivial tasks. They shape
a change while it is written; `simplify` tidies a finished, passing change and
`code-review` looks for reasons not to merge.

## 1. Think before coding
- State assumptions explicitly. If uncertain, ask instead of guessing.
- If a request has several interpretations, present them; do not silently pick
  one.
- If a simpler approach exists, say so and push back with reasons.
- If something is unclear, stop and name the confusion. Do not code around it.

## 2. Simplicity first
- Minimum code that solves the problem, nothing speculative.
- No features beyond the request, no abstraction for single-use code, no
  "flexibility" or configuration that was not asked for.
- No error handling for impossible scenarios.
- If you wrote 200 lines and 50 would do, rewrite it.
- Test: would a senior engineer call this overcomplicated? If yes, simplify.

## 3. Surgical changes
- Touch only what the request requires. Do not "improve" adjacent code,
  comments, or formatting.
- Do not refactor what is not broken. Match the existing style even if you would
  do it differently.
- If you find unrelated dead code, mention it; do not delete it.
- Clean up only the orphans your own change created: imports, variables, and
  functions it made unused.
- Test: every changed line traces directly to the request.

## 4. Goal-driven execution
- Turn each task into a verifiable goal. "Add validation" becomes "write tests
  for invalid inputs, then make them pass". "Fix the bug" becomes "write a test
  that reproduces it, then make it pass". "Refactor X" becomes "tests pass
  before and after".
- For multi-step work, state a brief plan with a check per step:
  1. step -> verify: check
  2. step -> verify: check
- Strong success criteria let you loop alone; weak criteria ("make it work")
  need constant clarification.

## Checklist
- [ ] Assumptions and ambiguity surfaced before coding
- [ ] No feature, abstraction, or configuration beyond the request
- [ ] Every changed line traces to the request; orphans of my change removed
- [ ] Goal stated as a verifiable check, with tests where practical
- [ ] Adjacent code, style, and pre-existing dead code left alone
