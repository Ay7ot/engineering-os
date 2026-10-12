---
name: verification-before-completion
description: Require fresh, first-hand command output before claiming work is complete, fixed, or passing. Use when about to report success, commit, open a PR, or accept a subagent's report. Not a test-writing method: see `testing`.
metadata:
  audience: builder, tester, reviewer, lead
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Verification Before Completion

## When to use
- About to say work is done, fixed, passing, or ready, in any wording.
- Before committing, pushing, opening a PR, or marking a task complete.
- Before accepting a subagent's or tool's success report.
- Before moving to the next task in a plan.

## The iron law
No completion claim without fresh verification evidence. If you have not run the
verification command in this turn, you cannot claim it passes. Claiming
otherwise is not efficiency, it is a false report. This applies to exact
wording, paraphrases, and any implication of success.

## The gate
Before any status statement:
1. Identify: which command proves this claim?
2. Run: the full command, fresh and complete (not a cached or partial run).
3. Read: the full output, the exit code, the failure count.
4. Confirm: does the output actually support the claim?
   - No: state the real status with evidence.
   - Yes: state the claim together with the evidence.
5. Only then make the claim.

Skipping a step is not verifying.

## What each claim requires
| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | test output showing 0 failures | a previous run |
| Lint clean | lint output showing 0 errors | a partial check |
| Build succeeds | build exit code 0 | lint passing, logs looking fine |
| Bug fixed | the original symptom's test now passing | code changed |
| Regression test works | red then green cycle observed | the test passing once |
| Requirements met | line-by-line checklist against the plan | tests passing |
| Subagent finished | the diff shows the change | the subagent's report |

## Red flags, stop
- "should", "probably", "seems to", "looks correct".
- Praise before proof: "Great", "Perfect", "Done" with no command run.
- Trusting an agent or tool that says "success" without checking the diff.
- Relying on a partial run, or extrapolating from a neighbouring check (a linter
  is not a compiler).
- "Just this once", "I am confident", "I am tired".

## Patterns
- Tests: run them, see 34 passed / 0 failed, then say "all tests pass".
- Regression: write, run (passes), revert the fix, run (must fail), restore,
  run (passes) only then claim the regression test.
- Requirements: re-read the plan, tick each criterion, report gaps per item.
- Delegation: read the diff or files, verify the change, and report the actual
  state.

Prefer the higher rungs of the `testing` verification ladder. When a check
cannot be run (missing command, environment, or credentials), say exactly what
is missing instead of claiming success.

## Checklist
- [ ] The proving command was run this turn, in full
- [ ] Output and exit code read, failures counted
- [ ] Claim matches the evidence; unverified parts labelled as such
- [ ] Subagent and tool reports independently confirmed against the diff
