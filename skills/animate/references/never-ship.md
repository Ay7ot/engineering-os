# Never ship

The self-check behind `animate`. Every row is an automatic block in
`review-animations`.

| Never | Instead |
| --- | --- |
| `transition: all` | Name the exact properties |
| `scale(0)` entrance | `scale(0.95)` plus `opacity: 0` |
| `ease-in` on a UI element | `ease-out` or a strong custom curve |
| Built-in `ease-out` on a deliberate animation | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Animation on a keyboard shortcut or 100+/day action | No animation |
| UI duration over 300ms with no reason | 150-250ms |
| `transform-origin: center` on a trigger-anchored popover | `var(--transform-origin)` (modals exempt) |
| Keyframes on toasts, toggles, rapidly triggered elements | CSS transitions |
| Animating `width`/`height`/`margin`/`padding`/`top`/`left` | `transform` and `opacity` |
| Motion `x`/`y`/`scale` props under load | Full `transform` string |
| Ungated `:hover` motion | `@media (hover: hover) and (pointer: fine)` |
| Missing `prefers-reduced-motion` | A gentler variant, not zero |
| Everything entering at once | 30-80ms stagger |

For the common cases (button press, dropdown, tooltip, modal, drawer, toast,
accordion, stagger, hold-to-confirm, tab indicator, scroll reveal,
drag-to-dismiss), start from a component-library primitive or an existing
implementation in the codebase rather than a blank file.
