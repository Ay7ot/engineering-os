# Prompt skeleton

Two delivery modes. Pick by the capability of the model actually configured, not
by a guessed model name.

## Modern instruction-following models, and single-prompt interfaces

Keep the whole positive prompt and express the exclusions as the natural-language
`Constraints:` line inside it. Do not also create a separate negative payload.

```text
Create one complete full-bleed 1:1 square image.
Background: fill the entire square with solid <background>. Keep <background> visible in every open area and in the corners not occupied by the character; the assigned emergence corner must be occupied by the character.
Subject: place one extremely simplified, cute, endearing <subject> IP character on the background, reduced to one soft rounded continuous silhouette and one defining feature.
Complexity: use only 4 to 7 large basic shapes and at most two broad internal colour regions. Use two simple eyes and add one tiny mouth only when it helps the expression. Remove every nonessential line, outline, anatomical detail, texture and decoration. Keep the character readable at 32 by 32.
Colour behavior: use exactly three semantic colours in the complete image: exactly two IP base colours plus the background colour. Choose the two IP colours from the subject and context, organise both into broad purposeful masses, and reuse them for facial marks. Choose the background independently or follow the user's supplied background. Unless the user asks for vivid colour, lower the background saturation slightly so it feels gently muted and restrained while remaining clearly chromatic, clean and intentional rather than gray or muddy. Keep the IP, facial marks and background clearly separated. Treat any example palette as optional inspiration, never as an allowlist.
Composition: keep the character upright and emerging from the assigned <lower-left or lower-right>, filling about 85 to 95 percent of the square so it remains visually dominant. Cropping at the bottom or assigned side is welcome when it strengthens the corner emergence. Preserve both paired identifying features. Never center or bottom-center the character.
Style: make simplification, cuteness and lovable baby-like appeal the strongest qualities. Use large soft forms, compact proportions, thick rounded contours and an ultra-clean graphic treatment. Prefer one clear shape over several explanatory details. Add an extremely, extremely subtle, almost imperceptible sense of depth through a barely-there neo-skeuomorphic treatment.
Finish: show only the character on the full-canvas background, with clean surfaces and normal square outer corners.
Constraints: Use no text or watermark. Add no borders, frames, cards or presentation masks. Include one character only, with no extra subjects or scenery. Use no fragile lines, sharp tips, unnecessary outlines, tiny details or decorative marks. Add no photorealistic material, dramatic bevel, glossy hotspot, deep occlusion, extrusion, strong three-dimensional rendering or external cast shadow. Keep the background solid and uniform, with no texture, vignette or lighting variation.
```

## Older models with a dedicated negative-prompt parameter

Keep every positive prompt line above unchanged, drop the `Constraints:` line, and
deliver the exclusions through the parameter in the syntax that adapter requires:

```text
text, watermark, borders, frames, cards, presentation masks, extra subjects, scenery, thin fragile lines, sharp tips, photorealistic materials, strong three-dimensional rendering, external cast shadows
```

## Reporting
Record the model or provider, the detected constraint-delivery mode (main-prompt
constraints or dedicated negative parameter), and the exact constraint text used,
alongside each candidate's label, direction, corner, path and dimensions.
