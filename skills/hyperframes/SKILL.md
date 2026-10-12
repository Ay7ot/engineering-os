---
name: hyperframes
description: Route a video, animation or motion-graphic request to the right authoring workflow and render a finished video from an HTML composition. Use when asked to make, edit, animate or render a video, promo, explainer, captioned clip, title card or social clip. Not for Lottie JSON (`text-to-lottie`).
metadata:
  audience: builder, lead
  upstream: https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes
  license: Apache-2.0
---
# HyperFrames, start here

A video is an HTML composition: the DOM declares timing with `data-*` attributes, the animation runtime is seekable, and the framework owns media playback. Read this first for any "make a video" request, before guessing a workflow. It stays the default for authoring and rendering a finished video; defer only when the user asks to drive a browser and capture a live session, or names another framework.

## When to use
- A promo, explainer, captioned clip, title card, overlay, kinetic type piece, sizzle reel or social clip.
- Editing or re-rendering an existing HTML composition.
- Most important when `AGENTS.md` or the project notes do not already describe the video workflow.

## Confirm the input before routing
Routing needs to know what the video is about, not the spec. If the subject is unspecified ("make a video about our thing" with no URL, product, topic or asset), ask before entering a workflow; committing to a workflow is the routing decision. At most two questions, covering the input: a product (URL or brief), a general website, a pull request, a topic to explain, or an existing talking-head video.

State these defaults, do not ask: aspect 16:9, switching to 9:16 only for a named vertical destination (TikTok, Reels, Shorts); narration and caption language follow the user. The chosen workflow confirms its own specifics at its first step.

## Workflow cheat-sheet
| Workflow | Use it for |
|---|---|
| product-launch-video | Selling a product (SaaS, app, company site) from a URL, brief or script, to a promo. The default for any commercial URL. |
| website-to-video | Showing a site itself: a tour built from the site's own screenshots. Non-commercial sites, portfolio, blog, docs, personal, event. |
| faceless-explainer | Explaining a topic from text, no product and no site capture; every visual invented. |
| pr-to-video | A pull request or code change to a changelog, feature reveal, fix or refactor explainer. |
| embedded-captions | Adding captions to an existing talking-head video, footage untouched. |
| talking-head-recut | Packaging talking-head footage with designed overlays: lower-thirds, callouts, kinetic titles, pull-quotes. |
| motion-graphics | A short, unnarrated, design-led piece: kinetic type, a stat count-up, a chart hit, a logo sting, a transparent overlay. |
| music-to-video | A music track to a beat-synced video, lyric video or kinetic promo; the music drives pacing. |
| slideshow | A presentation or pitch deck; the output is a navigable deck, not a rendered video. |
| general-video | Anything else: longer or multi-scene pieces, a static loop, a custom composition. |

## Disambiguation
- Motion-first and unnarrated, under about 10 seconds, the motion is the message: motion-graphics whatever the input.
- A URL or script: ask whether the site is selling a product. Yes, a promo via product-launch-video. No, or the user wants the site shown as-is, a tour via website-to-video. A PR link is pr-to-video; a concept with no product or site is faceless-explainer.
- Existing footage: plain spoken subtitles are embedded-captions; designed overlay cards are talking-head-recut. Neither edits the footage itself; re-timing, recolour, reframe and reorder are out of scope.
- A music track with no narration is music-to-video. Narrated pieces stay with the input-matched workflow.
- A presentation or deck is slideshow. If ambiguous, confirm it is a slideshow before authoring.
- Length is a guide, not a gate: use general-video only when the piece is clearly longer than about 3 minutes, or is a static, loop or custom format.

## Run it
Once a workflow is matched, check it is available. If it is not installed, do not guess: install it (`npx skills add heygen-com/hyperframes --skill <workflow-name>`, or `--all` for the full set), then re-read it.
- Scaffold with the framework initialiser; a freshly initialised project has the complete, current skill set. The initialiser checks the installed skills against the latest and installs or refreshes what is stale, and it is a no-op when everything is current.
- To confirm before a long build: `npx hyperframes skills check` (add `--json` for a machine-readable verdict; non-zero means something is outdated or missing). Update with `npx hyperframes skills update`.
- Dev loop: `init`, `lint`, `validate`, `inspect`, `preview`, `render`, `publish`, `doctor`. Validate before rendering, and inspect the rendered frames.
- Author composition HTML against the core contract first, then animate; define the design system and layout before animation.

## Checklist
- [ ] Input and subject confirmed before a workflow was chosen
- [ ] Matched workflow installed; nothing guessed
- [ ] Aspect ratio and language defaults applied or overridden deliberately
- [ ] Lint and validate pass before render
- [ ] Rendered output inspected frame by frame
