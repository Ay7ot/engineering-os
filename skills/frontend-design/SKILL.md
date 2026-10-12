---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with a deliberate aesthetic direction, avoiding generic generated defaults. Use when building web components, pages or posters that need real design quality rather than a default look. Not for design-system plumbing.
metadata:
  audience: builder
  upstream: https://github.com/anthropics/skills/tree/main/skills/frontend-design
  license: Apache-2.0
---
# Frontend Design

Create distinctive, production-grade interfaces that avoid generic aesthetics.
Ship real working code with exceptional attention to aesthetic detail and
creative choice, not a template.

## When to use
- Building a web component, page, artifact, poster or small app that needs a
  designed look.
- A UI has to feel intentional rather than assembled from defaults.
- For the landing-page specific rules (dials, hero discipline, pre-flight
  checks) use `design-taste-frontend`; for premium agency texture use
  `high-end-visual-design`; for editorial minimalism use `minimalist-ui`. For
  tokens and component plumbing use `tailwind-design-system`.

## Design thinking first
Before coding, understand the context and commit to a bold aesthetic direction.
- Purpose: what problem does this interface solve and who uses it?
- Tone: pick an extreme and mean it. Brutally minimal, maximalist chaos,
  retro-futuristic, organic, luxury or refined, playful and toy-like,
  editorial or magazine, brutalist and raw, art deco or geometric, soft pastel,
  industrial and utilitarian.
- Constraints: framework, performance budgets, accessibility requirements.
- Differentiation: what makes this unforgettable? What is the one thing someone
  will remember?

Choose one clear conceptual direction and execute it with precision. Bold
maximalism and refined minimalism both work; the key is intentionality, not
intensity.

## Aesthetic guidelines
- Typography: choose fonts that are beautiful, unique and interesting. Avoid
  generic families such as Arial, Roboto and Inter, and opt for distinctive
  choices that elevate the work. Check the licence before introducing a face.
- Colour and theme: commit to one cohesive aesthetic and drive it from CSS
  variables for consistency. Dominant colours with sharp accents outperform
  timid, evenly distributed palettes.
- Motion: use animation for effects and micro-interactions, and concentrate it
  on high-impact moments. One well-orchestrated page load with staggered reveals
  creates more delight than scattered micro-interactions everywhere.
- Spatial composition: unexpected layouts. Asymmetry, overlap, diagonal flow,
  grid-breaking elements, generous negative space or controlled density.
- Backgrounds and visual detail: create atmosphere and depth rather than
  defaulting to flat solid fills. Add contextual effects and textures that match
  the chosen aesthetic.

## Never use
- Overused font families: Inter, Roboto, Arial, system defaults.
- Clichéd colour schemes, particularly purple gradients on white.
- Predictable layouts and the same component patterns every project.
- The same aesthetic twice: no two designs from you should look alike.

Generic output is the failure mode. If the result could have come from a
default template, it is not finished.

## Match complexity to the vision
Scale the implementation to the direction you chose. Maximalist designs need
elaborate code, real animation and layered effects. Minimalist or refined
designs need restraint, precision and meticulous spacing, typography and subtle
detail. Do not decorate a minimal direction, and do not under-build a maximal
one.

Keep the result usable: readable contrast, keyboard-reachable controls, and
motion that respects `prefers-reduced-motion`. Design quality does not excuse
broken accessibility; check the details with `better-typography`,
`better-colors` and `better-ui`.

## Checklist
- [ ] Purpose, tone, constraints and differentiation stated before coding
- [ ] One clear aesthetic direction chosen and carried through the whole piece
- [ ] Type, colour, motion, composition and background all serve that direction
- [ ] No banned generic families, clichéd gradient scheme or stock layout
- [ ] Implementation complexity matches the direction
- [ ] Contrast, keyboard access and reduced motion respected
- [ ] The result does not resemble a default template
