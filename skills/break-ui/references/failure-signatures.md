# Failure signatures

The catalogue behind `break-ui`. Each row is something visible in the worst-case
render; the cause in the middle column is almost always the reason.

| What you see | Cause | Fix |
| --- | --- | --- |
| Avatar or icon squished into an oval or pill | Flex child shrinking | `flex-shrink: 0` on the avatar, icon and any fixed-size box |
| Text overflows instead of wrapping or truncating | Flex or grid child has `min-width: auto` | `min-width: 0` on the text column (`minmax(0, 1fr)` in grid) |
| Email or URL runs past the edge | No break opportunities in the string | `overflow-wrap: anywhere` on that element |
| Trailing action pushed off-screen or clipped | Middle content took all the space | `min-width: 0` on the middle, `flex-shrink: 0` on the action |
| Badge wraps onto two lines | Badge allowed to shrink | `white-space: nowrap; flex-shrink: 0`, and decide what yields |
| Avatar adrift beside a three-line name | `align-items: center` on rows of varying height | `align-items: flex-start` once text can wrap |
| Last row cut off at a hard edge mid-glyph | Fixed-height container with no affordance | Visible scrollbar or a fade mask; check `overflow` is intended |
| Long word breaks mid-word in a heading | `word-break: break-all` | `overflow-wrap: anywhere` breaks only when it has to |
| Wrong initials (J for Jo, or a replacement glyph for an emoji-first name) | Indexing code like `split(' ')[0][0]` | Grapheme clusters (`Intl.Segmenter`), first plus last word, fallback icon |
| Orphaned dash or empty line where the role was | Placeholder for a missing optional field | Omit the line, or reserve its height intentionally |
| "1 members", "0 member" | Hardcoded plural | `Intl.PluralRules`, or separate strings per count |
| Numbers jitter and columns misalign on update | Proportional figures | `font-variant-numeric: tabular-nums` |
| `1284`, `1,284.000000001`, `NaN`, `undefined` | Raw number rendered | `Intl.NumberFormat` with the user's locale; guard null |
| Long translated button label overflows | Fixed-width button | Width from content with `min-width`, never a fixed `width` |
| Diacritics or tall scripts clipped top or bottom | Tight `line-height` with `overflow: hidden` | Looser `line-height` or no clipping on text boxes |
| Broken-image icon in the avatar | No error fallback | Fall back to initials; `object-fit: cover` for any ratio |
| Truncated text with no way to read it | `text-overflow: ellipsis` and nothing else | A `title` or tooltip, and the full value in a detail view |
| Scrolling 1,000 rows stutters | Every row rendered | Virtualize or paginate, and say which |
| Raw `<b>`, `&amp;` or `**text**` rendered | Wrong escaping layer | Escape once, at render; never inject user data as HTML |

The cases that are not a single dataset need their own toggle positions or
fixtures: **empty** (zero items, the no-results state), **one** (a single item,
and every count at exactly 1), and **huge** (the realistic upper bound, 1,000+
rows if the list is unpaginated).
