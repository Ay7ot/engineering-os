---
name: canvas-design
description: Create a static art piece as .png or .pdf by first writing a named visual philosophy, then expressing it on a canvas through form, space, colour and pattern. Use when asked for a poster, a print, a piece of art or another static design. Not for generative code art (`algorithmic-art`).
metadata:
  audience: builder
  upstream: https://github.com/anthropics/skills/tree/main/skills/canvas-design
  license: Apache-2.0
---
# Canvas Design

Two steps, in order: write the design philosophy, then express it on a canvas. Output only markdown, PDF and PNG files.

## When to use
- A poster, a print, a piece of art, or any other static design piece.
- Not for anything interactive or time-based: use `algorithmic-art` for code-drawn work and `animate` for motion.

## Step 1: write the philosophy (markdown)
Create a visual philosophy, not a layout or a template. It is interpreted through form and space, colour and material, images and shapes and patterns, with minimal text as a visual accent.

- Name the movement in 1 or 2 words: "Brutalist Joy", "Chromatic Silence", "Metabolist Dreams".
- Articulate it in 4 to 6 paragraphs, covering: space and form; colour and material; scale and rhythm; composition and balance; visual hierarchy.
- Avoid redundancy: mention each design aspect once.
- Emphasise craftsmanship repeatedly: the final work must read as though it took countless hours.
- Leave creative space: be specific about the aesthetic direction, concise enough to allow interpretive choices.

Three worked examples:
- "Concrete Poetry": communication through monumental form and bold geometry. Massive colour blocks, sculptural typography, Brutalist spatial divisions, Polish poster energy meets Le Corbusier.
- "Chromatic Language": colour as the primary information system. Geometric precision where colour zones create meaning, Josef Albers' interaction meets data visualization.
- "Analog Meditation": quiet contemplation through texture and breathing room. Paper grain, ink bleeds, vast negative space, Japanese photobook aesthetic.

## Step 2: express it on the canvas (pdf or png)
- Generally use repeating patterns and perfect shapes; treat the abstract philosophy as if it were a scientific bible.
- Add sparse, clinical typography and systematic reference markers.
- Anchor the piece with a short phrase or two, positioned subtly.
- Use a limited palette that feels intentional and cohesive, not a spectrum.
- Aim for museum or magazine quality, as if someone at the top of their field laboured over every detail.

For colour discipline and contrast, `better-colors`; for type scale and pairing, `better-typography`.

## Checklist
- [ ] Movement named in 1 or 2 words
- [ ] Philosophy is 4 to 6 paragraphs, no redundancy, craftsmanship stated
- [ ] Canvas uses repeating patterns or perfect shapes
- [ ] Sparse typography, reference markers, a short anchored phrase
- [ ] Limited cohesive palette
- [ ] Only markdown, PDF and PNG produced
