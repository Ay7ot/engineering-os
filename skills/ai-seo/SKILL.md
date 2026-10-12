---
name: ai-seo
description: Optimize content to be discovered, extracted and cited by AI search assistants and AI answer engines. Use when you want citations in AI answers, are doing answer-engine or generative-engine optimization, or checking AI crawler access; not for classic technical SEO (`seo-audit`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/ai-seo
  license: MIT
---
# AI SEO

## When to use
- Getting cited in AI answers from Google AI Overviews, ChatGPT, Perplexity, Gemini or Copilot.
- Answer-engine or generative-engine optimization (AEO, GEO, LLMO).
- Checking whether AI crawlers can reach and cite your content.
- Traditional rankings are fine but AI answers never mention you.

## How AI search differs
- Traditional SEO earns a ranking; AI SEO earns a citation. A well-structured page can be cited from page 2 or 3 because selection weighs content quality, structure and relevance, not just position.
- Platforms select sources differently. AI Overviews summarise top-ranking pages, so there is a strong correlation with rankings. ChatGPT search draws from a wider set than the top-ranked. Perplexity cites sources with links and favours authoritative, recent, well-structured content. Gemini pulls from the Google index and Knowledge Graph. Copilot is Bing-powered.
- Working figures: AI Overviews appear in roughly 45% of Google searches and cut clicks to sites by up to 58%; brands are about 6.5x more likely to be cited via third-party sources than via their own domain; optimised content is cited about 3x more often; statistics and citations lift visibility by 40% or more.

## Google versus other engines
- For Google AI Overviews and AI Mode, optimise for people and core Search: strong E-E-A-T, original information, semantic HTML, clean indexability. No special markup, files or chunking are required, and there is no AI-specific Search Console report.
- Do not write separate content "for AI" (it risks the scaled-content-abuse policy) and do not split pages into tiny fragments. Use normal headings and paragraphs.
- Other engines reward extractable structure: question-shaped headings, self-contained answer blocks, FAQs, comparison tables, definition blocks and machine-readable files. These do not hurt Google; they are just good organisation.

## Query fan-out
- Google's AI generates concurrent related queries, so one page per keyword is weaker than covering the full topical cluster. Brainstorm the 5-10 related queries an AI would fan out to and make sure your content covers them.

## Visibility audit
1. Test 10-20 important queries across platforms and record whether an AI answer appears, whether you are cited, and who is. Query types: "What is [category]?", "Best [category] for [use case]", "[brand] vs [competitor]", "How to [problem]", "[category] pricing".
2. When competitors get cited and you do not, compare extractability, authority signals, freshness, schema and third-party presence.
3. Per priority page, check: a clear definition in the first paragraph; self-contained answer blocks; sourced statistics; comparison tables; a natural-language FAQ; schema (Article, HowTo, FAQPage, Product); a named expert author; an update within 6 months; headings that match query phrasing; and AI bots allowed in robots.txt.
4. Check robots.txt for Disallow rules against AI crawlers: OpenAI's GPTBot and ChatGPT-User, PerplexityBot, Anthropic's anthropic-ai, Google-Extended, and Bingbot for Copilot. Blocking a crawler stops that platform citing you. If you must limit training, block training-only crawlers such as CCBot rather than the search-and-cite ones.

## The three pillars
1. Structure, make it extractable. AI systems extract passages, not pages. Lead every section with a direct answer, keep key answer passages to 40-60 words, use H2/H3 headings phrased like queries, prefer tables for comparisons and numbered lists for process, and keep one idea per paragraph.
2. Authority, make it citable. The Princeton GEO research (KDD 2024) ranked methods by visibility lift: citing sources +40%, adding statistics +37%, expert quotations +30%, authoritative tone +25%, clarity +20%, technical terms +18%, unique vocabulary +15%, fluency +15-30%, and keyword stuffing minus 10% (it actively hurts). The best combination is fluency plus statistics, and low-ranking sites can gain up to 115% with citations. Cite original research with dates, use named authors and quoted experts, show "Last updated", and refresh competitive topics at least quarterly.
3. Presence, be where AI looks. Third-party sources often outrank your own site: factual reference sites, community discussions, industry publications and guest posts, review platforms (G2, Capterra, TrustRadius for B2B SaaS), video, and Q&A sites. Keep profiles accurate, participate genuinely, and earn roundup and comparison mentions.

## Machine-readable files and schema
- Opaque or JavaScript-rendered pricing, or a "contact sales" wall, gets filtered out of AI-mediated buying. Publish a plain-text or markdown pricing file (for example `/pricing.md`) covering unit, limits and what each tier includes, keep it current, and link it from the sitemap and pricing page.
- Add an `/llms.txt` overview (see llmstxt.org) that says what the product does, who it is for, and links key pages.
- Schema helps the non-Google engines: content with proper schema shows 30-40% higher AI visibility there. Use `schema-markup` for Article, HowTo, FAQPage, Product, ItemList, Review and Organization.

## Agentic access
- Autonomous agents read sites through visual rendering, the DOM and the accessibility tree. Render meaningful content without heavy client-side JavaScript, use semantic HTML and correct landmarks, label every interactive element, keep selectors and layouts stable, and keep pricing, specs and contact details on public indexable pages.

## Content types that get cited
- Comparison articles lead at roughly 33%, then definitive guides around 15%, original research 12%, best-of listicles 10%, product pages 10%, opinion and analysis 10%, and how-to guides 8%.
- Underperformers: unstructured blog posts, thin marketing product pages, gated content, undated or unattributed content, and PDF-only content.

## Monitoring
- Track AI Overview presence, brand citation rate, share of AI voice versus competitors, citation sentiment, and which pages get cited (referral traffic from AI sources). Tools such as Otterly AI, Peec AI, ZipTie and LLMrefs cover several platforms, or run your top 20 queries through the assistants monthly by hand and log who is cited.

## What not to do
- Write separate content for AI, or chunk pages into AI-bait fragments.
- Generate thin content at scale for ranking manipulation.
- Fabricate citations or bulk-spam mentions.
- Block search-and-cite crawlers if you want citations.
- Hide main content behind JavaScript that does not render, or skip E-E-A-T fundamentals.

## Checklist
- [ ] Priority queries tested across platforms; citation gaps logged
- [ ] Key answers self-contained, 40-60 words, under query-shaped headings
- [ ] Statistics cited with dates; expert authors named
- [ ] AI search crawlers allowed in robots.txt
- [ ] Pricing and key facts in a machine-readable file and linked
- [ ] Third-party presence accurate and active
- [ ] Freshness signal shown; competitive content refreshed quarterly
- [ ] No AI-only content, chunking, or fabricated mentions
