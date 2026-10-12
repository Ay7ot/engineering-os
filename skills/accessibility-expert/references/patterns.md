# Patterns

Ready-to-use markup behind `accessibility-expert`.

## ARIA widgets and live regions

```html
<!-- Only when HTML semantics are not enough -->
<div role="tablist" aria-label="Sections">
  <button role="tab" aria-selected="true">Tab 1</button>
  <button role="tab" aria-selected="false" tabindex="-1">Tab 2</button>
</div>

<!-- Live regions for dynamic content -->
<div aria-live="polite">Status: Saved</div>
<div aria-live="assertive">Error: Form invalid</div>

<!-- Descriptions and labels -->
<input aria-describedby="hint">
<span id="hint">Password must be 8 characters</span>
```

Composite widgets use roving tabindex: the active item is `0` and all others
`-1`, so Tab moves between widgets and arrow keys move within one.

## Semantic HTML

```html
<!-- Use the semantic element -->
<nav> instead of <div class="nav">
<button> instead of <div onclick>
<main> instead of <div id="main">
<article> instead of <div class="article">

<!-- Proper heading hierarchy -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

## Forms

```html
<!-- Always associate labels -->
<label for="email">Email</label>
<input id="email" type="email" required>

<!-- Group related fields -->
<fieldset>
  <legend>Shipping Address</legend>
  <!-- address fields -->
</fieldset>

<!-- Clear error messages -->
<input aria-invalid="true" aria-describedby="error">
<span id="error" role="alert">Please enter a valid email</span>
```
