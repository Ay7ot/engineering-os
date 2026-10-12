---
name: schema-markup
description: Add or fix schema.org structured data (JSON-LD) so search engines understand pages and can show rich results. Use when adding structured data, rich snippets or fixing schema validation errors; not for broader SEO audits (`seo-audit`) or AI answer visibility (`ai-seo`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/schema
  license: MIT
---
# Schema Markup

## When to use
- Adding schema.org structured data (JSON-LD) to a page or template.
- Fixing rich-result errors, warnings, or markup that no longer matches the page.
- Targeting a specific rich result such as FAQ, product, review or breadcrumb.

## Before implementing
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Establish the page type and its primary content; which rich results are possible; what schema already exists; and what data is available to populate it.

## Core principles
- Accuracy first: markup must represent the visible page content. Never mark up content that does not exist, and update the markup when the page changes.
- Use JSON-LD. Search engines recommend it, it is easier to maintain, and it goes in the head or at the end of the body.
- Only use types the search engine supports, avoid spam tactics, and review the eligibility requirements before relying on a rich result.
- Validate before deploying, then monitor the Search Console enhancement reports.

## Common types and required properties
- Organization (company homepage or about): name, url. Recommended logo, sameAs (social profiles), contactPoint.
- WebSite (homepage, search box): name, url.
- Article (blog posts, news): headline, image, datePublished, author. Recommended dateModified, publisher, description.
- Product (product pages): name, image, offers with price and availability. Recommended sku, brand, aggregateRating, review.
- SoftwareApplication (SaaS or app pages): name, offers.
- FAQPage (FAQ content): mainEntity, an array of Question and Answer pairs.
- HowTo (tutorials): name, step.
- BreadcrumbList (any page with breadcrumbs): itemListElement, each with position, name and item.
- LocalBusiness: name, address.
- Event (events, webinars): name, startDate, location.

## Combining types
Use `@graph` under one `@context` to emit several types on a page (for example Organization plus WebSite plus BreadcrumbList) rather than separate script blocks:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization" },
    { "@type": "WebSite" },
    { "@type": "BreadcrumbList" }
  ]
}
```

## Validation
- Google Rich Results Test at search.google.com/test/rich-results, the Schema.org validator at validator.schema.org, and the Search Console Enhancements reports.
- Fix the common errors: missing required properties; invalid values (dates must be ISO 8601, URLs fully qualified, enumerations exact); and any mismatch between the markup and the visible content.

## Implementation
- Static sites: add the JSON-LD in the HTML template, using includes or partials for reusable blocks.
- Dynamic sites (React, Next.js and similar): render a schema component server-side and serialise the data to JSON-LD.
- CMS: use a maintained plugin or theme support, and map custom fields to structured data.

## Output
Provide the full JSON-LD block, then a short note naming the rich result it targets and any data the page still needs.

## Checklist
- [ ] Markup matches the visible page content
- [ ] JSON-LD used, with all required properties present
- [ ] Dates ISO 8601, URLs fully qualified, enumerations exact
- [ ] Validates in the Rich Results Test with no errors
- [ ] Multiple types combined with `@graph` where useful
- [ ] Search Console monitored after deploy
