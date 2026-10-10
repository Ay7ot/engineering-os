---
name: simplify
description: Tidy a finished, passing change so reviewers see the smallest clear version of it, without changing what it does. Not a bug hunt and not a redesign. Use after a change works and its tests pass, before review.
metadata:
  audience: builder, lead
---
# Simplify

## When to use
- A change works and its tests pass, and it is about to go to review.
- A diff grew larger than the problem seemed to need.

Not for finding bugs (use `code-review`) and not for redesigning approved
architecture (stop and report instead).

## Safety limits (read first)
- **Behaviour must not change.** Edit only code that the tests actually
  exercise. For anything untested, report the opportunity instead of editing.
- **Never change persisted shape.** Removing a stored field, a cache, a column or
  a file format is an architecture change: report it.
- **Swap in an existing helper only after confirming it behaves the same**
  (rounding, errors, empty input, edge cases). If it differs, report it.
- **Concurrency only for read-only, order-independent work.** Running writes,
  external calls or anything inside a transaction in parallel changes ordering,
  error handling and rate limits: report it.

## Look for
1. **Duplication.** Code that re-implements something the codebase or standard
   library already provides. Search nearby modules and shared folders first.
2. **Excess structure.** Values stored but derivable from others (in memory
   only), near-identical blocks that differ by one value, nesting that early
   returns would flatten, one-caller wrappers that add indirection, dead code,
   unused parameters, leftover debug output, stale comments.
3. **Wasted work.** The same computation or I/O done twice; heavy work added to
   startup or hot paths; long-lived objects holding far more than they use.
4. **Root cause vs patch.** A special case bolted onto shared code to hide a
   symptom. If a small general fix to the underlying mechanism removes it,
   propose it; make it only if it stays inside the approved design.

## Apply
- One small, separate edit per improvement.
- After the edits, re-run the tests, typecheck and lint. If anything fails,
  revert that edit; do not "fix forward".
- Leave unrelated code and formatting alone.

## Output
- Each simplification, one line, with file:line.
- Opportunities reported but not applied (untested, persisted, behaviour or
  architecture risk), with the reason.
- Verification evidence: commands run and results.

## Checklist
- [ ] Only tested code edited; untested opportunities reported
- [ ] No persisted shape changed; helpers confirmed equivalent
- [ ] Parallelism only for read-only, order-independent work
- [ ] Duplication, excess structure, wasted work addressed
- [ ] Root-cause fixes stay inside the approved design
- [ ] Tests, typecheck, lint re-run and passing
