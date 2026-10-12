---
name: d3-visualization
description: Build custom data visualizations in D3, with scales, data joins, transitions, tooltips and responsive SVG. Use when implementing a bespoke chart, dashboard, map or network diagram in code rather than a ready-made chart component. Chart type and colour decisions belong to `dataviz`.
metadata:
  audience: builder, architect
  upstream: https://github.com/slb2248/ai-ux-skills/tree/main/skills/d3-visualization
  license: MIT
---
# D3 Visualization

Implementation guidance for bespoke charts, dashboards and maps in D3. Which chart to draw, and which colours to use, is `dataviz`; this file is how to build it once chosen.

## When to use
- A custom chart, dashboard, geographic map, network diagram or infographic in code.
- The chart type is settled and you need scales, joins, transitions, tooltips and responsiveness.
- Not for chart-type or palette decisions (`dataviz`) and not for interface layout around the chart (`better-layout`).

## Data first
- Inspect the real shape of the data (keys, types, nulls, ranges) before writing markup, and pick the chart from the question the data answers.
- Position encodes values most accurately, then length, then angle, then area, then colour. Use position or length for the value being read and reserve colour for categories.
- Data updates must transition, not jump. Plan for the enter, update and exit cases from the start.

## The D3 pattern
- One SVG with a `viewBox` so it scales with its container; size the plot area with margins, not the SVG itself.
- Scales map data to pixels: `scaleLinear` for continuous, `scaleBand` for categories, `scaleTime` for dates. Build each axis from its scale, never by hand.
- Bind data with a join: `selectAll(...).data(...).join(...)`. The join handles enter, update and exit so repeated renders stay safe.
- Transitions: `.transition().duration(400)` for the initial draw and for value changes. Keep them 300 to 500 ms; never animate on every resize tick.
- Tooltips: on pointer enter show the exact value and unit, prefer a positioned HTML element over an SVG `title`, and make the same detail reachable by keyboard.
- Responsive: on resize recompute width from the container, update the scale ranges and the elements, and reduce tick counts at narrow widths.

## Design and accessibility
- Colour: accessible categorical palettes (for example ColorBrewer), 5 to 7 categories at most, sequential for continuous values. Never rely on colour alone; add labels or markers.
- Type: labels 12 to 14 px, titles 16 to 18 px, tabular figures for numbers, contrast at least 4.5:1.
- Remove chart junk, keep scales and axes consistent, label axes and points, and state the takeaway in the title.
- Provide a text alternative: a summary sentence or the underlying table, so the chart is usable without seeing it.
- Touch targets at least 44 px.

## Checklist
- [ ] Chart type chosen from the question, not by preference
- [ ] Scales and axes built from the data; join handles enter, update and exit
- [ ] `viewBox` set plus a resize handler; ticks adapt
- [ ] Tooltip shows exact value and unit; keyboard reachable
- [ ] Palette of 5 to 7 accessible colours; contrast at least 4.5:1
- [ ] Text alternative provided; transitions 300 to 500 ms
