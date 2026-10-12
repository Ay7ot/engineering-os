# Advanced v4 Patterns

## Native CSS entry animations

`@starting-style` supplies the from-state for an element that is appearing, so a
dialog or popover can run a CSS-only entry animation without a mount class.

```css
@theme {
  --animate-dialog-in: dialog-in 0.2s ease-out;
  --animate-dialog-out: dialog-out 0.15s ease-in;

  @keyframes dialog-in {
    from { opacity: 0; transform: scale(0.96); }
    to { opacity: 1; transform: scale(1); }
  }

  @keyframes dialog-out {
    from { opacity: 1; transform: scale(1); }
    to { opacity: 0; transform: scale(0.96); }
  }
}

dialog {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s, transform 0.2s, overlay 0.2s allow-discrete,
    display 0.2s allow-discrete;
}
dialog:not([open]) {
  opacity: 0;
  transform: scale(0.96);
}
@starting-style {
  dialog[open] {
    opacity: 0;
    transform: scale(0.96);
  }
}
```

Two details that are easy to miss: transitioning `display` and `overlay` needs
`allow-discrete`, and exit animations need the element to stay rendered until the
transition finishes.

## Dark mode provider

One strategy per project: the `dark:` variant with Tailwind utilities, or CSS
variables under `[data-theme="dark"]` or `.dark` for component libraries.

```tsx
// components/theme-provider.tsx
"use client";
import { createContext, useContext, useEffect, useState } from "react";

type Theme = "light" | "dark" | "system";
const ThemeContext = createContext<{ theme: Theme; setTheme: (t: Theme) => void }>({
  theme: "system",
  setTheme: () => {},
});

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>("system");

  useEffect(() => {
    const stored = localStorage.getItem("theme") as Theme | null;
    if (stored) setTheme(stored);
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const isDark = theme === "dark" || (theme === "system" && systemDark);
    root.classList.toggle("dark", isDark);
    localStorage.setItem("theme", theme);
    document.querySelector('meta[name="theme-color"]')
      ?.setAttribute("content", isDark ? "#0a0a0a" : "#ffffff");
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

Set the theme once at the layout or page root; sections never override it. A
theme toggle reads `useTheme()`, cycles light, dark and system, and labels the
button for screen readers.

## Custom utilities and theme modifiers

```css
/* Reusable decorative and text utilities. */
@utility hairline {
  border-block-end: 1px solid var(--color-border);
}

@utility text-gradient {
  background-clip: text;
  color: transparent;
  background-image: linear-gradient(to bottom, var(--color-foreground), var(--color-muted-foreground));
}
```

- `@theme inline` inlines a reference to another CSS variable, which is what
  component libraries need when they define `--radius` and Tailwind maps it.
- `@theme static` (or `@import "tailwindcss" theme(static)`) always emits the
  variables, even when no utility references them, so they are available to
  JavaScript and to `var()` in component libraries.
- Namespace overrides clear a default scale:
  `@theme { --color-*: initial; }` then declare only the project's colours.
- Semi-transparent variants can be generated with `color-mix()` rather than
  listing every alpha step.
- Container queries use `--container-*` tokens plus `@container` variants, which
  is the right tool for component-level adaptation; prefer it to viewport
  breakpoints when only the component needs to change.

## v3 to v4 migration checklist
1. Replace `@tailwind base/components/utilities` with `@import "tailwindcss"`.
2. Move `theme.extend` values into `@theme` variables in CSS; delete the
   JavaScript config once empty.
3. Rename colour values into the `--color-*` namespace and convert hex to OKLCH
   (see `better-colors`).
4. Replace `darkMode: "class"` with
   `@custom-variant dark (&:where(.dark, .dark *))`.
5. Replace animation plugins with `--animate-*` variables plus `@keyframes`
   inside `@theme`.
6. Swap `@tailwindcss/postcss` or the Vite plugin in for the `tailwindcss`
   PostCSS plugin.
7. Update border and ring defaults, since v4 changed the default border colour to
   `currentColor`; set it explicitly in the base layer.
8. Convert `shadow-sm` and `rounded-sm` sizes to the renamed v4 utilities where
   the design depended on the old values.
9. Remove `forwardRef` wrappers where React 19 makes `ref` a normal prop.
10. Re-check both themes and every focus state after the move.

## Do and do not
- Do keep all tokens in `@theme`, keyed by purpose, and address them through
  semantic utilities.
- Do declare dark values as the same token names under the dark selector.
- Do give every component a `className` escape hatch merged through `cn()`.
- Do declare small-size fallbacks inside the responsive variants.
- Do not put raw colour, radius or spacing values in components.
- Do not keep two sources of truth (a CSS `@theme` block plus a JavaScript
  config) for the same token.
- Do not use `transition: all`; name the properties (see `better-ui`).
- Do not add `will-change` broadly; it is a targeted fix for observed stutter.
- Do not ship a component without hover, focus-visible, disabled and error
  states where those states exist.
