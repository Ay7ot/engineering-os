# Review output

The format for a standalone accessibility review from `better-accessibility`.

## Findings
Group all confirmed findings by principle. Use a markdown table with
**Severity**, **Location**, **Before**, **After** and **Why** columns, never
separate "Before:" and "After:" lines.

- **Severity**: `HIGH` prevents a task, hides content from assistive technology,
  or creates a systemic failure; `MEDIUM` makes an interaction meaningfully
  harder; `LOW` is isolated polish.
- **Location**: cite `path/to/file:line`. With no source files, cite the exact
  screen and component.
- **Before / After**: the current implementation and an actionable replacement.
- **Why**: the violated principle and its user impact.

Consolidate a repeated systemic issue into one row and list every affected
location. Omit principles with no findings.

When the interface is orchestrated by a broader design review, provide domain
evidence and findings to that review and let its output format, severity scale,
consolidation rules and verdict take precedence.

## Example
| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| HIGH | `src/Dialog.tsx:42` | `<button><XIcon /></button>` | Add `aria-label="Close"`; mark the icon `aria-hidden="true"` | The icon-only control has no accessible name |
| HIGH | `src/button.css:12` | `button:focus { outline: none; }` | `button:focus-visible { outline: 2px solid; outline-offset: 2px; }` | Keyboard users cannot see focus |
| HIGH | `src/EmailField.tsx:27` | Error shown only as `border-red-500` | Add `aria-invalid="true"` and `aria-describedby="email-error"` with inline error text | Colour alone neither explains nor announces the error |
| MEDIUM | `src/SignupForm.tsx:64` | Submit disabled until the form is valid | Keep submit enabled; on failure, focus the first invalid field | A disabled action hides what must be fixed |
| MEDIUM | `src/Toolbar.tsx:22` | `size-4` icon-only button | Extend the hit area to 44 x 44px with `after:absolute after:size-11` | The target is too small for reliable touch input |

## Verification and verdict
1. **Verification**: list the exact checks run and their observed results,
   including keyboard traversal, accessible-name inspection, and screen reader or
   automated checks. If a check was not run, state what still needs verification.
2. **Verdict**: `Block` if any `HIGH` finding remains, `Needs changes` if only
   `MEDIUM` or `LOW` findings remain, and `Approve` only when no actionable
   findings remain.

With no findings, omit the tables, state "No actionable accessibility findings",
report verification, and end with `Approve`.
