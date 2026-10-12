# Anti-patterns

Match and refuse. If you are about to write one of these, rewrite the element
with a different structure rather than softening it.

## Banned outright

- Side-stripe borders: `border-left` or `border-right` over 1px as a coloured
  accent on cards, list items, callouts or alerts. Use full borders, a background
  tint, leading numbers or icons, or nothing.
- Gradient text: `background-clip: text` with a gradient background. Use a solid
  colour and put emphasis in weight or size.
- Glassmorphism as a default: decorative blurs and glass cards. Rare and
  purposeful, or nothing.
- The hero-metric template: big number, small label, supporting stats, gradient
  accent. A cliche that reads as filler.
- Identical card grids: same-sized cards with icon, heading and text, repeated.
- The tracked uppercase eyebrow above every section. One deliberate kicker is
  voice; an eyebrow on every heading is scaffolding.
- Numbered section markers (01, 02, 03) as default scaffolding. Numbers earn
  their place only when the section really is an ordered sequence.
- Text that overflows its container. Test heading copy at every breakpoint; if
  it overflows, reduce the clamp maximum or rewrite the copy.

## Near-misses worth rewriting

- A 1px border plus a wide soft drop shadow on the same element. Pick one: a
  solid border, or a defined shadow of no more than 8px blur.
- Radius above 32px on cards, sections or inputs. Cards top out around 12 to
  16px; full-pill is fine for tags and buttons.
- Hand-drawn or sketchy SVG illustrations, paper-grain filters, and crude path
  scenes. If real assets are not available, ship no illustration.
- Repeating diagonal stripe backgrounds, and two-axis decorative grid overlays,
  unless the surface really is a canvas, map or measurement tool.

## Model-agnostic motion tells

- One identical entrance animation applied to every section. Staggering items
  inside one list is fine; the uniform reflex is the tell.
- Motion added because it was possible, not because it carries meaning.
- Hover feedback applied to a child image through a parent group, so the picture
  reacts instead of the control. Animate the control.

## The register question

Cross-register failures are the bans above. Register-specific failures are about
which lens you apply, not a separate rule file: a landing page that reads as a
dashboard, or a dashboard that reads as a campaign page, has failed at the
register level before any single rule.
