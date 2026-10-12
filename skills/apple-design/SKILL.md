---
name: apple-design
description: Apple's fluid-interface principles for the web: instant response, 1:1 drag tracking, interruptible springs, velocity handoff, momentum projection, rubber-banding and reduced motion. Use when building or reviewing gesture-driven UI, spring animations, or drag, swipe and sheet interactions.
metadata:
  audience: builder, reviewer, architect
  upstream: https://github.com/emilkowalski/skills/tree/main/skills/apple-design
  license: MIT
---
# Apple Design

## When to use
- Building or reviewing gesture-driven UI: drag, swipe, sheets, drawers,
  carousels.
- Choosing spring parameters, velocity handoff or momentum projection.
- Making motion feel physical and interruptible rather than scripted.

Materials, typography, multimodal feedback and the design foundations are in
`references/apple-design-detail.md`.

## Core idea
An interface feels alive when motion starts from the current on-screen value,
inherits the user's velocity, projects momentum forward, and can be grabbed and
reversed at any instant. Springs make that natural: they are interruptible and
velocity-aware.

## Rules
1. **Respond on pointer-down, not on release.** Highlight a pressed button
   instantly. Audit debounces, artificial timers, transition waits and the
   ~300ms tap delay: anything non-essential on the input path is a regression.
   Feedback must be continuous during the gesture, not only at the end.
2. **Track 1:1.** Use Pointer Events with `setPointerCapture`, respect the grab
   offset, and keep a short position and velocity history for release.
3. **Stay interruptible.** Never lock out input during a transition. Animate
   from the presentation (live on-screen) value, never the target, or the
   interrupt jumps. Avoid CSS transitions and `@keyframes` for gesture-driven
   motion. Blend velocity on reversal rather than hard-cutting it. Decompose 2D
   motion into independent X and Y springs.
4. **Behaviour over scripted animation.** Think in damping ratio (`1.0` is
   critically damped with no overshoot, lower is bouncier) and response (seconds
   to target, not a duration). Default most UI to damping `1.0`; add bounce
   (about `0.8`) only when the gesture carried momentum.
5. **Hand off velocity.** Pass release velocity as the spring's initial velocity;
   for an API that wants relative velocity use
   `gestureVelocity / (targetValue - currentValue)`.
6. **Project momentum.** Choose the target nearest the projected rest position,
   not the release point: `(v / 1000) * d / (1 - d)` with deceleration rate
   `d = 0.998` (use `0.99` for a snappier feel). Apple ships this exponential
   form, not `v * v / (2 * d)`.
7. **Keep spatial consistency.** Enter and exit along the same path, anchor
   popovers, menus and sheets to their trigger, and mirror easing on reversible
   transitions. Hint in the direction of the gesture.
8. **Rubber-band at boundaries.** Resist progressively instead of hard-stopping:
   `(overshoot * dimension * constant) / (dimension + constant * abs(overshoot))`
   with `constant = 0.55`.
9. **Keep frames smooth.** Animate only `transform` and `opacity`, use
   `requestAnimationFrame`, and hint with `will-change` where motion is imminent.
   For fast motion a subtle blur or stretch encodes speed.
10. **Ship reduced motion.** Under `prefers-reduced-motion`, replace slides and
    springs with short opacity cross-fades and drop overshoot.

## Gesture details
- Tap: highlight on touch-down, commit on touch-up, about 10px hysteresis,
  cancel by dragging away and back.
- Drag and swipe: require about 10px of movement before committing to a
  direction, then track 1:1.
- Detect plausible gestures in parallel from the first move and cancel the
  losers once intent is clear. Avoid recognizers that only report a final state.
- Decide reverse versus commit from the velocity sign, not the position.

## Quick reference
| Need | Technique | Value |
| --- | --- | --- |
| Default UI spring | Critically damped | `damping 1.0`, `response 0.3-0.4` |
| Momentum spring | Under-damped | `damping ~0.8`, `response 0.3-0.4` |
| Gesture to spring | Hand off velocity | `gestureVelocity / (target - current)` if normalized |
| Flick landing | Project momentum | `current + (v / 1000) * d / (1 - d)`, `d ~ 0.998` |
| Interrupt cleanly | Start from the live value | read the on-screen transform |
| Reversible transition | Mirror the curve | inverse cubic-bezier |
| Boundary | Rubber-band | progressive resistance |
| Reduced motion | Cross-fade, not slide | `@media (prefers-reduced-motion)` |

## Checklist
- [ ] Feedback fires on pointer-down and stays continuous through the gesture
- [ ] Motion starts from the current on-screen value and is interruptible
- [ ] Release velocity handed off; target chosen from the momentum projection
- [ ] Spring values come from the tables, not guesses
- [ ] Enter and exit paths symmetric; origins anchored to the trigger
- [ ] Only `transform` and `opacity` animate; reduced-motion variant shipped
