---
name: better-ui
description: Design engineering details that make interfaces feel polished: concentric radii, optical alignment, shadows, interruptible enter and exit animation, icon stroke and state handling, and motion restraint. Use when building or reviewing UI components, states, icons or micro-interactions.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/jakubkrehel/skills/tree/main/skills/better-ui
  license: MIT
---
# Details That Make Interfaces Feel Better

Great interfaces are rarely one thing: they are small details that compound.
Preserve the project's component library, tokens and density, and match its
established motion language except where a rule below prescribes an exact
pattern.

## When to use
- Building or refining UI components, surfaces, icons or interactions.
- Implementing enter, exit, hover, press and loading feedback.
- A screen "feels off" and the cause is a detail rather than the layout.

Related: `better-typography` owns anything text-related, `better-layout` owns
grouping, spacing and breakpoints, `better-accessibility` owns hit areas, focus
and keyboard behaviour, and `animate` owns motion design direction.

## Rules
1. Concentric radius: outer radius equals inner radius plus padding. Mismatched
   radii on nested elements is the most common cause of "off" interfaces.
2. Optical over geometric alignment: when geometric centering looks wrong, align
   optically. Buttons with icons, play triangles and asymmetric icons all need
   manual nudging.
3. Shadows for elevation, borders for structure. Where a border exists only to
   create depth on a button, card or container, prefer layered transparent
   `box-shadow` values. Keep borders that communicate structure or state:
   dividers, layout separators, selected and focus states.
4. Interruptible animation: use CSS transitions for interactive state changes
   because they can be interrupted mid-flight. Reserve keyframes for staged
   sequences that run once.
5. Split and stagger entrances: for an infrequent staged entrance where sequence
   communicates hierarchy, break the content into semantic chunks and stagger by
   about `100ms` rather than animating one container. Never stagger routine,
   high-frequency interactions.
6. Subtle exits: use a small fixed `translateY` rather than a full height
   collapse. Exits are softer than enters, and `ease-out` suits both.
7. Contextual icon animations: animate with `opacity`, `scale` and `blur`
   instead of toggling visibility. Use exactly scale `0.25` to `1`, opacity `0`
   to `1`, blur `4px` to `0px`. With `motion` or `framer-motion` in the
   dependency manifest, match that package's import path and use
   `transition: { type: "spring", duration: 0.3, bounce: 0 }`; bounce is always
   `0`. With no motion library, keep both icons in the DOM (one absolutely
   positioned) and cross-fade with CSS using `cubic-bezier(0.2, 0, 0, 1)`.
8. Image outlines: a subtle `1px` low-opacity outline keeps image depth
   consistent. It must be pure black in light mode (`oklch(0 0 0 / 0.1)`) and
   pure white in dark mode (`oklch(1 0 0 / 0.1)`), never a tinted near-black such
   as slate or zinc, which picks up the surface colour and reads as dirt.
9. Scale on press: `scale(0.96)` on click gives tactile feedback. Always `0.96`;
   never below `0.95`, which feels exaggerated. Offer a way to disable it where
   motion would distract.
10. Skip animation on first render: prevent enter animations on page load for
    stateful icons and toggles. Verify that intentional page entrances still
    play.
11. Never `transition: all`. Name the properties, for example
    `transition-property: scale, opacity`. Tailwind's `transition-transform`
    covers transform, translate, scale and rotate.
12. Use `will-change` sparingly: only for `transform`, `opacity` and `filter`,
    and only once you see first-frame stutter. Never `will-change: all`.
13. Match icon stroke to text weight: about `1.5px` beside regular (400) text
    and `2px` beside semibold (600). One stroke weight per icon set, and never
    mix libraries on one surface.
14. One SVG per icon, recoloured per state: icons use `currentColor` and get
    hover, selected and disabled states from CSS colour and opacity, never from
    separate assets. Outline is the default; fill marks the active state.
15. Motion restraint: no custom animation on high-frequency interactions, where
    the attention cost repeats on every trigger, and never let motion be the
    only feedback channel. Every animated state change also needs a static cue:
    colour, icon or label.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Nested parent and child share one radius | `outerRadius = innerRadius + padding` |
| Icons look off-centre | Adjust optically with padding, or fix the SVG |
| A border used only to fake elevation | Layered transparent `box-shadow`; keep structural and state borders |
| Jarring staged entrance or contextual exit | Stagger infrequent entrances; keep context-preserving exits subtle |
| A stateful icon animates its default state on load | Skip the enter animation on first render; keep page entrances |
| `transition: all` | Specify the exact properties |
| First-frame animation stutter | Add `will-change: transform`, sparingly |
| Hairline icon beside bold text | Match the stroke width to the text weight |
| A separate icon asset per state | One `currentColor` SVG with CSS states |
| Filled icons everywhere | Outline by default, fill for the active state |
| Entrance animation on every hover or keystroke | Instant feedback, or an opacity or colour transition of `150ms` or less |

## Review output
For a standalone UI polish review, slow the interface down: replay motion at 10%
speed in the animations panel and walk hover, focus, active, loading and empty
states. Present findings in one table with Severity, Location, Before, After and
Why columns; never separate Before and After lines. HIGH makes an interaction
misleading, unresponsive or repeatedly disruptive, MEDIUM is a noticeable craft
or consistency problem, LOW is isolated polish. Cite `path/to/file:line`, or
the exact screen and component when there are no source files. Consolidate a
systemic issue into one row and list every location. Then list the checks run
and give a verdict: Block with any HIGH left, Needs changes for MEDIUM or LOW
only, Approve when nothing actionable remains. If another review skill is
orchestrating, hand it the evidence and let its format win.

## Checklist
- [ ] Nested radii are concentric, or nested surfaces share no radius
- [ ] Icons optically aligned; stroke weight matches the adjacent text weight
- [ ] Elevation from layered shadows; structural and state borders kept
- [ ] Interactive state changes use interruptible transitions
- [ ] Entrances staggered only where sequence means something; exits subtle
- [ ] Icon transitions use the exact scale, opacity and blur values
- [ ] Press feedback at `scale(0.96)`
- [ ] No `transition: all`; `will-change` only where stutter was seen
- [ ] Motion never the only feedback; every animated change has a static cue
- [ ] States walked at slow replay, including loading and empty
