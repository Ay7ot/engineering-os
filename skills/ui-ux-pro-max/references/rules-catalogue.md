# Rules catalogue by priority

Every rule with its threshold. Apply top down.

## 1. Accessibility (critical)

- `color-contrast`: at least 4.5:1 for normal text, 3:1 for large text
  (18 px, or 14 px bold).
- `focus-states`: a visible focus ring on every interactive element.
- `alt-text`: descriptive alt text for every meaningful image.
- `aria-labels`: an `aria-label` on icon-only buttons.
- `keyboard-nav`: tab order matches visual order.
- `form-labels`: a `label` with a `for` attribute, not a placeholder alone.

## 2. Touch and interaction (critical)

- `touch-target-size`: minimum 44 by 44 px.
- `hover-vs-tap`: use click or tap for primary interactions, not hover.
- `loading-buttons`: disable the button while the async action runs.
- `error-feedback`: the error message sits next to the problem.
- `cursor-pointer`: clickable elements show the pointer cursor.

## 3. Performance (high)

- `image-optimization`: modern format, `srcset`, lazy loading.
- `reduced-motion`: honour `prefers-reduced-motion`.
- `content-jumping`: reserve space for async content to avoid layout shift.

## 4. Layout and responsive (high)

- `viewport-meta`: `width=device-width, initial-scale=1`.
- `readable-font-size`: at least 16 px body text on mobile.
- `horizontal-scroll`: content never exceeds the viewport width.
- `z-index-management`: a named scale (10, 20, 30, 50), never 9999.

## 5. Typography and colour (medium)

- `line-height`: 1.5 to 1.75 for body text.
- `line-length`: 65 to 75 characters per line.
- `font-pairing`: pair on a contrast axis, or use one family in several weights.

## 6. Animation (medium)

- `duration-timing`: 150 to 300 ms for micro-interactions.
- `transform-performance`: animate transform and opacity, not width or height.
- `loading-states`: skeleton screens or spinners for waits.

## 7. Style selection (medium)

- `style-match`: the style matches the product type.
- `consistency`: one style across all pages.
- `no-emoji-icons`: SVG icons from a single set, never emoji.

## 8. Charts and data (low)

- `chart-type`: the chart type matches the data shape.
- `color-guidance`: accessible series colours that survive colour blindness.
- `data-table`: a table alternative for screen readers.

## Style families the catalogue covers

The catalogue ships more than 50 styles, 97 palettes and 57 font pairings,
grouped for search. When picking a style, match it to product type (SaaS,
e-commerce, portfolio, dashboard), industry (healthcare, fintech, gaming) and
the brief's keywords, then check the anti-pattern list the search returns
alongside it.

Common style families to search by keyword: minimal, editorial, brutalist,
glass, claymorphism, neumorphism, retro, terminal, luxury, playful, corporate,
data-dense dashboard.

## Anti-patterns that recur

- Emoji standing in for an icon set.
- Hover effects that move the layout.
- Dark mode shipped with invisible borders or unreadable glass panels.
- A palette generated from a category reflex (fintech equals navy) rather than
  the brief.
- Charts with colour-only series encoding.
