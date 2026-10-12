# Anti-Slop Checklist

Banned patterns and the final pre-flight matrix for landing pages, portfolios
and marketing sites. These came out of real production tests of generated
pages. Treat them as hard bans unless the brief explicitly asks for one.

## Hero and top of page
- No version labels in the hero (`V0.6`, `BETA`, `EARLY ACCESS`) unless the
  brief is a launch or preview.
- No "Brand . No. 01"-style sub-eyebrows.
- Hero headline max 2 lines at desktop; subtext max 20 words and max 4 lines;
  CTAs visible without scrolling.
- Hero font scale is planned with the asset: `text-4xl md:text-5xl lg:text-6xl`
  normally, `text-6xl md:text-7xl` only for a 3 to 5 word headline. A 4-line
  headline is a font-size error, not a copy-length error.
- Hero top padding max `pt-24`. More means the hero floats halfway down the
  viewport.
- Max 4 text elements in the hero: eyebrow or brand strip (zero or one),
  headline, subtext, CTAs (one primary, at most one secondary). No tagline below
  the CTAs, no trust micro-strip, no pricing teaser, no feature bullets.
- The "Used by" logo wall sits directly under the hero, never inside it, is
  logos only with no category labels, and uses real SVG logos (Simple Icons,
  devicon) or a generated monogram, not plain text wordmarks.
- No pills, tags or credit captions overlaid on images.
- No decoration text strip at the hero bottom (`BRAND. MOTION. SPATIAL.`).
- No scroll cues (`Scroll`, `Scroll to explore`, mouse-wheel icons).

## Navigation and page structure
- Navigation renders on one line at desktop; if items do not fit at 1024px,
  condense labels or move to a hamburger.
- Navigation height max 80px, default 64 to 72px.
- No locale, city, time or weather strips unless the brief is genuinely
  place-focused or globally distributed.
- No version footers (`v1.4.2`, `Build 0048`, `last sync 4s ago`) on marketing
  pages.
- Footer link farms with four columns get simplified to main paths plus legally
  required links.

## Sections and grids
- Maximum 1 eyebrow per 3 sections; the hero counts as one. Count instances of
  `uppercase tracking` micro-labels across components: more than
  `ceil(sectionCount / 3)` fails.
- No split header (big headline left, small explainer paragraph right). Stack
  them vertically, headline above body.
- No section-numbering eyebrows (`00 / INDEX`, `001 . Capabilities`,
  `06 . how it works`) and no `01 / 4` pagination on tiles.
- One layout family per section, used at most once per page; 8 sections need at
  least 4 different families.
- Max 2 consecutive image-plus-text zigzag sections. The third fails.
- No 3-column equal feature cards. Use a 2-column zigzag, asymmetric grid,
  scroll-pinned or horizontal-scroll alternative.
- Bento grids have exactly as many cells as there are items, no empty cell in
  the middle or at the end, and at least 2 or 3 cells carry real visual
  variation (image, brand gradient, pattern, tint) rather than white-on-white
  text cards.
- Long lists over 5 items use a component, not a default list: grouped columns,
  card grid, tabs, scroll-snap pills, carousel or marquee.
- No `border-t` plus `border-b` on every row of a long list or spec table. Pick
  one and use it sparsely, or use the alternative components above.
- No scoring or progress bars with filled background tracks as comparison
  visuals on a marketing page.
- No floating top-right sub-text with no alignment to the section.
- No crosshair or hairline grid lines drawn as decoration.
- Mobile collapse is declared per section, not assumed.

## Motion
- Max one horizontal marquee per page.
- Every animation answers "what does this communicate?" with hierarchy,
  storytelling, feedback or a state change. "It looked cool" is not an answer.
- If motion is claimed above intensity 4, the page actually animates.
- Reduced motion collapses loops, parallax, scroll hijack and magnetic physics
  to static.

## Colour, matter and shape
- No pure `#000000` or `#ffffff`; use off-black and off-white.
- No neon or outer glows by default; no oversaturated accents; no gradient text
  on large headers.
- No custom mouse cursors.
- Cards only where elevation communicates hierarchy; otherwise group with
  space, `divide-y` or a border.
- Shadows are tinted to the background hue, never pure black on a light page.
- One radius system for the page (all sharp, all soft, or all pill), or a
  documented per-role rule that is followed everywhere.
- Attention: card plus ghost button as the only pairing, pill "New" and "Beta"
  badges, accordion FAQ, 3-card testimonial carousel with dots, sun/moon theme
  toggle, avatar circles only, modals for everything. Vary these.

## Content and data
- No `John Doe`, `Acme Corp`, `Lorem Ipsum`, or invented startup names like
  `Nexus` or `SmartFlow`. Use realistic, locale-appropriate, contextual names.
- No fake-perfect numbers (`99.99%`, `50%`, `1234567`). Use organic data
  (`47.2%`, `+1 (312) 847-1928`) or label the value as mock.
- No filler verbs: elevate, seamless, unleash, next-gen, revolutionize,
  game-changer, delve, tapestry.
- No "Quietly in use at", "From the field", "Currently on the bench",
  "Loose plates" style labels; use plain functional labels or none.
- No micro-meta-sentences under eyebrows. Eyebrow, headline and body are enough.
- No generic step labels (`Stage 1`, `Step 2`, `Phase 03`); use the verb-noun
  ("Install", "Configure", "Ship").
- No section numbering, mock-humble asides, or "we respect the X"-style copy.
- Quotes: max 3 lines of body, attribution with name plus role, real
  typographic quotes, no em dash in the attribution.
- One copy register per page. Re-read every visible string (headline, label,
  caption, alt text, error, footer) and rewrite anything grammatically broken,
  with unclear referents, or that sounds like generated wordplay.

## Code and assets
- Icons come from one allowed library (Phosphor, HugeIcons, Radix, Tabler);
  Lucide only on request; one stroke width across the surface; no hand-rolled
  SVG icon paths.
- No div-based fake product UI in the hero or anywhere else.
- Dependencies are verified in the dependency manifest before import; no
  hallucinated imports.
- Semantic HTML (`nav`, `main`, `article`, `aside`, `section`), meaningful alt
  text, a documented z-index scale, real meta tags, and no dead `#` links.

## Pre-flight matrix
Run every line. One honest miss means the page is not done.

- [ ] Design read declared in one line
- [ ] Dial values explicit and reasoned from the brief
- [ ] Design system chosen, or the aesthetic labeled honestly
- [ ] Redesign mode detected and audited where applicable
- [ ] Zero em dashes anywhere visible
- [ ] One theme, one accent, one radius system, one copy register
- [ ] CTA and form contrast checked against WCAG AA
- [ ] No CTA label wraps at desktop; no duplicate CTA intent
- [ ] Serif (if any) justified and not the previous project's serif
- [ ] Premium-consumer palette is not the beige plus brass family
- [ ] Italic descender clearance checked
- [ ] Hero fits the viewport; padding and stack discipline respected
- [ ] Eyebrow count within `ceil(sectionCount / 3)`
- [ ] No split header, no 3 zigzag sections in a row, no repeated layout family
- [ ] Logo wall is logos only, under the hero, with real SVG marks
- [ ] Bento has rhythm and an exact cell count with real visual variation
- [ ] Long lists use the right component
- [ ] Real images used; no fake screenshots; no decorative hand-rolled SVG
- [ ] No pills over images, no photo-credit decoration, no version footer
- [ ] No micro-meta sentences, no decoration strip, no floating corner text
- [ ] No locale strip, no scroll cue, no decorative status dots
- [ ] No hairline on every row of a long list
- [ ] Content density sane; no unlabeled fake-precise numbers
- [ ] Motion motivated, claimed motion shown, one marquee, reduced motion honored
- [ ] Scroll work uses `useScroll`, ScrollTrigger, IntersectionObserver or CSS
      scroll-driven animations, never a scroll event listener
- [ ] Dark mode tokens defined and both modes tested
- [ ] Mobile collapse explicit; `min-h-[100dvh]`, never `h-screen`
- [ ] Empty, loading and error states provided
- [ ] Core Web Vitals plausible: LCP under 2.5s, INP under 200ms, CLS under 0.1
- [ ] One design system in the project
