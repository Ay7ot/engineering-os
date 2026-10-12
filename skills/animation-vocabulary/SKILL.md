---
name: animation-vocabulary
description: Reverse-lookup glossary that turns a vague description of a web effect into its exact term (the bouncy popover that grows from its trigger is Pop in; the iOS overscroll feel is Rubber-banding). Use when asked what a motion effect is called, or when describing one without knowing its name.
metadata:
  audience: lead, planner, builder
  upstream: https://github.com/emilkowalski/skills/tree/main/skills/animation-vocabulary
  license: MIT
---
# Animation Vocabulary

Turn a vague description of a motion or effect into the precise term, so the user
knows what to ask for.

## When to use
- The user asks "what is it called when ...", or describes something they saw or
  felt ("springy", "slides off", "draws itself in").
- The user wants the right word to prompt an agent or a designer with.

Not for designing or building motion (`animate`), reviewing it
(`review-animations`), or auditing it (`improve-animations`).

## Method
1. **Match intent, not keywords.** Users describe what they see or feel, not
   the technical name. Map the sensation to a term in
   `references/glossary.md`.
2. **Quote the glossary verbatim.** Its descriptions are authoritative; do not
   paraphrase.
3. **Disambiguate close terms** so the user can pick: Clip-path versus Mask,
   Pop in versus Bounce, Shared element transition versus Layout animation.
4. **When nothing matches exactly,** name the closest term and say plainly it is
   an approximation, or describe the effect in glossary vocabulary ("a stagger
   of scale-in entrances").
5. **Stay within the glossary.** If a term genuinely is not there, say so rather
   than inventing one; you may still explain using these words.
6. **Keep it tight.** A naming question wants a name, not an essay. Lead with the
   term; expand only if asked.

## Output format
```
**Stagger** - Animate several items one after another with a small delay between each, creating a cascade.
```
If several terms fit, list the best match first, then one or two alternates with
a one-line note on how they differ.

## Examples
- "A popover that grows out of the button you clicked instead of from its middle"
  is **Origin-aware animation**.
- "One image turns into another image" is **Morph**. Alternates: **Crossfade** if
  they simply fade over each other in the same spot, **Shared element transition**
  if an element travels and transforms from one position into another.
- "The iOS scroll that resists and snaps back when you pull too far" is
  **Rubber-banding**.
- "It bounces into place when it opens" is **Pop in** rather than **Spring**
  (physics-driven) or **Bounce** (a spring that overshoots).

## Glossary index
`references/glossary.md` holds the full glossary under these headings: entrances
and exits; sequencing and timing; movement and transforms; transitions between
states; scroll; feedback and interaction; easing; spring animations; looping and
ambient motion; polish and effects; performance; principles to know. Load it
whenever a description needs matching; it mirrors the upstream project's
vocabulary page, so keep the two in sync when either changes.

## Checklist
- [ ] The matched term is given first, quoted verbatim from the glossary
- [ ] Close alternates listed with a one-line difference
- [ ] An approximation is stated plainly when nothing matches exactly
- [ ] No term invented outside the glossary
- [ ] The answer leads with the name
