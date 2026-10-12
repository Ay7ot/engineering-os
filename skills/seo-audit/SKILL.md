---
name: seo-audit
description: Audit a site for crawlability, technical, on-page, content and authority SEO issues. Use when organic traffic is falling, pages are not indexing or ranking, or you need a technical SEO audit; not for AI answer visibility (`ai-seo`) or structured data (`schema-markup`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills
  license: MIT
---
# SEO Audit

## When to use
- Organic traffic is declining or pages are not indexing or ranking.
- Auditing a new site, a migration, or a specific set of pages.
- Reviewing crawlability, on-page SEO, content quality or internal links.

## Before auditing
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Establish the site type and the primary business goal for SEO; known issues, traffic level and recent changes; and the scope (whole site or specific pages, technical plus on-page or one focus, whether there is Search Console access).

## Audit order
1. Crawlability and indexation: can search engines find and index it?
2. Technical foundations: is the site fast and functional?
3. On-page optimization: is the content optimized?
4. Content quality: does it deserve to rank?
5. Authority and links: does it have credibility?

## Technical
- Crawlability: robots.txt not blocking important pages; an XML sitemap that exists, is accessible, submitted, contains only canonical indexable URLs and is kept current; important pages within 3 clicks of the homepage; logical hierarchy; no orphan pages; for large sites, parameterised URLs and faceted navigation under control.
- Indexation: verify index status and the coverage report; no noindex on important pages; canonicals point the right way and self-reference unique pages; no redirect chains or loops; no soft 404s; no duplicate content without canonicals. Keep HTTP to HTTPS, www versus non-www and trailing-slash handling consistent.
- Core Web Vitals: LCP under 2.5s, INP under 200ms, CLS under 0.1. Also check TTFB, image optimisation, JavaScript execution, CSS delivery, caching headers, CDN use and font loading.
- Mobile: responsive rather than a separate mobile site, adequate tap targets, configured viewport, no horizontal scroll, same content as desktop.
- Security: HTTPS site-wide, a valid certificate, no mixed content, HTTP to HTTPS redirects, HSTS as a bonus.
- URLs: readable and descriptive, keyword where natural, consistent, lowercase and hyphen-separated, without unnecessary parameters.

## On-page
- Title tags: unique, primary keyword near the beginning, 50-60 characters, brand at the end. Watch duplicates, truncation, keyword stuffing and missing titles.
- Meta descriptions: unique, 150-160 characters, primary keyword, a clear value proposition and a call to action.
- Headings: one H1 containing the primary keyword, a logical hierarchy, descriptive rather than decorative. Watch multiple H1s, skipped levels and styling-only headings.
- Content: primary keyword in the first 100 words, related terms used naturally, enough depth to satisfy the search intent, better than the competitors. Watch thin pages, empty tag or category pages, doorway pages and near-duplicates.
- Images: descriptive file names, alt text on all images, compressed sizes, modern formats such as WebP, lazy loading and responsive sources.
- Internal linking: descriptive anchor text, important pages well linked, no broken links, no orphan pages, no over-optimised anchors, and not buried under excessive footer or sidebar links.
- Keyword targeting: one clear primary keyword per page, aligned across title, H1 and URL; keep a keyword map; avoid cannibalisation; build logical topical clusters.

## Content quality
- Experience, expertise, authoritativeness, trustworthiness: first-hand experience and original data; visible author credentials and sourced claims; recognition and citation by others; accuracy, transparency, contact details and HTTPS.
- Depth: comprehensive coverage, answers follow-up questions, better than the top-ranking competitors, updated and current.
- Engagement signals worth reviewing in context: time on page, bounce rate, pages per session, return visits.

## Output
- Executive summary: overall health, the top 3-5 issues, quick wins identified.
- Findings per category, each as Issue, Impact (High/Medium/Low), Evidence, Fix and Priority.
- Prioritized action plan: critical fixes blocking indexation or ranking, then high-impact improvements, quick wins, and long-term recommendations.

## Common issues by site type
- SaaS/product: product pages lack depth, blog not integrated with product pages, no comparison or alternative pages, thin feature pages, no glossary.
- E-commerce: thin category pages, duplicate product descriptions, missing product schema, faceted navigation creating duplicates, mishandled out-of-stock pages.
- Content/blog: outdated posts, keyword cannibalisation, no topical clustering, poor internal linking, missing author pages.
- Local business: inconsistent name, address and phone, missing local schema, an unoptimised business profile, no location pages.

## Checklist
- [ ] robots.txt and sitemaps allow and list the important URLs
- [ ] Indexation, canonicals and redirects verified
- [ ] Core Web Vitals within LCP 2.5s, INP 200ms and CLS 0.1
- [ ] Titles 50-60 chars, metas 150-160 chars, one H1 per page
- [ ] Each page has a primary keyword and no cannibalisation
- [ ] E-E-A-T signals present; thin pages flagged
- [ ] Findings carry impact, evidence, fix and priority
