# Accessibility code patterns

Markup and CSS behind `wcag-accessibility`. Each block is a before/after or a
ready-to-use pattern.

## Text alternatives and icon buttons

```html
<!-- Missing alt -->
<img src="chart.png">

<!-- Descriptive alt -->
<img src="chart.png" alt="Bar chart showing a 40% increase in Q3 sales">

<!-- Decorative image -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- Complex image with a longer description -->
<figure>
  <img src="infographic.png" alt="2024 market trends infographic"
       aria-describedby="infographic-desc">
  <figcaption id="infographic-desc">Detailed description of the chart.</figcaption>
</figure>
```

```html
<!-- No accessible name -->
<button><svg><!-- menu icon --></svg></button>

<!-- aria-label -->
<button aria-label="Open menu">
  <svg aria-hidden="true"><!-- menu icon --></svg>
</button>

<!-- Visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- menu icon --></svg>
  <span class="visually-hidden">Open menu</span>
</button>
```

## Visually hidden class

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Contrast and colour reliance

```css
/* Low contrast, about 2.5:1 */
.low-contrast { color: #999; background: #fff; }

/* Sufficient contrast, 7:1 */
.high-contrast { color: #333; background: #fff; }

/* Focus states need 3:1 against the background (WCAG 1.4.11) */
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
```

```html
<!-- Only colour indicates the error -->
<input class="error-border">

<!-- Colour plus icon plus text -->
<div class="field-error">
  <input aria-invalid="true" aria-describedby="email-error">
  <span id="email-error" class="error-message">
    <svg aria-hidden="true"><!-- error icon --></svg>
    Please enter a valid email address
  </span>
</div>
```

## Media alternatives

```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Descriptions">
</video>

<audio controls>
  <source src="podcast.mp3" type="audio/mp3">
</audio>
<details>
  <summary>Transcript</summary>
  <p>Full transcript text.</p>
</details>
```

## Keyboard access

```html
<!-- Non-interactive element with click only: not focusable, no keyboard activation -->
<div class="card" onclick="handleAction()">Open</div>

<!-- Best: a native button handles focus, Enter/Space, and semantics -->
<button type="button" onclick="handleAction()">Open</button>
```

```javascript
// Only when a non-interactive element must be used (for example a div with
// role="button"). Do NOT add this to a native <button>: Enter and Space already
// fire click, so you would double-trigger.
element.setAttribute('role', 'button');
element.setAttribute('tabindex', '0');
element.addEventListener('click', handleAction);
element.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handleAction();
  }
});
```

Users must be able to Tab into and out of every component. A modal traps focus
while open, sets `inert` on the background, and returns focus to the trigger on
close; the native `<dialog>` element handles this automatically.

## Focus visible and focus not obscured

```css
/* Never leave focus invisible */
*:focus { outline: none; } /* wrong on its own */

:focus-visible {
  outline: 2px solid currentColor; /* inherits text colour, already contrast-checked */
  outline-offset: 2px;
}

/* Or a brand colour verified at 3:1 against every background it lands on */
button:focus-visible {
  box-shadow: 0 0 0 3px rgba(0, 95, 204, 0.5);
}
```

```css
/* Keep a focused element clear of sticky or fixed chrome (WCAG 2.4.11) */
:target { scroll-margin-top: 80px; }
:focus { scroll-margin-top: 80px; scroll-margin-bottom: 60px; }
```

## Skip link

```html
<a class="skip-link" href="#main">Skip to content</a>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 1rem;
  top: 1rem;
  z-index: 100;
  padding: 0.5rem 1rem;
  background: #fff;
  outline: 2px solid currentColor;
}
```

## Target size and dragging

```css
button,
[role="button"],
input[type="checkbox"] + label,
input[type="radio"] + label {
  min-width: 24px; /* WCAG 2.5.8 AA minimum */
  min-height: 24px;
}

.touch-target {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

Any action that requires dragging needs a single-pointer alternative, for
example buttons to move a sortable list item up and down.

## Timing and motion

```javascript
function showSessionWarning() {
  createModal({
    title: 'Session Expiring',
    content: 'Your session will expire in 2 minutes.',
    actions: [
      { label: 'Extend session', action: extendSession },
      { label: 'Log out', action: logout }
    ],
    timeout: 120000
  });
}
```

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Page language and navigation

```html
<html lang="en">

<p>The French word for hello is <span lang="fr">bonjour</span>.</p>

<nav aria-label="Main">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

## Form labels and errors

```html
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email" required>

<!-- Group related fields -->
<fieldset>
  <legend>Shipping address</legend>
  <!-- address fields -->
</fieldset>

<!-- Clear error, announced and described -->
<input aria-invalid="true" aria-describedby="error">
<span id="error" role="alert">Please enter a valid email</span>
```

Validate on submit, mark failing fields with `aria-invalid="true"`, point
`aria-describedby` at the inline error text, and focus the first invalid field.

## Redundant entry and authentication

```html
<fieldset>
  <legend>Shipping address</legend>
  <label>
    <input type="checkbox" id="same-as-billing" checked>
    Same as billing address
  </label>
</fieldset>
```

```html
<input type="password" id="password" autocomplete="current-password">

<button type="button">Sign in with passkey</button>
<button type="button">Email me a login link</button>
```

## Native elements versus ARIA

```html
<!-- ARIA role on a div -->
<div role="button" tabindex="0">Click me</div>

<!-- Native button -->
<button>Click me</button>

<!-- ARIA checkbox -->
<div role="checkbox" aria-checked="false">Option</div>

<!-- Native checkbox -->
<label><input type="checkbox"> Option</label>
```

When ARIA is needed, use the correct roles and states, and keep them in sync
with the visual state. For tabs:

```html
<div role="tablist" aria-label="Sections">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2" tabindex="-1">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Panel one</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>Panel two</div>
```

## Live regions

```html
<div aria-live="polite" role="status">Status: Saved</div>
<div role="alert">Error: form invalid</div>
```

For reliable repeated polite announcements, render a stable empty region before
updating its text. Dynamically inserted alerts have different support and must be
tested with the target screen readers.

## Screen reader commands

- VoiceOver (macOS): `Cmd+F5` to toggle, `Ctrl+Option+Right` to move on,
  `Ctrl+Option+Space` to activate, `Ctrl+Option+U` for the rotor.
- NVDA (Windows): `Insert+Down` to read all, `H` for the next heading, `B` for
  the next button, `Insert+F7` for the element list.
