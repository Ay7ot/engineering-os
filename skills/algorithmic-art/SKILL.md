---
name: algorithmic-art
description: Create generative art in code: write an algorithmic philosophy, then a self-contained p5.js sketch with seeded randomness and live parameters. Use when asked for generative or algorithmic art, a code-drawn composition or an interactive viewer. Not for static pieces (`canvas-design`).
metadata:
  audience: builder
  upstream: https://github.com/anthropics/skills/tree/main/skills/algorithmic-art
  license: Apache-2.0
---
# Algorithmic Art

Two steps: write the algorithmic philosophy (markdown), then express it as p5.js generative art (a self-contained HTML viewer plus the JS algorithm).

## When to use
- Algorithmic or generative art: seeded randomness, noise fields, particle systems, flow fields, L-systems.
- An interactive viewer where the viewer changes parameters and the canvas re-renders.
- Not for a fixed static composition (`canvas-design`) and not for UI motion (`animate`).

## Step 1: write the philosophy (markdown)
An algorithmic philosophy is a computational aesthetic movement expressed through code. Name the movement in 1 or 2 words ("Organic Turbulence", "Quantum Harmonics", "Emergent Stillness"), then write 4 to 6 paragraphs covering: computational processes and mathematical relationships; noise functions and randomness patterns; particle behaviours and field dynamics; temporal evolution and system states; parametric variation and emergent complexity.

Three worked examples:
- "Organic Turbulence": chaos constrained by natural law, order emerging from disorder. Flow fields driven by layered Perlin noise, thousands of particles following vector forces, trails accumulating into organic density maps.
- "Quantum Harmonics": discrete entities exhibiting wave-like interference. Particles initialised on a grid, each carrying a phase; nearby phases interfere, constructive ones create bright nodes, destructive ones create voids.
- "Recursive Whispers": self-similarity across scales. Branching structures subdividing recursively, L-systems that feel both mathematical and organic.

## Step 2: implement in p5.js
Seed everything from a single integer so the same seed always produces identical output:

```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

Expose parameters as one object, and wire each entry to a control in the viewer:

```javascript
let params = {
  seed: 12345,
  // quantities, scales, probabilities, ratios, angles, thresholds
};
```

Changing a parameter re-renders from scratch; never accumulate state across frames in a way that breaks reproducibility.

## Craft
- Balance: complexity without visual noise, order without rigidity.
- Colour harmony: a chosen palette, never random RGB values.
- Composition: keep a visual hierarchy even inside randomness.
- Reproducibility: the same seed and parameters produce identical output. This is the acceptance test.
- Keep the seed in any exported image filename or shareable URL so a result can be regenerated.

## Output
1. The philosophy as markdown.
2. One self-contained HTML artifact: canvas, controls and sketch inlined, no external build.
3. The algorithm as a JS file. Seeding details, a deterministic render loop and export notes are in references/p5-patterns.md.

## Checklist
- [ ] Movement named; philosophy is 4 to 6 paragraphs
- [ ] One integer seed drives `randomSeed` and `noiseSeed`
- [ ] Parameters object exposed with live controls
- [ ] Palette chosen deliberately, not random
- [ ] Same seed and parameters reproduce identical output
