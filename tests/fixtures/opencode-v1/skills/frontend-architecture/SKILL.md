---
name: frontend-architecture
description: Design maintainable frontend architecture (state, data fetching, components, styling, routing, performance). Use when planning or reviewing frontend work.
metadata:
  audience: architect, builder
---
# Frontend Architecture

## When to use
- Planning or implementing frontend features (SPA, SSR, mobile web).
- Reviewing frontend code for maintainability and performance.

## Rules
- Component model: presentational vs container/smart components; keep data-fetching at the edges.
- State management: local state first; shared state only when truly shared; server state in a cache with invalidation strategy, not duplicated in client state.
- Data fetching: typed clients, error/loading states, optimistic updates with rollback, refetch/invalidation, dedupe.
- Routing: nested routes matching component tree; loading + error boundaries per route.
- Styling: one consistent approach (CSS modules, Tailwind, CSS-in-JS) — documented; design tokens for theme.
- Accessibility: semantic HTML, keyboard navigation, focus management, contrast; not an afterthought.
- Performance: bundle budgets, code splitting by route, lazy images, memoization only where measurable, avoid layout thrash, Core Web Vitals targets.
- Forms: controlled/uncontrolled decision, validation consistent, disabled/loading states, idempotent submit.
- Security: XSS prevention (escape output, avoid dangerouslySetInnerHTML), CSP headers, CSRF awareness, no secrets in client bundles.
- Testing: component tests for behavior, E2E for critical user journeys, not snapshot tests.

## Checklist
- [ ] Data fetching at edges, cache with invalidation
- [ ] Local state before shared state
- [ ] Consistent styling + tokens
- [ ] A11y basics (semantics, keyboard, focus)
- [ ] Performance: code splitting, budgets, CWV
- [ ] XSS/CSP/CSRF handled
- [ ] Testing: behavior + E2E for critical journeys