---
name: ads
description: Plan, launch and optimise paid campaigns on Google, Meta, LinkedIn, TikTok and X, covering structure, audiences, budgets and bidding. Use when setting up a campaign, choosing targeting, or diagnosing high CPA, low CTR or wasted spend; not for ad copy (`ad-creative`) or landing pages (`page-cro`).
metadata:
  audience: builder, lead
  upstream: https://github.com/coreyhaines31/marketingskills/tree/main/skills/ads
  license: MIT
---
# Paid Ads

## When to use
- Setting up a paid campaign on a new or existing platform.
- Choosing platforms, audiences, budgets and bidding.
- Diagnosing a campaign: high CPA, low CTR, high CPM, or spend going nowhere.
- Planning retargeting.

## Before starting
- Read the project marketing context document (for example `docs/marketing-context.md`) first.
- Goals: objective (awareness, traffic, leads, sales, installs), target CPA or ROAS, budget, and any compliance or geographic constraints.
- Offer: what is promoted, the landing page URL, and why it is compelling.
- Audience: ideal customer, the problem solved, what they search for, and whether customer data exists for lookalikes.
- Current state: past campaigns and results, existing conversion data, and the current funnel conversion rate.

## Platform selection
| Platform | Best for | Use when |
|---|---|---|
| Google Ads | High-intent search traffic | People actively search for the solution |
| Meta | Demand generation, visual products | Creating demand, strong creative assets |
| LinkedIn | B2B decision-makers | Job title and company targeting matter, higher price points |
| X | Tech audiences, thought leadership | The audience is active there and content is timely |
| TikTok | Younger demographics, viral creative | The audience skews 18-34 and video capacity exists |

## Account structure
One campaign per objective and audience, one ad set per targeting variation, and several ads per ad set so creative can be tested. Name campaigns `[Platform]_[Objective]_[Audience]_[Offer]_[Date]`, for example `META_Conv_Lookalike-Customers_FreeTrial_2026Q1`.

Budget: during the first 2-4 weeks put about 70 percent on proven campaigns and 30 percent on new audience and creative tests. When scaling, consolidate into winning combinations, raise budgets 20-30 percent at a time, and wait 3-5 days between increases for the algorithm to relearn.

## Targeting
- Lookalikes: base them on the best customers by lifetime value, not all customers.
- Retargeting: segment by funnel stage, and match the message to the stage. Hot (cart or trial) 1-7 days, warm (key pages) 7-30 days, cold (any visit) 30-90 days.
- Exclusions: remove existing customers unless upselling, recent converters, bounced visitors, and irrelevant pages. Do not let overlapping audiences bid against each other.
- Targeting detail per platform: `references/platform-playbook.md`.

## Copy frameworks
Problem, agitate, solve (problem, sharpened pain, solution, call to action); before, after, bridge (current painful state, desired future state, the product as bridge); and social proof lead (an impressive statistic or testimonial, what you do, then the call to action).

## Creative
- Image: real product screenshots, before and after, statistics as the focal point, real faces, and readable text overlay kept under about 20 percent.
- Video, 15-30 seconds: hook in the first 3 seconds, problem at 3-8, solution at 8-20, call to action at 20-30. Always caption, because most viewers watch without sound. Native feel outperforms polished.
- Test in this order of impact: concept and angle, then hook and headline, then visual style, body copy, and finally the call to action (`ad-creative`).

## Optimisation
| Objective | Primary metrics |
|---|---|
| Awareness | CPM, reach, video view rate |
| Consideration | CTR, CPC, time on site |
| Conversion | CPA, ROAS, conversion rate |

- High CPA: check the landing page first (the problem may be post-click), tighten targeting, test new angles, improve relevance, then adjust bid strategy.
- Low CTR: creative is not resonating, the audience is mismatched, or the creative fatigued. Refresh in that order.
- High CPM: the audience is too narrow, competition is high, or relevance is low. Expand or change placements.
- Bid strategy: start manual or with cost caps, collect at least 50 conversions, then move to automated targets from historical data.

## Reporting
Review weekly: spend versus budget pacing, CPA and ROAS against target, top and bottom ads, audience breakdown, frequency and fatigue risk, and landing page conversion rate.

Platform-reported conversions are inflated, so use consistent UTM parameters, compare platform data with the analytics tool, and judge on blended acquisition cost rather than a single platform's CPA (`analytics`).

## Google responsive search ads
When the request is for Google responsive search ads, follow the output contract in `references/google-rsa-output.md`: exact element counts, character limits printed, ad group structure, at least 8 negative keywords, sitelinks and callouts, in a fixed order so nothing is truncated.

## Pre-launch
- [ ] Conversion tracking tested with a real conversion
- [ ] Landing page loads in under 3 seconds and works on mobile
- [ ] UTM parameters working; budget set correctly
- [ ] Targeting matches the intended audience, with exclusions applied

## Common mistakes
- Launching without conversion tracking, or optimising for the wrong metric.
- Too many campaigns, fragmenting budget, or spreading budget too thin.
- Changing budgets or stopping campaigns during the learning phase.
- Audiences too narrow, too broad, or overlapping; forgetting to exclude existing customers.
- One ad per ad set, no creative refresh, or a mismatch between the ad and the landing page.

## Checklist
- [ ] Marketing context read; goal, budget and target named
- [ ] Platform chosen against the fit table
- [ ] Campaign, ad set and ad structure built with clear naming
- [ ] Budget split between proven and testing, scaled gradually
- [ ] Audiences and exclusions configured, retargeting segmented by stage
- [ ] Creative tests a concept before a hook before a visual
- [ ] Conversion tracking and UTMs verified before launch
- [ ] Weekly review against pacing, CPA and ROAS
