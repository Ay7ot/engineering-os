---
name: create-design-md
description: Create or update a DESIGN.md that records a product's design language: gather evidence from the repo or a live URL, map it to the schema, then lint and export it. Use when asked to document a design system or give coding agents persistent UI context.
metadata:
  audience: architect, builder
  upstream: https://github.com/ibelick/ui-skills/tree/main/skills/create-design-md
  license: MIT
---
# Create DESIGN.md

Write one `DESIGN.md` for one product or coherent website, recording the design
language that governs it, not every value that happens to exist.

## When to use
- Asked to document an interface's design language, or reconstruct its visual
  system from a repository or a public site.
- Asked to extract design tokens and guidance from current evidence, so coding
  agents have persistent UI context.
- To build tokens rather than document them, use `tailwind-design-system` or
  `better-colors` instead.

## Boundaries
- Modify only `DESIGN.md`: no product source, dependencies, configuration or
  generated files, and no exported files.
- Use the schema in references/schema.md, never a competing one.
- Do not copy every discovered token or component into the document.
- Do not convert repetition, local styling or visual preference into intent.

## Choose the mode
Repository mode (preferred) applies when a local product repository exists: write
`DESIGN.md` at the root of the selected product, or ask which product when
ownership is ambiguous. Repository evidence establishes normative values, token
names, ownership and documented rationale.

URL mode applies when the user supplies a public URL without source: write a
labelled reconstructed draft in the workspace. It needs rendered browser access:
the DOM, computed styles and publicly loaded stylesheets at desktop and mobile
widths, sampling up to three same-origin pages that represent distinct templates.
Screenshots support interpretation but cannot establish exact values. URL evidence
establishes observable patterns and computed values only, never internal token
names, ownership or canon. Without rendered inspection, ask for screenshots or
source files; never build the document from copy, metadata or HTML structure
alone. Repository mode wins whenever source exists.

## Evidence pipeline
Both modes produce the same record and output:

```
role -> value -> source -> scope -> recurrence -> confidence
```

Collect evidence, record source, scope and recurrence per candidate, normalise
into the schema, omit anything uncertain, local without a contract or not
implementation relevant, validate the frontmatter shape and export compatibility,
then write Markdown. The document stays private until validation passes: never
return, display or summarise a draft earlier. On an invalid shape or a missing
export category, rewrite the frontmatter and rerun; if the category cannot be
repaired, remove it and report it as omitted.

## Trace the evidence
Repository mode inspects in order: existing `DESIGN.md` and explicit guidance;
tokens, themes, variables and global styles; shared primitives and variants;
representative routes and rendered consumers; surface-local implementations. A
source participates only when the product imports, references, inherits or renders
it; exclude proposals, migrations, examples, generated output, legacy
implementations and similarly named packages.

URL mode samples colours and surface roles, typography roles, spacing and layout,
borders, radii and elevation, navigation, buttons, inputs, cards and repeated
structures, at desktop and mobile. Prefer computed values and loaded declarations
over visual estimation. Every URL claim needs all three proofs: observable on the
rendered page, measured or recurring across the required samples, and changing a
concrete implementation choice. If one is missing, omit the claim. Ledger fields
and promotion rules: references/schema.md.

## Decide what belongs
- Write YAML only from named shared tokens and roles in governing sources, never
  from utility classes, repeated literals or component values.
- Token groups are mappings, never sequences:
  `typography.mono.fontFamily: Geist Mono`, not `typography.mono: Geist Mono`.
- Normalise one group-level token such as `--radius` to `base`; never derive
  `sm`, `md`, `lg` or `xl` from utilities. Resolve framework utilities through
  the active theme first.
- Identify the export target before writing: `css-tailwind` for Tailwind v4,
  `json-tailwind` for v3, `dtcg` otherwise; names must be valid for it.
- Check `npx @google/design.md spec` before encoding theme modes, and never
  create parallel `-light` and `-dark` token names.
- A repository-mode prose rule needs explicit guidance, a named token or variant,
  or a shared owner used by at least two audited surfaces. A URL-mode rule must
  be directly observable, and a site-wide rule must recur across at least two
  sampled templates. URL colours stay flat (`background-primary`) and match
  `^[a-zA-Z0-9][a-zA-Z0-9-]*$`.

## Write the document

```yaml
---
version: alpha
name: <string>
description: <string>
---
```

Only `name` is required. Add `colors`, `typography`, `rounded`, `spacing` or
`components` only when a governing source already defines that named system, and
reference tokens as `{path.to.token}`.

Then `## Overview` states the product's purpose and evidenced design direction
only, not a summary of pages or tokens. Add only supported sections, in this
order: Colors, Themes, Typography, Layout, Elevation & Depth, Shapes, Components,
Do's and Don'ts. Do not add a section because the format has one, reorder or
duplicate, and include a Don't only when a governing source states an explicit
prohibition. Exact values live in the frontmatter, except alternate-theme values
in the fallback table; rationale lives in Markdown. Preserve accepted decisions
from an existing `DESIGN.md` unless the user or current evidence replaces them,
and keep citations, audit notes, rejected candidates, conflicts and open
questions out of the document.

Before saving, delete any token not named by a governing source, any page-local
behaviour presented as product-wide, any pattern conflicting with explicit
guidance, any prohibition not explicitly stated, any exact value outside the
frontmatter or fallback table, any component configuration or methodology in
Markdown, and any sentence that does not change the document. Finish with a no-op
pass against vague advice. When implementation conflicts with explicit guidance,
document the guidance and report the conflict outside `DESIGN.md`.

## Validate, then report

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format <format> DESIGN.md
```

Every populated category the target supports must appear in the export; an empty
or missing one is a schema failure even on a successful exit. For
`css-tailwind`, expect `colors` to `--color-*`,
`typography.<name>.fontFamily` to `--font-*`, `typography.<name>.fontSize` to
`--text-*`, `rounded` to `--radius-*` and `spacing` to `--spacing-*`. If
`typography` is populated but the export has neither `--font-*` nor `--text-*`,
rewrite before reporting, and report an exporter limitation rather than dropping
supported information. When updating, keep the original and run
`npx @google/design.md diff <previous-file> DESIGN.md`, restoring any removed
accepted decision current evidence does not replace.

Report the mode and audited product or URL, the created or updated file, the
governing sources used, conflicts or unsupported areas omitted, and the final
lint and export results; label URL-mode output as a reconstructed draft.

## Checklist
- [ ] Mode chosen (repository preferred) and boundaries respected
- [ ] Evidence traced in order; non-participating sources excluded
- [ ] URL claims carry observation, basis and consequence, or were omitted
- [ ] Only named shared tokens written; mappings, never sequences
- [ ] Export target identified and token names valid for it
- [ ] Theme modes encoded per the installed specification, or parked in the table
- [ ] Sections limited to the supported order; Overview states purpose only
- [ ] No invented personality, citations, audit notes or open questions
- [ ] Lint passes; every populated category appears in the export
- [ ] Report lists mode, sources, omissions and results
