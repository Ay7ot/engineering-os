---
name: wayfinder
description: Chart a shared map of investigation tickets on the issue tracker for work too big for one agent session, then resolve them one at a time until the route is clear. Use when a loose idea is wrapped in fog and the destination is not yet visible.
metadata:
  audience: planner, lead, architect
  upstream: https://github.com/mattpocock/skills/tree/main/skills/in-progress/wayfinder
  license: MIT
---
# Wayfinder

A loose idea has arrived, too big for one agent session, wrapped in fog: the way
from here to the destination is not visible yet. Wayfinding finds that way,
charting the route as a shared map on the issue tracker and resolving its tickets
one at a time. Naming the destination comes first; it shapes every ticket, and
might be a spec to hand off, a decision to lock, or a change made in place.

## When to use
- Work is too large for one session and the route is unclear.
- Several decisions must settle one at a time before implementation starts.
- Collaborators need a durable, shared map of where the effort is headed.

## Plan, do not do
Wayfinder is planning by default: each ticket resolves a decision, and the map is
done when nothing is left to decide before someone goes and does the thing. The
pull to just do the work usually means you reached the edge of the map and should
hand off. An effort may override this in its Notes and carry execution into the
map; absent that, produce decisions, not deliverables.

## Refer by name
Every map and ticket is an issue, so it has a name: its title. In everything a
human reads, refer to it by that name, never by a bare id, number or slug: a wall
of `#42, #43, #44` is illegible, while names read at a glance.

## The map
The map is a single issue labelled `wayfinder:map`, the canonical artefact; its
tickets are child issues. The map is an index, not a store: a decision lives in
exactly one place, its ticket, so the map gists it and links, never restates it.
Follow the project's issue-tracker doc for how this repo expresses the map,
blocking and frontier queries, defaulting to the local markdown tracker when it
is absent. `references/map-format.md` holds the map body template, the ticket
anatomy, the frontier rules, and the four ticket types with when to use each.

## Fog and scope
The map is deliberately incomplete: do not chart what you cannot yet see. Beyond
the live tickets lies the fog, decisions you can tell are coming but cannot yet
pin down; resolving a ticket graduates what is now specifiable into fresh tickets
and clears each patch from Not yet specified. Work beyond the destination is out
of scope, never fog, and it never graduates. The fog-or-ticket test and the
scope boundary rules are in `references/map-format.md`.

## Chart the map
1. **Name the destination** with the user, pinning down the spec, decision or
   change this map is finding its way to. It fixes scope, so settle it first.
2. **Map the frontier** breadth-first: fan out across the whole space rather than
   deep on one thread, surfacing open decisions and the first steps takeable now.
   If this surfaces no fog, the way is already clear and the journey fits one
   session: stop and ask the user how to proceed.
3. **Create the map** with Destination and Notes filled, Decisions so far empty,
   and the fog sketched into Not yet specified.
4. **Create the tickets you can specify now**, then wire blocking edges in a
   second pass, since issues need ids before they can reference each other.
5. Stop. Charting the map is one session's work; do not also resolve tickets.

## Work through the map
A ticket is optional on invocation; without one, you pick the next decision, not
the user. Either way, never resolve more than one ticket per session.
1. Load the map: the low-resolution view, not every ticket body.
2. Choose the ticket: the one the user named, else the first frontier ticket in
   order. Claim it by assigning it to yourself before any work.
3. Resolve it, fetching the full body of any related or closed ticket on demand
   and consulting the skills the Notes block names.
4. Record the resolution: post the answer as a resolution comment, close the
   issue, and append a context pointer to Decisions so far.
5. Add newly surfaced tickets (create, then wire) and graduate any fog the answer
   made specifiable, clearing each patch from Not yet specified. If the answer
   puts another ticket beyond the destination, rule it out of scope rather than
   resolving it on the route. If the decision invalidates other map parts, update
   or delete those tickets.

Other sessions may run unblocked tickets in parallel, so expect the tracker to be
edited concurrently.

## Checklist
- [ ] Destination named and scope fixed before any ticketing
- [ ] Map issue created and labelled `wayfinder:map`
- [ ] Tickets are decisions sized to one session, not deliverables
- [ ] Blocking wired natively; frontier is open, unblocked and unclaimed
- [ ] Ticket claimed before work; at most one resolved per session
- [ ] Fog graduated to tickets; out-of-scope tickets closed, not resolved
