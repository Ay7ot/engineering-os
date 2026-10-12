---
name: product-marketing-context
description: Create and maintain the shared product marketing context document that other marketing work reads for positioning, audience, voice and proof. Use when starting marketing for a product, when a brief is missing or stale, or when another marketing task needs agreed context.
metadata:
  audience: lead, builder
  upstream: https://github.com/coreyhaines31/marketingskills
  license: MIT
---
# Product Marketing Context

## When to use
- Marketing work is starting on a product and no shared brief exists.
- Another marketing task needs positioning, audience, voice or proof points.
- The product, audience or pricing changed and the brief is now stale.

## Where it lives
Write the document to `docs/marketing-context.md` in the project. Every other
marketing task reads it at the start and asks only for what is missing or
specific to that task, so nobody repeats the same questions.

## Workflow
1. Check for an existing file with `glob` before asking anything. If it exists, `read` it, summarise what is captured, and ask which sections to update. Gather only those.
2. If it does not exist, offer auto-drafting from the repo first (recommended): `read` the README, landing pages, meta descriptions and package manifest, draft every section, present it, then ask "what needs correcting, what is missing?".
3. Otherwise walk through the sections one at a time, conversationally. Do not dump all questions at once.
4. Validate as you go: summarise each section and confirm before moving on.
5. `write` the file, then keep it current. Treat it as the source of truth for later marketing tasks, not a one-off document.

## Sections to capture
- Product overview: one-line description, what it does in 2-3 sentences, category (how customers search for it), product type, business model and pricing.
- Target audience: target company type, decision-makers and roles, primary use case, jobs to be done, specific scenarios.
- Personas (B2B only): for each stakeholder (user, champion, decision maker, financial buyer, technical influencer), what they care about, their challenge, the value promised to them.
- Problems and pain points: the core challenge before finding you, why current solutions fall short, what it costs them, the emotional tension.
- Competitive landscape: direct, secondary and indirect competitors, and how each falls short.
- Differentiation: capabilities alternatives lack, how you solve it differently, why that is better, why customers choose you.
- Objections and anti-persona: the top three objections heard in sales and how to answer them, plus who is not a good fit.
- Switching dynamics: push, pull, habit and anxiety.
- Customer language: how customers describe the problem and the solution in their own words, phrases to use, phrases to avoid, product glossary.
- Brand voice: tone, communication style, three to five personality adjectives.
- Proof points: metrics to cite, notable customers, testimonial snippets, value themes and their evidence.
- Goals: primary business goal, the key conversion action, current metrics if known.

## Tips
- Ask "What is the number one frustration that brings them to you?" rather than "What problem do you solve?".
- Capture exact customer words over polished descriptions; verbatim language is more valuable.
- Ask for an example whenever an answer is abstract.
- Skip sections that do not apply, for example personas for a B2C product.

## Checklist
- [ ] Existing document checked before any question was asked
- [ ] Auto-draft from the repo offered first
- [ ] Verbatim customer language captured, not paraphrased
- [ ] Every section confirmed with the user, not assumed
- [ ] Written to `docs/marketing-context.md` and linked from this task
