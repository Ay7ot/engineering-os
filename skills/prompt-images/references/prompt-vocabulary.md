# Image prompt vocabulary

## Camera and lens
- Film stocks: Kodak Portra 800, Fuji Velvia 50, Ilford HP5.
- Lens characteristics: 50mm Summilux wide open, 85mm f/1.4, 24mm wide-angle.
- Depth of field: shallow (subject sharp, background blurred), deep (everything in
  focus).
- Shooting techniques: golden hour, blue hour, long exposure, double exposure.

## Lighting setups
- Rembrandt: classic portrait lighting with a triangle of light on the cheek.
- Soft diffused studio: crisp highlights and gentle shadows.
- Rim lighting or backlight: subject outlined with light from behind.
- Flat diffused light: overcast, even illumination, minimal shadows.
- Volumetric: visible light beams, fog, haze.

## Composition
- Rule of thirds, centred composition, symmetry.
- Wide shot, medium shot, close-up, macro.
- High angle, low angle, eye level, bird's-eye view.
- Tilt-shift for miniature effects.

## Text rendering
- Wrap desired text in double quotation marks inside the prompt: "Design a poster with
  the title \"BLUE NOTE SESSIONS\" in bold condensed sans-serif".
- Stick to readable fonts; highly stylised text works less well.
- Editing existing text: "Change 'old text' to 'new text'".
- Match text length where possible; big shifts in character count change layout.
- Be explicit about preserving font style when it matters. Some models can inpaint
  text and match the original font.

## Style transfer
- Name the exact style: "impressionist painting", "1960s pop art", "Sumi-e ink wash".
- Reference specific artists or movements for clearer guidance.
- If a label fails, describe the traits: "visible brushstrokes, thick paint texture,
  rich colour depth".
- State what stays the same, for example "keep the original composition".
- Example-based editing: give a before/after pair then a third image and the model
  infers the transformation. Some models also accept a style reference image.

## Character consistency
- Fix a verbatim reference description and paste it into every prompt.
- Say what changes (setting, activity, style) and what stays (face, expression, clothing).
- Use reference images where supported; some models take several at once.
- Break complex changes into steps: outfit first, then scene.
- For training data: generate many images of the character, pick the best, and reuse
  them as references or fine-tuning input.

## Multi-image and storyboards
- Ask for "a series", "a set", or a grid such as "2x2 storyboard grid".
- Describe each panel individually with consistent character descriptions.
- Repeat exact descriptions to hold style and character continuity.
- Some models support example-based editing across a batch: show one before/after pair,
  then apply the same transformation to the rest.

## Product and commercial work
- Materials precisely: "brushed steel", "matte aluminum", "kraft paper", "frosted glass".
- Lighting: "soft diffused studio lighting, crisp highlights and gentle shadows".
- For brand assets, look for native vector output when the deliverable is an icon.
- For layouts with copy, look for models with strong typography and composition.

## Fine-tuning and LoRAs
- Use the trigger words of the trained model in every prompt.
- Combine multiple LoRAs with scale parameters, typically 0.9 to 1.1.
- Generate synthetic training data, pick the best, retrain.
- A consistent-character workflow can generate training data from one reference image.

## Common pitfalls
1. Keyword-stuffed prompts: write a scene, not a tag list.
2. "Transform" for a small edit: it can swap the whole identity.
3. Not saying what to keep when editing.
4. Negative prompts on models not trained for them: they add noise. Check the docs.
5. Guidance scale too high: "burnt", over-contrast output. Use the model's range.
6. Expecting live knowledge: no model has internet access.
7. Short prompts for complex scenes: use the token budget.
8. Ignoring aspect ratio: most models are best near one megapixel; too large gives
   edge artifacts, too small gives harsh crops.
9. Wrong model for the task: switch models rather than fighting the prompt.
10. Not iterating: the best results come from small changes and repeats.
