---
name: directory-submissions
description: Plan and run directory submissions that build dofollow backlinks, discovery and AI citations. Use when choosing directories and tiers, preparing listing copy, or running a review drive; not for the launch plan (`launch`) or destination pages (`programmatic-seo`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/directory-submissions
  license: MIT
---
# Directory Submissions

## When to use
- A product is about to launch and needs its directory layer planned.
- Building or running an ongoing backlink and discovery campaign.
- Deciding which directories to submit to, in which order, with what positioning.
- Setting up a review drive on a review site.

## Before starting
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Note the category (AI, traditional SaaS, no-code, dev tool), because it changes the tier mix.

## Core philosophy
Directories are the foundation layer of distribution, never the whole strategy. They do three things well:

1. Pass dofollow backlinks from high domain-rating sites into your marketing pages, raising domain rating for the whole site.
2. Create discovery surface: people browsing these directories are in-market buyers.
3. Get cited by AI assistants, which pull heavily from high-authority directories for "best [category]" questions. AI-referred traffic converts well above traditional search.

Directories alone do not generate meaningful leads. They pass link equity into pages that do, so build the destinations first.

## Three hard rules
1. Foundation before submission. Do not submit until the page a directory links to is live and has: a single `h1` with sequential heading order, a real pricing page, privacy policy and terms, logo assets (PNG, SVG, square and favicon), 5-8 real product screenshots, a 60-90 second demo video, FAQ schema, and `Organization`, `Product` and `SoftwareApplication` structured data.
2. Destination pages before directories. At minimum: 3-5 competitor alternative pages (`/alternatives/[competitor]`), 3-5 use-case pages (`/for/[audience]`), a template or asset gallery if the category allows, and one honest "best of" post about your own category.
3. Positioning varies by directory type. Never paste one description everywhere; AI systems down-weight duplicate content and each audience responds to different framing.
- Full tier catalog and the positioning variant table: `references/tiers-and-positioning.md`.

## Workflow
1. Readiness: confirm the product is publicly reachable, the pricing page, policy pages and assets exist, landing pages carry schema and structured data, at least 3 alternative and 3 use-case pages are live and indexed, and about 20 early users could leave a review. Items up to the pages are hard blocks; the review pool is a soft block.
2. Choose tiers: pick only where the product is a genuine fit. Forcing a listing into a wrong category burns the first-submission advantage and gets rejected.
3. Prepare asset variants per tier: a tagline under 10 words, a 60-character description, a 150-word description, 5-8 category tags, logo assets, screenshots and demo video, and a 2-3 sentence founder story.
4. Batch submit, working through a tracker. Per submission: copy the tier-appropriate variant, fill the form, upload assets, submit, then log the date, URL, status and moderator notes.
5. Verify the backlink is dofollow once live: `bash` a HEAD request and check the response for a `rel=` attribute. If absent, the link is dofollow.

## Reviews playbook
A review-site listing is close to worthless without reviews; 10 reviews is the threshold for grid placement. Run the 10-in-30 protocol in launch month:

1. Identify 20 users who completed a meaningful action.
2. Send each a personal note with the direct review URL. Direct links cut friction sharply versus forms or landing pages.
3. Offer a modest, platform-allowed thank-you (a small gift card is usually permitted; check current rules).
4. Follow up once after about 5 days, never twice.
5. Target 50 percent conversion, so 10 reviews from 20 asks.

Respect review-report cutoffs; missing one means waiting a quarter. The free badge tier usually requires 20 reviews at a 4.0 average, while paid grid and award badges can wait until year two.

## GEO
- One `h1` per page with sequential headings, dense factual content with specific numbers, FAQ schema, comparison tables, and an explicit "what it is" paragraph in the first 100 words.
- Get genuine mentions in communities that AI systems index, and publish original research that others cite.
- Claim and complete company profiles: business database, company page and open knowledge-base entry.
- Measure monthly by asking AI assistants "what are the best [category] tools?" and logging where the product appears.
- Detail: `ai-seo`.

## KPIs
Track weekly, and investigate a stalled number instead of submitting more directories:

| Metric | Day 0 | Day 30 | Day 90 |
|---|---|---|---|
| Domain rating | 0 | 20 | 30+ |
| Referring domains | 0 | 30 | 80+ |
| Indexed pages | 0 | 50 | 200+ |
| Organic clicks per day | 0 | 30 | 200+ |
| Listings live | 0 | 50 | 70+ |
| Review-site reviews | 0 | 10 | 25 |
| AI citations (manual check) | 0 | 3 | 15+ |

## What not to do
- Do not pay for submission services; the work is free and takes an afternoon.
- Do not submit to spam directories (very low domain rating, no traffic, no editorial standards).
- Do not use one generic description across directories.
- Do not treat directories as the whole go-to-market plan.
- Do not submit without reviews, or before the destination page exists.
- Do not lie on comparison pages; AI systems cross-reference claims.
- Do not over-index on a single launch-day spike. The flywheel is templates, alternatives, reviews and ongoing content.

## Checklist
- [ ] Marketing context read; category and tier mix chosen
- [ ] Readiness items confirmed, hard blocks cleared
- [ ] Destination pages live and indexed
- [ ] Asset variants prepared per tier, descriptions not duplicated
- [ ] Tracker set up; submissions logged with status
- [ ] Live backlinks verified as dofollow
- [ ] Review drive planned against the 10-in-30 protocol
- [ ] KPIs baselined and reviewed weekly
