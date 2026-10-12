---
name: prompt-images
description: Write prompts for AI image generation and editing models: natural-language scene descriptions, photographic lighting vocabulary, text, style and character consistency. Use when prompting an image model or building an image generation feature. Not for video (`prompt-videos`).
metadata:
  audience: builder, architect
  upstream: https://github.com/replicate/skills/tree/main/skills/prompt-images
  license: Apache-2.0
---
# Prompting Image Models

Transferable techniques for image generation and editing models, distilled from model
provider write-ups. The techniques outlive the specific models, so treat model names
as examples, not requirements.

## When to use
- Writing a prompt for an image model, or building image generation into a feature.
- Editing an existing image, removing objects, changing backgrounds or transferring style.
- For character mascots with a fixed brief, `ip-as-logo` adds the character rules.

## Pick the model from the API, not from memory
The model landscape changes weekly. Query the provider API or model catalogue for
current options, read the model's schema (input names, defaults, aspect ratios,
whether it supports negative prompts) before running anything, and compare pricing
and strengths across candidates. Do not assume a model exists, or is best, because
you remember the name. Different models win at different tasks: text rendering,
object removal, style transfer, background edits.

## Writing prompts
- Natural language, not keyword lists. "A woman standing in a Tokyo alleyway at dusk,
  neon signs reflecting off wet pavement", not "woman, Tokyo, dusk, neon, wet".
- Be specific and unambiguous: exact colours, materials, lighting, camera gear,
  spatial relationships. "Make it better" or "artistic" gives unpredictable results.
- Name subjects directly: "the woman with short black hair", "the red car". Avoid
  pronouns, which are ambiguous to these models.
- Long, detailed prompts beat short ones. Modern models accept thousands of tokens
  and a prompt with 12 plus specific requirements can work, if each one is stated
  clearly. The longer and more complex the prompt, the more likely something is missed.
- Start simple and iterate: make a small change, evaluate, refine. Editing models
  support iterative editing, so build on what works instead of one-shotting.

## Photographic language
These models understand camera and lighting vocabulary deeply, which gives precise
control over the look: film stocks (Kodak Portra 800, Fuji Velvia 50, Ilford HP5);
lenses (50mm wide open, 85mm f/1.4, 24mm wide-angle); depth of field; golden hour,
blue hour, long exposure, double exposure; and named lighting setups (Rembrandt,
soft diffused studio, rim or backlight, flat overcast, volumetric with fog). Full
lists, plus composition and framing vocabulary, are in references/prompt-vocabulary.md.

## Text, style, characters
- Text in images: wrap the exact string in double quotes inside the prompt, stick to
  readable fonts, edit with the pattern "Change 'old text' to 'new text'", keep the
  character count similar, and prefer models that compose text rather than stamp it.
- Style: name the exact style or artist or movement; if the label fails, describe its
  traits ("visible brushstrokes, thick paint texture, rich colour depth"); say what
  must stay the same ("keep the original composition"). Some models accept a style
  reference image or a before/after pair.
- Character consistency is the hardest part: fix a verbatim reference description,
  state what changes and what stays, use reference images when supported, and break
  complex changes into steps (outfit first, then scene).

## Editing an image
- Always state what to keep: "keeping the pose and expression unchanged", "maintain
  the original composition". Unstated, models may change anything.
- Choose verbs carefully. "Transform" implies a full rework; use the exact action:
  "change the clothes to a blue jacket", "replace the background with a beach".
- Be precise about scope: "change the background to a beach while keeping the person
  in the exact same position; maintain identical subject placement, camera angle,
  framing and perspective; only replace the environment around them".
- Object removal: describe what fills the space, not only what leaves. If one model
  leaves structural artifacts, try another.
- Perspective and angle changes are the hardest edits and not every model handles them.
- Inpainting and outpainting: mask the region, then prompt what should fill it.
  Describing only the masked region makes the model weight the prompt more, which
  helps targeted edits. Edge or depth conditioning helps preserve structure.

## Watch out
The frequent failures are keyword-stuffed prompts, using "transform" for a small
edit, omitting what must stay the same, negative prompts on models not trained for
them, an over-high guidance scale, ignoring the aspect ratio, and one-shotting a
complex scene. The full list of ten is in references/prompt-vocabulary.md.

## Checklist
- [ ] Model chosen from the live API and schema, not from memory
- [ ] Prompt is prose and names subjects directly, no pronoun ambiguity
- [ ] Lighting, materials and framing stated concretely
- [ ] For edits, what to keep is stated explicitly
- [ ] Aspect ratio and parameters match the model's recommendations
- [ ] Iterated with small changes rather than a single attempt
