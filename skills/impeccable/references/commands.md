# Commands

Commands are grouped by intent. Setup runs first for every one of them: load
project context, read the existing design system, pick the register.

## Build

- `shape [feature]`: plan the UX and UI before writing code. Use when the shape
  of the screen is still open.
- `craft [feature]`: shape, then build the feature end to end. The default for
  a new surface.
- `init`: set up project context, the product brief, the design document, and
  next steps. Required before anything else when no brief exists.
- `document`: generate the design document from existing project code. Use when
  the interface exists but is undocumented.
- `extract [target]`: pull reusable tokens and components into a design system.

## Evaluate

- `critique [target]`: UX design review with heuristic scoring. Reads as a
  backlog for `polish`.
- `audit [target]`: technical quality checks across accessibility, performance
  and responsive behaviour.

## Refine

- `polish [target]`: final quality pass before shipping.
- `bolder [target]`: amplify a safe or bland design.
- `quieter [target]`: tone down an aggressive or overstimulating design.
- `distill [target]`: strip to the essence, remove complexity.
- `harden [target]`: production readiness: errors, i18n, edge cases.
- `onboard [target]`: first-run flows, empty states, activation.

## Enhance

- `animate [target]`: add purposeful motion.
- `colorize [target]`: add strategic colour to a monochrome UI.
- `typeset [target]`: improve type hierarchy and font choice.
- `layout [target]`: fix spacing, rhythm and visual hierarchy.
- `delight [target]`: add personality and memorable touches.
- `overdrive [target]`: push past conventional limits.

## Fix

- `clarify [target]`: UX copy, labels and error messages.
- `adapt [target]`: devices and screen sizes.
- `optimize [target]`: diagnose and fix UI performance.

## Iterate

- `live`: visual variant mode, pick elements in the browser and generate
  alternatives. Use when a running dev server is available.

## Routing

- No argument means "what should I do?". Read the context signals, then lead
  with two or three highest-value commands and a one-line reason each, followed
  by the full menu. Never auto-run a command; recommend and let the user choose.
- A first word that matches a command loads that command's flow.
- A first word that does not match but clearly maps to one command ("fix the
  spacing" maps to layout, "rewrite this error" maps to clarify) runs as if
  invoked. If two fit, ask once.
- No match means general design work: apply setup, the general rules and the
  register.
