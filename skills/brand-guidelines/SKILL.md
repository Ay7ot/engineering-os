---
name: brand-guidelines
description: Apply an official brand palette and typography to an artifact so it reads as one brand, using exact hex colors for surfaces, text and accents plus heading and body fonts with safe fallbacks. Use when brand colors, style guidelines or company design standards apply.
metadata:
  audience: builder, architect
  upstream: https://github.com/anthropics/skills/tree/main/skills/brand-guidelines
  license: Apache-2.0
---
# Brand Guidelines

Applies a fixed brand identity to any artifact: a slide, doc, report, chart, diagram, email or HTML page. If the project ships its own brand file or design tokens, read those and replace the values below; the method is the same. This is not for choosing a new palette from scratch (`better-colors`) or deciding a whole visual direction (`frontend-design`).

## When to use
- Applying official brand colours and fonts to an artifact of any kind.
- An artifact looks off-brand, or several palettes and typefaces have crept in.
- Post-processing output so it matches the rest of the company's material.

## Colours
Main:
- Dark `#141413`: primary text and dark backgrounds.
- Light `#faf9f5`: light backgrounds, and text on dark.
- Mid gray `#b0aea5`: secondary elements.
- Light gray `#e8e6dc`: subtle backgrounds.

Accents:
- Orange `#d97757`: primary accent.
- Blue `#6a9bcc`: secondary accent.
- Green `#788c5d`: tertiary accent.

Non-text shapes use accent colours, cycling orange, blue then green, so one artifact does not collapse to monochrome. Never put mid gray on light gray or light text on a light surface; check each pairing you actually use.

## Typography
- Headings at 24pt and larger: the heading face (Poppins), fallback Arial.
- Body text: the body face (Lora), fallback Georgia.
- Use installed fonts when present and fall back silently when they are not; never block output on a font download. The fallback must stay readable.
- Keep the heading and body hierarchy: do not set body copy in the heading face, and do not shrink body text to fit a slide.

## Apply it
1. Pick the value for each role from the tokens above, not a near match: text, background, secondary text, subtle background, accents.
2. Apply heading and body faces by role, with the fallback declared alongside.
3. Give shapes and rules accent colours in the fixed cycle, not a random choice per element.
4. State colours as exact hex or RGB so fidelity holds across systems.
5. Recheck contrast after the theme is applied, especially any dark surfaces.

## Checklist
- [ ] Every colour comes from the token set, no approximate values
- [ ] Headings and body use their own face, fallbacks declared
- [ ] Accents cycle orange, blue, green on non-text shapes
- [ ] Contrast checked on each text and background pairing
- [ ] No third typeface introduced
