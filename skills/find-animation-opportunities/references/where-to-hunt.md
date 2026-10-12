# Where to hunt

The seam catalogue behind `find-animation-opportunities`. Each class is a known
source of genuine opportunity; every candidate still has to pass all four gate
questions.

- **Feedback gaps**: pressable elements with no `:active` state (scale 0.95-0.98
  with `transition: transform 160ms ease-out`); destructive actions confirmed
  with a plain click where a hold-to-confirm fill would prevent slips
  (`clip-path: inset(0 100% 0 0)` overlay, 2s linear on press, 200ms ease-out
  snap-back on release).
- **Teleporting state**: content that swaps, appears or vanishes instantly
  (conditional renders, route content, expanding sections) needs a fade or scale
  entrance from `scale(0.95-0.97)` plus `opacity: 0`, `ease-out`, never
  `scale(0)`; `@starting-style` for entry without JS; accordions that snap open
  need a height plus opacity transition; list items added or removed with no
  bridge need enter/exit transitions (CSS transitions, not keyframes, so rapid
  triggers retarget smoothly).
- **Missing spatial story**: panels, popovers and menus appearing with no
  connection to their trigger (scale from `transform-origin` at the trigger, Base
  UI: `var(--transform-origin)`; modals are exempt and stay centred);
  dismissable surfaces that exit a different way than they entered (symmetric
  paths, `translateY(100%)` percentages rather than hardcoded pixels).
- **Group entrances**: a grid or list that pops in all at once on a page users
  see occasionally gets a 30-80ms stagger, decorative and never blocking
  interaction.
- **Gesture seams**: draggable or swipeable elements that snap with no physics
  need springs (`{ type: "spring", duration: 0.5, bounce: 0.2 }`, bounce
  0.1-0.3), velocity-based dismissal when `abs(distance) / elapsedMs > ~0.11`,
  and rubber-banding at boundaries instead of hard stops.
- **The delight budget**: rare, high-emotion moments rendered flat (first run,
  empty states, success, celebration) are the only places bounce or a longer beat
  are welcome.

## Sweeps

Use `grep` to find the seams: `{isOpen &&` and `display: none` toggles, `onClick`
handlers on elements with no `:active` or transition styles, `details` and
accordion markup, drag handlers, `.map(` renders of entering lists, and
empty-state or success components.
