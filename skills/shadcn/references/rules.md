# Enforced Rules, With Pairs

Each rule below is always enforced. The pairs show the common incorrect code and
the correct replacement. For edge cases, read the component docs the CLI returns
from `npx shadcn@latest docs <component>`.

## Styling and Tailwind
`className` is for layout, not for overriding component colours or typography.

```tsx
<Button className="px-6" />                          // correct: layout only
<Button className="bg-blue-500 text-white font-bold" />  // wrong: component styling
```

Spacing uses flex and `gap-*`; `space-x-*` and `space-y-*` are not used.

```tsx
<div className="flex flex-col gap-4">   // correct
<div className="space-y-4">             // wrong
```

Equal dimensions use `size-*`, and truncation uses the shorthand.

```tsx
<Avatar className="size-10" />          // correct
<Avatar className="w-10 h-10" />        // wrong
<p className="truncate" />              // correct
<p className="overflow-hidden text-ellipsis whitespace-nowrap" />  // wrong
```

Use semantic tokens instead of manual dark-mode overrides.

```tsx
<div className="bg-background text-muted-foreground" />  // correct
<div className="bg-white text-gray-600 dark:bg-gray-900 dark:text-gray-300" />  // wrong
```

Conditional classes go through `cn()`, not template literal ternaries, and
overlay components handle their own stacking, so do not set `z-index` on Dialog,
Sheet, Popover and their peers.

## Forms and inputs
Form layout is `FieldGroup` plus `Field`. A `div` with `space-y-*` or a grid gap
is not a form layout.

```tsx
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
    <FieldDescription>We only use this for receipts.</FieldDescription>
  </Field>
</FieldGroup>
```

Buttons inside inputs use `InputGroup` with `InputGroupAddon`; text inputs inside
an `InputGroup` must be `InputGroupInput` or `InputGroupTextarea`, never the raw
components.

```tsx
<InputGroup>
  <InputGroupInput placeholder="Search" />
  <InputGroupAddon><SearchIcon /></InputGroupAddon>
</InputGroup>
```

Option sets of 2 to 7 choices use `ToggleGroup` with `ToggleGroupItem`; do not
loop `Button` with manual active state. Related checkboxes or radios are grouped
with `FieldSet` plus `FieldLegend`, not a `div` with a heading.

Validation state is expressed with data attributes and ARIA:

```tsx
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Enter a valid email address.</FieldDescription>
</Field>
```

`data-invalid` goes on `Field`, `aria-invalid` on the control; `data-disabled`
goes on `Field` with `disabled` on the control.

## Composition
Items always sit inside their group: `SelectItem` in `SelectGroup`,
`DropdownMenuItem` in `DropdownMenuGroup`, `CommandItem` in `CommandGroup`.
Custom triggers use `asChild` with the radix base and `render` with the base
library; read the `base` field from `npx shadcn@latest info` before choosing.

Dialog, Sheet and Drawer always need a Title (`DialogTitle`, `SheetTitle`,
`DrawerTitle`); add `className="sr-only"` when it should not be visible. Use the
full Card composition (`CardHeader`, `CardTitle`, `CardDescription`,
`CardContent`, `CardFooter`) rather than dumping everything into `CardContent`.

Buttons have no `isPending` or `isLoading` prop. Compose the pending state:

```tsx
<Button disabled>
  <Spinner data-icon="inline-start" />
  Saving
</Button>
```

`TabsTrigger` must be inside `TabsList`; never render triggers directly in
`Tabs`. `Avatar` always needs `AvatarFallback` for when the image fails.

Prefer components over custom markup: `Alert` for callouts, `Empty` for empty
states, `toast()` from `sonner` for toasts, `Separator` instead of `<hr>` or a
bordered div, `Skeleton` instead of a custom `animate-pulse` div, and `Badge`
instead of a styled span.

## Icons
Icons inside `Button` carry `data-icon="inline-start"` or `"inline-end"`, and
the component handles sizing, so no `size-4` or `w-4 h-4` on the icon. Icons are
passed as components, not string keys.

```tsx
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>
<Item icon={CheckIcon} />          // correct
<Item icon="check" />              // wrong
```

Use the project's `iconLibrary` for every import, including icons that arrive
with a registry item: swap `lucide-react` imports and icon names for the project
library before moving on.

## Key patterns

```tsx
// Form layout: FieldGroup plus Field, not div plus Label.
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// Validation: data-invalid on the Field, aria-invalid on the control.
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Invalid email.</FieldDescription>
</Field>

// Icons in buttons: data-icon, no sizing classes.
<Button><SearchIcon data-icon="inline-start" />Search</Button>

// Spacing: gap-*, not space-y-*.
<div className="flex flex-col gap-4" />

// Equal dimensions: size-*, not w-* h-*.
<Avatar className="size-10" />

// Status colours: Badge variants or semantic tokens, never raw colours.
<Badge variant="secondary">+20.1%</Badge>
```

## Component selection

| Need | Use |
| --- | --- |
| Button or action | `Button` with the right variant |
| Form inputs | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| Toggle between 2 to 5 options | `ToggleGroup` with `ToggleGroupItem` |
| Data display | `Table`, `Card`, `Badge`, `Avatar` |
| Navigation | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination` |
| Overlays | `Dialog`, `Sheet`, `Drawer`, `AlertDialog` |
| Feedback | `sonner`, `Alert`, `Progress`, `Skeleton`, `Spinner` |
| Command palette | `Command` inside `Dialog` |
| Charts | `Chart`, which wraps Recharts |
| Layout | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible` |
| Empty states | `Empty` |
| Menus | `DropdownMenu`, `ContextMenu`, `Menubar` |
| Tooltips and info | `Tooltip`, `HoverCard`, `Popover` |
