# Security Policy

## Reporting a vulnerability

Please report security issues **privately**, using GitHub's private
vulnerability reporting:

https://github.com/Ay7ot/engineering-os/security/advisories/new

Do not open a public issue, and do not include secrets or personal data in any
report. You will get an acknowledgement as soon as the maintainer sees it, and
credit in the advisory if you want it.

## What is in scope

The public engine repository:

- `scripts/eng` — the bootstrap/health/worktree CLI
- `mcp/engineering-memory/server.py` — the stdio MCP server
- `opencode/` — agent, skill, and command definitions
- `.github/` — CI and repo configuration, including branch protection

## What is out of scope

- Your private data directory (`~/EngineeringOS/data`, or `$ENGINEERING_OS_DATA`).
  That is your content, not part of this project.
- OpenCode itself, and any other agent runtime. Report those to their projects.
- Anything that requires an attacker to already have local code execution or
  write access to your machine.

## Design expectations you can rely on

- The engine contains **no personal data** and **no secrets**, by rule
  (`PRINCIPLES.md` §7).
- The MCP server is **stdlib-only** and speaks newline-delimited JSON-RPC over
  stdio. It does not listen on a network port.
- The data directory is the only coupling point, via `$ENGINEERING_OS_DATA`.
  Nothing is ever written outside the engine, the data directory, and
  `~/.config/opencode/`.
- Privileged operations (production deploys, destructive migrations,
  irreversible data changes) require explicit human approval.

## If you find a secret in the repo

If you believe a real credential has been committed, treat it as compromised:
rotate it first, then report the location privately. Do not assume deleting the
commit is enough, because history is public.
