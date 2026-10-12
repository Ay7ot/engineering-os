---
name: shadcn
description: Work with shadcn/ui projects and registries: read project context, fetch component docs, add or update components safely, compose them correctly and keep styling semantic. Use when a project has components.json or the task mentions shadcn, presets or registry items.
metadata:
  audience: builder
  upstream: https://github.com/shadcn/ui/tree/main/skills/shadcn
  license: MIT
---
# shadcn/ui

shadcn is a framework for building UI, components and design systems: components
are added to the project as source code by a CLI. Run every command through the
project's package runner (`npx shadcn@latest`, `pnpm dlx shadcn@latest` or
`bunx --bun shadcn@latest`) chosen from `packageManager`; examples use `npx`.

## When to use
- The project has a `components.json`, or the task mentions shadcn, a component
  registry, presets or a preset code.
- Adding, updating, fixing, debugging or composing shadcn components.
- Initializing a project from a preset.
- For hand-built Tailwind tokens and variants with no registry, use
  `tailwind-design-system` instead.

## Start with project context
Run `npx shadcn@latest info --json` and read these fields before advising:
`aliases` (the real import prefix, never hardcode one), `isRSC` (when true,
anything using `useState`, `useEffect`, event handlers or browser APIs needs
`"use client"`), `tailwindVersion` (v4 uses `@theme inline`, v3 uses
`tailwind.config.js`), `tailwindCssFile` (the only global CSS file to edit),
`base` (`radix` or `base`, which changes triggers from `asChild` to `render`),
`iconLibrary` (`lucide` means `lucide-react`, `tabler` means
`@tabler/icons-react`; never assume), and `resolvedPaths`, `framework`,
`packageManager`, `style` and `preset` for destinations, routing, install
command, visual treatment and resolved preset values.

## Principles
1. Use existing components first: search the registries with
   `npx shadcn@latest search` before writing custom UI.
2. Compose, do not reinvent: a settings page is Tabs plus Card plus form
   controls; a dashboard is Sidebar plus Card plus Chart plus Table.
3. Use built-in variants (`variant="outline"`, `size="sm"`) before custom styles.
4. Use semantic colours (`bg-primary`, `text-muted-foreground`), never raw values
   such as `bg-blue-500`.

## Always-enforced rules
- Styling: `className` is for layout, never to override component colours or
  typography. No `space-x-*` or `space-y-*`; use flex with `gap-*`. Use `size-*`
  when width and height are equal, and `truncate` rather than the three longhand
  utilities. No manual `dark:` colour overrides. Use `cn()` for conditional
  classes. No manual `z-index` on overlay components.
- Forms: use `FieldGroup` plus `Field`, never a `div` with `space-y-*`. Inside
  `InputGroup` use `InputGroupInput` or `InputGroupTextarea` with
  `InputGroupAddon` for buttons. Option sets of 2 to 7 choices use
  `ToggleGroup`; group related checkboxes or radios with `FieldSet` and
  `FieldLegend`. Validation is `data-invalid` on the field plus `aria-invalid`
  on the control; disabled is `data-disabled` plus `disabled`.
- Composition: items always live inside their group (`SelectItem` in
  `SelectGroup`, `CommandItem` in `CommandGroup`). Dialog, Sheet and Drawer
  always need a Title, with `className="sr-only"` when hidden. Use the full Card
  composition. Button has no `isPending`; compose `Spinner` plus `data-icon`
  plus `disabled`. `TabsTrigger` goes inside `TabsList`. `Avatar` always needs
  `AvatarFallback`.
- Prefer components over custom markup: `Alert` for callouts, `Empty` for empty
  states, `toast()` from `sonner`, `Separator` instead of `<hr>`, `Skeleton` for
  loading, `Badge` instead of a styled span.
- Icons: inside `Button` pass `data-icon="inline-start"` or `"inline-end"` and
  add no sizing classes. Pass icon components as objects (`icon={CheckIcon}`),
  never string lookups.

Incorrect and correct pairs for every rule, plus the component selection table:
references/rules.md.

## Workflow
1. Refresh context with `npx shadcn@latest info` if the injected context is
   stale.
2. Check installed components before `add`: read the `components` list or list
   the `resolvedPaths.ui` directory. Do not import what has not been added or
   re-add what exists.
3. Find what you need with `npx shadcn@latest search`, filtered with `-q` and
   `-t`.
4. Run `npx shadcn@latest docs <component>` and `webfetch` the returned URLs
   before creating, fixing, debugging or using a component.
5. Install or update with `npx shadcn@latest add`; preview with `--dry-run`,
   `--diff` and `--view` first.
6. After adding from any registry, read the added files: missing sub-components,
   missing imports, wrong composition, hardcoded import paths that do not match
   the project aliases, and icons that do not match `iconLibrary` all need
   fixing before moving on.
7. Do not guess a registry. If the request names none, ask which one to use.
8. To update a component while keeping local changes, use `--dry-run` and
   `--diff` per file and merge by hand; never run `--overwrite` without explicit
   approval, and never fetch raw files from GitHub by hand.

Presets, project creation, flags and the full command reference:
references/cli-and-presets.md.

## Checklist
- [ ] Project context read; aliases, base, icon library and Tailwind version used
- [ ] Existing components checked before adding anything
- [ ] Docs and examples fetched with the CLI and `webfetch` before writing code
- [ ] Added files read and repaired (sub-components, imports, icons, aliases)
- [ ] Registry named explicitly, or the user asked which one to use
- [ ] Semantic colours and variants used; no raw colour values
- [ ] Full composition used (groups, Card parts, overlay titles, Avatar fallback)
- [ ] Form fields use `FieldGroup` and `Field`, with `data-invalid` and
      `aria-invalid` on errors
- [ ] `"use client"` present where the project is RSC and behavior requires it
- [ ] Updates used `--dry-run` and `--diff`; `--overwrite` only with approval
