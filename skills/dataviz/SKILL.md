---
name: dataviz
description: Guidance for presenting numbers visually so they are honest, easy to read and accessible on light and dark themes, whatever the charting library. Use when building a chart, stat tile, metrics page or dashboard, or picking colours for data.
metadata:
  audience: builder, architect
---
# Data Visualization

## When to use
- Building any chart, graph, sparkline, KPI/stat tile or dashboard.
- Choosing colours for data series.
- Reviewing a dashboard that is hard to read.

## Pick the form from the question
| Question | Form |
|---|---|
| How does a value change over time? | Line (area only if the total matters) |
| How do categories compare? | Horizontal bar, sorted |
| What is the part of a whole? | Stacked bar; pie only for 2 or 3 parts |
| How are values distributed? | Histogram or box plot |
| Do two measures relate? | Scatter |
| What is the single number right now? | Stat tile with comparison (vs last period, vs target) |

If a table answers the question better, use a table.

## Colour
- Define colours once as tokens (CSS variables or a theme object), never inline
  per chart. Every chart uses the same series order and colours.
- Categorical: a small fixed palette (up to about 6). More categories means
  group the tail into "Other".
- Sequential (low to high): one hue, varying lightness. Diverging (below/above a
  midpoint): two hues around a neutral middle.
- Status colours (good/warning/bad) are reserved for status, not for series.
- Check contrast against both light and dark backgrounds, and do not rely on
  colour alone: add labels, markers or patterns so colour-blind users can read
  it.
- White-label or themed products: chart colours come from the theme tokens, so
  a brand swap does not break contrast. Test with at least two brand colours.

## Marks, axes, text
- Bars start at zero. Lines may not, but say so on the axis.
- Label directly where possible instead of a legend. Remove gridlines that do
  not help reading values.
- Units and time ranges always visible. Numbers formatted for humans (1.2k,
  12%), with exact values on hover or in a table.
- Titles state the takeaway or the question, not just the metric name.

## Interaction and states
- Tooltips show the exact value, unit and date.
- Every chart has loading, empty ("no data for this range") and error states.
- Keyboard and screen reader: chart has a text alternative (summary or table).

## Dashboards
- Most important number top left; group by question, not by data source.
- One time-range control for the whole view.
- Same metric, same colour and name everywhere.

## Checklist
- [ ] Form chosen from the question (or a table)
- [ ] Colours from shared tokens; palette type matches the data
- [ ] Readable in light and dark; not colour-only
- [ ] Zero baseline for bars; units and ranges visible
- [ ] Loading, empty and error states; text alternative
