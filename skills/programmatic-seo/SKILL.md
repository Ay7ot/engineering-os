---
name: programmatic-seo
description: Design and ship SEO pages generated at scale from templates and data, such as location, comparison and integration pages. Use when planning many similar pages around one keyword pattern, or when a live set is thin or not indexing; not for auditing SEO (`seo-audit`) or single pieces (`copywriting`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/programmatic-seo
  license: MIT
---
# Programmatic SEO

## When to use
- Planning pages at scale from a repeating keyword pattern: location, comparison, integration, template, glossary, persona, directory.
- A programmatic set is live but thin, cannibalising, or not indexing.
- Deciding whether a page set is worth building at all.

## Before starting
- Read the project marketing context document (for example `docs/marketing-context.md`) first, then ask only what is missing.
- Establish the conversion goal for the pages, the search patterns to cover, how many pages are realistic, the volume distribution (head vs long tail), and who currently ranks.
- Check the site can support the volume of URLs before generating them.

## Core principles
1. Unique value per page: more than swapped variables. Maximise genuinely differentiated content.
2. Proprietary data wins. Defensibility order: proprietary, product-derived, user-generated, licensed, then public (weakest).
3. Clean URLs: subfolders (`yoursite.com/templates/resume/`), not subdomains, so domain authority consolidates instead of splitting.
4. Match real search intent: each page must answer the query it targets.
5. Quality over quantity: 100 great pages beat 10,000 thin ones.
6. Avoid penalties: no doorway pages, keyword stuffing, duplicate content, or pages built for crawlers rather than users.

## Choose a pattern
- Proprietary data: directories, profiles. Integrations: integration pages. Design or creative product: templates, examples. Multi-segment audience: personas. Local presence: locations. Utility product: conversions. Content or expertise: glossary, curation. Competitor landscape: comparisons.
- Patterns can be layered, for example "best coworking spaces in San Diego".
- Full list with patterns, examples and selection guide: `references/playbooks.md`.

## Implementation
1. Keyword pattern: name the repeating structure and its variables, count unique combinations, then validate demand (aggregate volume, head vs long tail, trend direction).
2. Data: list what populates each page, whether it is first-party, scraped, licensed or public, and how it is refreshed.
3. Template: header with the target phrase, a unique intro, data-driven sections, related pages, and CTAs matched to intent. Add conditional content and per-page analysis so pages differ from their siblings.
4. Internal linking: one hub page plus spokes, cross-links between related spokes, breadcrumbs with structured data, and no orphan pages.
5. Indexation: prioritise high-volume patterns, `noindex` very thin variations, separate sitemaps by page type, and manage crawl budget.

## Before launch
- Each page answers intent, reads usefully, and differs from its siblings.
- Unique titles and meta descriptions, sane heading order, structured data (`schema-markup`), acceptable page speed.
- Linked from site architecture and related pages, present in the sitemap, crawlable, with no conflicting `noindex`.

## After launch
- Track indexation rate, rankings, traffic, engagement and conversion.
- Watch for thin content warnings, ranking drops, manual actions and crawl errors.

## Common mistakes
- Thin content that just swaps a city or product name.
- Cannibalisation: several pages chasing one query.
- Over-generation: pages with no search demand.
- Stale or incorrect data.
- Pages built for crawlers, not users.

## Checklist
- [ ] Pattern and variables defined; demand validated
- [ ] Data source and refresh cadence named
- [ ] Each page carries unique value, not swapped variables
- [ ] URLs use subfolders; hub and internal links in place
- [ ] Unique titles, meta and headings; structured data added
- [ ] Sitemaps separated; thin variations `noindex`ed
- [ ] Indexation, rankings and engagement monitored after launch
