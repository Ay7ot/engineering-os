# Decision tables

Exact values behind `animate`. Use these; never approximate or hand-roll.

## Tool: cheapest that works
Walk down and stop at the first fit.

| Need | Tool |
| --- | --- |
| Hover, press, colour, a state toggle driven by class or attribute | CSS transition |
| Entry animation on mount with no JS state | CSS `@starting-style` |
| Predetermined motion that must stay smooth while the page is busy | CSS animation (off the main thread) |
| Programmatic control with CSS performance | WAAPI (`element.animate()`) |
| Springs, layout animations, exit animations, gesture-driven values | Motion (`motion.dev`) |

CSS animations beat JS under load. `requestAnimationFrame`-based animation drops
frames while the browser loads, scripts or paints, so use CSS for predetermined
motion and JS for dynamic, interruptible motion.

## Easing
| Situation | Easing |
| --- | --- |
| Entering or exiting | `ease-out` |
| Moving or morphing on screen | `ease-in-out` |
| Hover or colour change | `ease` |
| Constant motion (marquee, progress) | `linear` |
| Default | `ease-out` |

Built-in CSS easings are too weak for UI. Use these instead:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

`--ease-drawer` is the iOS-like drawer curve (Ionic). Need another one? Take it
from easing.dev or easings.co; do not hand-roll a curve.

At the same 200ms, `ease-out` feels faster than `ease-in`, because `ease-in`
starts slow and delays the moment the user is watching.

## Duration
| Element | Duration |
| --- | --- |
| Button press feedback | 100-160ms |
| Tooltips, small popovers | 125-200ms |
| Dropdowns, selects | 150-250ms |
| Modals, drawers | 200-500ms |
| Marketing, explanatory | Can be longer |

UI animations stay under 300ms; a 180ms dropdown feels more responsive than a
400ms one.

## Springs
Reach for a spring instead of a curve when the motion is drag with momentum, an
element that should feel alive, a gesture the user can interrupt or reverse, or
decorative mouse-tracking.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }            // Apple style, easier to reason about
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // traditional physics, more control
```

Keep bounce at 0.1-0.3, and avoid bounce in most UI: reserve it for
drag-to-dismiss and playful interactions.
