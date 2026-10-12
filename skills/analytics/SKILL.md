---
name: analytics
description: Plan, implement and audit marketing and product analytics tracking such as events, properties, conversions and UTMs. Use when setting up or debugging tracking, GA4 or a tag manager, writing a tracking plan, or asking how a result gets measured; not for running experiments (`ab-testing`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics
  license: MIT
---
# Analytics Tracking

## When to use
- Setting up or auditing web or product analytics (GA4, a tag manager, product analytics tools).
- Writing or reviewing a tracking plan, event schema or conversion definitions.
- Debugging events that are missing, wrong, duplicated or leaking personal data.
- Answering "how will we know this worked?".

## Before implementing
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Establish the business context (what decisions this data informs, what the key conversions are), the current state (what tracking exists, which tools), and the technical context (stack, privacy and consent requirements, who implements).

## Principles
- Track for decisions, not data. Every event should inform a choice; avoid vanity metrics and prefer quality over quantity.
- Start with the questions: what do you need to know, and what will you do with the answer? Work backwards to the events.
- Name things consistently, and document the convention before implementing.
- Maintain data quality: validate the implementation, monitor for issues, and prefer clean data over more data.

## Tracking plan
- Structure: Event Name, Category, Properties, Trigger, Notes.
- Event types: pageviews (automatic, enriched with metadata), user actions (clicks, submissions, feature use), system events (signup completed, purchase, subscription changed), and custom conversions (goals, funnel stages).

## Event naming
- Use object_action, lowercase with underscores: signup_completed, form_submitted, article_read, checkout_payment_completed.
- Be specific: cta_hero_clicked beats button_clicked.
- Put context in properties, not the event name; avoid spaces and special characters; document the decision.

## Essential events and properties
- Marketing site: cta_clicked (button_text, location), form_submitted (form_type), signup_completed (method, source), demo_requested.
- Product or app: onboarding_step_completed (step_number, step_name), feature_used (feature_name), purchase_completed (plan, value), subscription_cancelled (reason).
- Standard properties: page (page_title, page_location, page_referrer); user (user_id, user_type, account_id, plan_type); campaign (source, medium, campaign, content, term); product (product_id, product_name, category, price).
- Reuse consistent names, include only useful context, do not duplicate automatic properties, and keep personally identifiable information out.

## GA4 and tag manager
- GA4 setup: create the property and data stream, install gtag.js or a tag manager, enable enhanced measurement, configure custom events, then mark conversions in Admin.
- Custom event example: gtag('event', 'signup_completed', {'method': 'email', 'plan': 'free'}).
- Tag manager components: tags are the code that fires, triggers decide when, variables supply dynamic values such as click text or data-layer values.
- Push to the data layer rather than scraping the DOM, for example dataLayer.push({'event': 'form_submitted', 'form_name': 'contact', 'form_location': 'footer'}).

## UTM strategy
- utm_source (google, newsletter), utm_medium (cpc, email, social), utm_campaign (spring_sale), utm_content (hero_cta), utm_term (paid keywords).
- Lowercase everything, keep one separator convention, be specific but concise (blog_footer_cta, not cta1), and record every UTM in one place.

## Validation
- Debug with GA4 DebugView, tag manager preview mode, and browser tag or dataLayer inspectors.
- Check that events fire on the right triggers, property values populate, there are no duplicate events, it works across browsers and mobile, conversions are recorded, and no personal data leaks.
- Common faults: events not firing (trigger config, container not loaded), wrong values (variable path, data-layer shape), duplicates (multiple containers, a trigger firing twice).

## Privacy
- Cookie consent is required in the EU, UK and Canada; never put personal data in properties; set data retention; support user deletion.
- Implement consent mode (wait for consent), IP anonymisation, and collect only what you need.

## Output
Produce a tracking plan document: an overview (tools, last updated), an events table (Event Name, Description, Properties, Trigger), custom dimensions (Name, Scope, Parameter), conversions (Conversion, Event, Counting), and a metrics plan naming what to measure.

## Checklist
- [ ] Every event maps to a decision someone will make
- [ ] Event and property names follow one documented convention
- [ ] Conversions marked and verified end to end
- [ ] No duplicate events; validated across browsers and mobile
- [ ] UTMs follow one convention and are recorded
- [ ] Consent, IP handling and no personal data verified
