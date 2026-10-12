---
name: pm-handoff
description: Compact the current conversation into a handoff document so a fresh agent can continue the work. Use when ending a session mid-task, or when another session will pick the work up. Not for durable project knowledge, which belongs in the memory tools.
metadata:
  audience: lead, builder
  upstream: https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff
  license: MIT
---
# Handoff

## When to use
- The session is ending with work unfinished and another agent continues it.
- Context must move to a fresh session without the full transcript.

## Write the document
- Save it to the temporary directory of the user's OS, not the workspace.
- Include a "Suggested skills" section naming the skills the next agent should
  load, for example `debugging`, `testing`, `code-review`.
- Do not duplicate what other artefacts already capture (PRDs, plans, ADRs,
  issues, commits, diffs): reference them by path or URL instead.
- Redact sensitive information: API keys, passwords, and personal data.
- If the user passed arguments, treat them as the focus of the next session and
  tailor the document to it.

## Cover
- The goal, and where it stands: done, in progress, blocked.
- The next concrete action, with the command or file to start from.
- Decisions made this session and why, especially ones not yet recorded.
- Open questions and traps you hit on the way.
- Verified state: what was run, what passed, and what is still unverified.

## Checklist
- [ ] Saved outside the workspace, in the OS temporary directory
- [ ] Suggested skills section present
- [ ] No duplication of PRDs, plans, ADRs, issues or commits, only links
- [ ] Secrets, keys and personal data redacted
- [ ] Next action is concrete and unblocked
