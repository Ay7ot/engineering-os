# Apple Design: reference detail

Deep material behind `apple-design`: materials and depth, multimodal feedback,
preference-based variants, typography, the design foundations, and process.

## Materials and depth
Apple uses translucent materials as a floating functional layer that brings
structure without stealing focus. On the web, approximate with `backdrop-filter`.

- Build nav bars, toolbars and sheets as translucent layers with content
  scrolling underneath, not opaque bars that consume a fixed strip.
- Material weight encodes hierarchy: darker or heavier materials separate
  structural regions (sidebars); lighter materials draw attention to interactive
  elements (buttons). Never stack a light translucent surface on another,
  legibility collapses.
- Bigger surfaces read as thicker: stronger blur and a deeper shadow than small
  chips. Consider a context-aware shadow, heavier over busy text and lighter over
  plain backgrounds.
- Dim to focus, separate to keep flow. A modal task pairs the surface with a
  dimming scrim and pushes the background back. A parallel, non-blocking panel
  uses translucency and offset without a scrim. Stacked sheets progressively dim
  and push back each parent layer.
- Vibrancy keeps text legible over changing backgrounds: use higher contrast,
  slightly heavier weight and a small letter-spacing bump, and put colour on a
  solid layer rather than the translucent foreground.
- Use scroll edge effects, not hard dividers: fade a small blur or gradient mask
  where content meets floating chrome, only where floating UI actually overlaps
  content.
- Materialize, do not just fade: for glass and blur surfaces animate blur radius
  and scale together so the surface reads as a material arriving.

```css
.toolbar {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  border-top: 1px solid rgba(255, 255, 255, 0.4);
}
```

## Multimodal feedback
Three rules for combining motion, sound and haptics:
1. **Causality**: make it obvious what caused the feedback. Trigger on the real
   causal event (the toggle flipping, the item snapping home) and match its
   character to the action's physicality.
2. **Harmony**: the visual, the sound and the haptic fire on the same frame.
   Latency between them destroys the illusion. Do not let a CSS transition lag
   the audio or the Vibration API.
3. **Utility**: add feedback only where it earns its place. Reserve haptics and
   sound for meaningful moments (success, error, commit, snap); over-feedback
   trains users to ignore all of it.

## Preference-based variants
Respond to three independent signals and bake them into components:
- `prefers-reduced-motion: reduce`: replace slides, springs and parallax with
  short opacity cross-fades or static transitions. Drop elastic overshoot. Keep
  opacity and colour changes that aid comprehension.
- `prefers-reduced-transparency: reduce`: make translucent surfaces frostier or
  solid by raising background opacity and dropping the blur.
- `prefers-contrast: more`: near-solid backgrounds with a defined contrasting
  border.

```css
@media (prefers-reduced-motion: reduce) {
  .sheet { transition: opacity 200ms ease; transform: none !important; }
}
@media (prefers-reduced-transparency: reduce) {
  .toolbar { background: white; backdrop-filter: none; }
}
```

Also avoid full-viewport moving backgrounds, slow looping oscillations near
0.2 Hz (one cycle per 5 seconds), and abrupt brightness jumps (ease dark to light
theme changes). Make large moving objects semi-transparent while they travel, and
fade big surfaces out during a large reposition and back in once settled.

## Typography
- Tracking (letter-spacing) is size-specific, never one value for all sizes.
  Large display text wants negative tracking because letters read too far apart
  as they grow; small text wants slightly positive tracking. Tighten headings,
  leave body near `0`.
- Leading (line-height) tracks size inversely: tight on large headings, looser on
  body copy. Increase it for tall ascenders and descenders; tighten it for dense,
  information-heavy UI.
- Build hierarchy from weight, size and leading as a set, not size alone.
  Emphasise with weight: it adds presence without taking more space.
- Respect the user's text-size setting (Dynamic Type) and scale layout with the
  text: spacing in `rem` or `em`, not fixed px.
- Default to the platform system font before a custom face; it already ships
  optical sizing, tracking tables and legibility tuning. Override with a reason.

```css
:root { font: 100%/1.5 system-ui, sans-serif; }

.display {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-optical-sizing: auto;
}
```

## Design foundations
1. **Purpose.** Make with intention; decide what not to build. Every feature asks
   for the user's time, attention and trust.
2. **Agency.** Keep people in control and offer choices. Back it with
   forgiveness: easy undo for slips, a confirmation dialog only for genuinely
   destructive, irreversible actions. Overusing the dialog trains people to click
   through it.
3. **Responsibility.** Act in the user's interest. Ask for privacy at the right
   moment, only for what is needed, transparently. Anticipate misuse and harm,
   especially with AI (an allergy-aware recipe app must not suggest a harmful
   ingredient). Add previews, confirmations and disclaimers, and cut a feature
   whose risk outweighs its value.
4. **Familiarity.** Build on what people already know. Use metaphors that are
   neither too literal nor too abstract, and honour their physics. Things that
   look the same must behave the same and live in the same place. Break a
   familiar pattern only if you can prove it is better, then test it.
5. **Flexibility.** Design for different contexts, devices and the full range of
   abilities. Adapt to the platform (quick touch on a phone, deep workflows with
   a precise pointer on desktop). Design inclusively, and let people personalise
   when no single layout fits everyone.
6. **Simplicity, not minimalism.** Strip the unnecessary so the core purpose
   shines; burying everything in one place looks minimal but is not simple. Be
   concise and clear (hierarchy through order, spacing and contrast). Show the
   common path first, advanced options one level deeper.
7. **Craft.** Every spacing, timing and alignment value is a deliberate choice
   you can defend. Jittery scroll, misaligned icons and layouts that break on
   rotation read as carelessness. Craft needs iteration and longevity.
8. **Delight.** The result of getting the other seven right, not confetti tacked
   on top. Decide the emotion you want people to feel and reinforce it in every
   decision.

Tactical rules that serve them:
- Feedback comes in four kinds: status, completion, warning, error. Confirm
  meaningful actions, expose ongoing status, warn before problems, and validate
  inline rather than on submit.
- Wayfinding: every screen answers where am I, where can I go, what is there, and
  how do I get out. Never trap the user.
- Grouping and mapping: proximity implies relationship. Place a control near what
  it affects, and arrange controls to mirror what they change. If a label is
  needed to explain a control, the mapping is weak.
- Direct, specific labels beat safe generic ones: name nav items for their
  contents, not vague umbrellas.

## Process
- Prototype interactively: a working demo is worth a million static designs, and
  it sets a concrete bar that prevents a mediocre final implementation.
- Design interaction and visuals together; you should not be able to tell where
  one ends and the other begins. Motion is not a layer added after the pixels.
- Test with real people in real context, and review motion with fresh eyes in
  slow motion or frame by frame.
