# Allow architect to write markdown docs only

Date: 2026-09-10T02:08:27+00:00
Project: global

## Context
User requested architect be able to write md files. Prior state was edit:deny (all writes blocked), which caused Write failures when architect tried to produce architecture documents.

## Decision
Architect edit permission changed from blanket deny to granular allowlist: edit *: deny, *.md: allow (last-match-wins per OpenCode permissions docs). Architect may now Write/Edit markdown docs directly; all code writes still denied. Prompt discipline updated to match.

## Alternatives
Full edit:allow (rejected — would let architect modify app code, breaking read-only guarantee). Keep edit:deny (rejected per user — architect needs to write docs).
