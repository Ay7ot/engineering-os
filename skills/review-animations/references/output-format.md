# Output format

The required report shape for `review-animations`. Two parts, in this order.

## Part 1: findings table (required)
A single markdown table, one row per issue. Never a "Before:" / "After:" list.

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; `all` animates unintended properties off-GPU |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Nothing appears from nothing; `scale(0)` looks like it came from nowhere |
| `ease-in` on dropdown | `ease-out` plus a custom curve | `ease-in` delays the moment the user watches most, so it feels sluggish |
| `transform-origin: center` on popover | `var(--transform-origin)` (Base UI) | Popovers scale from their trigger, not centre (modals are exempt) |
| `x: 100` in Motion | `transform: "translateX(100px)"` | Shorthands are not hardware accelerated and drop frames under load |
| `width 300ms` on a drawer | `transform 250ms ease-out` | Layout properties trigger layout, paint and composite |

## Part 2: verdict (required)
Group remaining commentary by impact tier, highest first, and omit empty tiers.

1. **Feel-breaking regressions**: sluggish easing, comes-from-nowhere, fires on
   high-frequency or keyboard actions.
2. **Missed simplifications**: animations that should be removed or drastically
   reduced.
3. **Performance**: non-GPU properties, dropped-frame risks, recalc storms.
4. **Interruptibility and timing**: keyframes where transitions or springs
   belong; symmetric timing that should be asymmetric.
5. **Origin, physicality and cohesion**: wrong origin, mismatched personality,
   jarring crossfades.
6. **Accessibility**: reduced-motion and pointer or hover gating.

Close with an explicit decision:

- **Block**: any feel-breaking regression, animation on a keyboard or
  high-frequency action, `scale(0)` or `ease-in` on UI, or a non-GPU animation
  with an easy GPU fix.
- **Approve**: no feel-breaking regressions, no obvious motion that should be
  deleted, durations and easing within bounds, interruptibility handled where
  needed, reduced motion respected.

Be specific and cite `file:line`. When a value is needed (a curve, a duration, a
spring config), pull the exact one from the tables in `SKILL.md` rather than
approximating. State any part of the scope you could not review, and why.
