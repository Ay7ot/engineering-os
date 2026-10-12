# Map format and ticket anatomy

Reference detail for the `wayfinder` skill. Physical storage is tracker-specific:
follow the project's issue-tracker doc, defaulting to the local markdown tracker.

## The map body

The whole map at low resolution, loaded once per session. Open tickets are NOT
listed; they are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change
this effort is finding its way to. One or two lines; every session orients to it
before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index, one line per closed ticket: enough to judge relevance, then zoom the link for detail -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you cannot ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- work ruled beyond the destination; closed, never graduates -->
```

## Tickets

Every map and ticket is an issue, so it has a name: its title. In narration and
in the map's Decisions so far, refer to it by that name, never by a bare id,
number or slug. The id and URL do not vanish, they ride inside the name.

Each ticket is a child issue of the map; the tracker's issue id is its identity.
Its body is the question, sized to one agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label, one of `research`, `prototype`,
`grilling`, `task`.

A session claims a ticket by assigning it to the dev driving the map, first,
before any work, so concurrent sessions skip it. That assignee is the claim: an
open, unassigned ticket is unclaimed.

Blocking uses the tracker's native dependency relationship, which renders the
frontier visually in the tracker's own UI so the human sees what is takeable
without opening the map. Only a tracker lacking native blocking falls back to a
body convention. A ticket is unblocked when every ticket blocking it is closed;
the frontier is the open, unblocked, unclaimed children.

The answer is not part of the body. It is recorded on resolution: post the answer
as a resolution comment, close the issue, and append a context pointer to
Decisions so far. Assets created while resolving a ticket are linked from the
issue, not pasted in.

## Ticket types

- **Research** (AFK): reading documentation, third-party APIs, or local resources
  such as knowledge bases. Creates a markdown summary as a linked asset. Use when
  knowledge outside the current working directory is required.
- **Prototype** (HITL): raise the fidelity of the discussion by making a cheap,
  rough, concrete artifact to react to: an outline, a rough take, a stub, or
  UI/logic code via `prototype`. Links the prototype as an asset. Use when "how
  should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): conversation, one question at a time. The default case.
- **Task** (HITL or AFK): manual work that must happen before a decision can be
  made, with nothing to decide, prototype or research, but the discussion is
  blocked until it is done. Signing up for a service so its API can be judged,
  provisioning access, moving data so its shape can be seen. This is the one type
  that does rather than decides, and it earns its place by unblocking a decision,
  not by delivering the destination. The agent drives it alone where it can
  (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when
  the work is done; the answer records what was done and any resulting facts
  (credentials location, new URLs, row counts) that later tickets depend on.

## Fog and scope rules

Fog is in scope but not sharp enough to ticket. Not yet specified excludes what
is already decided, what is already a live ticket, and what is out of scope, and
it doubles as a signpost for collaborators reading where the effort is headed.

The test is whether you can state the question precisely now, not whether you can
answer it now:

- **Ticket** when the question is already sharp, even if it is blocked and you
  cannot act on it yet.
- **Not yet specified** when you cannot phrase it that sharply. Do not pre-slice
  the fog into ticket-sized pieces: it is coarser than a ticket, and one patch
  may graduate into several tickets, or none.

Resolving a ticket clears the fog ahead of it, graduating whatever is now
specifiable into fresh tickets, one at a time, until the way to the destination
is clear and no tickets remain. Clear each graduated patch from Not yet specified
so it lives only as its new ticket.

Out of scope is a scoping act, not a step on the route. Ruling something out is
not progress on the way, so it never appears in Decisions so far, which records
the route actually walked. A ticket that turns out to sit past the destination,
mis-scoped in while charting or exposed by a resolution, is closed, and the scope
boundary keeps one line in Out of scope: the gist, why it is out of scope, and a
link to the closed ticket. Because the frontier stops at the destination,
out-of-scope work can only return if the destination is redrawn, and then as a
fresh effort rather than a resumption.
