---
name: test-driven-development
description: Write a failing test before the implementation, watch it fail for the right reason, then write the minimum code to pass (Red-Green-Refactor). Use when implementing a feature, fixing a bug, refactoring, or changing behaviour. For test strategy and coverage, see `testing`.
metadata:
  audience: builder, tester
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Test-Driven Development

## When to use
- Adding any new behavior, feature, or bugfix.
- Refactoring or changing existing behavior, so the change is pinned down.
- Clearing a reported bug: write the failing test that reproduces it first.

Agree exceptions with the human first: throwaway prototypes, generated code,
pure configuration. Everything else uses the cycle. Thinking "skip it just this
once" is the rationalization the cycle exists to stop.

## The iron law
- Write no production code without a failing test that demands it.
- Wrote code before the test? Delete it and start again. Do not keep it as
  reference, do not adapt it while writing the test, do not read it.
- Implementing the behavior fresh, from the test, is the point.

## The cycle
One behavior per iteration. See `references/rationalizations.md` for the excuses
this guards against.

1. **Red.** Write one minimal test with a clear name showing what should happen,
   using real code (mocks only when unavoidable). Run it with the project's
   command, for example `npm test path/to/test.test.ts`.
   - It must fail, not error. If it passes, it tests existing behavior: fix it.
   - It must fail for the expected reason (feature missing), not a typo.
   - If it errors, fix the error and re-run until it fails correctly.
2. **Green.** Write the simplest code that makes it pass. Nothing speculative:
   no extra flags, options, or "flexibility" the test does not demand. Re-run:
   the new test passes, other tests still pass, output is clean.
   - It fails? Fix the code, not the test.
   - Others fail? Fix them now.
3. **Refactor.** Only while green: remove duplication, improve names, extract
   helpers, without adding behavior. Keep tests green after each edit.
4. **Repeat.** Next behavior, next failing test.

## Good tests
- One thing each. If the name needs "and", split the test.
- The name describes the behavior, not "test1".
- Tests drive the code through its real interface; a test that asserts on a mock
  asserts the mock.
- Each reported bug gets a regression test that fails before the fix (pair with
  `debugging`).

## Why order matters
- Tests written after code pass immediately, and a test that never failed proves
  nothing: it may test the wrong thing, the implementation, or miss the edge
  cases you did not think of.
- Manual testing leaves no record, cannot be re-run when code changes, and gets
  forgotten under pressure.
- "Deleting hours of work is wasteful" is sunk cost: unverified code is debt.
- "Hard to test" means the design is hard to use. Listen to the test and
  simplify the interface rather than mocking everything.

## Checklist
- [ ] Each new behavior has a test written before the code
- [ ] Each test was watched failing, for the expected reason
- [ ] Minimal code written to pass; no speculative options added
- [ ] Full suite green and output clean after each cycle
- [ ] Bug fixes have a regression test that failed first
