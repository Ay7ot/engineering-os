# Common mistakes

The frequent accessibility mistakes behind `better-accessibility`, each with its
fix.

| Mistake | Fix |
| --- | --- |
| `outline: none` to remove the focus ring | Style `:focus-visible`; mouse clicks will not show it |
| Custom focus colour assumed to work everywhere | Verify the full indicator against every adjacent colour and in forced-colors mode |
| `<div onClick>` for a button or link | `<button>` for actions, `<a href>` for navigation |
| Placeholder used as the only label | Add a visible `<label for>`; placeholders disappear on input |
| Positive `tabindex` to fix focus order | Fix the DOM order; only use `0` and `-1` |
| Repeated polite update inconsistently announced | Keep a stable empty status region and update its text |
| `assertive` live region for a routine toast | Use `polite`; reserve `assertive` for errors |
| `aria-hidden="true"` on a focusable element | Remove it or make the element non-focusable |
| Functional icon alt describes the picture | Describe the action: `alt="Search"`, not `alt="magnifying glass"` |
| Submit disabled until the form is valid | Keep it enabled; validate on submit and focus the first error |
