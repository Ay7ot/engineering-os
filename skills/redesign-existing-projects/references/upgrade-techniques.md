# Upgrade Techniques

Structural upgrades that replace generic patterns. Pull from these after the
quick wins in the priority order, and only where the brief calls for them.

## Typography
- Variable font animation: interpolate weight or width on scroll or hover.
- Outlined-to-fill transitions: text starts as a stroke outline and fills on
  scroll entry or interaction.
- Text mask reveals: large type acts as a window to video or animated imagery.

## Layout
- Broken grid and asymmetry: elements that deliberately ignore the columns,
  overlap, bleed off-screen, or sit offset with calculated randomness.
- Whitespace maximisation: aggressive negative space to force focus onto one
  element.
- Parallax card stacks: sections that stick and physically stack during scroll.
- Split-screen scroll: two halves sliding in opposite directions.
- Sticky pinning: pin a section while content scrolls behind it.

## Motion
- Smooth scroll with inertia: decouple scrolling from browser defaults for a
  heavier, cinematic feel.
- Staggered entry: elements cascade in with slight delays, combining a Y
  translate with an opacity fade. Never mount everything at once.
- Spring physics: replace linear easing with spring-based motion.
- Scroll-driven reveals: content entering through expanding masks, wipes or
  draw-on SVG paths tied to scroll progress.

## Surfaces
- True glassmorphism: beyond `backdrop-filter: blur`, add a 1px inner border
  and a subtle inner shadow to simulate edge refraction.
- Spotlight borders: card borders that illuminate under the cursor.
- Grain and noise overlays: a fixed `pointer-events-none` layer that breaks
  digital flatness.
- Coloured, tinted shadows: shadows carrying the background hue instead of
  generic black.

Keep motion honest: every animation answers what it communicates (hierarchy,
storytelling, feedback, state change), honours `prefers-reduced-motion`, and
uses `transform` and `opacity` only. Structural skeleton recipes for sticky
stacks, horizontal pan and staggered reveals are in
`design-taste-frontend/references/motion-recipes.md`.
