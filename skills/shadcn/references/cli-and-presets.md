# CLI, Presets and Project Setup

## Commands

```bash
# Inspect the project.
npx shadcn@latest info --json

# Create a project.
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite
npx shadcn@latest init --name my-app --preset base-nova --template next --monorepo

# Initialize an existing project.
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults          # template next, preset nova, base implied

# Apply a preset to an existing project.
npx shadcn@latest apply a2r6bw
npx shadcn@latest apply a2r6bw --only theme
npx shadcn@latest apply a2r6bw --only theme,font

# Inspect preset codes and project preset state.
npx shadcn@latest preset decode a2r6bw
npx shadcn@latest preset url a2r6bw
npx shadcn@latest preset open a2r6bw
npx shadcn@latest preset resolve            # add --json for structured values

# Add components.
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
npx shadcn@latest add owner/repo/item
npx shadcn@latest add --all

# Preview changes before adding or updating.
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
npx shadcn@latest add @acme/form --view button.tsx

# Search registries.
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search owner/repo -q "login"
npx shadcn@latest search @shadcn -q "menu" -t ui
npx shadcn@latest search                    # all configured registries

# Docs and examples, then fetch the returned URLs.
npx shadcn@latest docs button dialog select

# Inspect registry items that are not installed yet.
npx shadcn@latest view @shadcn/button
```

Named presets: `nova`, `vega`, `maia`, `lyra`, `mira`, `luma`. Templates:
`next`, `vite`, `start`, `react-router`, `astro` (all support `--monorepo`) and
`laravel` (not supported for monorepo). Preset codes are version-prefixed base62
strings such as `a2r6bw` or `b0`, produced by the preset builder at
https://ui.shadcn.com.

Never decode a preset code or build a preset URL by hand: use `preset decode`,
`preset url`, `preset open`, and `preset resolve` for project-aware detection.
Apply codes with `apply` in an existing project, or `init --preset` when
initializing.

## Switching presets
Ask the user which of the four behaviours they want before running anything:
overwrite, partial, merge or skip.

- Inspect current state with `npx shadcn@latest preset resolve` (`--json` for
  structured values); inspect the incoming preset with `preset decode <code>`.
- Overwrite: `npx shadcn@latest apply <code>`. This overwrites detected
  components, fonts and CSS variables.
- Partial: `npx shadcn@latest apply <code> --only theme,font`. Supported values
  are `theme` and `font`; `icon` is intentionally not supported because icon
  changes may need a full component reinstall and transforms.
- Merge: `npx shadcn@latest init --preset <code> --force --no-reinstall`, then
  `npx shadcn@latest info` to list installed components, then smart-merge each
  one individually with `--dry-run` and `--diff`.
- Skip: `npx shadcn@latest init --preset <code> --force --no-reinstall`. This
  updates config and CSS and leaves components alone.

Preset commands run inside the user's project directory. `apply` needs an
existing project with a `components.json`. The CLI preserves the current `base`
(radix or base) automatically, and codes do not encode the base; if you must use
a scratch directory, pass `--base <current-base>` explicitly.

## Updating components while keeping local changes
1. `npx shadcn@latest add <component> --dry-run` lists every affected file.
2. `npx shadcn@latest add <component> --diff <file>` shows upstream against
   local, per file.
3. Decide per file: no local changes means it is safe to overwrite; local
   changes mean reading the file, analysing the diff, and applying the upstream
   update while preserving local modifications.
4. If the user says "just update everything", confirm first, then `--overwrite`.

## Registry and import hygiene
The CLI rewrites imports for its own UI files, but third-party registry
components may keep default paths. After adding anything from a community
registry (`@bundui`, `@magicui`, `owner/repo`), read `npx shadcn@latest info`
for the real `ui` alias and rewrite hardcoded imports such as
`@/components/ui/...` to match. Then check for missing sub-components, missing
imports, wrong composition and rule violations, and swap icon imports to the
project's `iconLibrary`.
