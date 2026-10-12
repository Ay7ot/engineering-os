---
name: ip-as-logo
description: Generate a simple, cute, personified square IP character image with one bold silhouette, two character colors, one solid background, rooted in a lower corner. Use when making a mascot or creature image, or proposing three directions and six candidates.
metadata:
  audience: builder
  upstream: https://github.com/s1dashu/ip-as-logo-skill
  license: MIT
---
# IP as Logo

One image of the simplest possible cute IP character: a compact symbol that stays recognizable at 32 by 32, not a character illustration. `prompt-images` covers general prompting; this is the character brief.

## When to use
- A mascot, creature, robot, ghost, plant or object character image.
- The agent should propose directions first, then generate a batch of candidates.

## Workflow
1. Parse the request for an explicit IP subject and product context. Do not ask the user to pick a colour mode unless they want to control it.
2. No subject and the workspace is a product repo: read the README, product docs, package or app metadata, landing copy, manifests and design tokens first. Context is sufficient when purpose, audience and personality can be inferred.
3. If context is insufficient, ask one consolidated round about what the product does, who it serves and how it should feel. Never start a second questionnaire; continue with the best interpretation.
4. Always present three concise directions before generating, and propose six independent candidates in one batch. Do not generate until the user agrees, unless the request already authorizes six outputs or says to proceed.
5. Choose the three directions deliberately: with a fixed subject, vary the treatment (silhouette, secondary colour region, defining feature, personality emphasis); without one, propose three different subjects, each tied to a different product attribute. One line each: subject, product connection, defining silhouette.
6. Generate as one-pass draws: never compose a contact sheet, never use a previous candidate as a reference, never retry or repair output. Deliver every returned image with its label, direction, assigned corner, path, prompt and dimensions.

## Distribution
- All three directions accepted: two variants each, `A1`, `A2`, `B1`, `B2`, `C1`, `C2`. Lower-left gets `A1`, `B1`, `C1`; lower-right gets `A2`, `B2`, `C2`, so each direction is tested from both sides.
- One direction and six images: `A1` to `A6`; odd numbers to lower-left, even to lower-right.
- Otherwise split an even batch evenly between the two corners; for an odd batch assign the extra side deliberately and record the imbalance. Never bottom-centre unless asked.

## Complexity budget
- One dominant continuous outer silhouette from 4 to 7 large basic shapes. Merge or delete any shape that carries no identity, expression or recognition.
- At most one species-defining feature (a pouch beak, curled horns, a broad visor). At most two broad internal colour regions. The face is two eyes, plus one tiny mouth only when the expression needs it.
- No feathers, scales, fur tufts, armour plates, buttons, screws, numbers, labels, outlines, highlights or texture. No glossy hotspots or detailed cavity rendering in small features.
- Cuteness and an endearing baby-like personality are decisive: large head, compact proportions, soft cheeks, widely spaced simple eyes, calm friendly expression.
- Must read as a black silhouette and stay recognizable at 32 by 32. If a feature turns to noise at that size, enlarge, merge or remove it.

## Shape and composition
- Thick, rounded, weighty contours and broad colour masses. Forbid sharp corners, pointed ears or beaks, needle tails, thin antennae, thin smiles, narrow gaps and acute tips; blunt every necessary tip.
- Show both members of paired features (ears, horns, wings, gills). Keep the character upright; never rotate the canvas without an explicit request.
- Place the character upright, emerging from the assigned lower-left or lower-right corner and filling 85 to 95 percent of the canvas. Cropping at the bottom or that side is welcome. Never centre or bottom-centre it.

## Colour and canvas
- Exactly three semantic colours in the whole image: two IP base colours plus one background. Reuse the two IP colours for facial marks; introduce no fourth colour.
- Choose both subject colours from the product context, subject and personality, and organise them into broad masses. Choose the background independently, or from a user-supplied palette. Unless vivid colour is asked for, lower the background saturation slightly so it is clearly chromatic but muted, not gray or muddy.
- Keep the IP, its facial marks and the background clearly separated. If a supplied background kills separation, adjust the subject colours, not the background.
- Solid, uniform background: no scenery, texture, halo, vignette or lighting variation. One subtle dimensional sentence is allowed; incidental gradients the generator returns are acceptable and must not trigger retries.
- Output a 1:1 square with square corners, request about 1536 by 1536, and accept a native 1254 by 1254 limit without resampling.

## Model, parallelism and prompt
- Require a top-tier image model. Prefer the strongest instruction-following image model available; if none is configured, ask the user to enable one or supply an API key. Never fall back to SVG. Use a weaker model only with explicit consent, and say quality may differ.
- If parallel agents are available (`task`), run the six candidates concurrently with the same brief and one direction each; otherwise run separate generation jobs.
- Route constraints by capability: modern instruction-following models take the exclusions in a natural-language `Constraints:` line; older models with a dedicated negative-prompt parameter take them there instead, and the line is dropped.
- Never describe the output as a logo, brand mark, app icon or icon asset inside the generation prompt.
- The full prompt skeleton is in references/prompt-skeleton.md.

## Checklist
- [ ] Three directions stated; six candidates proposed and approved
- [ ] Corners assigned and every label recorded
- [ ] 4 to 7 shapes; one defining feature; two eyes
- [ ] Three semantic colours; solid uniform background
- [ ] Readable at 32 by 32; upright; corner-rooted
- [ ] Every result delivered as-is with prompt and dimensions
