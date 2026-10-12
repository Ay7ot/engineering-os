---
name: redesign-existing-projects
description: Audit an existing site or app and upgrade it to premium quality without breaking it: generic fonts and colours, layout, spacing, missing states and content. Use when asked to redesign, modernise or polish a project that already exists. Not for greenfield builds.
metadata:
  audience: builder, architect
  upstream: https://github.com/leonxlnx/taste-skill/tree/main/skills/redesign-skill
  license: MIT
---
# Redesign Existing Projects

Upgrade an existing site or app to high-end quality in place. Works with any CSS
framework or vanilla CSS.

## When to use
- A project already exists and the user wants it to look or feel better.
- Modernising a dated site without a rewrite, or hardening it before launch.
- For a brand-new page with no existing code, use `design-taste-frontend` or
  `frontend-design` instead.

## Sequence
1. **Scan.** Read the codebase. Identify the framework, styling method (Tailwind,
   plain CSS, CSS Modules, styled-components) and the current patterns.
2. **Diagnose.** Walk the audit in references/audit-checklist.md. List every
   generic pattern, weak point and missing state you find.
3. **Fix.** Apply targeted upgrades inside the existing stack. Do not rewrite
   from scratch and do not migrate frameworks or styling libraries.

## Highest impact first
Apply in this order and stop when the brief is satisfied.
1. Font swap: the largest instant improvement, the lowest risk.
2. Colour cleanup: remove clashing or oversaturated colours.
3. Hover, active and focus states: makes the interface feel alive.
4. Layout and spacing: proper grid, `max-width` container, consistent padding.
5. Replace generic components with less obvious alternatives.
6. Loading, empty and error states: makes it feel finished.
7. Typography scale and spacing polish: the final premium touch.

## Rules
- Before importing any library, check the dependency manifest; never assume a
  package exists.
- If the project uses Tailwind, check whether it is v3 or v4 before touching
  config (see `tailwind-design-system`).
- If there is no framework, use vanilla CSS in the project's existing style.
- Keep changes reviewable: small targeted improvements beat big rewrites.
- Run the project after each change and confirm existing behaviour still works.
- Do not add code comments unless they explain non-obvious rationale.

## What not to break
Ask before changing: URL structure and slugs, primary nav labels, form field
names or order, the brand logo or wordmark, legal and consent copy, and any
event names or section IDs that analytics depends on.

## Common fixes at a glance
- Replace browser defaults and Inter with a font that has character; add Medium
  (500) and SemiBold (600) between Regular and Bold; turn on
  `font-variant-numeric: tabular-nums` for changing numbers; fix orphans with
  `text-wrap: balance` or `text-wrap: pretty`.
- Replace pure `#000000` backgrounds with off-black or tinted dark; keep one
  accent under 80% saturation; stay inside one grey family; tint shadows to the
  background hue; break up flat sections with imagery or subtle texture.
- Break symmetry: replace three equal feature cards with a 2-column zigzag, an
  asymmetric grid or a masonry layout. Replace `height: 100vh` with
  `min-height: 100dvh`. Add a container near 1200 to 1440px with auto margins.
- Add hover and pressed feedback (200 to 300ms transitions), a visible focus
  ring, skeleton loaders, and composed empty and error states. Never use
  `window.alert()`.
- Replace placeholder people, companies and numbers with realistic, contextual
  content, and cut copy cliches (elevate, seamless, unleash, next-gen).
- Improve code quality while you are in there: semantic HTML instead of div
  soup, no inline styles mixed with classes, relative units instead of hardcoded
  pixel widths, real alt text, a documented z-index scale, and verified imports.

Deeper lists, including component patterns, iconography and the omissions most
generated designs forget: references/audit-checklist.md. Bigger structural
upgrades: references/upgrade-techniques.md.

## Checklist
- [ ] Framework and styling method identified before editing
- [ ] Audit written down with every generic pattern and missing state
- [ ] Changes use the existing stack; no framework or styling migration
- [ ] Fixes applied in the priority order above
- [ ] Hover, active, focus, loading, empty and error states present
- [ ] Realistic names, numbers and copy; no cliches or lorem ipsum
- [ ] No silent changes to routes, nav labels, form fields, logo or legal copy
- [ ] App still works after each change; dependencies verified before import
