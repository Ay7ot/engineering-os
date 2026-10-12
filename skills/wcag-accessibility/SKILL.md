---
name: wcag-accessibility
description: Audit and remediate web accessibility against WCAG 2.2 A and AA: alt text, contrast, keyboard access, focus visibility, target size, forms, live regions. Use when asked for an a11y audit, WCAG compliance, or to make a page accessible. For component craft use `better-accessibility`.
metadata:
  audience: builder, tester, reviewer
  upstream: https://github.com/addyosmani/web-quality-skills
  license: MIT
---
# Accessibility (WCAG 2.2)

Make content usable by everyone, including people with disabilities, by auditing
against WCAG 2.2 and fixing what the audit finds.

## When to use
- Asked to improve accessibility, run an a11y audit, or reach WCAG compliance.
- Checking a page for screen reader support, keyboard navigation, contrast,
  target size, or reduced motion.

For component-level craft (focus rings, ARIA in widgets, hit areas) use
`better-accessibility`; for a fast level-by-level checklist while building use
`accessibility-expert`.

## POUR and conformance
| Principle | Meaning |
| --- | --- |
| Perceivable | Content can be perceived through different senses |
| Operable | The interface can be operated by all users |
| Understandable | Content and interface are understandable |
| Robust | Content works with assistive technologies |

Level A must pass, AA should pass (a legal requirement in many jurisdictions),
AAA is nice to have.

## The numbers
| Text | AA minimum | AAA |
| --- | --- | --- |
| Normal text (under 18px, or under 14px bold) | 4.5:1 | 7:1 |
| Large text (18px+, or 14px+ bold) | 3:1 | 4.5:1 |
| UI components, graphics, focus indicators | 3:1 | 3:1 |

Interactive targets are at least 24 x 24 CSS pixels (WCAG 2.5.8), with 44 x 44 the
comfortable touch size. Content must survive 200% zoom and reflow at 320px width
without horizontal scrolling.

## Perceivable
- Images need purposeful alt text; decorative images get `alt=""` (plus
  `role="presentation"` where useful); complex images use a caption or
  `aria-describedby`.
- Icon-only buttons need an accessible name: an `aria-label`, or visually hidden
  text, with the icon marked `aria-hidden="true"`.
- Never rely on colour alone: pair it with an icon, text or underline.
- Video needs captions, and descriptions where the visual carries meaning; audio
  needs a transcript.

## Operable
- All functionality is keyboard accessible. Prefer native elements; add manual key
  handling only to a non-interactive element, and never to a native `<button>`,
  where Enter and Space already fire click.
- No keyboard traps. A dialog uses a focus trap or the native `<dialog>`.
- Never remove focus outlines. Style `:focus-visible` with at least a 2px
  indicator meeting 3:1 against its background; keep system colours in
  forced-colors mode.
- Focused elements must not be hidden by sticky headers: add `scroll-margin-top`.
- Provide a skip link past repeated navigation.
- Any action that requires dragging needs a single-pointer alternative.
- Time limits are extendable or dismissible. Respect `prefers-reduced-motion`.

## Understandable
- Set the page language (`<html lang="en">`) and a `lang` on any inline language
  change.
- Keep navigation, and any repeated help mechanism, in the same relative order
  across pages.
- Every input has a programmatically associated label; placeholders are never
  labels.
- Announce errors: `aria-invalid="true"`, `aria-describedby` at the inline
  message, and focus the first invalid field on submit.
- Do not force re-entry of information already provided in the same session.
- Authentication must not require a cognitive test unless copy and paste or
  autofill works, or an alternative such as a passkey or email link exists.

## Robust
- Prefer native elements over ARIA roles bolted onto `div`s. ARIA only when native
  semantics are not enough, and then with correct roles and states.
- Use live regions to announce dynamic content changes without moving focus:
  `role="status"` for polite updates, `role="alert"` for urgent errors.

## Code patterns
`references/a11y-patterns.md` holds the markup and CSS for alt text and icon
buttons, the visually hidden class, focus-visible, skip links, the modal focus
trap, target size, timing, reduced motion, page language, navigation, form labels,
error handling, redundant entry, authentication, native versus ARIA, and live
regions.

## Priority and verification
Fix in impact order: **critical** (missing form labels or alt text, insufficient
contrast, keyboard traps, no focus indicators), then **serious** (missing page
language or heading structure, non-descriptive link text, autoplaying media,
missing skip links), then **moderate** (missing ARIA labels on icons, inconsistent
navigation, missing error identification, timing without controls, missing
landmark regions).

Automated tools catch only part of the problem, so always pair them with a manual
pass. `references/issue-priority.md` lists the commands and the manual checklist.

## Checklist
- [ ] Every image has purposeful alt text; icon buttons have accessible names
- [ ] Contrast meets 4.5:1 (normal) and 3:1 (large, UI, focus indicators)
- [ ] Fully keyboard operable, no traps, visible focus, skip link present
- [ ] Targets are at least 24 x 24px; no drag-only action; time limits extendable
- [ ] Language, headings, landmarks and form labels are programmatic
- [ ] Errors announced and focused; no redundant entry; paste never blocked
- [ ] Automated and manual checks run, with results reported by location
