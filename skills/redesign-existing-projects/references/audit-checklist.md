# Redesign Audit Checklist

Check each item against the real code and rendered page, then record what you
find before changing anything.

## Typography
- Browser default fonts or Inter everywhere: replace with a font that has
  character (Geist, Outfit, Cabinet Grotesk, Satoshi), or pair a serif heading
  with a sans body for editorial work.
- Headlines lack presence: increase display size, tighten tracking, reduce
  line-height.
- Body text too wide: cap paragraphs near 65 characters and raise line-height.
- Only weights 400 and 700 present: add 500 and 600 for subtler hierarchy.
- Numbers in a proportional font: enable `font-variant-numeric: tabular-nums`
  or use a monospace face for data-heavy UI.
- Missing tracking adjustments: negative for large headings, positive for small
  caps and labels.
- All-caps subheaders everywhere: try sentence case, small caps or lowercase
  italics.
- Orphaned words on the last line: fix with `text-wrap: balance` or
  `text-wrap: pretty`.

## Colour and surfaces
- Pure `#000000` background: use off-black, charcoal or a tinted dark
  (`#0a0a0a`, `#121212`).
- Oversaturated accents: keep saturation under 80% so accents blend with the
  neutrals.
- More than one accent colour: keep one and remove the rest.
- Warm and cool greys mixed: pick one grey family and tint consistently.
- Purple or blue "AI gradient" aesthetic: replace with neutral bases and one
  considered accent.
- Generic `box-shadow`: tint the shadow to the background hue instead of pure
  black at low opacity.
- Flat design with zero texture: add subtle noise, grain or a micro-pattern.
- Perfectly even gradients: break the uniformity with radial, mesh or noise
  overlays rather than a 45-degree linear fade.
- Inconsistent lighting: audit every shadow so they imply one light source.
- A random dark section in a light page: either commit to dark or stay in one
  background tone; a slightly darker shade of the same palette is allowed.
- Empty flat sections: add background imagery, texture or an ambient gradient.

## Layout
- Everything centered and symmetrical: break it with offset margins, mixed
  aspect ratios or left-aligned headers.
- Three equal card columns as the feature row: replace with a 2-column zigzag,
  asymmetric grid, horizontal scroll or masonry.
- `height: 100vh` for full-screen sections: use `min-height: 100dvh`.
- Complex flexbox percentage math: replace with CSS Grid.
- No max-width container: add one near 1200 to 1440px with auto margins.
- Equal card heights forced by flexbox: allow variable heights or masonry.
- One uniform border-radius everywhere: tighter inside, softer on containers.
- No overlap or depth: use negative margins to layer elements.
- Symmetrical vertical padding: adjust optically; the bottom often needs more.
- Dashboard always has a left sidebar: consider top navigation, a command menu
  or a collapsible panel.
- Missing whitespace: double the spacing on marketing surfaces.
- Card CTAs at random heights: pin buttons to the bottom of each card.
- Pricing or comparison lists starting at different Y positions: align the list
  start with consistent spacing or fixed-height title and price blocks.
- Misaligned shared elements between side-by-side cards: align titles, prices
  and buttons across items.
- Mathematically centered but optically off: nudge icons, play buttons and text
  in buttons by 1 or 2px.

## Interactivity and states
- No hover states on buttons: add a background shift, slight scale or translate.
- No pressed feedback: add `scale(0.98)` or `translateY(1px)`.
- Zero-duration transitions: add 200 to 300ms transitions.
- Missing focus ring: add a visible one for keyboard users. This is required.
- No loading states: replace circular spinners with skeletons that match the
  layout shape.
- No empty state: compose a "getting started" view instead of a blank panel.
- No error state: add clear inline errors; never `window.alert()`.
- Dead links: link somewhere real or disable them visually.
- No current-page indication in navigation: style the active link.
- Scroll jumping on anchors: add `scroll-behavior: smooth`.
- Animations on `top`, `left`, `width` or `height`: switch to `transform` and
  `opacity`.

## Content
- Generic names (John Doe, Jane Smith): use diverse, realistic names.
- Fake round numbers (`99.99%`, `$100.00`): use organic data such as `47.2%`,
  `$99.00`, `+1 (312) 847-1928`.
- Placeholder companies (Acme, Nexus, SmartFlow): invent believable,
  contextual brands.
- Copy cliches: elevate, seamless, unleash, next-gen, game-changer, delve,
  tapestry, "in the world of".
- Exclamation marks in success messages: remove them.
- "Oops!" error messages: be direct ("Connection failed. Please try again.").
- Passive voice: use active voice ("We couldn't save your changes").
- Identical blog dates: spread them out.
- The same avatar for several people: use unique assets per person.
- Lorem ipsum: write real draft copy.
- Title Case on every header: use sentence case.

## Component patterns
- Generic card look (border plus shadow plus white): use border, background or
  spacing alone; cards only where elevation carries hierarchy.
- Always one filled and one ghost button: add text links or tertiary styles.
- Pill "New" and "Beta" badges: try square badges, flags or plain labels.
- Accordion FAQ: consider a side-by-side list, searchable help or inline
  progressive disclosure.
- 3-card testimonial carousel with dots: try a masonry wall, embedded posts or
  one rotating quote.
- Three-tower pricing table: highlight the recommended tier with colour and
  emphasis, not only extra height.
- Modals for everything: use inline editing, slide-over panels or expandable
  sections for simple actions.
- Avatar circles only: try squircles or rounded squares.
- Sun and moon theme toggle: consider a dropdown, system preference or a
  setting.
- Four-column footer link farm: reduce to main paths plus legally required
  links.

## Iconography
- Lucide or Feather everywhere: swap to Phosphor, Heroicons or a custom set.
- Cliché metaphors (rocketship for launch, shield for security): use less
  obvious icons such as bolt, fingerprint, spark, vault.
- Mixed stroke widths: standardise to one weight.
- Missing favicon: add a branded one.
- Stock "diverse team" photos: use real team photos, candids or one consistent
  illustration style.

## Code quality
- Div soup: use `nav`, `main`, `article`, `aside`, `section`.
- Inline styles mixed with classes: keep styling in the project's system.
- Hardcoded pixel widths: use `%`, `rem`, `em` or `max-width`.
- Missing alt text: describe meaningful images; never `alt=""` or `alt="image"`
  on content images.
- Arbitrary z-index such as `9999`: define a z-index scale in the theme.
- Commented-out dead code: remove it before shipping.
- Import hallucinations: check every import exists in the dependency manifest.
- Missing meta tags: add `title`, `description`, `og:image` and social tags.

## Omissions that generated designs forget
- No legal links: add privacy policy and terms of service in the footer.
- No back navigation: every page needs a way back.
- No branded 404 page.
- No form validation: add client-side checks for email, required fields and
  formats.
- No "skip to content" link: add a hidden skip-link for keyboard users.
- No cookie consent: add a compliant banner where the jurisdiction requires it.
