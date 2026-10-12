# Skills

Every skill is a playbook an agent loads when a task matches. The source of
truth is `skills/<name>/SKILL.md`; the per-editor adapters render them into
each editor (`eng sync`). Descriptions below are the trigger lines agents see.

## Core engineering

| Skill | Use when |
|---|---|
| `api-design` | creating or extending HTTP/REST, GraphQL, RPC, or internal service APIs |
| `architecture-analysis` | designing or evaluating a system, component, API, or significant change |
| `backend-architecture` | planning or reviewing backend work |
| `code-review` | reviewing a diff, branch, PR or files written by someone else |
| `database-design` | creating or modifying tables, collections, or data models |
| `dataviz` | building a chart, stat tile, metrics page or dashboard, or picking colours for data |
| `debugging` | diagnosing a reported problem |
| `diagrams` | producing architecture proposals, implementation plans, ADRs, runbooks, or explaining a system, flow, state machine, or change visually |
| `documentation` | creating or updating docs |
| `frontend-architecture` | planning or reviewing frontend work |
| `git-workflow` | git commands are run |
| `memory-hygiene` | Audit and tidy EngineeringOS memory, finding duplicate or contradictory ADRs, superseded decisions, stale project state and dead tasks, then correc... |
| `observability` | adding observability to a system or debugging an incident |
| `payments` | building or reviewing billing/payments code |
| `project-planning` | Turn approved architecture into small, verifiable implementation tasks with dependencies and acceptance criteria. Use before delegating implementation |
| `repository-exploration` | starting work in a repo or area you have not mapped yet |
| `security-review` | Review code, configs, and dependencies for security weaknesses. Use before merge when changes touch auth, payments, data, webhooks, secrets, or inf... |
| `simplify` | Tidy a finished, passing change so reviewers see the smallest clear version of it, without changing what it does. Not a bug hunt and not a redesign... |
| `skill-authoring` | adding a new skill, changing a skill's scope, or when a skill is being ignored or loaded for the wrong tasks |
| `technical-research` | investigating unfamiliar technology, evaluating a tool, comparing approaches, or writing a research report |
| `testing` | creating tests, running the suite, verifying acceptance criteria, or confirming a change works end to end |
| `agent-instructions` | asked to check, audit, update or fix AGENTS.md, or when project context has gone stale |

## Design, frontend and design systems

| Skill | Use when |
|---|---|
| `frontend-design` | building web components, pages or posters that need real design quality rather than a default look |
| `design-taste-frontend` | building or redesigning a landing page, portfolio or marketing section |
| `minimalist-ui` | the brief asks for a minimal, document-style or workspace-style UI |
| `high-end-visual-design` | a page must feel premium or Awwwards-tier, or when a design looks cheap and generic |
| `redesign-existing-projects` | asked to redesign, modernise or polish a project that already exists |
| `better-typography` | picking fonts, setting a type scale, or reviewing how text renders and wraps |
| `better-colors` | creating a colour system, converting colours, checking contrast, or fixing dark mode |
| `better-layout` | structuring a page or component, or reviewing spacing and responsive collapse |
| `better-ui` | building or reviewing UI components, states, icons or micro-interactions |
| `tailwind-design-system` | creating a component library, design tokens or theming |
| `shadcn` | a project has components.json or the task mentions shadcn, presets or registry items |
| `create-design-md` | asked to document a design system or give coding agents persistent UI context |
| `web-interface-guidelines` | asked to review a UI, audit accessibility or check a site against web best practices |

## Motion and accessibility

| Skill | Use when |
|---|---|
| `apple-design` | building or reviewing gesture-driven UI, spring animations, or drag, swipe and sheet interactions |
| `animate` | asked to animate something, add motion, or build a transition |
| `review-animations` | reviewing a diff, branch or PR that adds or changes motion, transitions, keyframes, easing or gestures |
| `break-ui` | asked to break, stress-test, or find edge cases in a component |
| `animation-vocabulary` | asked what a motion effect is called, or when describing one without knowing its name |
| `improve-animations` | asked to improve the animations, audit the motion, or make an app feel better |
| `find-animation-opportunities` | asked what could be animated here, or how to make this feel more alive |
| `wcag-accessibility` | asked for an a11y audit, WCAG compliance, or to make a page accessible |
| `better-accessibility` | building or reviewing a component, modal, menu, form or widget, or told to make it accessible |
| `accessibility-expert` | you need a quick a11y checklist while building or reviewing a page |

## Product, discovery and AI product

| Skill | Use when |
|---|---|
| `brainstorming` | starting a feature, component or behaviour change, before any code or scaffolding is written |
| `to-prd` | asked to create a PRD from context already in the session |
| `writing-plans` | turning a spec into step-by-step tasks before touching code |
| `prototype` | sanity-checking whether a state model or logic feels right, or exploring what a UI should look like before committing to a design |
| `triage` | asked what needs attention, or to triage, label, or close a reported issue or external PR |
| `to-issues` | turning approved scope into tracker issues |
| `wayfinder` | a loose idea is wrapped in fog and the destination is not yet visible |
| `opportunity-solution-tree` | structuring product discovery, prioritising what to build next, or comparing solutions before committing |
| `user-research` | asked for a research plan, interview guide, survey design or research questions |
| `usability-testing` | planning user tests, validating a prototype, or investigating why users struggle with a product |
| `ai-evals` | building evals for an LLM product, measuring output quality, or designing test cases and scoring rubrics |
| `pm-handoff` | ending a session mid-task, or when another session will pick the work up |
| `working-backwards` | defining a new product or feature, writing a PR/FAQ, or working back from a future state |
| `scoping-cutting` | defining an MVP, fighting scope creep, or deciding what to drop to ship sooner |
| `product-manager-toolkit` | scoring or sequencing product work, planning capacity, or sizing a feature portfolio |
| `customer-journey-map` | mapping the customer experience, finding friction or drop-off, or improving onboarding and retention |
| `ai-product` | building or reviewing an AI feature, or debugging unreliable model output |
| `ai-product-strategy` | planning an AI feature or roadmap, or when AI is being added without a clear user problem |
| `grilling` | asked to stress-test thinking, harden a plan, or resolve open questions before implementation |

## Engineering process

| Skill | Use when |
|---|---|
| `test-driven-development` | implementing a feature, fixing a bug, refactoring, or changing behaviour |
| `verification-before-completion` | about to report success, commit, open a PR, or accept a subagent's report |
| `subagent-driven-development` | a plan has mostly independent tasks |
| `dispatching-parallel-agents` | 2 or more problems are independent and share no state |
| `karpathy-guidelines` | writing, reviewing, or refactoring code, before adding features or abstractions |
| `using-git-worktrees` | starting work that must not disturb the current checkout |
| `executing-plans` | handed a plan to implement in a separate session |

## Marketing, SEO and growth

| Skill | Use when |
|---|---|
| `copywriting` | drafting or rewriting page or ad copy, positioning a headline, or writing button text |
| `copy-editing` | editing, proofreading, tightening or refreshing copy, or auditing content for staleness |
| `page-cro` | a page is not converting, a URL is shared for feedback, or form abandonment is the problem |
| `onboarding-cro` | users sign up but do not stick, activation is low, or you are designing onboarding flows, empty states or checklists |
| `seo-audit` | organic traffic is falling, pages are not indexing or ranking, or you need a technical SEO audit |
| `ai-seo` | you want citations in AI answers, are doing answer-engine or generative-engine optimization, or checking AI crawler access |
| `schema-markup` | adding structured data, rich snippets or fixing schema validation errors |
| `analytics` | setting up or debugging tracking, GA4 or a tag manager, writing a tracking plan, or asking how a result gets measured |
| `ab-testing` | comparing two versions, deciding whether a change is worth testing, or building an experimentation programme |
| `emails` | building an automated email flow or drip campaign, choosing sequence length and timing, or writing sequence copy |
| `cold-email` | writing prospecting or SDR emails, subject lines, opening lines, or a multi-touch follow-up sequence |
| `launch` | preparing to ship publicly, writing a launch or go-to-market plan, or announcing a release |
| `programmatic-seo` | planning many similar pages around one keyword pattern, or when a live set is thin or not indexing |
| `competitor-alternatives` | creating alternative, vs or "A vs B" pages, or refreshing comparison content |
| `content-strategy` | deciding what to write about, building content pillars, topic clusters or an editorial calendar |
| `directory-submissions` | choosing directories and tiers, preparing listing copy, or running a review drive |
| `lead-magnets` | choosing what to give away, designing an opt-in, or fixing a magnet that does not convert |
| `ad-creative` | asked for headlines, descriptions or RSA copy, or iterating on winning and losing ads |
| `ads` | setting up a campaign, choosing targeting, or diagnosing high CPA, low CTR or wasted spend |
| `social` | planning a content calendar, repurposing long-form content, or scripting a Reel |
| `marketing-psychology` | asking why people buy, picking a bias such as anchoring or social proof, or designing a nudge |
| `marketing-ideas` | stuck on how to market, asking what else to try, or shortlisting channels |
| `product-marketing-context` | starting marketing for a product, when a brief is missing or stale, or when another marketing task needs agreed context |

## Founder, GTM and monetisation

| Skill | Use when |
|---|---|
| `referral-program` | building a refer-a-friend or affiliate programme, choosing incentives, or diagnosing a low referral rate |
| `churn-prevention` | customers keep cancelling, designing an exit survey and save offers, or setting up dunning |
| `founder-sales` | doing early outreach, running first discovery calls, qualifying leads, or deciding when to hire a salesperson |
| `pitch-deck` | building or reviewing a fundraising deck or asking what slides to include |
| `yc-pitch-deck` | preparing for YC, Demo Day, or a Sequoia-format pitch |
| `fundraising` | weighing venture capital against bootstrapping, preparing to meet investors, or running a round |
| `measuring-product-market-fit` | asking if you have PMF, reading retention data, or choosing between scaling and iterating |
| `pricing-strategy` | setting a price for the first time, moving between freemium and paid, or testing monetisation changes |

## Content, docs and media

| Skill | Use when |
|---|---|
| `ux-writing` | writing or reviewing product UI text |
| `doc-coauthoring` | writing a proposal, spec, PRD or decision doc with the user |
| `internal-comms` | drafting a team or company-wide update |
| `research` | asked to research a topic, gather docs or API facts, or delegate reading legwork to a background agent |
| `ppt-visual` | building or redesigning presentation slides, fixing a text-heavy deck, or specifying a slide layout |
| `brandkit` | generating a brand-guidelines board, logo concept sheet or identity deck image |
| `ip-as-logo` | making a mascot or creature image, or proposing three directions and six candidates |
| `brand-guidelines` | brand colors, style guidelines or company design standards apply |
| `theme-factory` | a slide deck, doc, report or HTML page needs a consistent look |
| `canvas-design` | asked for a poster, a print, a piece of art or another static design |
| `algorithmic-art` | asked for generative or algorithmic art, a code-drawn composition or an interactive viewer |
| `d3-visualization` | implementing a bespoke chart, dashboard, map or network diagram in code rather than a ready-made chart component |
| `text-to-lottie` | asked to create, edit, fix or preview a Lottie animation |
| `prompt-images` | prompting an image model or building an image generation feature |
| `prompt-videos` | prompting a video model or building a video generation feature |
| `hyperframes` | asked to make, edit, animate or render a video, promo, explainer, captioned clip, title card or social clip |

## Design process and tooling

| Skill | Use when |
|---|---|
| `design-critique` | reviewing a mockup, prototype or live UI with peers, or receiving feedback on your own design |
| `wireframe-prototyping` | sketching a new screen or flow, building an interactive prototype for feedback, or deciding how much fidelity a concept needs |
| `design-workshop-facilitation` | running a problem definition, ideation, journey mapping or alignment session, or planning a design sprint |
| `loop-me` | asked to design or spec a repeating workflow, or to find loops worth delegating |
| `just-scrape` | you need content from a URL, structured data from a site, or change tracking |
| `find-skills` | asked whether a skill exists for something, or to extend what agents can do |
| `deploy-to-vercel` | asked to deploy an app, get a preview link, push a site live, or check a deployment |
| `agent-browser` | asked to test a web app, open a site, capture a page, or reproduce a UI bug |
| `gstack` | asked to open or test a site, verify a deployment, walk a user flow, or file a bug with screenshots |
| `extract-design-system` | asked to bootstrap a design system from a live site |
| `ui-ux-pro-max` | building or reviewing a screen, page or component and you need concrete thresholds |
| `impeccable` | building or refining UI, when a design looks generic or templated |

## Provenance

Many skills were distilled on 2026-10-12 from the
[aiuxplayground.com skills catalogue](https://aiuxplayground.com/skills) (175
listed). Each adapted skill carries `metadata.upstream` (source repo) and
`metadata.license`; only permissively licensed sources were adopted.

Adopted licences: **MIT** for coreyhaines31/marketingskills, mattpocock/skills,
obra/superpowers, leonxlnx/taste-skill, jakubkrehel/skills, emilkowalski,
RefoundAI/lenny-skills, phuryn/pm-skills, shawnpang, guia-matthieu, sickn33,
vercel-labs, slb2248/ai-ux-skills, addyosmani/web-quality-skills,
multica-ai/andrej-karpathy-skills, diffusionstudio/lottie, scrapegraphai,
claude-office-skills, garrytan, arvindrk, nextlevelbuilder, s1dashu,
agentspace-so, jamesrochabrun, ehmo, sleekdotdesign, stripe, and others;
**Apache-2.0** for anthropics/skills, anthropics/knowledge-work-plugins,
anthropics/claude-plugins-official, replicate/skills, heygen-com/hyperframes,
google-labs-code/stitch-skills, ReScienceLab/opc-skills, pbakaus/impeccable,
vercel-labs/agent-browser.

**Not adopted.** The source-available Anthropic document skills (`docx`, `pdf`,
`pptx`, `xlsx`) and skills whose source repo declares no licence (`unslop`,
`firecrawl`, `ai-image-generation`, `remotion-*`, `notion-*`, `review-loop`,
and others) were left out.

## Attribution

Distilled skills are adapted works of the upstream projects named in each
skill's `metadata.upstream`. Their notices are honoured here rather than
copied verbatim: the wording is the EngineeringOS editors', the substance
belongs to the upstream authors. Remove a skill, or its `metadata.upstream`
line, if a licence changes.

