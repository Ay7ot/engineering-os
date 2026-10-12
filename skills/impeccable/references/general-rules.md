# General rules

## Colour

- Verify contrast. Body text 4.5:1 or better against its background; large text
  (18 px, or 14 px bold) 3:1 or better. Placeholder text needs the same 4.5:1,
  not the default muted grey. The most common failure is muted grey body text on
  a tinted near-white. If contrast is even close, push the body colour toward
  the ink end of the ramp; light grey "for elegance" is the single biggest reason
  an interface is hard to read.
- Grey text on a coloured background looks washed out. Use a darker shade of the
  background's own hue, or a transparency of the text colour.
- Use OKLCH for new palettes. Tint neutrals by adding 0.005 to 0.015 chroma
  toward the brand hue, not toward warm or cool by reflex.
- Avoid the cream, sand and beige body background. The whole near-white warm
  band reads as the default AI palette of the decade, and names like paper,
  cream, sand, bone or linen are tells. Instead: a saturated brand colour as the
  body, a true off-white at zero chroma, or a darker mid-tone in the brand's own
  hue. Warmth belongs in accent, type and imagery, not the body.
- Dark versus light is never a default. Write one sentence of physical scene
  first: who uses this, where, under what ambient light, in what mood. If the
  sentence does not force an answer, it is not concrete enough.
- Pick a colour strategy before colours: restrained (tinted neutrals plus one
  accent under 10 percent), committed (one saturated colour carries 30 to 60
  percent of the surface), full palette (3 to 4 named roles, used deliberately),
  drenched (the surface is the colour).

## Typography

- Body line length 65 to 75 characters.
- Do not pair fonts that are similar but not identical (two geometric
  sans-serifs, two humanist sans-serifs). Pair on a contrast axis, or use one
  family in several weights.
- Display heading ceiling: `clamp()` max at or below 6rem. Above that the page
  is shouting, not designing.
- Display letter-spacing floor: not tighter than -0.04em. -0.02 to -0.03em is
  enough for a tight grotesque.
- Use `text-wrap: balance` on h1 to h3 for even lines, and `text-wrap: pretty`
  on long prose to reduce orphans.

## Layout

- Vary spacing for rhythm rather than one gap everywhere.
- Cards are the lazy answer. Use them only when they are the best affordance,
  and never nest them.
- Flexbox for one dimension, grid for two. Do not reach for grid when
  `flex-wrap` is simpler.
- Responsive grids without breakpoints: `repeat(auto-fit, minmax(280px, 1fr))`.
- Build a semantic z-index scale: dropdown, sticky, modal backdrop, modal, toast,
  tooltip. Never arbitrary values such as 999 or 9999.

## Motion

- Motion is part of the build, not an afterthought.
- Do not animate CSS layout properties unless truly needed.
- Ease out with exponential curves (quart, quint, expo). No bounce, no elastic.
- Reach for a motion library when the effect needs one.
- Reduced motion is not optional. Every animation needs a
  `prefers-reduced-motion: reduce` alternative, typically a crossfade or an
  instant transition.
- Staggering items inside one list is fine. The tell is the uniform reflex: one
  identical entrance applied to every section. Suppressing that reflex is never a
  reason to ship a page with no motion.
- Reveal animations must enhance an already-visible default. Transitions pause on
  hidden tabs and in headless renderers, so a class-gated reveal never fires and
  the section ships blank.
- Premium motion is not only transform and opacity: blur, backdrop-filter,
  clip-path, mask and shadow are part of the palette when they materially improve
  an effect and stay smooth.

## Interaction

- Dropdowns rendered with `position: absolute` inside an `overflow: hidden` or
  `overflow: auto` container will be clipped. Use the native dialog or popover
  API, `position: fixed`, or a portal to escape the stacking context.
- Never animate an image on hover, including through a parent hover group. The
  image is not the action target; animate the card's background, border or
  shadow instead.
