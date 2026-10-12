# TDD rationalizations to expect

Answers to the excuses that appear when the cycle feels inconvenient.

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. The test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve the same goals" | Tests-after ask "what does this do?". Tests-first ask "what should this do?". |
| "Already manually tested" | Ad-hoc is not systematic: no record, cannot re-run. |
| "Deleting X hours is wasteful" | Sunk cost. Keeping unverified code is technical debt. |
| "Keep it as reference, write tests first" | You will adapt it. That is testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw the exploration away and start with the cycle. |
| "Hard to test means design is unclear" | A hard-to-use interface is the finding. Simplify it. |
| "TDD will slow me down" | Test-first beats debugging in production, which is slower. |
| "Manual test is faster" | Manual does not prove edge cases, and you re-test every change. |
| "Existing code has no tests" | You are improving it. Add tests for the code you touch. |

## Red flags, stop and start over
- Code before test; test after implementation.
- The test passes the first time it runs.
- You cannot explain why the test failed.
- Tests "added later".
- Rationalizing "just this once", or "this case is different".
- "I already manually tested it" or "it is about spirit, not ritual".
- "Keep as reference" or "adapt the existing code".
- "Deleting is wasteful" after time already spent.

All of these mean: delete the untested code and start again from a failing test.

## When stuck
| Problem | Move |
|---|---|
| Do not know how to test it | Write the wished-for API first, or write the assertion first. Ask the human. |
| The test is too complicated | The design is too complicated. Simplify the interface. |
| You must mock everything | The code is too coupled. Inject dependencies. |
| Test setup is huge | Extract helpers. Still huge? Simplify the design. |
