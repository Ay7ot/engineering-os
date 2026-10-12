# Testing and issue priority

How to verify a WCAG audit and in what order to fix what it finds.

## Automated testing
```bash
npx lighthouse https://example.com --only-categories=accessibility
axe https://example.com
```

## Manual testing
- [ ] **Keyboard navigation:** Tab through the entire page, use Enter and Space to
  activate
- [ ] **Screen reader:** test with VoiceOver (Mac), NVDA (Windows) or TalkBack
  (Android)
- [ ] **Zoom:** content usable at 200% zoom
- [ ] **High contrast:** test with Windows High Contrast Mode
- [ ] **Reduced motion:** test with `prefers-reduced-motion: reduce`
- [ ] **Focus order:** logical and follows the visual order
- [ ] **Target size:** interactive elements meet the 24 x 24px minimum

See `a11y-patterns.md` for VoiceOver and NVDA shortcuts.

## Common issues by impact
**Critical (fix immediately)**
1. Missing form labels
2. Missing image alt text
3. Insufficient colour contrast
4. Keyboard traps
5. No focus indicators

**Serious (fix before launch)**
1. Missing page language
2. Missing heading structure
3. Non-descriptive link text
4. Auto-playing media
5. Missing skip links

**Moderate (fix soon)**
1. Missing ARIA labels on icons
2. Inconsistent navigation
3. Missing error identification
4. Timing without controls
5. Missing landmark regions
