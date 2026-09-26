# USER.md — Operator Profile (edit me)

Your private profile lives at `<data>/USER.md` (default `~/EngineeringOS/data/USER.md`).
`eng setup` seeds it from this example on first run. Agents read it before asking
working-style questions, so keep it about *you and how you work* — no secrets.

- Role: <e.g. software engineer + technical architect, across design, implementation, review>
- Primary coding tool: <e.g. OpenCode / Codex / Claude Code>
- What I provide: business/product intent, constraints, answers to decisions needing human judgment, architectural approval, final approval for consequential changes.
- What agents handle: research, repo exploration, requirements, architecture discovery/proposals, tradeoff analysis, planning, implementation, testing, debugging, review, security review, documentation, state/knowledge management, coordination.
- Goal: make me a better architect. Explain architectural reasoning (why this fits this system, alternatives, tradeoffs, risks, confidence) — don't hide behind "best practice". Don't pretend certainty where evidence is weak.
- Minimize questions. First inspect repo, project docs, EngineeringOS knowledge, official docs, existing implementations, run tests/commands. Ask only for genuine human/product judgment or significant consequences.
- Approval gates (always ask): major architecture decisions, destructive DB migrations, production deploys, security-sensitive changes, irreversible data ops, significant infra changes, major product behavior, substantial cost implications. Routine implementation details: infer safely, don't ask.
- Preferences (defaults — update as we learn):
  - Simplicity first: filesystem + Git + SQLite + MCP + shell/Python scripts before new infra.
  - Deterministic verification: compilers, type checks, tests, lint, build, static analysis over LLM opinion.
  - Small tasks with acceptance criteria; parallelize with git worktrees, never two writers on one tree.
  - Conventional commits; ADRs for significant decisions.
