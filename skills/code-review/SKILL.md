---
name: code-review
description: Adversarial code review that looks for reasons NOT to merge by reading the change several times, each time with one question in mind. Use when reviewing a diff, branch, PR or files written by someone else.
metadata:
  audience: reviewer, lead
---
# Code Review

## When to use
- Reviewing changes before merge (diff, branch, PR, files).
- Independent verification of another agent's work.

## Review packet
Confirm you have:
1. The exact diff and changed-file list.
2. The plan, acceptance criteria, and any approved architecture or ADR.
3. The project rules that govern the changed paths.
4. Raw verification output: tests, typecheck, lint, clean build, and CI status.
5. The sensitive-path flags: auth, payments, PII or PHI, data or migrations, concurrency, build config, public APIs, dependencies, secrets, infrastructure, deployment.

If a piece is missing, say so. If a verification command is outside your allowlist, ask the lead to have the tester run it and pass the raw output. Do not guess at results.

## Scope first
1. Pin the exact commit SHA. Get the change: the PR/branch diff against its base at that SHA, plus uncommitted work if the review runs before commit. That diff is the scope.
2. For every changed hunk, read the **whole enclosing function** too. A bug in an
   unchanged line of a touched function is in scope: the change re-exposes it or
   failed to fix it.
3. Read the project's rule files (`AGENTS.md`, contributing guides, or the
   editor's equivalent) that govern the changed paths.
4. Read what the change was supposed to do: the plan, acceptance criteria, and
   any approved architecture or ADR it implements.

## Method: independent passes
Run each pass on its own and write candidates down before judging them. A
single read-through misses what a focused pass catches. Each candidate gets a
location and a concrete failure scenario (inputs or state, then the wrong
result).

| Pass | Ask |
|---|---|
| **Intent** | Does it meet the requirements and every acceptance criterion? Does it follow the approved architecture, or quietly redesign it (stop-and-report territory)? |
| **Line by line** | For each changed line: what input, state, timing or platform makes it wrong? Inverted conditions, off-by-one, null/undefined, missing `await`, falsy zero, copy-paste with the wrong variable, swallowed errors, unescaped regex or shell input. |
| **Removed behaviour** | For each deleted or replaced line: which guard, validation, error path or test did it provide? Where is that re-established? If nowhere, that is a finding. |
| **Callers and callees** | For each changed function: find its callers. Does a new precondition, return shape, exception or ordering break any of them? Does a parallel change make a call unsafe? |
| **Security** | AuthN/Z, tenant isolation, input validation, secrets, injection, SSRF, IDOR, webhooks, races, sensitive data in logs. Use the `security-review` skill for anything security-critical. |
| **Data and concurrency** | Transactions, idempotency, migrations, partial failure, races, locking. |
| **Compatibility** | Public APIs, schemas, events, file formats, config and CLI flags used outside this repo: does anything break for existing consumers or stored data? |
| **Failure handling** | Errors surfaced or swallowed, partial states, retries, timeouts, and whether failures are observable (logs, metrics). Edge cases: empty, boundaries, timezones, unicode. |
| **Duplication** | Does new code re-implement a helper the codebase already has? Name the helper. |
| **Weight** | Redundant state, copy-paste variants, dead code, repeated I/O, heavy work on hot or startup paths. |
| **Root cause vs patch** | Is this fixed where the problem lives, or is a special case bolted onto shared code? Name the deeper, simpler change if there is one. |
| **Project rules** | Quote the exact rule from a governing rules file and the exact line that breaks it. No vague "spirit of the doc" findings. |
| **Tests** | Do tests cover the risky paths with meaningful assertions? Would they fail if the bug came back? |

## Semantic passes
Run these in addition to the passes above. They catch the bugs that survive typecheck and tests: a value that comes from the wrong field, a state that renders the wrong label, a count that collapses a one-to-many, a date that shifts by a timezone.

| Pass | Ask | Evidence |
|---|---|---|
| **Surface inventory** | Every entry point that reaches the changed surface. Is each one wired, gated and covered? | entry point -> path |
| **Data provenance** | For every value rendered or sent, where does it come from? Does the label, unit, format, null/empty handling and default match the source? Is a hardcoded value shadowing data that exists? | source field -> render |
| **State matrix** | Enumerate every status, enum, access state and permission. For each: label, visibility, CTA, copy and gate. Which state falls into a default that lies? | state -> expected -> actual |
| **Cardinality** | Every join, group-by, dedupe and count. Can a one-to-many collapse? Does a total count every row? | query -> consumer |
| **Time** | Every date-only/timestamp, local/UTC, day/month boundary, DST, "today"/"this month" preset and clamped navigation. | input + timezone -> expected |
| **Copy truth** | Every user-facing promise (charge timing, availability, next step) against the code path that actually runs. | copy -> code path |
| **Optional-field render** | Every combination of optional fields. Does a details control open when any field is present? | field set -> rendered |
| **Money and concurrency** | Every event ordering, retry, double submit, webhook delay, partial failure and idempotency key. | ordering -> outcome |

A pass that does not apply gets `n/a` and the reason. A pass you did not run is a gap, not a zero.

## Cross-boundary pass
Run this even when the diff looks local. Name both sides of the boundary and the
exact mismatch.

| Boundary | Ask |
|---|---|
| **DB type vs parameter** | Is an enum column compared to a `text[]` or string parameter? Does the query need an explicit cast? Are the values valid for the enum? Does a `CHECK` constraint silently never match? |
| **Timestamp precision** | Is `timestamptz` microsecond precision compared to a JS `Date` millisecond value, or a serialized ISO string? Does the round trip truncate? Is `date_trunc` at the right precision? |
| **Client/server boundary** | Does a `'use client'` file import a runtime value from a `server-only` module? Does DB code, a secret, or a Node built-in reach the client bundle? |
| **Bundle boundary** | Does a barrel import, side effect, package export, dynamic import, or rollup scope pull in the wrong code? Does a clean build still pass? |
| **Serialization** | Does JSON round-trip preserve `Date`, `undefined`, `null`, `BigInt`, `Decimal`, `NaN`, or `Infinity`? Does an API or event schema match its consumer? |
| **Concurrency token** | Does an optimistic concurrency token preserve the precision of the stored value? Is the compare-and-swap atomic? Can a retry double-apply? |

## Triage
- Merge duplicates (same defect, same place, same reason).
- Rank: correctness and security first, then data, then cleanup.
- Keep a candidate if you can state a concrete failure scenario. Drop it only
  when you can show it cannot happen, not because you are unsure. Label findings
  you could not confirm as inference.
- Where cheap, confirm a finding deterministically (a failing input, a test,
  typecheck), or ask the tester to, and say which.

## Output format
Start with the head SHA and a coverage table:

| Pass | Run? | Findings |
|---|---|---|
| Surface inventory | yes / n/a | count |
| Data provenance | yes / n/a | count |
| State matrix | yes / n/a | count |
| Cardinality | yes / n/a | count |
| Time | yes / n/a | count |
| Copy truth | yes / n/a | count |
| Optional-field render | yes / n/a | count |
| Money and concurrency | yes / n/a | count |

Per issue: **Severity** (blocker / major / minor / nit), **Location** (path:line),
**Issue**, **Failure scenario**, **Suggested fix**. End with **Verdict**:
APPROVE / CHANGES REQUESTED + blocker summary, the head SHA the verdict covers,
and any part of the scope you could not review (and why).

## Rules
- Be adversarial: your job is to find reasons NOT to merge.
- Cite specific code. Distinguish fact (verified) from inference.
- Report only; never fix during review.
- A source-pin test (regex or `readFileSync` over a source file) is not evidence for logic, money, time, state or copy. Say so when it is the only test.
- Prefer deterministic evidence (tests, typecheck, lint, clean build, CI) when in scope. Report the command and result. Author-reported results are not verified.

## Checklist
- [ ] Head SHA pinned; exact diff gathered; enclosing functions, rules and plan read
- [ ] Review packet complete; verification evidence read or the gap stated
- [ ] Every pass run, candidates written before judging
- [ ] Semantic passes run: surfaces, data provenance, state matrix, cardinality, time, copy truth, optional fields, money/concurrency
- [ ] Requirements, acceptance criteria and approved architecture checked
- [ ] Removed behaviour accounted for
- [ ] Callers of changed functions checked; external compatibility checked
- [ ] Security, data integrity and failure handling reviewed
- [ ] Cross-boundary pass run: DB type, timestamp precision, client/server, bundle, serialization, concurrency token
- [ ] Duplication / weight / root cause considered
- [ ] Project rule violations quoted exactly
- [ ] Duplicates merged, ranked by severity
- [ ] Coverage table complete; verdict names the head SHA and any unreviewed scope
