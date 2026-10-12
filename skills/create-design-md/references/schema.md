# DESIGN.md Schema Notes

## Frontmatter shape
- `version`: `alpha` in current documents.
- `name`: required, one product or coherent site.
- `description`: one line.
- Optional groups: `colors`, `typography`, `rounded`, `spacing`, `components`.
  Add a group only when a governing source defines that named system.
- Token references inside the document use `{path.to.token}`.

## Shape rules (hard gate, not style)
- A token group is a mapping whose children are schema fields. Never emit a
  scalar typography entry (`sans: Geist`), an arbitrary nested source object
  (`font-family: { mono: ... }`), or rounded keys copied from CSS variable names
  (`radius-sm`, `radius-md`).
- Use mappings, never sequences, for token groups.
- `colors`: a flat mapping of valid token names to values.
- `typography`: a mapping of named scales; each scale is a mapping using only
  `fontFamily`, `fontSize`, `lineHeight`, `fontWeight` and `letterSpacing`.
- `rounded` and `spacing`: flat mappings of valid token names to values.
- `components`: may reference canonical token paths but may not introduce a
  second token schema.
- Every emitted name matches `^[a-zA-Z0-9][a-zA-Z0-9-]*$`. Reject and rewrite a
  key that would fail.
- If normalisation would require inventing a token name, field, scale or semantic
  relationship, omit the candidate.

Good and bad shapes:

```yaml
typography:
  sans:
    fontFamily: Geist
  display:
    fontFamily: Geist
    fontSize: 64px
    lineHeight: 64px
    fontWeight: 510
  mono:
    fontFamily: Geist Mono

# wrong, scalar scale
typography:
  mono: Geist Mono

# wrong, source nesting or invented radius steps
font-family:
  mono: Geist Mono
rounded:
  radius-sm: 0.625rem
```

When a source exposes only `--radius`, write `rounded.base: 0.625rem`. Preserve
semantic token names rather than source object nesting, and resolve framework
utilities through the active theme or configuration before writing values.

## URL mode specifics
- Role-based names are reconstructed; schema field names are not. Reconstructed
  role names may vary, but never emit URL-specific aliases such as `family`,
  `size`, `weight`, `mobile-display` or nested `sans` and `mono` values inside a
  typography scale.
- Colour roles are flattened into valid token names: `background-primary`,
  `foreground-secondary`, `border-muted`, never `background.primary`.
- Use `css-tailwind` as the compatibility export target unless the user
  specifies another.
- Do not create aliases such as `primary`, `elevated` or `display` merely to
  organise observations.
- A component section needs the same interaction or surface treatment to recur
  across at least two sampled pages and to change a concrete implementation
  choice.
- Normalise the frontmatter before writing Markdown: collect evidence, choose the
  export target, map into the schema, reject invalid shapes, then write. Never
  draft prose first and retrofit the YAML.

## Evidence ledger and promotion
Keep a private ledger per sampled page and viewport with: page, viewport, element
role, computed property and value, and the matching loaded declaration or custom
property when available. Inspect the public stylesheets the page loads, including
custom properties and media-query rules. A stylesheet value is usable only when it
is connected to a rendered element or recurs across the sampled pages.

Promote a URL value when the rendered computed value and a loaded declaration or
custom property agree, or when the same computed value recurs for the same role
across the required samples. Otherwise omit it. Do not invent semantic aliases
from a raw value, and resolve framework utilities through the active theme or
configuration before writing exact values.

## Theme modes
Run `npx @google/design.md spec` to check what the installed specification
supports. With `themes` and `default-theme` support, use the theme-aware token
syntax. Without it, put the default value under each canonical semantic token and
record alternate values in a `## Themes` table. Do not create parallel `-light`
and `-dark` names, do not discard alternate-theme values, and do not pretend the
fallback table makes the frontmatter theme-aware.

## Export expectations
| Target | Use | Names must produce |
| --- | --- | --- |
| `css-tailwind` | Tailwind v4 | `--color-*`, `--font-*`, `--text-*`, `--radius-*`, `--spacing-*` |
| `json-tailwind` | Tailwind v3 | the same token families in the config shape |
| `dtcg` | anything else | Design Tokens Community Group format |

Typography entries are named scales: `fontFamily`, `fontSize` and `lineHeight`
live inside each scale, never under arbitrary source nesting such as
`font-family`.
