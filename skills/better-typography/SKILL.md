---
name: better-typography
description: Web typography rules: font choice and pairing, formats, type scale, heading hierarchy, line-height, letter-spacing, measure, wrapping, truncation and underlines. Use when picking fonts, setting a type scale, or reviewing how text renders and wraps. Not for colours or layout.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/jakubkrehel/skills/tree/main/skills/better-typography
  license: MIT
---
# Typography

Good typography is mostly restraint: a sensible scale, comfortable spacing and
enough contrast beat any clever effect. A label, a table cell, a headline and
an article paragraph do not share one set of rules.

## When to use
- Choosing or pairing typefaces, or loading font files.
- Setting a type scale, heading hierarchy, line-height or letter-spacing.
- Fixing measure, wrapping, truncation, underlines or mobile input sizing.
- Reviewing code for how text renders, wraps and behaves.

Related: `better-colors` owns contrast measurement, `better-layout` owns spatial
RTL layout and logical properties, `better-accessibility` owns heading semantics
and text alternatives.

## Match the project's styling system
Before writing any fix, check how the codebase styles things and express every
change in that system: Tailwind utilities in a Tailwind project, plain
declarations in CSS, or the project's CSS Modules, styled-components or StyleX.
Never introduce a second styling approach to apply a typography fix.

## Rules
1. Serve `.woff2` on the web (Brotli, broadly supported). `.woff` is a
   fallback for very old browsers; `.ttf` and `.otf` are raw desktop formats
   with no web compression. How the files load is the project's concern.
2. When a CSS property exists, use it: `font-weight: 650` over
   `font-variation-settings: "wght" 650`, `font-optical-sizing: auto` over
   `"opsz"`, `font-variant-numeric: tabular-nums` over
   `font-feature-settings: "tnum" 1`. Properties keep working when a
   non-variable fallback renders. Reserve raw tags for custom axes
   (`"GRAD" 80`) and features with no property of their own (`"ss01" 1`).
3. Load the faces the design actually uses; browsers synthesize missing weights
   and styles. Set `font-synthesis: none` only after verifying that bold,
   italic, small-caps, superscript and subscript stay visually distinct across
   the whole fallback stack.
4. Rarely more than three fonts. Pair for contrast, not similarity: a serif
   headline with a sans body reads as deliberate; two near-identical sans faces
   read as a mistake. Below `18px` stay at weight `400` or heavier; weights
   under `300` are display-only (`28px` and up).
5. Define a small set of sizes and deviate as little as possible. Solo projects
   can use default names such as `text-sm` if usage rules are clear; on a team
   name sizes by use (`text-body-sm`), not by size.
6. Heading sizes descend with level. Adjacent levels may share a size toward the
   small end of the scale as long as weight or spacing keeps them distinct. Pick
   heading elements for semantics, then set the visual size in CSS.
7. Line-height by role: headings near `1.1`, body `1.5` to `1.6`, unitless so it
   scales with font size. Anything that wraps to three or more lines needs at
   least `1.4`, even in height-constrained rows.
8. Letter-spacing by size: slightly negative on large headings, slightly
   positive on small uppercase labels, neither at reading sizes.
9. Cap the measure around 60 to 75 characters per line. `65ch` measures
   directly; at `16px` body size that lands near `560px` to `680px`, so
   `max-w-xl` or `max-w-2xl` fit. What matters is that a cap exists.
10. Wrap deliberately: `text-wrap: balance` on headings, `text-wrap: pretty` on
    descriptions, neither in long-form text. `overflow-wrap: break-word` where
    long words, links or IDs could escape. `white-space: nowrap` on labels and
    badges where a break looks broken.
11. `font-variant-numeric: tabular-nums` on any value that changes: digits have
    different widths by default, so timers, counters and prices shift layout.
12. Truncate without losing content: single line is `text-overflow: ellipsis`
    with `overflow: hidden` and `white-space: nowrap`; multiple lines is
    `line-clamp`. If the missing text matters, keep the full value reachable in
    a tooltip or expanded view.
13. Store text in natural case and control presentation with `text-transform`,
    so redesigns never rewrite copy. Use smart punctuation: curly quotes in
    prose and straight quotes in code, the single ellipsis character, a
    non-breaking space to keep values such as `16 px` together, a soft hyphen to
    control where long words may break.
14. Underlines from the font: `text-underline-position: from-font` and
    `text-decoration-thickness: from-font`, tuned with `text-underline-offset`
    and `text-decoration-skip-ink`. `text-decoration-style: dotted` is a common
    hint that a word carries extra information. Only colour animates reliably on
    a real underline, so build an animated underline as a separate element.
15. Inputs at `16px` on mobile: iOS Safari zooms the page when input text is
    smaller. Ask which fix the design wants: size the input up on mobile
    (`text-base sm:text-sm`), or keep `font-size: 16px` and render the intended
    size with `transform: scale()`, compensating width and line-height.
16. Size floors: start long-form body near the browser default of `16px`, then
    judge it in the actual typeface, measure, platform and density. UI text can
    go to `14px` for inputs and menus (`16px` on mobile), `13px` for captions,
    rarely below `12px`. When text looks low-contrast, measure with
    `better-colors` and classify with `better-accessibility`; do not change
    colours unless asked.
17. On macOS text renders heavier than intended: apply
    `-webkit-font-smoothing: antialiased` and
    `-moz-osx-font-smoothing: grayscale` (Tailwind `antialiased`) once on the
    root layout so they cover all text.
18. Set `lang` so browsers and assistive technology choose the right
    pronunciation, quotes and hyphenation. Set `dir` where direction changes,
    preserve digit order, and use `<bdi>` for isolated mixed-direction values.
19. Keep useful text selectable. `::selection` can carry brand when the selected
    combination stays legible. Use `user-select: none` only on a specific
    draggable or gesture surface where accidental selection interferes.

## Review output
When the user asks for a standalone typography review, present findings in one
table with Severity, Location, Before, After and Why columns; never separate
Before and After lines. HIGH makes text unreadable or structurally misleading,
MEDIUM harms hierarchy, wrapping or scanning, LOW is polish. Cite
`path/to/file:line`, or the exact screen and component when there are no source
files. Consolidate a systemic issue into one row and list every affected
location. Then list the checks run (wrapping, hierarchy, resize, font loading,
dynamic values) and give a verdict: Block with any HIGH left, Needs changes for
MEDIUM or LOW only, Approve when nothing actionable remains. If another review
skill is orchestrating, hand it the evidence and let its format win.

## Checklist
- [ ] `.woff2` served; the faces the design uses are loaded
- [ ] High-level CSS properties used instead of raw variation tags
- [ ] Three fonts or fewer; contrast pairing; no thin weights below `18px`
- [ ] Type scale defined; heading sizes descend with level
- [ ] Line-height by role; `1.4` minimum on anything wrapping to 3+ lines
- [ ] Measure capped near 60 to 75 characters
- [ ] `text-wrap`, `overflow-wrap` and `nowrap` set where they belong
- [ ] `tabular-nums` on changing values
- [ ] Truncation keeps the full value reachable
- [ ] Inputs hold `16px` on mobile by one of the two agreed fixes
- [ ] Root layout applies font smoothing once
- [ ] `lang` and `dir` set; mixed-direction values isolated
- [ ] Findings reported as a table with a verdict, or the orchestrator's format
