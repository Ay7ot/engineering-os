---
name: page-cro
description: Analyze and improve conversion on marketing pages and lead forms such as homepage, landing, pricing and feature pages. Use when a page is not converting, a URL is shared for feedback, or form abandonment is the problem; not for post-signup onboarding (`onboarding-cro`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/cro
  license: MIT
---
# Page Conversion Rate Optimization

## When to use
- A page is not converting, or a URL is shared with "why is this not working?".
- Reviewing a homepage, landing page, pricing page, feature page or blog page.
- Diagnosing form abandonment.

## Before analysing
- Read the project marketing context document (for example `docs/marketing-context.md`) first, then ask only what is still missing.
- Identify the page type, the primary conversion goal (signup, demo, purchase, subscribe, download, contact sales) and the traffic source (organic, paid, email, social).

## Analysis, in order of impact
1. Value proposition clarity: can a visitor tell what this is and why they should care within 5 seconds? Watch feature-first framing, vagueness or cleverness, and trying to say everything at once.
2. Headline effectiveness: does it state the core value, stay specific, and match the traffic source? Patterns that work: "Get [outcome] without [pain point]", include numbers or timeframes, or social proof such as "Join 10,000+ teams who...".
3. CTA placement, copy and hierarchy: one clear primary action visible without scrolling, written as value not action ("Start Free Trial", "Get My Report" rather than "Submit" or "Learn More"), with a logical primary/secondary structure repeated at decision points.
4. Visual hierarchy and scannability: can a scanner grasp the main message? Check prominence of key elements, white space, and whether images support or distract.
5. Trust and social proof: named testimonials with specifics, case snippets with real numbers, review scores and counts, security badges. Place near CTAs and after benefit claims.
6. Objection handling: price and value, "will this work for my situation?", implementation difficulty, "what if it does not work?". Address with FAQ, guarantees, comparisons and process transparency.
7. Friction: too many form fields, unclear next steps, confusing navigation, unnecessary required fields, mobile issues, slow loads.

## Output format
- Quick wins: easy changes with likely immediate impact.
- High-impact changes: bigger effort, significant conversion gain.
- Test ideas: hypotheses for `ab-testing` rather than assumptions.
- Copy alternatives: 2-3 options for the headline or CTA with rationale.

## Page-specific
- Homepage: clear positioning for cold visitors, a quick path to the most common conversion, and something for both ready-to-buy and still-researching visitors.
- Landing page: message match with the traffic source, a single CTA (remove navigation if possible), the full argument on one page.
- Pricing page: clear plan comparison, an indicated recommended plan, and an answer to "which plan is right for me?".
- Feature page: feature to benefit, use cases and examples, a clear path to try or buy.
- Blog post: contextual CTAs matching the topic, placed at natural stopping points.

## Forms
- Ask only for what you need at this step; every extra field costs conversion.
- Prefer one column, clear labels above fields, inline validation and helpful error messages.
- For long forms, split into steps with visible progress and keep the first step cheap.
- Test field count, label wording, error handling, and required against optional fields.

## Checklist
- [ ] Above-the-fold value clear within 5 seconds
- [ ] One primary CTA, value-bearing copy, visible without scrolling
- [ ] Social proof near CTAs and after benefit claims
- [ ] Top objections answered on the page
- [ ] Form asks only for necessary fields with inline validation
- [ ] Recommendations split into quick wins, high-impact and tests
