---
name: dispatching-parallel-agents
description: Split unrelated failures or tasks into independent problem domains and dispatch one agent per domain to run concurrently, then integrate and verify. Use when 2 or more problems are independent and share no state. Not for coupled work: see `subagent-driven-development`.
metadata:
  audience: lead
  upstream: https://github.com/obra/superpowers
  license: MIT
---
# Dispatching Parallel Agents

## When to use
- Three or more failing test files with different root causes, or several
  subsystems broken independently.
- Each problem can be understood without the others' context.
- No shared state: no same-file edits, no shared resources, no shared lock.

Do not use when fixing one problem may fix another, when the whole system state
must be understood at once, or when you do not yet know what is broken
(exploratory debugging is a single `debugging` job).

## Pattern
1. **Identify independent domains.** Group by what is broken, not by file. One
   domain per agent, for example: abort timing, batch completion not executing,
   tool approval race.
2. **Write one focused prompt per domain.** Each is focused (one problem),
   self-contained (all context needed, including failing test names and error
   output), constrained (what not to touch), and specific about its return
   value.
3. **Dispatch them concurrently** as separate `task` calls and let them run.
4. **Review and integrate.** Read each summary, check for conflicting edits,
   run the full suite, and spot check the fixes. Agents can make the same
   systematic error, so a green suite is checked, not assumed.

## Prompt shape
```
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:
1. "should abort tool with partial output capture" expects 'interrupted at'
2. "should handle mixed completed and aborted tools"
3. "should properly track pendingToolCount" expects 3, gets 0

Read the test file and understand what each test verifies. Find the root cause:
timing or a real bug. Fix it by replacing arbitrary timeouts with event-based
waiting, and fix the implementation if the tests exposed a bug.
Do NOT just increase timeouts.

Constraints: do not change other code.
Return: the root cause found and the changes made.
```

## Common mistakes
- Too broad ("fix all the tests"): the agent gets lost. Name one file or
  subsystem.
- No context ("fix the race condition"): paste the errors and test names.
- No constraints: the agent refactors everything. State what is off limits.
- Vague output ("fix it"): ask for the root cause and the changes.

## Worked example
Six failures across three files after a refactor: abort (3, timing), batch
completion (2, tools not executing), approval race (1, count is zero). Three
independent domains, three agents dispatched together. Fixes came back
independent and conflict free, the full suite went green, and three problems
were solved in the time of one.

## Checklist
- [ ] Each domain is genuinely independent (no shared state or files)
- [ ] One agent per domain; prompts focused, self-contained, constrained
- [ ] Expected return value stated per prompt
- [ ] Summaries read and conflicting edits checked
- [ ] Full suite run and fixes spot checked after integration
