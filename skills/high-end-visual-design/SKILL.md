---
name: high-end-visual-design
description: Design expensive-looking, agency-grade interfaces: archetype selection, double-bezel containers, nested CTAs, choreographed motion and layout collapse rules. Use when a page must feel premium or Awwwards-tier, or when a design looks cheap and generic.
metadata:
  audience: builder
  upstream: https://github.com/leonxlnx/taste-skill/tree/main/skills/soft-skill
  license: MIT
---
# High-End Visual Design

Engineer agency-grade experiences, not just pages: haptic depth, cinematic
spatial rhythm, obsessive micro-interactions, fluid motion. The variance
mandate: never generate the same layout or aesthetic twice in a row. Vary the
archetypes below while keeping an Apple-esque or Linear-tier language.

## When to use
- A page must read as a premium, agency-built product rather than a template.
- Adding haptic depth, choreographed motion or refined surfaces to existing UI.
- For flat editorial minimalism instead, use `minimalist-ui`; for a full
  redesign of an existing site, start with `redesign-existing-projects`.

## The Absolute Zero directive
If the code contains any of these, the design fails.
- Banned fonts: Inter, Roboto, Arial, Open Sans, Helvetica. Assume premium
  families such as Geist, Clash Display, PP Editorial New or Plus Jakarta Sans.
- Banned icons: thick-stroked Lucide, FontAwesome, Material Icons. Use
  ultra-light precise lines (Phosphor Light, Remix Line).
- Banned borders and shadows: generic 1px solid grey borders; harsh dark drop
  shadows such as `shadow-md` or `rgba(0,0,0,0.3)`.
- Banned layouts: edge-to-edge sticky navbars glued to the top; symmetrical
  3-column Bootstrap-style grids with no whitespace gaps.
- Banned motion: `linear` or `ease-in-out` transitions; instant state changes
  with no interpolation.

## Roll the variance engine
Pick one vibe and one layout before writing code.

Vibe and texture archetypes:
1. Ethereal Glass (SaaS, AI, tech): deepest OLED black `#050505`, radial mesh
   gradients behind the content, vantablack cards with `backdrop-blur-2xl` and
   pure white/10 hairlines, wide geometric grotesk type.
2. Editorial Luxury (lifestyle, real estate, agency): warm cream `#FDFBF7`,
   muted sage or deep espresso, high-contrast variable serif headings, CSS noise
   or film-grain overlay at `opacity-[0.03]` for a paper feel.
3. Soft Structuralism (consumer, health, portfolio): silver-grey or white
   backgrounds, massive bold grotesk type, airy components with soft diffused
   ambient shadows.

Layout archetypes:
1. Asymmetrical Bento: grid of varying card sizes, for example a
   `col-span-8 row-span-2` next to stacked `col-span-4` cards.
2. Z-Axis Cascade: elements stacked like physical cards with small overlaps and
   a `-2deg` or `3deg` rotation to break the grid.
3. Editorial Split: massive type in the left half (`w-1/2`), interactive
   scrollable image pills or staggered cards on the right.

Mobile override, universal: any asymmetric layout above `md:` falls back to
`w-full`, `px-4`, `py-8` below 768px. Bento resets overrides to `col-span-1`
and stacks with `gap-6`. Cascade removes rotations and negative margins below
768px, because overlaps cause touch-target conflicts. Never use `h-screen`; use
`min-h-[100dvh]` to stop iOS Safari viewport jumping.

## Micro-aesthetics
- Double-bezel containers: never place a premium card flat on the background.
  Outer shell: a wrapper with `bg-black/5` or `bg-white/5`, a hairline border
  (`ring-1 ring-black/5`), padding such as `p-1.5`, and a large radius such as
  `rounded-[2rem]`. Inner core: its own background, an inner highlight
  (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and a mathematically
  smaller radius (`rounded-[calc(2rem-0.375rem)]`) so the curves stay concentric.
- Buttons are full pills (`rounded-full`, `px-6 py-3`). A trailing arrow never
  sits naked: nest it in its own circle `w-8 h-8 rounded-full bg-black/5` flush
  with the right inner padding.
- Spatial rhythm: double the usual padding. Sections use `py-24` to `py-40`.
  Precede major headings with a microscopic pill eyebrow
  (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]`), and follow
  the eyebrow budget in `design-taste-frontend`.

## Motion choreography
All motion simulates mass and spring. Use custom beziers such as
`ease-[cubic-bezier(0.32,0.72,0,1)]` over 700ms.
- Nav: closed state is a floating glass pill (`mt-6 mx-auto w-max
  rounded-full`). The hamburger lines rotate and translate into a real `X`. The
  menu opens as a screen-filling overlay (`backdrop-blur-3xl bg-black/80`), and
  its links fade and slide up from `translate-y-12 opacity-0` with staggered
  `delay-100`, `delay-150`, `delay-200`.
- Buttons: on `:active` scale to `0.98` to simulate a press; the nested icon
  circle translates diagonally on hover (`group-hover:translate-x-1
  group-hover:-translate-y-[1px]`) and scales to `105`.
- Scroll entry: elements never appear statically. As they enter the viewport
  they resolve `translate-y-16 blur-md opacity-0` to
  `translate-y-0 blur-0 opacity-100` over 800ms or more. Use
  `IntersectionObserver` or `whileInView`, never a scroll event listener.

## Performance guardrails
- Animate `transform` and `opacity` only; never `top`, `left`, `width` or
  `height`. Use `will-change: transform` sparingly, only while animating.
- Apply `backdrop-blur` only to fixed or sticky elements, never to scrolling
  containers or large content areas, which forces continuous GPU repaints.
- Attach grain and noise only to fixed, `pointer-events-none` pseudo-elements
  (`position: fixed; inset: 0; z-index: 50`), never to scrolling containers.
- Reserve z-index for systemic layers: sticky nav, modals, overlays, tooltips.

## Execution protocol
1. Roll the variance engine: choose one vibe and one layout archetype.
2. Scaffold the background texture, macro-whitespace scale and type sizes.
3. Architect the DOM with double-bezel enclosures for major cards, inputs and
   feature grids, using exaggerated squircle radii.
4. Choreograph the custom beziers, staggered nav reveals and button hover
   physics.
5. Deliver pixel-perfect code with no generic fallbacks.

## Checklist
- [ ] No banned font, icon, border, shadow, layout or motion pattern present
- [ ] One vibe archetype and one layout archetype chosen and applied
- [ ] Major containers use the double-bezel architecture
- [ ] CTA trailing icons are nested in their own circle
- [ ] Section padding at least `py-24`
- [ ] All transitions use custom beziers, no `linear` or `ease-in-out`
- [ ] Scroll entry animation present; nothing appears statically
- [ ] Layout collapses below 768px to a single column with `px-4`
- [ ] Only `transform` and `opacity` animate; blur is fixed-element only
