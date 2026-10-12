---
name: text-to-lottie
description: Author a Lottie (Bodymovin) JSON animation that renders in a Skottie-based player, with scene folders, editable slots and seekable frames. Use when asked to create, edit, fix or preview a Lottie animation. Not for video rendered from HTML (`hyperframes`).
metadata:
  audience: builder
  upstream: https://github.com/diffusionstudio/lottie/tree/main/skills/text-to-lottie
  license: MIT
---
# Text to Lottie

The deliverable is a Lottie JSON plus a previewable scene, not just a file. The rules below assume a Skottie-based player (Skia's Skottie module): slots, the properties panel and the `?frame=` controls only hold in that runtime.

## When to use
- Create, edit, fix or preview a Lottie (Bodymovin) animation.
- Not for HTML or React compositions (`hyperframes`) and not for choosing easing in UI (`animate`).

## Set up the player
Use the official player project, never a hand-rolled viewer: a custom page or a different renderer diverges, and the verification below will not apply. If it is not already present:

```bash
npx degit diffusionstudio/lottie my-animation
cd my-animation
npm install   # postinstall copies the CanvasKit wasm into /public
npm run dev   # serves http://localhost:3030
```

If it exists, run `npm install && npm run dev`. Open the printed local URL.

## Layout the scanner enforces
```
public/
  canvaskit.wasm                 # Skia wasm, from postinstall
  projects/
    <project-slug>/
      <scene-N>/
        lottie.json              # required
        controls.json            # optional, properties-panel metadata
        <images>                 # .png .jpg .jpeg .webp .gif .svg
```
- Slugs become the URL path `/<project>/<scene>`; the sidebar label is the slug title-cased.
- Scene order is the trailing number in the slug (`/-(\d+)$/`). Name new scenes `scene-<N>`; a slug with no number sorts last.
- A scene folder without `lottie.json` is dropped; a project with no valid scene disappears.
- Images are referenced by bare filename in `assets[].p` and resolved from the same folder.
- The watcher live-updates the tree on folder changes. Editing a `lottie.json`'s contents does not reload the active scene; reload the page.

## Write the file
Write to `public/projects/<project>/<scene-N>/lottie.json`. Re-read from disk before editing: the UI writes control changes back over HTTP, so an earlier copy may be stale. A new scene gets the next `scene-<N>` index so existing work is not clobbered. Give the document a root `nm` string; the player shows it as a label.

## Slots and the properties panel
A slot makes a value editable live with no re-parse. Declare a top-level `slots` map keyed by slot id, point the property at it with `sid`, and put the default in the slot's `p`.

| Slot value | Control |
|---|---|
| scalar | slider |
| colour, RGBA 0 to 1 | colour picker |
| vec2 `[x, y]` | two number inputs |
| string | text input |

Every animation must expose at least one control for the background colour. The panel appears as soon as one slot exists; slots are discovered automatically, so list them nowhere else. Add labels and slider ranges in `controls.json` next to `lottie.json`: `sid` must match a slot id, and `min`, `max` and `step` shape scalars and vec2 (ignored for colour and text). The full example `lottie.json` and `controls.json` are in references/lottie-json.md.

## Verify
- Valid JSON, no comments and no trailing commas: `node -e "JSON.parse(require('fs').readFileSync('public/projects/<project>/<scene-N>/lottie.json','utf8'))"`.
- Read the dev server context: `curl -s http://localhost:3030/__context` returns the project tree, the active scene, and live playback state including the current frame and total frames. Use it instead of guessing from screenshots.
- Pin a frame to seek and pause for inspection: `http://localhost:3030/<project>/<scene>?frame=60`. Navigate or reload to change frames; the canvas is `<canvas id="main-canvas">`. A blank canvas with no error usually means the group wrapping is wrong.
- New scene: screenshot frame `0`, `op/2` and `op-1` to catch start, mid-motion and end pose. Small edit: one or two frames around the change.
- Hunt for artifacts, not only prompt fidelity: the result must look clean, intentional and production-ready.

## Best practices
- Use real easings; linear is usually wrong. Consider pacing, transitions and continuity.
- For procedural animations, generate the JSON from a script; for targeted changes, edit the JSON directly.

## Checklist
- [ ] File at `public/projects/<project>/<scene-N>/lottie.json`; scene named `scene-<N>`
- [ ] JSON valid and `nm` set
- [ ] Official player project, dev server running, scene visible
- [ ] At least one slot, including the background colour
- [ ] Frames 0, op/2 and op-1 verified
- [ ] Saved path and prompt recorded
