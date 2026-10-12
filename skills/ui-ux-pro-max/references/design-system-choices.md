# Choosing a design system

Pick the system from the priority-ordered catalogue in `rules-catalogue.md`.
There is no search script to run; the catalogue is read, not queried.

## What to decide, in order
1. Layout pattern: from the product type (dashboard, marketing page, catalogue,
   feed, editor).
2. Style: from the style keywords in the brief (editorial, minimal, brutalist,
   playful, utilitarian).
3. Palette: one dominant colour with sharp accents; check contrast before
   committing.
4. Type pairing: a display face and a body face; check the body face survives
   long-form reading.
5. Chart types: from the question the data answers, not the shape of the data.

## Where depth lives
- Style, colour, typography, landing and UX rules: `rules-catalogue.md`.
- Palette mechanics and contrast maths: `better-colors`.
- Type scale and wrapping: `better-typography`.
- Chart and colour decisions for data: `dataviz`.

## Stack notes
The catalogue is framework-agnostic. Express the chosen tokens in the project's
own system: Tailwind `@theme` tokens for Tailwind, theme variables for a
component library, `shadcn` variants for shadcn. Do not copy a preset wholesale.

## Reconciling conflicts
When the style says editorial and the product type says dashboard, resolve in
favour of the product's job, then re-check accessibility. A palette that fails
contrast is a defect however it was chosen.
