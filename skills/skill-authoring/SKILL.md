---
name: skill-authoring
description: Write or improve an EngineeringOS skill so agents load it at the right moment and follow it reliably, and test that it triggers. Use when adding a new skill, changing a skill's scope, or when a skill is being ignored or loaded for the wrong tasks.
metadata:
  audience: lead
---
# Skill Authoring

## When to use
- Adding a new playbook to `skills/`.
- A skill is not being picked up when it should be, or is picked up for the
  wrong tasks.
- Splitting or merging skills.

## How skills get chosen
Agents see only each skill's `description` until they decide to load it. The
description is the trigger: if it does not say *when* to use the skill, in the
words a task would actually use, the skill will be skipped.

## Write the description
- First sentence: what the skill does.
- Then a "Use when ..." sentence naming the concrete situations, in the
  vocabulary of real requests ("reviewing a PR", "a reported bug").
- Say what it is **not** for if a neighbouring skill could be confused with it.
- One line, at most 300 characters (the tests enforce this). No marketing words.

## Write the body
- `# Title`, then `## When to use`, the procedure, rules, and a `## Checklist`.
  Match the shape of the existing skills.
- Steps an agent can execute and verify. Prefer "run X and check Y" over
  "consider X".
- Name the tools and other skills it relies on (`engineering-memory` tools,
  `diagrams`, `testing`).
- Keep it editor-neutral: no editor-specific tool names or paths. Adapters
  handle editor differences.
- Short. If it passes about 100 lines, it is probably two skills.

## Frontmatter
- `name` equal to the directory name, `description`, optional
  `metadata.audience` (which agents use it).
- YAML subset only: maps and scalars, no lists. The loader rejects anything else
  with `file:line`.
- If the name collides with an editor's built-in skill, the editor's adapter
  renames it on install (see `SKILL_RENAMES` in the Claude adapter). Add the
  rename in the same change.
- **How to refer to another skill:** always write its name in backticks, for
  example `diagrams` or `testing`. Some skills are renamed when installed into an
  editor (see `SKILL_RENAMES`), and the adapter rewrites references to them. A
  one-word renamed name is only rewritten when it is in backticks, so ordinary
  prose using the same word is left alone. Writing such a skill's name as plain
  prose would point agents at the editor's own skill of that name instead; the
  tests flag it. Always write the **source** name (the directory name under
  `skills/`), never an editor's renamed form.

## Test it
1. `python3 tests/test_adapters.py` validates frontmatter and description rules
   for every skill.
2. Trigger check: write three requests that **should** load the skill and three
   that should **not** (they belong to a neighbouring skill). Read the
   description against each. If any is ambiguous, tighten the description.
3. Run `eng sync` and confirm the skill appears in each editor.
4. Use it once on a real task and fix whatever step the agent stumbled on.

## Checklist
- [ ] Description says what it does and "Use when ..."
- [ ] Neighbouring skills distinguished where confusable
- [ ] Body has When to use, procedure, rules, checklist
- [ ] Editor-neutral; references real tools and skills
- [ ] Frontmatter valid; name matches directory; renames added if needed
- [ ] Tests pass; trigger check done; synced to editors
