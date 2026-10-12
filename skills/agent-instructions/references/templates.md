# Instruction file templates

Starting shapes by project type. Use only the sections that are relevant and
delete the rest; a short accurate file beats a long one.

## Common sections

Commands, architecture, key files, code style, environment, testing, gotchas,
workflow. Each section holds facts an agent cannot cheaply infer from the code.

## Application service

```
# AGENTS.md
## Overview
<one paragraph: what the service does and who calls it>
## Commands
install / dev / test / lint / build / deploy, with the directory to run in
## Architecture
<requests in, data stores, external services, background work>
## Key files
<entry point, config, the file to touch for the common change>
## Environment
<required variables, how to obtain them, test-mode values>
## Testing
<how to run one test, where fixtures live, what must be mocked>
## Gotchas
<non-obvious behaviour that costs time if missed>
```

## Monorepo

- A root file for shared commands, layout, and the map of packages.
- A nested file per package for its own commands, entry points, and quirks.
- In the root file, state which nested file to read for a given area, so an
  agent does not load every one.

## Library

- Emphasise the public surface, versioning rules, and how to run the example or
  test suite.
- Name the compatibility promise and where release notes live.

## Data or ML repository

- How to get data, where it lives, and what is safe to run locally.
- How to reproduce a training or evaluation run, and its cost.

## Rules for any template

- Lead with the commands an agent will run most often.
- One fact per line; drop adjectives.
- Link to the deeper doc instead of copying it.
- Keep a local override file for personal preferences, untracked, so shared
  content stays team-neutral.
