---
name: prompt-videos
description: Write prompts for AI video generation models, covering scene description, camera and lens language, audio and dialogue, time-coded multi-shot structure and reference inputs. Use when prompting a video model or building a video generation feature. Not for image prompts (`prompt-images`).
metadata:
  audience: builder, architect
  upstream: https://github.com/replicate/skills/tree/main/skills/prompt-videos
  license: Apache-2.0
---
# Prompting Video Models

Transferable techniques for video generation, distilled from model provider write-ups. A good video prompt is a scene description, not a caption: write what happens, where, and how it looks.

## When to use
- Writing a prompt for a video generation model, or building video generation into a feature.
- Directing camera motion, dialogue, sound or a multi-shot sequence.
- For picture and still generation use `prompt-images`; for video rendered from HTML or React, use `hyperframes`.

## Pick the model from the API, not from memory
The landscape changes weekly. Query the provider API or model catalogue for current options, read each model's schema (resolutions, clip length, whether it accepts images, audio or multi-shot prompts) before running anything, and compare candidates. Do not assume a model exists, or is best, from memory.

## Layer every prompt
Layer seven elements into every prompt: subject, context, action, style, camera,
composition, and ambience (mood and lighting). Concrete examples of each are in
references/video-technique.md.

Overdescribe. "A man on the phone" becomes "a desperate man in a weathered green trench coat picks up a rotary phone mounted on gritty brick, bathed in the eerie glow of a green neon sign." Every concrete detail leaves the model less room to improvise badly. Name subjects directly ("the woman in the red jacket"), never by pronoun.

## Camera and cinematography
- Shot types: wide or establishing, medium (waist up), close-up, extreme close-up.
- Camera motion: static, pan, tilt, dolly, tracking, crane, handheld, drone or aerial, dolly zoom.
- Camera position: eye level, low angle (powerful), high angle (vulnerable), over-the-shoulder, POV.
- Lens and focus: shallow depth of field, deep focus, macro, wide-angle, tilt-shift.

A natural escalation for an 8 to 15 second clip is wide, then medium, then close-up, then extreme close-up. Concrete time blocks, audio layers, transitions and style language are in references/video-technique.md.

## Multi-shot and time codes
Some models generate several shots in one clip (up to about 15 seconds). Write the
timestamps into the prompt:

```text
[0-4s]: Wide establishing shot, static camera, misty bamboo forest at dawn.
[4-9s]: Medium shot, slow push-in, the fighter steps forward.
[9-15s]: Close-up, orbit shot, the fighter strikes, slow motion.
```

State transitions explicitly ("hard cut to", "seamless morph into", "whip pan to",
"snap cut to"), or the model improvises.

## Audio and dialogue
Prompt all four layers: dialogue, ambient sound, sound effects and music. Skipping
ambient audio makes models hallucinate it, a common failure being a live studio
audience. Prevent baked-in subtitles with a colon for dialogue ("She says: Hello
there"), an explicit "(no subtitles)" and, if it persists, a repeat. Spell names
phonetically when pronunciation fails, and tie lines to distinctive visuals so the
model does not mix up speakers. Match dialogue length to the clip: 8 seconds holds
roughly 2 to 3 short sentences.

## Reference inputs
Many models accept images, clips or audio alongside the text prompt, which shifts the
work from prompting to directing:
- Image to video: the image is the first frame; describe the change, not the static
  scene, and carry style through.
- First and last frame: the model fills the transition, good for morphs and
  before/after states.
- Subject references: hold a character, product or object consistent across clips,
  often addressed with bracket tags such as `[Image1]`.
- Audio driven: lip sync and beat-matched cuts; transcribe the audio too and match
  the video duration to it.

## Style and consistency
Name the style explicitly ("claymation", "Pixar animation style", "anime", "stop-motion",
"8-bit retro", "blueprint technical drawing"): the label changes how characters move,
not only how the frame looks. Use film and genre references for mood, and quality anchors
such as "hyper-realistic, cinematic" for fidelity. For precise style, generate a starting
image first and pass it in. Hold a character consistent with a verbatim character sheet
repeated in every prompt, and vary only action, location and camera.

## Watch out
The frequent failures are undescribed audio (models hallucinate sound), dialogue that
does not fit the clip length, omitting what must stay unchanged, no camera direction,
and subtitle contamination. The full list of ten is in references/video-technique.md.

## Checklist
- [ ] Model chosen from the live API and schema, not from memory
- [ ] All seven layers present, overdescribed, subjects named
- [ ] Camera motion and framing directed explicitly
- [ ] Audio layers prompted; dialogue length matched to clip length
- [ ] Transitions stated for multi-shot prompts
- [ ] Reference inputs and style anchors chosen deliberately
