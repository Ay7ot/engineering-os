---
name: accessibility-expert
description: A fast WCAG 2.2 reference for inclusive interfaces: level A, AA and AAA requirements, semantic HTML swaps, ARIA patterns, keyboard keys, contrast numbers and testing tools. Use when you need a quick a11y checklist while building or reviewing a page. For a full audit use `wcag-accessibility`.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/slb2248/ai-ux-skills/tree/main/skills/accessibility-expert
  license: MIT
---
# Accessibility Expert

## When to use
- You need a quick accessibility checklist or pattern while building a page.
- Reviewing a page against the WCAG 2.2 levels and the common patterns.

Create inclusive digital experiences that work for everyone. This is the quick
reference; for full WCAG 2.2 criteria and remediation use `wcag-accessibility`, and for
component-level focus and screen-reader craft use `better-accessibility`.

## WCAG 2.2 quick reference
**Level A (minimum)**: all images have alt text, videos have captions, content is
keyboard accessible, no seizure-triggering content, pages have titles.

**Level AA (the target for most sites)**: 4.5:1 contrast for text, 3:1 contrast
for UI components, text resizable to 200%, focus visible on all interactive
elements, error suggestions provided.

**Level AAA (enhanced)**: 7:1 contrast ratio, sign language for video, extended
audio descriptions, no timing-based interactions.

## Semantic HTML first
Prefer the semantic element over a styled `div`: `<nav>` not
`<div class="nav">`, `<button>` not `<div onclick>`, `<main>` not
`<div id="main">`, `<article>` not `<div class="article">`. Keep a proper heading
hierarchy: one `<h1>`, then `<h2>` for sections and `<h3>` for subsections.

## ARIA when needed
Only when HTML semantics are not enough. Give composite widgets the right roles
and states (`role="tablist"` with `role="tab"` buttons and `aria-selected`), use
live regions for dynamic content (`aria-live="polite"` for status,
`aria-live="assertive"` for errors), and connect descriptions with
`aria-describedby`. `references/patterns.md` has the markup for all three.

## Keyboard navigation
Focus management: a visible focus indicator on every interactive element, a
logical tab order that follows the visual order, a skip link to the main content,
and a focus trap in modals that returns focus to the trigger on close.

| Key | Action |
| --- | --- |
| Tab | Move to the next element |
| Shift+Tab | Move to the previous element |
| Enter / Space | Activate a button |
| Arrow keys | Navigate within a component |
| Escape | Close a modal or menu |

## Screen reader support
Structure: use landmarks (main, nav, aside, footer), write descriptive link text
rather than "click here", announce dynamic changes, and provide text alternatives.

Testing checklist:
- [ ] Can navigate with the keyboard only
- [ ] Screen reader announces all content
- [ ] Focus order makes sense
- [ ] Dynamic content is announced
- [ ] Forms have proper labels
- [ ] Errors are clearly communicated

## Colour and contrast
Do not rely on colour alone: add icons or patterns, use text labels, and provide
multiple indicators. Normal text needs 4.5:1, large text (18px+) 3:1, UI
components 3:1, and focus indicators 3:1.

## Forms
Every input needs a visible `<label for>` with a matching `id`; group related
fields in a `<fieldset>` with a `<legend>`; report errors with
`aria-invalid="true"`, an `aria-describedby` pointing at the message, and
`role="alert"` on the message. `references/patterns.md` has the markup.

## Testing tools
- **axe DevTools**: browser extension.
- **WAVE**: web accessibility evaluation.
- **Lighthouse**: built into Chrome.
- **NVDA / VoiceOver**: screen readers.
- **Colour Contrast Analyser**: check contrast.

## Checklist
- [ ] Alt text, captions and page titles present
- [ ] Semantic elements used; headings form a proper hierarchy
- [ ] ARIA limited to cases native HTML cannot cover
- [ ] Focus visible, tab order logical, skip link and modal focus trap present
- [ ] Contrast meets 4.5:1 text and 3:1 UI and focus indicators
- [ ] Labels, error messages and responsive text resize handled
- [ ] Checked with an automated tool and a screen reader
