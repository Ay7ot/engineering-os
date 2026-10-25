---
name: theme-factory
description: Style an artifact with a designed theme, one cohesive palette plus a heading and body font pairing, chosen from a set of presets or generated to fit. Use when a slide deck, doc, report or HTML page needs a consistent look. Not for a fixed corporate palette (`brand-guidelines`).
metadata:
  audience: builder
  upstream: https://github.com/anthropics/skills/tree/main/skills/theme-factory
  license: Apache-2.0
---
# Theme Factory

A theme is a small closed set of decisions: a palette with hex codes, a heading font, a body font, and the rules for applying them to surfaces, text, accents and borders. Apply one theme to every element so nothing is styled off-theme.

## When to use
- A slide deck, document, report, HTML landing page or other artifact needs a consistent visual identity.
- The user should choose from ready-made themes rather than apply their company palette (`brand-guidelines`) or have a design language invented (`frontend-design`).

## Choose a theme
1. Show a showcase: render a sample of the artifact's own components (title, body, a table or list, an accent shape) in each candidate theme. A swatch strip alone does not show how a theme behaves on real content.
2. Ask which theme to apply, and for anything that overrides it (a required brand colour, a dark variant, a print version).
3. Wait for explicit confirmation. Do not apply a theme on a guess.
4. Apply the chosen theme's colours and fonts everywhere, then check contrast and readability before finishing.

## Preset themes
1. Ocean Depths: calm, professional maritime blues.
2. Sunset Boulevard: warm, vibrant sunset tones.
3. Forest Canopy: grounded natural earth tones.
4. Modern Minimalist: clean contemporary grayscale.
5. Golden Hour: rich, warm autumnal palette.
6. Arctic Frost: cool, crisp winter tones.
7. Desert Rose: soft, sophisticated dusty tones.
8. Tech Innovation: bold modern tech aesthetic.
9. Botanical Garden: fresh organic garden colours.
10. Midnight Galaxy: dramatic deep cosmic tones.

## Generate a custom theme
When none fit, build one from the inputs: pick a base surface, a text colour, one primary accent and one secondary accent, then a heading and body pair that contrast in weight or class (for example a geometric sans heading over a humanist serif body). Name it after what the pairing represents, in the same style as the presets. Then apply it exactly as a preset: one palette, one pair, used consistently.

## Rules
- Define a theme's colours as tokens once (CSS variables or a theme object), never inline per element, so a brand swap changes one place.
- One theme per artifact. Do not mix two presets.
- Keep body text at a readable size and check contrast on every surface the theme defines: text on base, text on accent, accent on base.
- Preserve the artifact's existing hierarchy; a theme changes look, not structure or wording.

## Checklist
- [ ] Showcase rendered on the artifact's real components
- [ ] Theme chosen and confirmed, not assumed
- [ ] Colours defined as tokens and applied consistently
- [ ] Heading and body fonts come only from the pairing
- [ ] Contrast checked on every surface
