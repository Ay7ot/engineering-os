---
name: find-skills
description: Find, vet and install third-party agent skills from the open skills ecosystem using the skills CLI when a task needs a capability this project lacks. Use when asked whether a skill exists for something, or to extend what agents can do.
metadata:
  audience: lead, builder
  upstream: https://github.com/vercel-labs/skills/tree/main/skills/find-skills
  license: MIT
---
# Find Skills

Skills are installable packages of knowledge and workflow. When a request needs
a capability no local skill covers, search the ecosystem before improvising.

## When to use
- "How do I do X" where X is a common, packaged task.
- "Is there a skill for X", "find a skill for X", "can you do X".
- A task needs a tool, template or workflow this project does not have.
- The user wants to extend what the agents can do.

To write or fix a skill in this repository, use `skill-authoring` instead; this
skill installs from outside.

## The CLI
The skills CLI is the package manager for the open skills ecosystem:

```bash
npx skills find [query]     # search interactively or by keyword
npx skills add <package>    # install from GitHub or another source
npx skills check            # check for updates
npx skills update           # update installed skills
npx skills init <name>      # scaffold your own skill
```

Browse the catalogue, ranked by installs, at https://skills.sh/

## Workflow
1. Identify the need: domain (react, testing, design, deployment), the specific
   task, and whether it is common enough that someone packaged it.
2. Check the leaderboard first. Popular, battle-tested packages beat a lucky
   search hit. For web work, official sources such as vercel-labs and
   anthropics dominate.
3. Search by keyword when the leaderboard does not cover it:
   `npx skills find react performance`.
4. Vet before recommending. Do not propose a skill from search results alone.
5. Present the option: name, what it does, install count, source, the install
   command, and a link.
6. Install only if the user agrees: `npx skills add <owner/repo@skill> -g -y`.
   `-g` installs for the user, `-y` skips the confirmation prompt.

## Vet the source
- Install count: prefer 1K or more. Treat anything under 100 with caution.
- Source reputation: an official organisation beats an unknown author.
- Repository health: check the source repo; under about 100 stars deserves
  scepticism.
- Read what the skill actually does before installing. Installed skills run
  with the agent's access, so treat an unknown skill like any untrusted code.

## Search tactics
- Use specific keywords: "react testing" beats "testing".
- Try synonyms when a term fails: deploy, deployment, ci-cd.
- Categories worth trying: web development, testing, devops, documentation,
  code quality, design, productivity.

## When nothing is found
Say so plainly, then offer to do the task with the current tools. If it is
something this project does repeatedly, offer to write a project skill with
`skill-authoring` rather than reinstalling a third-party one.

## Checklist
- [ ] Leaderboard checked before a keyword search
- [ ] Candidate vetted: installs, source reputation, repo stars, actual content
- [ ] Options presented with name, source, install count and command
- [ ] Installed only with the user's agreement
- [ ] No match reported honestly, with a local alternative offered
