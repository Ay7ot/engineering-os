---
name: web-interface-guidelines
description: Review UI code against the Web Interface Guidelines: fetch the current rules, check the files given and report findings as file and line. Use when asked to review a UI, audit accessibility or check a site against web best practices.
metadata:
  audience: reviewer, builder
  upstream: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
  license: MIT
---
# Web Interface Guidelines Review

Review UI files for compliance with the Web Interface Guidelines and report
findings against the live rule set.

## When to use
- Asked to review a UI, audit accessibility or check a site or component against
  web best practices.
- Auditing a page against an external, maintained rule list.
- For design direction or aesthetics, use `design-taste-frontend` or
  `frontend-design`; for deep dives in one area use `better-typography`,
  `better-colors`, `better-layout`, `better-ui` or `wcag-accessibility`.

## Procedure
1. Fetch the current guidelines before every review; never rely on a cached copy
   or on memory. Retrieve
   `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
   with `webfetch`.
2. Take the files to check from the request. If the user gave a pattern, resolve
   it with `glob`; if they gave nothing, ask which files or area to review before
   starting.
3. Read each file and check it against every rule in the fetched guidelines. The
   fetched content carries the rules and the required output format; follow it as
   written.
4. Report findings in the terse `file:line` form the guidelines specify, with the
   violated rule and the smallest fix for each.
5. If the fetch fails, say so and ask whether to proceed with a local copy, a
   different source, or stop. Do not invent rule text.

## Rules of engagement
- Report what the guidelines actually say. Do not add preferences of your own to
  their list; keep personal suggestions clearly separate and optional.
- Cite every finding to a real file and line (or the exact screen and component
  when there is no source file).
- Group repeated occurrences of one rule instead of repeating the same finding
  for every line, but list every affected location.
- Do not change code unless asked; a review reports.
- Say which rules could not be checked and why (no rendered page, no source,
  missing environment), rather than implying full coverage.
- Guidelines age: if a fetched rule contradicts the project's own documented
  convention, report the conflict rather than silently following one side.

## Checklist
- [ ] Guidelines fetched fresh from the source URL for this review
- [ ] Scope confirmed: files or pattern identified, otherwise the user was asked
- [ ] Every fetched rule checked against the files, not a sample of rules
- [ ] Findings reported in the guidelines' `file:line` output format
- [ ] Locations cited; repeated occurrences grouped with all locations listed
- [ ] Unchecked rules and reasons stated
- [ ] No code edited unless the user asked for fixes
