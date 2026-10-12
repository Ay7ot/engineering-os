---
name: better-layout
description: Layout structure for web interfaces: grouping with space, alignment edges, reading order, progressive disclosure, control spacing, full-bleed content and adaptive breakpoints. Use when structuring a page or component, or reviewing spacing and responsive collapse. Not for visual polish.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/jakubkrehel/skills/tree/main/skills/better-layout
  license: MIT
---
# Layout That Communicates Structure

Layout communicates before a word is read: position, spacing and alignment carry
hierarchy on their own, and generous space beats decoration. A good layout
survives stress: resize it, translate it, mirror it for RTL, and it still holds.

## When to use
- Structuring a page, panel or component, or deciding what collapses at small
  sizes.
- Spacing or aligning controls, grouping content, or ordering by importance.
- Handling RTL and direction-aware layout.
- Reviewing frontend code for layout structure.

Related: `better-accessibility` owns hit-area sizes and focus behaviour,
`better-ui` owns radius, shadows and animation, `better-typography` owns line
length and text spacing.

The numeric values below are starting points for interfaces with no established
density or spacing system. Preserve deliberate platform chrome, compact
professional tools and project tokens when they remain usable under hit-area,
zoom, localization and viewport stress tests.

## Match the project's styling system
Express every change in the system already in use: Tailwind utilities, plain CSS
declarations, CSS Modules, CSS-in-JS. Never introduce a second styling approach
to apply a layout fix.

## Rules
1. Group with space, not lines. Negative space is the primary grouping tool,
   background shapes second, separator lines last and only where space cannot
   carry the structure. The gap between groups must be at least twice the gap
   within a group, for example `8px` inside and `16px` or more between, or the
   grouping reads as noise.
2. Keep controls distinct from content. Interactive elements must look
   interactive: a background shape, a border, or a consistent placement zone.
   Never style a control identically to adjacent static text.
3. Align to shared edges and stick to them; every stray edge reads as noise. Use
   one project spacing step per level of subordination (`16px` is a useful
   default). Use logical properties (`padding-inline-start`,
   `margin-inline-end`) for direction-dependent layout, and reserve physical
   left and right for genuinely physical geometry.
4. Order by importance. The most important content sits near the top and the
   leading edge, and reading order flows top to bottom, leading to trailing.
   Think leading and trailing, not left and right.
5. Hint at hidden content. Progressive disclosure needs a visible affordance:
   use the project's established cue, or let the next item peek `16px` to `32px`
   past the scroll edge, or show a disclosure control. Content hidden with zero
   cue may as well not exist.
6. Give targets breathing room. Without an established density system, start
   with `12px` between adjacent bordered or filled controls and `24px` of
   clearance around borderless text-only and icon-only controls. Compact layouts
   may use less when hit areas do not overlap and controls stay visually
   distinct.
7. Inset buttons from the edges. In content layouts keep full-width buttons
   inside the layout margins (starting near `16px` inline on mobile) with a
   visible radius. Edge-to-edge actions are fine when they intentionally follow
   established platform or application chrome, respect safe areas, and stay
   distinguishable from system UI.
8. Content bleeds, controls float. Backgrounds and media extend to the viewport
   edges; controls and text stay inside the layout margins and safe areas
   (`env(safe-area-inset-*)`). Sticky chrome floats above the content layer and
   does not dam it.
9. Hold structure until it breaks. Breakpoints come from the content, not device
   presets: keep the expanded layout as long as it genuinely fits and collapse
   late. Prefer container queries for component-level adaptation. Test the
   smallest and largest sizes first.
10. Plan for growth and clipping. Plan for substantial, language-dependent
    string growth rather than one universal percentage: no fixed widths or
    heights on text containers, and let rows wrap. Never park a critical action
    where resizing or scrolling clips it; keep it in the normal flow or in stable
    chrome.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| A separator line where spacing would do | Remove the line and double the gap between groups |
| `margin-left` or `padding-right` in a localizable layout | `margin-inline-start` or `padding-inline-end` |
| A content-layout button touching the viewport edge | Inset it within the project margins, or keep deliberate platform chrome |
| A carousel that looks complete | Let the next item peek `16px` to `32px` past the edge |
| Adjacent controls merge, or expanded hit areas overlap | Increase the gap on the project scale; `12px` and `24px` are starting points |
| Breakpoints at 768 or 1024 because they are defaults | Break where the content stops fitting |
| A fixed-width text container sized to one language | `max-width` plus wrapping; test pseudo-localization and representative locales |
| The primary action sits at a clip-prone pane bottom | Sticky positioning or stable chrome with safe-area padding |

## Review output
For a standalone layout review, present findings in one table with Severity,
Location, Before, After and Why columns; never separate Before and After lines.
HIGH blocks content or an action at a supported viewport, MEDIUM harms hierarchy,
reading order or adaptability, LOW is isolated alignment or spacing polish.
Cite `path/to/file:line`, or the exact screen and component when there are no
source files. Consolidate a systemic issue into one row and list every location.
Then list the checks run across the relevant widths, reading order, zoom and RTL
state, and give a verdict: Block with any HIGH left, Needs changes for MEDIUM or
LOW only, Approve when nothing actionable remains. If another review skill is
orchestrating, hand it the evidence and let its format win.

## Checklist
- [ ] Grouping carried by space; separators used only where space cannot work
- [ ] Between-group gap at least twice the within-group gap
- [ ] Controls visually distinct from adjacent static text
- [ ] Shared alignment edges; logical properties for direction-dependent layout
- [ ] Reading order top to bottom, leading to trailing
- [ ] Hidden content has a visible cue, with the next item peeking
- [ ] Control spacing follows the project scale, no overlapping hit areas
- [ ] Backgrounds and media bleed; controls and text inset, with safe areas
- [ ] Breakpoints derived from content; smallest and largest sizes tested
- [ ] Text containers wrap; no fixed sizes that clip on other languages
- [ ] Findings reported as a table with a verdict
