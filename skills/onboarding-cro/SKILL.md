---
name: onboarding-cro
description: Improve post-signup onboarding, activation and first-run experience so users reach the aha moment faster. Use when users sign up but do not stick, activation is low, or you are designing onboarding flows, empty states or checklists; not for the signup page itself (`page-cro`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/onboarding
  license: MIT
---
# Onboarding CRO

## When to use
- Users sign up but do not activate, return, or complete setup.
- Designing or fixing the first session, empty states, checklists or product tours.
- Setting activation metrics and diagnosing funnel drop-off.

## Before advising
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Establish the product type and whether it is B2B or B2C; the activation definition (the action that marks "they get it"); what happens immediately after signup; and where users currently drop off.

## Define activation
- Pick the action that correlates most with retention: what do retained users do that churned users do not, and what is the earliest signal of future engagement?
- Examples: project tool, create a first project and add a teammate; analytics, install tracking and see a first report; design tool, create a first design and export it; marketplace, complete a first transaction.
- Track activation rate, time to activation, steps to activation and activation by cohort or source.

## Core principles
- Time to value is everything: remove every step between signup and core value.
- One goal per session: one successful outcome first, advanced features later.
- Do, do not show: interactive beats a tutorial.
- Progress motivates: show advancement, celebrate completions, make the path visible.

## First 30 seconds
- Product-first (simple products, B2C, mobile): risk is blank-slate overwhelm.
- Guided setup (products needing personalisation): risk is friction before value.
- Value-first (demo data): risk is that it does not feel real.
- Whatever you choose: one clear next action, no dead ends, progress indication for multi-step.

## Onboarding checklist pattern
- Use when setup has multiple steps, several features to discover, or the product is self-serve B2B.
- 3-7 items ordered by value, quick wins first, a progress bar, celebration on completion, and a dismiss option so users are not trapped.

## Empty states and tours
- Empty states are onboarding, not dead ends: explain what the area is for, show what it looks like with data, give a clear primary action to add the first item, and optionally pre-populate example data.
- Tours: at most 3-5 steps, dismissable at any time, never repeated for returning users.

## Email support
- Email reinforces in-app actions; it does not duplicate them. Trigger-based: welcome (immediate), incomplete onboarding (24h, 72h), activation achieved, then feature discovery at days 3, 7 and 14. Each email drives back into the product with a specific CTA.

## Stalled users
- Define "stalled" (for example X days inactive or incomplete setup), then use an email sequence (value reminder, blockers, help), in-app recovery (welcome back, pick up where they left off), and personal outreach for high-value accounts.

## Metrics
- Activation rate (percent reaching the activation event), time to activation, onboarding completion, and day 1/7/30 retention.
- Map the funnel step by step, for example signup 100% to step 1 80% to step 2 60% to activation 40% to retention 25%, and fix the biggest drop first.

## Output format
- Audit: for each issue, Finding, Impact, Recommendation, Priority.
- Flow design: activation goal, step-by-step flow, checklist items, empty-state copy, email triggers and a metrics plan.

## Product-type patterns
- B2B SaaS: setup wizard, first value action, team invite, deep setup.
- Marketplace: complete profile, browse, first transaction, repeat loop.
- Mobile app: permissions, quick win, push setup, habit loop.
- Content platform: follow or customise, consume, create, engage.

## Checklist
- [ ] Activation event defined and measurable
- [ ] Time to first value minimised; one goal for the first session
- [ ] Every screen has a clear next action and no dead ends
- [ ] Empty states teach and prompt a first action
- [ ] Checklist has 3-7 value-ordered items and is dismissable
- [ ] Email triggers complement in-app onboarding rather than duplicating it
- [ ] Funnel drop-off measured and the biggest drop targeted
