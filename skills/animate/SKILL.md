---
name: animate
description: Build an animation from scratch, deciding in order whether to animate at all, the purpose, tool, properties, easing and duration, interruption and exit. Use when asked to animate something, add motion, or build a transition. For critiquing existing motion use `review-animations`.
metadata:
  audience: builder
  upstream: https://github.com/emilkowalski/skills/tree/main/skills/animate
  license: MIT
---
# Building Animations

## When to use
- Asked to animate something, add motion, make a component feel alive, or build a
  transition.
- Choosing easing, duration or spring config, or deciding how a motion exits.

Not for auditing a codebase (`improve-animations`), critiquing a diff
(`review-animations`), or finding missing motion
(`find-animation-opportunities`).

## Hard rules
1. Run the sequence in order. Steps 1 and 2 gate everything; do not reach for a
   curve before deciding whether it animates at all.
2. No approximated values. Every curve, duration and spring config comes from
   `references/decision-tables.md`.
3. Extend the codebase's tokens (`--ease-*`, duration scales) and use the cheapest
   tool that works; do not add a parallel system or install a motion library for a
   fade.
4. Reduced motion and hover gating ship with the animation, not as a follow-up.
5. Never present motion as a menu of options. Make the call, state the reason in
   one line, write the code.

## The build sequence
**1. Should it animate at all?**

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette) | No animation, ever. Stop here. |
| Tens of times/day (hover, list navigation) | Near-imperceptible only |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare or first-time (onboarding, success) | The delight budget lives here |

Keyboard-initiated actions are a disqualifier, not a judgment call. If the request
fails this gate, say so and offer the non-motion alternative.

**2. What is the purpose?** Name it: feedback, spatial consistency, state
indication, preventing a jarring change, explanation (marketing or onboarding
only), or delight (rare or first-time only). Cannot name it? Do not build it. Data
the user is reading or acting on must not move for style.

**3. Pick the tool, the cheapest that works.** Walk
`references/decision-tables.md` and stop at the first fit: CSS transition for
hover, press, colour and class-driven state; `@starting-style` for entry on mount;
CSS animation for predetermined motion that must stay smooth while the page is
busy (it runs off the main thread); WAAPI (`element.animate()`) for programmatic
control with CSS performance; Motion for springs, layout and exit animations, and
gesture-driven values. If the task needs a component (toast, drawer, command menu)
rather than an animation, use a component library with built-in focus management
instead of hand-rolling one.

**4. Pick the properties.**
- `transform` and `opacity` only; they skip layout and paint. Never animate
  `width`, `height`, `margin`, `padding`, `top` or `left` (`clip-path` is the
  sanctioned exception, `height` only for accordions).
- Never `scale(0)`. Start from `scale(0.9-0.97)` plus `opacity: 0`.
- Set `transform-origin` at the trigger for popovers, dropdowns, menus and
  tooltips (Base UI: `var(--transform-origin)`); modals are exempt and stay
  centred. Percentages in `translate()` are relative to the element's own size.
- In Motion, use the full transform string: the `x`/`y`/`scale` shorthands are not
  hardware accelerated and drop frames under load. Never drive a child's transform
  from a CSS variable on the parent.

**5. Easing and duration, or a spring.** Entrances and exits use `ease-out`,
on-screen movement `ease-in-out`, hover and colour `ease`, constant motion
`linear`, and never `ease-in` on UI: it delays the exact moment the user is
watching. Built-in CSS easings are too weak, so use the curves in
`references/decision-tables.md` rather than hand-rolling one. Durations: press
feedback 100-160ms, tooltips and small popovers 125-200ms, dropdowns and selects
150-250ms, modals and drawers 200-500ms, marketing longer. UI animations stay
under 300ms. Reach for a spring when the motion is drag with momentum, an element
that should feel alive, or a gesture the user can interrupt; keep bounce at
0.1-0.3 and reserve it for drag-to-dismiss and playful interactions.

**6. Interruption and exit.**
- Transitions, not keyframes, for anything triggered rapidly (toasts, toggles):
  transitions retarget from the current value, keyframes restart from zero.
- Springs for gestures; they carry velocity through an interruption.
- Exit the way it entered; symmetric paths make swipe-to-dismiss feel obvious.
- Asymmetric timing where the user is deciding: slow on the deliberate phase
  (hold-to-confirm 2s linear), snappy on the system response (release 200ms
  ease-out).

**7. Reduced motion and pointer gating.** Ship both, every time.
`@media (prefers-reduced-motion: reduce)` keeps opacity, colour and comprehension
transitions but drops movement and position changes;
`@media (hover: hover) and (pointer: fine)` gates hover motion, because touch
fires false hovers on tap. In JS, `const reduce = useReducedMotion()` and pick the
value that does not move.

## Never ship
Each item in `references/never-ship.md` is an automatic block in
`review-animations`: `transition: all`, a `scale(0)` entrance, `ease-in` on UI,
animation on a keyboard or 100+/day action, a UI duration over 300ms, keyframes on
toasts, animating layout properties, an ungated `:hover`, missing reduced motion.

## Output
Write the code, then in a few lines: the gate result (frequency tier, named
purpose), the ingredients (tool, properties, curve, duration or spring config),
and what to feel-check (play at 2-5x duration, step through the animation
inspector, test gestures on a real device). The code is the deliverable.

## Checklist
- [ ] Frequency gate passed and the purpose named in one of the six words
- [ ] Cheapest tool chosen; existing tokens extended, not forked
- [ ] Only `transform` and `opacity` (plus sanctioned exceptions) animated
- [ ] Curve and duration from `references/decision-tables.md`, UI under 300ms
- [ ] Interruption handled; exit mirrors entry; timing asymmetric where needed
- [ ] `prefers-reduced-motion` and hover gating shipped with the change
- [ ] `references/never-ship.md` checked before finishing
