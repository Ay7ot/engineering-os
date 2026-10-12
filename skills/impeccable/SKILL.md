---
name: impeccable
description: Design, redesign, critique, audit and polish frontend interfaces against a high craft bar, with hard rules and explicit anti-pattern bans. Use when building or refining UI, when a design looks generic or templated; not for backend-only work.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/pbakaus/impeccable
  license: Apache-2.0
---
# Impeccable

Produce ready-to-ship frontend interfaces, not prototypes or starting points: real code, committed design choices, exceptional craft.

## When to use
- Building a new page, component, form, settings screen or empty state.
- Redesigning or polishing an interface that already exists.
- Auditing a UI for quality, then refining what the audit found.
- A design reads as generic and needs a deliberate direction.

For a design language document, use `create-design-md`. For palette maths, use
`better-colors`. For component-level detail, use `better-ui`. For motion review,
use `animate`. For a full accessibility pass, use `wcag-accessibility`.

## Setup, in order
1. Load project context: the product brief, and the design document when one
   exists. If there is no brief, write one before touching UI. Read at least one
   real project file (tokens, theme, a component or page) and follow what is
   already there.
2. Pick the register: brand, where design is the product (marketing, landing
   page, campaign, long-form content, portfolio); product, where design serves
   the product (app UI, admin, dashboard, tool). Brand and product are lenses on
   the same rules, not separate files: apply `references/general-rules.md`
   through the chosen register.
3. For a brand-new project with no committed brand colour, choose a seed colour
   and compose the palette around it in OKLCH. If committed tokens exist,
   preserve them: identity-preservation wins.

## Rules that decide most outcomes (full rules in `references/general-rules.md`)

- Contrast: body text 4.5:1 or better; large text (18 px, or 14 px bold) 3:1 or
  better; placeholder text gets 4.5:1 too. Greys on a tinted near-white are the
  most common failure.
- Body line length 65 to 75 characters. Never pair two similar-but-not-identical
  fonts; pair on a contrast axis or use one family in several weights.
- Display headings: `clamp()` max at or below 6rem, letter-spacing not tighter
  than -0.04em. Use `text-wrap: balance` on h1 to h3.
- Vary spacing for rhythm. Cards only when they are the best affordance, never
  nested. Flexbox for one dimension, grid for two.
- Semantic z-index scale (dropdown, sticky, modal backdrop, modal, toast,
  tooltip), never 999.
- Motion is part of the build, eases out exponentially, never animates layout
  properties, and always has a `prefers-reduced-motion` alternative; reveals
  must enhance an already-visible default, never gate content visibility.
- A dropdown inside an `overflow: hidden` container will be clipped; use the
  dialog or popover API, `position: fixed`, or a portal.

## Absolute bans
Rewrite the element with different structure rather than softening it. The full
list, including near-misses, is in `references/anti-patterns.md`.

- A coloured `border-left` or `border-right` over 1px as a card accent.
- Gradient text via `background-clip: text`.
- Glassmorphism as a default rather than a rare, purposeful choice.
- The hero-metric template, and identical card grids repeated down the page.
- A tiny uppercase eyebrow, or numbered section markers, above every section.

## The slop test
If a stranger could look at the interface and say "AI made that" without doubt,
it failed.
- First-order: if the theme and palette are guessable from the category alone,
  it is the training-data reflex. Rework the brief and the colour strategy until
  the answer is not obvious.
- Second-order: if the aesthetic family is guessable from category plus
  anti-references ("a fintech that is not navy and gold, so terminal dark mode"),
  it is the trap one tier deeper. Rework again.

## Commands
Setup runs first for all of them. Full list in `references/commands.md`.
- Build: shape, craft, init, document, extract.
- Evaluate: critique (UX heuristics) and audit (accessibility, performance,
  responsive).
- Refine: polish, bolder, quieter, distill, harden, onboard.
- Enhance: animate, colorize, typeset, layout, delight, overdrive.
- Fix: clarify, adapt, optimize. Iterate: live.

## Checklist
- [ ] Project context and existing design system read before any change
- [ ] Register chosen (brand or product) and its rules applied
- [ ] Contrast, type scale and spacing verified against the numbers above
- [ ] No banned pattern shipped
- [ ] Reduced-motion alternative present for every animation
- [ ] First-order and second-order slop checks passed
- [ ] Screenshot or live check done at mobile and desktop widths
