---
name: better-colors
description: OKLCH colour practice for web projects: convert hex, rgb and hsl to oklch, generate palettes, measure contrast, handle gamut limits and theme semantic tokens. Use when creating a colour system, converting colours, checking contrast, or fixing dark mode. Not for typography or layout.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/jakubkrehel/skills/tree/main/skills/better-colors
  license: MIT
---
# OKLCH Colours

OKLCH is a perceptually uniform colour space where lightness, chroma and hue are
useful design controls. Use it when the project already uses OKLCH, when creating
a new colour system, or when the user asks for conversion or palette work.
Otherwise preserve the project's established tokens and notation: a consistent
hex or RGB token system beats introducing a second colour representation for one
fix. To explore interactively, visit https://oklch.fyi.

## When to use
- Creating a colour system, palette or theme tokens.
- Converting hex, rgb or hsl values, or authoring new values in OKLCH.
- Checking or reporting contrast, or fixing dark mode.
- Reviewing frontend code for colour misuse.

Related: `better-typography` owns text rendering and sizing,
`better-accessibility` owns the contrast requirement the colour must satisfy,
and `dataviz` owns colour choices for series in charts.

## Why a perceptual space
- Equal `L` steps read as equal brightness: `oklch(0.5 ...)` is visually mid,
  whereas hsl `lightness: 50%` varies wildly by hue.
- Hue is stable across lightness; an hsl blue drifts toward purple as it
  lightens.
- Chroma is an absolute measure of colourfulness, independent of lightness,
  unlike hsl saturation.
- The gamut is finite: not every OKLCH value maps to a displayable sRGB colour,
  so high-chroma values at some hues clip and need a gamut check.

## Write and format values consistently

```
oklch(L C H)
oklch(L C H / alpha)
```

- `L`: 0 to 1, `0` is black and `1` is white, perceptually uniform.
- `C`: 0 to roughly 0.4. `0` is grey; the maximum depends on `L` and `H`.
- `H`: 0 to 360 degrees.
- `alpha`: 0 to 1, optional, slash syntax.

Use three decimal places for `L` and `C` and up to three for `H`. Drop trailing
zeros and write `-0` as `0`. Examples: `oklch(0.637 0.237 25.331)` and
`oklch(0.8 0.05 200 / 0.5)`. OKLCH is Baseline 2023; when support requirements
are unusually broad, check the target project's browser matrix rather than
assuming a coverage percentage.

## Measure contrast, gamut and palette behaviour

| Rule | Value |
| --- | --- |
| Light/dark boundary | `L` above 0.73 is a light background, so use dark text; below it light text still scores higher |
| Lightness gap, light background | foreground `L` below 0.35 when background `L` is above 0.9 |
| Lightness gap, dark background | foreground `L` above 0.9 when background `L` is below 0.25 |
| Hue drift threshold | more than 10 degrees spread across palette steps is visible drift |
| APCA body text | absolute `Lc` 75 minimum, 90 preferred |
| APCA non-body text | absolute `Lc` 60 minimum |
| WCAG 2 normal text | 4.5:1 (AA), 7:1 (AAA) |
| Contrast fix, only when asked | adjust `L` first, preserve `C` and `H`, then remeasure the rendered pair |

## Rules
- Respect the existing system. Do not convert notation merely because this skill
  was loaded; reuse or add the correct role token in the project's own format
  unless the task includes a colour-system migration.
- One colour, one meaning. If a hue already means one thing, a second use needs a
  neutral or a new token, never a borrowed value.
- Use the same chroma percentage (of each hue's maximum) for consistent
  vividness, not the same absolute `C` across hues.
- Clamp high chroma to the maximum for its `L` and `H` in sRGB; add a
  `@media (color-gamut: p3)` fallback when emitting P3 colours.
- Fill only the single primary action with colour; secondary controls stay
  neutral, and only one coloured control background should appear in a view.
- Build dark mode from the light palette as a starting point, then tune chroma
  and lightness, and recheck every foreground and background pair.
- In Tailwind v4, convert hex values inside `@theme` to OKLCH, and use slash
  alpha syntax rather than comma syntax.

## Common mistakes

| Issue | Fix |
| --- | --- |
| Raw colour bypasses the semantic token system | Reuse or add the correct role token in the project's notation |
| An isolated OKLCH value in a hex or RGB codebase | Preserve the established notation unless migrating the colour system |
| hsl palette ramp with hue drift | Rebuild with constant OKLCH hue |
| Failing contrast | Report the pair, its measured `Lc` and the threshold it misses; change colours only when asked, then adjust `L` and keep `C` and `H` |
| High chroma without a gamut check | Clamp to the maximum chroma for that `L` and `H` in sRGB |
| Same absolute `C` across hues | Same `C` percentage of each hue's maximum |
| P3 colour with no sRGB fallback | Add the `color-gamut: p3` pattern |
| Dark mode made by reversing the light palette | Tune chroma and lightness, then recheck every pair |
| Hex left inside Tailwind v4 `@theme` | Convert to OKLCH |
| Same hue used for two meanings | One colour, one meaning; give the second use a neutral |
| A separator token used as text colour | Add a token for the missing role; never borrow by value |
| Several coloured control backgrounds in one view | Fill only the primary action |
| Palette verified in light mode only | Recheck every pair in both appearances |

## Review output
For a standalone colour review, present findings in one table with Severity,
Location, Before, After and Why columns; never separate Before and After lines.
HIGH makes content unreadable or assigns a misleading semantic colour, MEDIUM
creates a visible theme, gamut or consistency failure, LOW is isolated polish.
Cite `path/to/file:line`, include the measured contrast or gamut evidence, and
consolidate a systemic issue into one row listing every location. Then list the
checks run (contrast, gamut, both appearances) and give a verdict: Block with any
HIGH left, Needs changes for MEDIUM or LOW only, Approve when nothing actionable
remains. If another review skill is orchestrating, hand it the evidence and let
its format win.

## Checklist
- [ ] The project's existing tokens and notation preserved, or a migration agreed
- [ ] Values written as `oklch(L C H)` with the documented precision
- [ ] Contrast measured for every foreground and background pair, both modes
- [ ] Gamut checked; P3 colours have an sRGB fallback
- [ ] Chroma expressed as a percentage of each hue's maximum
- [ ] One colour, one meaning; primary action is the only filled control
- [ ] Findings reported as a table with measured evidence and a verdict
