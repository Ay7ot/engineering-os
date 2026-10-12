---
name: design-taste-frontend
description: Design direction for landing pages, marketing sites and portfolios so they do not read as templated: read the brief, set the variance, motion and density dials, then build. Use when building or redesigning a landing page, portfolio or marketing section. Not for dashboards or data tables.
metadata:
  audience: builder, architect
  upstream: https://github.com/leonxlnx/taste-skill/tree/main/skills/taste-skill
  license: MIT
---
# Design Taste for Frontend

Landing pages, portfolios and marketing sites only. Not dashboards, not data
tables, not multi-step product UI.

## When to use
- Building a landing page, portfolio, marketing page or about page.
- Redesigning one of those; `redesign-existing-projects` owns the audit pass.
- A page looks templated and you need to find out why.

## Read the brief first
Before writing code, infer what the user wants and state it in one line:
"Reading this as: <page kind> for <audience>, with a <vibe> language, leaning
toward <design system or aesthetic family>."

Read: page kind; the vibe words the user used; linked URLs, screenshots and
competitors; who the audience is; brand assets that already exist; quiet
constraints such as accessibility-first, public sector, regulated industries,
trust-first commerce, kids' products. Constraints override aesthetic preference.

If the design read genuinely diverges, ask exactly one question, never a list.
If you can infer from context, do not ask.

Do not default to: purple gradients, a centered hero over a dark mesh, three
equal feature cards, glassmorphism on everything, Inter plus slate-900.

## Set the three dials
Every layout, motion and density decision is gated by these. Baseline 8 / 6 / 4.

- `DESIGN_VARIANCE`: 1 = perfect symmetry, 10 = artsy chaos.
- `MOTION_INTENSITY`: 1 = static, 10 = cinematic physics.
- `VISUAL_DENSITY`: 1 = airy gallery, 10 = packed cockpit.

Infer from the brief: minimalist, calm or editorial 5-6 / 3-4 / 2-3; premium
consumer, Apple-like or luxury 7-8 / 5-7 / 3-4; playful, Awwwards or agency
9-10 / 8-10 / 3-4; trust-first, public sector or regulated 3-4 / 2-3 / 4-5.
A redesign that preserves the brand keeps the existing values with motion +1.
Use these names only; never invent aliases.

## Pick the foundation honestly
When the brief reads as an existing system, install its official package instead
of hand-rebuilding it: Microsoft or enterprise SaaS -> Fluent UI; a Google-like
product -> Material Web plus Material 3 tokens; IBM-style analytics -> Carbon;
Shopify apps -> Polaris; Atlassian-style product -> Atlaskit; GitHub-style
devtool -> Primer; UK public sector -> GOV.UK Frontend; US public sector ->
USWDS; a modern accessible React foundation -> Radix Themes; components you own
-> shadcn/ui (see `shadcn`); indie and small-team SaaS -> Tailwind v4 utilities
(see `tailwind-design-system`). One system per project, never two.

When the brief is an aesthetic rather than a system (glassmorphism, bento,
brutalism, editorial, dark tech, aurora, kinetic type), no official package
exists: build with native CSS, Tailwind and a maintained component library, and
say in a comment what is borrowed inspiration. Apple Liquid Glass is documented
for Apple platforms only; on the web it is a labeled approximation.
Install commands and canonical sources: references/design-systems.md.

## Design engineering directives
- Type: display `text-4xl md:text-6xl tracking-tighter leading-none`; body
  `text-base leading-relaxed max-w-[65ch]`. Inter is banned as the default;
  reach for Geist, Outfit, Cabinet Grotesk or Satoshi. Serif is very discouraged
  as a default: keep it for a brand that names one or a genuinely editorial,
  luxury or heritage brief. Fraunces and Instrument Serif are banned. Italic
  display words containing `y g j p q` need `leading-[1.1]` plus `pb-1`, or the
  descender clips. Emphasize with italic or bold of the same family, never by
  dropping a serif word into a sans headline.
- Colour: one accent, saturation under 80%, neutral base. No automatic purple
  glow. One palette per project, and once an accent is chosen it is used on the
  whole page. For premium-consumer briefs the beige/cream plus brass/clay/
  oxblood/espresso family is banned as the default; rotate instead (cold luxury,
  forest, black and tan, cobalt and cream, terracotta and slate, monochrome plus
  one pop).
- Layout: avoid centered heroes when `DESIGN_VARIANCE` is above 4. Never use
  `h-screen`; use `min-h-[100dvh]`. Use CSS Grid, never flexbox percentage math.
  Constrain the page with `max-w-[1400px] mx-auto`.
- States: skeleton loaders instead of spinners, composed empty states, inline
  error states, `scale-[0.98]` press feedback. Every CTA passes WCAG AA contrast
  against its background, its label does not wrap at desktop, and one intent
  keeps one label across the page.
- Density: a section is short headline (8 words) plus short sub-paragraph (25
  words) plus one asset or one CTA. Lists over 5 items need another component
  (card grid, tabs, scroll-snap pills, carousel, marquee), not a longer list.

## Non-negotiables
- Zero em dashes in visible copy; date and number ranges use a hyphen.
- One theme per page; sections do not invert mid-page.
- Real images: an image-generation tool first, then `picsum.photos/seed/...` or
  real brand assets, and labeled placeholder slots when neither exists. Div-based
  fake screenshots and hand-rolled decorative SVG are banned.
- Motion is motivated (hierarchy, storytelling, feedback, state change), at most
  one marquee per page, `prefers-reduced-motion` honored above intensity 3, and
  `window.addEventListener("scroll")` is banned. Recipes:
  references/motion-recipes.md.

## Detect AI tells
references/anti-slop-checklist.md lists the banned patterns (hero, eyebrow,
pills, dividers, locale strips, copy cliches) and the full pre-flight matrix.
Walk it before handing anything over.

## Checklist
- [ ] Design read stated in one line
- [ ] Dial values explicit and reasoned from the brief
- [ ] Foundation chosen; official package used where one exists
- [ ] Zero em dashes; no banned hero, eyebrow, pill or label patterns
- [ ] One theme, one accent, one radius system, one copy register per page
- [ ] Hero fits the viewport with the CTA visible without scroll
- [ ] Images, empty, loading and error states done
- [ ] Contrast checks pass for CTAs and forms
- [ ] references/anti-slop-checklist.md walked end to end
