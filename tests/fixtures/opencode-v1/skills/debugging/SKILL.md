---
name: debugging
description: Systematic bug investigation. Investigate, reproduce, and test hypotheses before modifying code. Use when diagnosing a reported problem.
metadata:
  audience: lead, builder, tester
---
# Debugging

## When to use
- A reported bug, error, or incident.
- Unexplained behavior in a feature.

## Procedure
1. **Investigate logs.** Find logs for the problem window. Use observability (dashboards, error trackers) if available. Correlate timestamps.
2. **Inspect relevant code.** Map the code path (entry point -> failing point). Read the actual implementation, not assumptions.
3. **Search recent changes.** `git log`, `git diff` for commits that could have introduced the regression.
4. **Reproduce where possible.** Write a test or run a controlled command that reproduces. If not reproducible, document the evidence gap.
5. **Identify hypotheses.** Rank plausible root causes by likelihood, each tied to evidence.
6. **Test hypotheses.** Support/refute with logs, tests, targeted experiments BEFORE changing code.
7. **Implement the fix.** Smallest correct change; follow conventions.
8. **Add regression test.** A test that would have failed before the fix.
9. **Verify.** Run tests, typecheck, lint, build. Confirm reproduction no longer fails.
10. **Report.** Root cause (with evidence), fix, verification evidence, regression coverage.

## Discipline
- Do NOT patch based on the first hypothesis. Investigate first.
- If blocked (no logs, can't reproduce), say so and propose the most likely cause with supporting evidence — do not guess a fix.
- One fix per confirmed cause. Don't pile on speculative fixes.

## Checklist
- [ ] Logs investigated
- [ ] Code path mapped
- [ ] Recent changes searched
- [ ] Reproduction attempted (or gap documented)
- [ ] Hypotheses tested before coding
- [ ] Regression test added
- [ ] Verified with deterministic tooling