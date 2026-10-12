---
name: ppt-visual
description: Design slide layouts and visuals for a deck: layout pattern, hierarchy, colour, type and per-slide specs. Use when building or redesigning presentation slides, fixing a text-heavy deck, or specifying a slide layout.
metadata:
  audience: lead, builder
  upstream: https://github.com/claude-office-skills/skills
  license: MIT
---
# Slide Visual Design

## When to use
- Building a new deck and choosing a layout per slide.
- Redesigning a deck that is a wall of bullets.
- Writing a design spec someone else will implement in the deck tool.

This is layout and visual craft for slides. Chart choice and data accuracy are `dataviz`; the words on a slide are `copywriting`.

## Procedure
1. Gather: the slide content, the presentation purpose, the audience, the room (projector, screen share, print) and any existing brand styles.
2. Pick one design direction for the whole deck: minimalist, corporate, creative, data-focused or storytelling.
3. Give each slide one idea, then one layout pattern from references/layout-patterns.md: title, big statement, three columns, image plus text, data highlight, timeline, comparison, process flow, quote plus image.
4. Size the content to the layout, not the layout to the content. Move overflow to the next slide or an appendix.
5. Write the per-slide spec below and hand it to whoever builds the deck.

## Layout rules
- One idea per slide. Two messages means two slides.
- Hierarchy top to bottom: title, key point, supporting detail, source or footer. One element must clearly win.
- Align to a grid and keep consistent margins; content should not touch the edges.
- Place key elements near a third intersection rather than dead centre when the layout allows.
- Contrast carries emphasis: large vs small, dark vs light, colour vs neutral, image vs text.
- Cap body copy at roughly 6 lines or 6 bullets. If it does not fit, cut it.
- Kill bullet lists where a visual makes the same point.

## Visual elements
- Icons: one consistent set and stroke weight throughout.
- Images: full-bleed or a clean half-split; one strong image beats a collage.
- Shapes: for purpose, not decoration; the same shape means the same thing across the deck.
- Charts: label directly, one number per slide where possible; see `dataviz`.

## Colour and type
- Define four tokens and reuse them: background, primary text, accent, highlight.
- Keep text on background above WCAG AA contrast: 4.5:1 for body, 3:1 for large text and graphics.
- Pair at most two families: one for headings, one for body. Fix a size for title, subtitle, body and caption.
- Test on the real projector or screen; colours shift in a dim room.

## Per-slide spec
State, per slide:
- Slide type and layout pattern.
- Exact text per element, with font, size, weight and colour.
- Visual elements (icons, images, shapes, charts) with position.
- Colour tokens used and the type scale.
- Animation, only where it supports the story.

A wireframe sketch plus the spec is usually enough. Wireframes, example specs, colour schemes and font pairings: references/layout-patterns.md and references/design-specs.md.

## Common mistakes
- Bullet dumps copied straight from a document.
- Five fonts and six colours across eight slides.
- Every slide filled to the edges, with no breathing room.
- Decorative animation that delays the point.

## Checklist
- [ ] One message per slide
- [ ] Layout pattern chosen and reused consistently
- [ ] Title, key point, detail and source hierarchy is obvious
- [ ] Body copy within the line and bullet cap
- [ ] Colour tokens and type scale defined; contrast checked
- [ ] One icon set and one image style throughout
- [ ] Deck tested on the target screen
