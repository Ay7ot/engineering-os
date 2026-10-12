---
name: ui-ux-pro-max
description: A priority-ordered design rule set for web and mobile UI covering accessibility, touch, performance, layout, typography, colour, motion and charts. Use when building or reviewing a screen, page or component and you need concrete thresholds.
metadata:
  audience: builder, reviewer, architect
  upstream: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
  license: MIT
---
# UI/UX Pro Max

A priority-ordered catalogue of UX and UI rules, styles, palettes, font pairings
and chart types, so the rules that block delivery are never traded against the
rules that only polish it.

## When to use
- Building a new screen, page or component and choosing layout, type, colour.
- Reviewing UI code for UX and accessibility defects.
- Choosing a palette, a font pairing or a chart type for a product.

For palette mechanics and contrast maths, use `better-colors`. For type scale
and wrapping, use `better-typography`. For charts, use `dataviz`. For a full
accessibility audit, use `wcag-accessibility`.

## Priority order
Fix top down. Never trade a critical rule for a medium one.

| Priority | Category | Impact |
|---|---|---|
| 1 | Accessibility | critical |
| 2 | Touch and interaction | critical |
| 3 | Performance | high |
| 4 | Layout and responsive | high |
| 5 | Typography and colour | medium |
| 6 | Animation | medium |
| 7 | Style selection | medium |
| 8 | Charts and data | low |

The full rule list, with every threshold, is in
`references/rules-catalogue.md`.

## The rules that block delivery
- Contrast: 4.5:1 minimum for normal text, 3:1 for large text.
- Visible focus rings on every interactive element.
- Descriptive alt text on meaningful images; `aria-label` on icon-only buttons.
- Form inputs have a real label associated with the field, not just a
  placeholder; tab order matches visual order.
- Touch targets at least 44 by 44 px.
- Disable a button while its async action runs; show the spinner on the button.
- Error messages next to the problem they describe, not in a summary far away.
- Body text at least 16 px on mobile; line length 65 to 75 characters;
  line-height 1.5 to 1.75.
- Images in a modern format with `srcset` and lazy loading; respect
  `prefers-reduced-motion` and reserve space so async content does not shift the
  layout.
- No horizontal scroll at 375, 768, 1024 and 1440 px.

## Workflow
1. Extract the brief: product type, style keywords, industry, and stack.
2. Choose the system in order: layout pattern, style, palette, type pairing, then
   chart types, following `references/design-system-choices.md`.
3. Apply the priority order to the result. A palette that fails contrast is a
   defect however it was chosen.
4. Review against the pre-delivery checks below.

## Pre-delivery checks
- Visual quality: one SVG icon set and never emoji; hover states that do not
  shift the layout; theme colours referenced directly.
- Interaction and modes: pointer cursor and hover feedback on clickable
  elements; transitions around 150 to 300 ms; visible keyboard focus; light and
  dark mode both tested, with borders and glass surfaces visible in each.
- Layout and accessibility: floating elements keep their distance from edges and
  nothing hides behind a fixed bar; images have alt text and inputs have labels;
  colour is never the only state signal.

## Checklist
- [ ] Priority order applied; no critical defect traded for polish
- [ ] Contrast, focus, labels and alt text verified
- [ ] Touch targets and button states checked
- [ ] Responsive at 375, 768, 1024 and 1440 px, no horizontal scroll
- [ ] Light and dark mode both reviewed
- [ ] Reduced motion respected
- [ ] Charts have an accessible alternative
