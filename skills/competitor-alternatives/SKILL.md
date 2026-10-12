---
name: competitor-alternatives
description: Build competitor comparison and alternative pages that rank for competitive searches and help evaluators decide. Use when creating alternative, vs or "A vs B" pages, or refreshing comparison content; not for whole-site SEO audits (`seo-audit`) or general page copy (`copywriting`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills
  license: MIT
---
# Competitor and Alternative Pages

## When to use
- Creating comparison or alternative pages for named competitors.
- Refreshing comparison content whose pricing, features or positioning changed.
- Adding a hub that links all competitor content together.

## Before writing
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Gather your positioning: core value, key differentiators, ideal customer, pricing, and the honest weaknesses you will disclose.
- Gather the competitive landscape: direct and indirect competitors, their positioning, and likely search volume.
- Decide the goal: capturing search traffic, sales enablement, winning switchers, or brand positioning.

## Page formats
- `[Competitor] alternative` (singular). Intent: actively switching. URL `/alternatives/[competitor]`. Structure: why people look for alternatives, you as the alternative, detailed comparison, who should switch, migration path, social proof, CTA.
- `[Competitor] alternatives` (plural). Intent: researching options. URL `/alternatives/[competitor]-alternatives`. Structure: why look, criteria framework, 4-7 real alternatives (you first), comparison table, detail, recommendation by use case, CTA. Include 4-7 genuinely useful options; honesty ranks better and reads better.
- `You vs [Competitor]`. Intent: direct comparison. URL `/vs/[competitor]`. Structure: TL;DR, comparison table, detail by category, who each suits, testimonials, migration support, CTA.
- `[A] vs [B]` (both competitors, not you). URL `/compare/[a]-vs-[b]`. Structure: overview of both, comparison, who each suits, then introduce yourself as the third option, a three-way table, CTA.

## Core principles
- Honesty builds trust: acknowledge competitor strengths, be accurate about your limits, and never misrepresent their features. Readers verify claims.
- Depth over surface: explain why differences matter and in which scenarios, rather than shipping a bare checklist.
- Help them decide: state clearly who each option is best for, including when a competitor wins.
- Centralise competitor data: keep one source of truth per competitor so a correction propagates to every page.

## Sections every page needs
- TL;DR of the key differences in 2-3 sentences for scanners.
- Paragraph comparison per dimension, beyond the table.
- Feature comparison per category with strengths, limits, and a bottom line.
- Pricing: tier by tier, what is included, hidden costs, and total cost for a sample team size.
- An explicit "who this is for" for each option.
- Migration: what transfers, what needs reconfiguration, support offered, and quotes from customers who switched.

## Research process
- For each competitor: sign up and use the product, document current pricing and hidden costs, mine review sites for recurring themes, talk to customers who switched in both directions, and read their positioning, comparison pages and changelog.
- Refresh quarterly for pricing and major features, immediately when a customer flags a change, and in full once a year.

## SEO
- Target the phrases in the formats above, including reversed order ("[Competitor] vs [You]").
- Link related competitor pages to one another, link from feature pages into relevant comparisons, and build a hub page.
- Add FAQ structured data (`schema-markup`) for questions such as "what is the best alternative to [competitor]?".

## Checklist
- [ ] Marketing context read; positioning and weaknesses agreed
- [ ] Format and URL chosen for the search intent
- [ ] TL;DR, comparison table and paragraph comparisons present
- [ ] Pricing compared tier by tier with hidden costs
- [ ] Who each option is for stated honestly
- [ ] Migration path and switcher quotes included
- [ ] Related competitor pages and hub linked; FAQ schema added
