---
name: minimalist-ui
description: Build clean editorial interfaces with a warm monochrome palette, typographic contrast, flat bento grids and muted pastel accents. Use when the brief asks for a minimal, document-style or workspace-style UI. Not for playful, maximalist or dark-tech looks.
metadata:
  audience: builder
  upstream: https://github.com/leonxlnx/taste-skill/tree/main/skills/minimalist-skill
  license: MIT
---
# Minimalist UI

An editorial, document-style directive: high-contrast warm monochrome palette,
bespoke type hierarchy, generous macro-whitespace, bento grids, an ultra-flat
component layer and sparing muted pastel accents. It rejects standard generic
SaaS design.

## When to use
- A brief asks for minimal, calm, editorial, document-style or workspace-style
  interfaces.
- A page needs typographic hierarchy and whitespace to carry the design.
- For an expressive or high-motion direction instead, use
  `high-end-visual-design` or `frontend-design`.

## Banned defaults
- No Inter, Roboto or Open Sans.
- No thin-line icon sets (Lucide, Feather, Heroicons) as the default.
- No heavy drop shadows: `shadow-md`, `shadow-lg`, `shadow-xl` are out; shadows
  are practically absent or ultra-diffuse below 0.05 opacity.
- No primary-coloured backgrounds for large sections or heroes.
- No gradients, neon, or 3D glassmorphism beyond a subtle navbar blur.
- No `rounded-full` pills for large containers, cards or primary buttons.
- No emojis in code, markup, copy, headings or alt text; use real icons or clean
  SVG primitives.
- No placeholder content (John Doe, Acme Corp, Lorem Ipsum); use realistic,
  contextual content.
- No copy cliches: elevate, seamless, unleash, next-gen, game-changer, delve.
  Write plain, specific language.

## Typography
- Body, UI and buttons: a clean geometric or native sans with character, e.g.
  `'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`.
- Hero headings and quotes: an editorial serif, e.g.
  `'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`,
  with tight tracking (`-0.02em` to `-0.04em`) and tight line-height (`1.1`).
- Code, keystrokes and metadata: `'Geist Mono', 'SF Mono', 'JetBrains Mono',
  monospace`.
- Body text is never absolute black: use off-black or charcoal (`#111111` or
  `#2F3437`) with `line-height: 1.6`. Secondary text is muted grey (`#787774`).

## Palette
Colour is scarce: semantic meaning and subtle accents only.
- Canvas: pure white `#FFFFFF`, warm bone `#F7F6F3` or `#FBFBFA`.
- Card surface: `#FFFFFF` or `#F9F9F8`.
- Borders and dividers: ultra-light grey `#EAEAEA` or `rgba(0,0,0,0.06)`.
- Accents are highly desaturated pastels only: pale red `#FDEBEC` with text
  `#9F2F2D`; pale blue `#E1F3FE` with text `#1F6C9F`; pale green `#EDF3EC` with
  text `#346538`; pale yellow `#FBF3DB` with text `#956400`.

## Components
- Bento feature grids: asymmetrical CSS Grid; every card has exactly
  `border: 1px solid #EAEAEA`; radius `8px` or `12px` maximum; internal padding
  `24px` to `40px`.
- Primary button: `#111111` background, `#FFFFFF` text, radius `4px` to `6px`,
  no box-shadow. Hover shifts to `#333333` or scales to `0.98` on `:active`.
- Tags and badges: pill radius, `text-xs`, uppercase with `letter-spacing:
  0.05em`, background from the muted pastels above.
- Accordions: strip container boxes, separate items with a single
  `border-bottom: 1px solid #EAEAEA`, and use a sharp `+` and `-` toggle.
- Keystrokes: `<kbd>` with `border: 1px solid #EAEAEA`, `border-radius: 4px`,
  `background: #F7F6F3`, monospace font.
- Software mockups: wrap in a minimal container with a white top bar carrying
  three small light grey circles.

## Iconography and imagery
- Icons: Phosphor (bold or fill) or Radix UI Icons, one standard stroke width
  across the surface.
- Illustrations: monochrome continuous-line ink sketches on white, with one
  offset geometric shape filled in a muted pastel.
- Photography: desaturated, warm tone, with a subtle warm overlay (`opacity:
  0.04`) so images blend into the monochrome palette. Never oversaturated stock.
  When real assets are missing use a seeded placeholder such as
  `https://picsum.photos/seed/{context}/1200/800`.
- No section is an empty flat background: use full-width imagery at very low
  opacity, a soft warm radial light spot (`opacity: 0.03`), or minimal geometric
  line patterns.

## Motion
Quiet sophistication, never spectacle.
- Scroll entry: `translateY(12px)` plus `opacity: 0` resolving over `600ms`
  with `cubic-bezier(0.16, 1, 0.3, 1)`, driven by `IntersectionObserver`, never
  a scroll event listener.
- Hover: cards move from `0 0 0` to `0 2px 8px rgba(0,0,0,0.04)` over `200ms`;
  buttons use `scale(0.98)` on `:active`.
- Staggered reveals: `animation-delay: calc(var(--index) * 80ms)`, never mount
  everything at once.
- Optional ambient motion: one very slow radial blob (`20s` or longer, opacity
  `0.02` to `0.04`) on a `position: fixed; pointer-events: none` layer behind the
  hero, never on a scrolling container.
- Animate `transform` and `opacity` only; no layout-triggering properties. Use
  `will-change: transform` sparingly.

## Execution order
1. Set the macro-whitespace: massive vertical padding between sections (`py-24`
   or `py-32`).
2. Constrain typographic content to `max-w-4xl` or `max-w-5xl`.
3. Apply the type hierarchy and monochrome variables before anything else.
4. Check that every card, divider and border obeys the `1px solid #EAEAEA` rule.
5. Add scroll-entry animation to all major content blocks.
6. Give every section depth through imagery, ambient gradient or texture.
7. Ship code that already reflects the aesthetic; no manual cleanup later.

## Checklist
- [ ] No banned font, icon set, shadow, gradient, emoji or placeholder text
- [ ] Serif headings, sans body, mono metadata, applied from the hierarchy
- [ ] Body text off-black with `line-height: 1.6`; accents from the pastels
- [ ] Every border is `1px solid #EAEAEA`; radius at most `12px`
- [ ] Cards, buttons, badges, accordions and keystrokes follow the specs
- [ ] Sections are not empty flat backgrounds
- [ ] Scroll entry, hover and stagger motion applied; reduced motion respected
