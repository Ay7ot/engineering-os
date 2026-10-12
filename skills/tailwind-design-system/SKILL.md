---
name: tailwind-design-system
description: Build a scalable design system on Tailwind CSS v4: CSS-first @theme tokens, semantic colour and radius variables, dark mode, component variants with cva, and grid primitives. Use when creating a component library, design tokens or theming. Not for one-off page styling.
metadata:
  audience: builder, architect
  upstream: https://github.com/wshobson/agents/blob/main/plugins/frontend-mobile-development/skills/tailwind-design-system/SKILL.md
  license: MIT
---
# Tailwind Design System (v4)

Build a production design system with Tailwind CSS v4: CSS-first configuration,
design tokens, component variants, responsive patterns and accessible states.
This targets v4 (2024 and later); for v3 projects see the Tailwind upgrade guide.
If the project uses a registry of owned components instead of hand-built ones,
use `shadcn`.

## When to use
- Creating a component library or standardising UI patterns across a codebase.
- Implementing design tokens and theming with CSS-first configuration.
- Building responsive or accessible components with variants and states.
- Migrating a v3 project to v4.
- For marketing pages and one-off sections, use `frontend-design` or
  `design-taste-frontend` instead.

## v4 changes to know

| v3 pattern | v4 pattern |
| --- | --- |
| `tailwind.config.ts` | `@theme` in CSS |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| `darkMode: "class"` | `@custom-variant dark (&:where(.dark, .dark *))` |
| `theme.extend.colors` | `@theme { --color-*: value }` |
| `require("tailwindcss-animate")` | CSS `@keyframes` in `@theme` plus `@starting-style` for entry animations |

For v4, do not add the `tailwindcss` plugin to `postcss.config.js`; use
`@tailwindcss/postcss` or the Vite plugin.

## Token and component architecture
```
Brand tokens (abstract) -> semantic tokens (purpose) -> component tokens
Base styles -> variants -> sizes -> states -> overrides
```
A brand value such as `oklch(45% 0.2 260)` becomes `--color-primary`, which
becomes the `bg-primary` utility. Components address semantic tokens only.

## Theme skeleton

```css
@import "tailwindcss";

@theme {
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);
  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);
  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);
  --color-destructive: oklch(53% 0.22 27);
  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  --animate-fade-in: fade-in 0.2s ease-out;

  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }
}

@custom-variant dark (&:where(.dark, .dark *));

.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);
  --color-border: oklch(22% 0.02 264);
  --color-ring: oklch(83% 0.02 264);
}

@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground antialiased; }
}
```

The full token set (secondary, accent, card, ring-offset, animation variables and
dark overrides for every token) is in references/patterns.md. Keyframes declared
inside `@theme` are emitted only when referenced by an `--animate-*` variable, and
dark overrides change the same token names, never a parallel set of `-dark`
names.

## Rules
- Use semantic utilities (`bg-primary`, `text-muted-foreground`); never raw
  values such as `bg-blue-500` in components.
- Every component accepts `className` and merges it last through `cn()`, which
  combines `clsx` and `tailwind-merge`, so callers can override layout without
  fighting the base classes.
- Variants and sizes are data (`cva`), not branches in JSX. Add states
  (hover, focus-visible, disabled) to the base string once.
- Focus is visible on every interactive element, usually
  `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
  focus-visible:ring-offset-2`.
- Inputs with errors set `aria-invalid` and `aria-describedby` pointing at the
  message element, which carries `role="alert"`; error borders use the
  destructive token.
- Disabled controls use `disabled:pointer-events-none disabled:opacity-50`.
- Tailwind v4 setup targets React 19, where `ref` is a normal prop: no
  `forwardRef` wrapper.

Component code for variants, compound components, forms and grids:
references/patterns.md. Native animations, the dark-mode provider, custom
`@utility`, theme modifiers and the full v3 to v4 migration checklist:
references/advanced-patterns.md.

## Checklist
- [ ] `@import "tailwindcss"` and `@theme` used; no `tailwind.config.ts` tokens
- [ ] Semantic tokens defined per purpose, addressed by semantic utilities
- [ ] Dark mode defined as the same tokens under `.dark` or the dark variant
- [ ] Radius, spacing, colour and animation tokens declared in `@theme`
- [ ] Components built on `cva` variants and sizes, composed rather than forked
- [ ] `cn()` (clsx plus tailwind-merge) used so `className` merges last
- [ ] Focus rings visible; error and disabled states wired to ARIA attributes
- [ ] Contrast checked in both themes with `better-colors`
- [ ] Keyframes referenced by an `--animate-*` variable so they are emitted
