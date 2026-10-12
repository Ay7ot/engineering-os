# p5 patterns

## Seeded randomness
The Art Blocks pattern: one integer seed feeds both generators, so every draw is a
pure function of the parameters.

```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

## Parameter structure
Keep every knob in one object so the viewer can iterate over it and build controls
automatically, and so a run can be serialised into a URL or a filename.

```javascript
let params = {
  seed: 12345,
  count: 2000,
  scale: 0.004,
  speed: 0.6,
  palette: 0,
};
```

## Deterministic render
Draw the whole frame from seed and parameters rather than from accumulated motion.
If the piece evolves over time, drive it from a frame counter, not from wall-clock
time, so frame N is always identical for a given seed.

```javascript
function draw() {
  let t = frameCount / 60;
  // derive everything from params and t
}
```

## Export
Name exports with the seed and parameters so any image can be regenerated, for
example `art-<seed>-<palette>.png`. On export, resize the canvas, save the image
with `saveCanvas`, then restore the on-screen size.

## Reproducibility check
Run the sketch twice with the same parameters and compare the output; they must be
identical. If they are not, a value is coming from `Date`, `frameCount` reset, or a
non-seeded random source.
