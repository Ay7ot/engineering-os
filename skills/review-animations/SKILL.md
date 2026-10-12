---
name: review-animations
description: Review animation and motion code against a high craft bar, defaulting to flagging and earning approval. Use when reviewing a diff, branch or PR that adds or changes motion, transitions, keyframes, easing or gestures. Motion only, not general code review.
metadata:
  audience: reviewer
  upstream: https://github.com/emilkowalski/skills/tree/main/skills/review-animations
  license: MIT
---
# Reviewing Animations

## When to use
- A diff, branch or PR changes motion: transitions, keyframes, easing, springs,
  durations, gestures, hover effects.
- Deciding whether an animation is good enough to merge.

Not for general code (use `code-review`), not for writing features, and not for
auditing a whole codebase (`improve-animations`).

Your bias is toward motion that feels right, not motion that merely runs. A
transition that works but feels sluggish, lands from the wrong origin, fires too
often or drops frames is a regression. Default to flagging; approval is earned.

## The ten standards
1. **Justified motion.** Every animation answers why it animates: spatial
   consistency, state indication, feedback, explanation, or preventing a jarring
   change. "It looks cool" on a frequently-seen element blocks.
2. **Frequency-appropriate.** Keyboard-initiated and 100+/day actions get no
   animation, tens/day gets near-imperceptible motion, occasional gets standard,
   rare and first-time may have delight.
3. **Responsive easing.** Entrances and exits use `ease-out` or a strong custom
   curve. `ease-in` on UI is a block: it delays the moment the user watches most.
   Built-in CSS easings are too weak, so expect custom cubic-beziers.
4. **Sub-300ms UI.** UI animations stay under 300ms; anything slower needs a
   stated reason. Budgets: press feedback 100-160ms, tooltips and popovers
   125-200ms, dropdowns 150-250ms, modals and drawers 200-500ms.
5. **Origin and physical correctness.** Popovers, dropdowns and tooltips scale
   from their trigger, not their centre. Never animate from `scale(0)`; start from
   `scale(0.9-0.97)` plus opacity. Modals are exempt and stay centred.
6. **Interruptibility.** Rapidly triggered or gesture-driven motion (toasts,
   toggles, drags) must retarget from current state: CSS transitions or springs,
   not keyframes that restart from zero.
7. **GPU-only properties.** Animate `transform` and `opacity` only. Animating
   `width`, `height`, `margin`, `padding`, `top` or `left`, or Motion `x`/`y`/
   `scale` shorthands under load, is a performance finding.
8. **Accessibility.** `prefers-reduced-motion` is honoured (gentler, not zero:
   keep opacity and colour, drop movement) and hover motion is gated behind
   `@media (hover: hover) and (pointer: fine)`.
9. **Asymmetric enter and exit.** Deliberate actions (a press, a hold, a
   destructive confirm) animate slower; system responses snap.
10. **Cohesion.** Motion matches the component's personality and the rest of the
    product: a playful app can be bouncier, a dashboard stays crisp. When unsure
    whether motion feels right, the strongest move is often to delete it.

## Escalation triggers (flag on sight)
- `transition: all`, or a `scale(0)` or pure-fade entrance with no initial
  transform
- `ease-in` on any UI interaction, or weak built-in easing on a deliberate
  animation
- Animation on a keyboard shortcut, command-palette toggle, or 100+/day action
- UI duration over 300ms with no stated reason
- `transform-origin: center` on a trigger-anchored popover, dropdown or tooltip
- Keyframes on toasts, toggles, or anything triggered rapidly
- Animating layout properties, or Motion `x`/`y`/`scale` props on motion that runs
  while the page is busy
- Updating a CSS variable on a parent to drive a child transform
- Missing `prefers-reduced-motion` handling on movement, or ungated `:hover`
  motion
- Symmetric enter and exit timing on a press-and-release or hold interaction
- Everything-at-once entrance where a 30-80ms stagger belongs

## Remedial hierarchy (prefer earlier moves)
1. Delete the animation (high frequency, no purpose, keyboard-triggered).
2. Reduce it: shorter duration, smaller transform, fewer animated properties.
3. Fix the easing: `ease-in` to `ease-out` or a strong cubic-bezier such as
   `cubic-bezier(0.23, 1, 0.32, 1)`.
4. Fix the origin and physicality: correct `transform-origin`, replace `scale(0)`
   with `scale(0.95)` plus opacity.
5. Make it interruptible: keyframes to transitions, or a spring for gestures.
6. Move it to the GPU: layout props to `transform` and `opacity`.
7. Asymmetric timing: slow the deliberate phase, snap the response.
8. Polish: blur to mask crossfades, stagger for groups, `@starting-style`, spring.
9. Accessibility and cohesion: reduced motion, hover gating, personality.

## Output
Two parts, in this order: a findings table (one row per issue, columns Before,
After and Why, never before/after lists), then a verdict grouped by impact tier,
highest first, ending in **Block** or **Approve**. `references/output-format.md`
holds the worked example, the tier order, and the exact criteria for each
decision. Cite `file:line` and pull values from the tables above rather than
approximating; when unsure whether motion feels right, recommend reviewing it in
slow motion or frame by frame.

## Checklist
- [ ] Every animation measured against all ten standards
- [ ] Escalation triggers checked on sight and reported
- [ ] Fixes proposed in remedial order, earliest move first
- [ ] Findings table with Before, After and Why; no before/after lists
- [ ] Verdict given: Block or Approve, with a blocker summary
- [ ] Every finding cites `file:line`; facts and inference distinguished
