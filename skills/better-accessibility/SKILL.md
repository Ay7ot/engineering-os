---
name: better-accessibility
description: Build accessibility into product UI as a craft floor: focus rings, keyboard support, ARIA, forms, screen readers, hit areas, motion and zoom. Use when building or reviewing a component, modal, menu, form or widget, or told to make it accessible. For a full site audit use `wcag-accessibility`.
metadata:
  audience: builder, reviewer, tester
  upstream: https://github.com/jakubkrehel/skills/tree/main/skills/better-accessibility
  license: MIT
---
# Accessibility that comes with the craft

## When to use
- Building or reviewing a component, modal, menu, form or custom widget.
- The user asks to make something accessible, or a keyboard or screen-reader
  problem is reported.

Accessibility is the floor for interface craft, not a compliance checkbox bolted
on at the end. Most of it is free if you use the platform: native elements ship
with keyboard support, real labels announce themselves, and a visible focus ring
is one CSS rule. Match the project's styling system when you fix something.

When reviewing, walk the interface as a keyboard-only user first (every flow must
complete without a mouse), then as a screen-reader user: does each control
announce a name, a role and its state? When unsure, prefer the platform default
over a custom rebuild, and remove ARIA rather than add it.

For full WCAG criteria and remediation use `wcag-accessibility`; for a fast
level-by-level checklist use `accessibility-expert`.

## Principles
1. **Native elements first.** Do not use ARIA when a native element exists.
   `<button>` for actions, `<a href>` for navigation (it must support Cmd, Ctrl
   and middle click), never `<div onClick>`. No ARIA is better than bad ARIA.
2. **Visible focus rings.** Style `:focus-visible`, not bare `:focus`, so
   keyboard users get a ring and mouse users usually do not. Prefer the browser's
   unmodified indicator; a custom ring must be verified against every adjacent
   colour it crosses and in forced-colors mode. Use at least a 2px solid
   perimeter, and never `outline: none` without a verified replacement.
3. **Full keyboard support.** Every pointer interaction needs a keyboard path,
   following the ARIA APG patterns: Escape closes overlays, arrow keys move within
   composite widgets (tabs, menus, listboxes), Tab moves between widgets, Enter
   and Space activate. Only `tabindex="0"` and `tabindex="-1"`, never positive
   values; composite widgets use roving tabindex (active item `0`, others `-1`).
4. **Trap and restore focus.** Modals set `inert` on the background, move focus
   inside on open, and return focus to the trigger on close. Add
   `overscroll-behavior: contain` so background content does not scroll.
5. **Minimum hit area.** WCAG 2.5.8 AA is 24 x 24 CSS pixels, with defined
   spacing, equivalent-control, inline, user-agent and essential exceptions. Aim
   for 44 x 44px in touch contexts and 40 x 40px on desktop when density permits.
   Extend with a pseudo-element if the visible element stays smaller, and never
   let extended hit areas overlap.
6. **Label and type every control.** Every input gets a `<label for>` or a
   wrapping `<label>`; a placeholder is never a label, and label and control share
   one hit target with no dead zones. Add `autocomplete` with a meaningful `name`,
   the correct `type`, and `inputmode` for the keyboard. Never block paste: users
   paste passwords and one-time codes.
7. **Errors that announce.** Keep submit enabled until the request starts, then
   disable with a spinner while keeping the original label. Validate on submit:
   `aria-invalid="true"` on failing fields, `aria-describedby` at the inline error
   text, and focus the first invalid field. Use native `disabled` when a control
   is genuinely unavailable; use `aria-disabled="true"` only when retaining
   focusability is intentional, then block pointer, keyboard and form behaviour.
8. **Accessible names everywhere.** Icon-only buttons need a descriptive
   `aria-label`. Visible label text must appear in the accessible name.
   Decorative elements get `aria-hidden="true"`, never on a focusable element.
9. **Do not rely on colour alone.** Status needs a redundant cue: icon, text or
   underline. Determine which contrast requirement applies, then use
   `wcag-accessibility` to measure the rendered foreground and background pair. When
   contrast fails, report the pair and the requirement it misses; do not change
   the project's colours unless asked.
10. **Honour prefers-reduced-motion.** Wrap motion in
    `@media (prefers-reduced-motion: no-preference)` so it is opt-in. Under
    reduced motion, replace slides and scales with opacity crossfades and kill
    parallax and autoplay. Independently: autoplaying media needs a visible pause
    control, and toasts carrying actions or errors stay until dismissed.
11. **Announce dynamic content.** Use `aria-describedby` for field validation, a
    polite live region (`role="status"`) for non-urgent updates not tied to a
    control, and `role="alert"` only for urgent errors not tied to a control. For
    reliable repeated announcements, render a stable empty region before updating
    its text.
12. **Alt text by purpose.** Decorative images get `alt=""`; informative images
    describe the meaning; functional images describe the action, so a search icon
    button is `alt="Search"`, not `alt="magnifying glass"`.
13. **Structure is navigation.** Use headings that describe their sections and
    form a coherent outline (one page-level `<h1>`, properly nested levels). Expose
    one visible primary `<main>` landmark, and when repeated navigation precedes
    it, make a "Skip to content" link the first focusable element. Anchored
    headings get `scroll-margin-top`.
14. **Survive zoom and text resize.** The page must work at 200% zoom and reflow
    at 320px width without horizontal scrolling. Use `min-height` instead of fixed
    `height` on text containers, prefer `rem` breakpoints where they fit the
    codebase, and keep the viewport meta from capping zoom.

## Common mistakes
`references/common-mistakes.md` pairs each frequent mistake (removing the focus
outline, `<div onClick>` as a button, a placeholder as the only label, positive
`tabindex`, an assertive toast, disabled submit) with its fix.

## Review output
When the user asks for a standalone accessibility review, group confirmed findings
by principle in a markdown table with **Severity**, **Location**, **Before**,
**After** and **Why** columns. `references/review-output.md` gives the severity
scale, the consolidation rule, the verification step and the verdict thresholds.

## Checklist
- [ ] Native elements used; ARIA only where needed and correct
- [ ] `:focus-visible` ring present and verified against adjacent colours
- [ ] Full keyboard path for every interaction; no traps; focus restored
- [ ] Hit areas at least 24 x 24px, 44 x 44px in touch contexts
- [ ] Every control labelled and typed; paste never blocked
- [ ] Errors announced, described and focused; submit stays enabled
- [ ] Accessible names on icon-only controls; colour never the only cue
- [ ] Reduced motion honoured; autoplay and toasts handled
- [ ] Works at 200% zoom and 320px width with no horizontal scroll
