# Video prompt technique

## The seven layers
1. Subject: who or what is in the scene.
2. Context: where the subject is (a city street, a forest, a spaceship corridor).
3. Action: what the subject does (walks, turns, picks up a phone, runs).
4. Style: the visual aesthetic (cinematic, stop-motion, documentary).
5. Camera: how it moves (dolly, tracking, static, handheld).
6. Composition: how the shot is framed (wide, close-up, over-the-shoulder).
7. Ambience: mood and lighting (warm tones, blue light, golden hour, overcast).

## Shot types
- Wide or establishing: the full scene and environment.
- Medium: the subject from roughly the waist up.
- Close-up: the frame filled with the face or a key object.
- Extreme close-up: an isolated detail (an eye, a hand on a handle, a drop of water).

## Camera motion
- Static or tripod: locked off.
- Pan: horizontal rotation. Tilt: vertical rotation.
- Dolly: the camera moves toward or away from the subject.
- Tracking: the camera moves alongside the subject.
- Crane: the camera rises or descends vertically.
- Handheld: shaky, documentary style.
- Drone or aerial: overhead or sweeping.
- Dolly zoom: background stretches while the subject stays locked.

## Camera position
- Eye level: neutral. Low angle or worm's eye: subjects feel powerful.
- High angle or bird's eye: subjects feel small or vulnerable.
- Over-the-shoulder, and POV or first-person.

## Lens and focus
- Shallow depth of field, deep focus, macro lens, wide-angle lens, tilt-shift.

## Escalation pattern for short clips
Wide, then medium, then close-up, then extreme close-up, mapped onto time:
- 0 to 3s: wide establishing shot of the location.
- 3 to 7s: medium shot, the subject enters or acts.
- 7 to 12s: close-up on the key moment.
- 12 to 15s: extreme close-up on a detail (a hand, an eye, a drop of rain).

## Time-coded multi-shot example

```text
[0-4s]: Wide establishing shot, static camera, misty bamboo forest at dawn
[4-9s]: Medium shot, slow push-in, the fighter steps forward
[9-15s]: Close-up, orbit shot, the fighter strikes, slow motion
```

Transition language: "hard cut to" (abrupt), "seamless morph into" (fluid), "whip pan
to" (fast, energetic), "snap cut to" (jarring, dramatic).

### Worked commercial

```text
(0-3s) Macro shot of a luxury perfume bottle among scattered pink peonies,
       shallow depth of field, petals floating in warm afternoon light,
       soft ambient music.
(3-7s) Camera glides closer, a feminine hand enters frame from the right,
       fingers gently touch the glass bottle, the sound of silk rustling.
(7-12s) Hard cut to slow-motion spray, golden mist diffuses through the air,
        particles catching rim light against a dark background,
        the hiss of the atomizer.
(12-15s) Seamless pull-out to hero frame, product centered, volumetric
         lighting, minimal cream background, elegant silence.
```

## Style anchors
- Style labels: claymation, Pixar animation style, anime, stop-motion, 8-bit retro,
  graphic novel, documentary footage, origami, LEGO, blueprint technical drawing.
- Quality anchors: "hyper-realistic, 8k", "cinematic".
- Film and genre: "Michael Mann cinematography" (neon, night, urban), "Wes Anderson"
  (symmetrical, pastel, quirky), "Roger Deakins lighting" (naturalistic, precise),
  "Blade Runner 2049 cinematography" (atmospheric, orange and teal), "National
  Geographic documentary" (nature, steady, observational).
- Grain and texture: "slightly grainy, film-like" or "VHS aesthetic" pushes away from
  the too-clean AI look.

## Character sheet
Fix the wording once and paste it into every prompt:

"John, a man in his 40s with short brown hair, wearing a blue jacket and glasses,
looking thoughtful"

Specify age, hair, skin, build, exact garments and colours, accessories, and
demeanour. Vary the action, location and camera, never the character description. A
clear reference photo is more reliable than text for holding facial features.

## Common pitfalls
1. Not describing audio: models then hallucinate inappropriate sound.
2. Too much dialogue for the clip length: unnaturally fast speech.
3. Too little dialogue: gibberish or awkward pauses fill the gap.
4. Not stating what to keep unchanged when using references or editing.
5. Expecting variety from identical prompts: change the prompt, not just the seed.
6. Not prompting camera motion: unintended static or erratic shots.
7. Subtitle contamination: use colons, "(no subtitles)", and repeat if needed.
8. Vague prompts for complex scenes: a 12 plus requirement prompt works if each is clear.
9. Ignoring resolution and aspect ratio: check what the model supports before choosing.
10. Expecting live knowledge: no model has internet access.
