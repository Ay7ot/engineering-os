# gstack command catalogue

`$B` is the resolved browse binary. Commands are grouped as the CLI reports
them; run `$B status` for a health check and `$B stop` to shut the server down.

## Navigation and tabs

| Command | Description |
|---|---|
| `goto <url>` | navigate (http, https, or file within the allowed dirs) |
| `back` / `forward` / `reload` | history and reload |
| `url` | print the current URL |
| `load-html <file>` | load HTML content directly |
| `newtab [url]` / `tab <id>` / `tabs` / `closetab [id]` | tab control |
| `tab-each <command>` | run one command on every open tab |

## Reading

| Command | Description |
|---|---|
| `snapshot [flags]` | accessibility tree with refs |
| `accessibility` | full ARIA tree |
| `text` | cleaned page text |
| `html [selector]` | element or full page HTML |
| `links` | links as text and href |
| `forms` | form fields as JSON |
| `data [--jsonld|--og|--meta|--twitter]` | structured data |
| `media [--images|--videos|--audio]` | media elements and URLs |
| `console [--errors]` / `network` / `perf` | console, requests, timings |
| `cookies` / `storage` | cookies and web storage |
| `ux-audit` | page structure as JSON for UX analysis |

## Snapshot flags

| Flag | Meaning |
|---|---|
| `-i` | interactive elements only, with `@e` refs (enables cursor scan) |
| `-C` | cursor-interactive elements as `@c` refs (clickable divs) |
| `-c` | compact, drop empty structural nodes |
| `-d <N>` | limit tree depth |
| `-s <sel>` | scope to a CSS selector |
| `-D` | unified diff against the previous snapshot |
| `-a` | annotated screenshot with boxes and ref labels |
| `-o <path>` | output path for the annotated screenshot |
| `-H <json>` | heatmap overlay, for example `{"@e1":"green","@e3":"red"}` |

## Interaction

| Command | Description |
|---|---|
| `click <sel>` / `hover <sel>` | click or hover |
| `fill <sel> <val>` / `type <text>` | set or type text |
| `select <sel> <val>` | choose a dropdown option |
| `press <key>` | keyboard key, for example `Enter`, `Shift+Enter` |
| `scroll [sel]` / `wait <sel>` | scroll into view, wait for element or network idle |
| `upload <sel> <file>` | upload files |
| `dialog-accept [text]` / `dialog-dismiss` | pre-arm dialog handling |
| `cookie <name>=<value>` / `cookie-import <json>` / `cookie-import-browser` | cookie setup |
| `header <name>:<value>` | extra request header |
| `viewport <WxH>` / `useragent <string>` | viewport and user agent |
| `cleanup [--ads|--cookies|--all]` | strip page clutter |

## Inspection and assertions

| Command | Description |
|---|---|
| `is <prop> <sel|@ref>` | `visible`, `hidden`, `enabled`, `disabled`, `checked`, `editable`, `focused` |
| `attrs <sel|@ref>` | attributes as JSON |
| `css <sel> <prop>` | computed style |
| `inspect [selector]` | CSS cascade and box model |
| `js <expr>` / `eval <file>` | run JavaScript in the page |
| `cdp <Domain.method> [params]` | raw DevTools call, limited to an allowlist |

## Visual and capture

| Command | Description |
|---|---|
| `screenshot [--selector s] [--clip x,y,w,h] [--viewport] [path]` | screenshot |
| `prettyscreenshot [--cleanup] [--hide sel] [path]` | clean screenshot |
| `responsive [prefix]` | mobile, tablet and desktop screenshots |
| `pdf [path] [--format a4]` | page to PDF |
| `diff <url1> <url2>` | text diff between pages |
| `archive [path]` | complete page as MHTML |
| `download <url|@ref> [path]` | download using browser cookies |
| `scrape <images|videos|media>` | bulk media download with a manifest |

## Sessions, chaining and servers

| Command | Description |
|---|---|
| `chain` | run a JSON array of commands from stdin, stopping at the first error |
| `state save|load <name>` | persist cookies and URLs |
| `connect` / `disconnect` / `handoff` / `resume` | headed takeover for the user |
| `watch [stop]` | periodic snapshots while the user browses |
| `status` / `stop` / `restart` | health check and lifecycle |
| `frame <sel|main>` | switch iframe context |
| `domain-skill <save|list|show|edit|rm>` | per-site notes the agent keeps |

## Practical tips

1. Navigate once, query many times.
2. Start with `snapshot -i` and act by ref.
3. Use `snapshot -D` after each action to see exactly what changed.
4. Prefer `is` assertions over parsing page text.
5. Use `snapshot -a` when a bug report needs an annotated screenshot.
6. Use `snapshot -C` when a clickable element is missing from the tree.
7. Check `console` after interactions to catch silent JS errors.
8. Use `chain` for long flows to avoid per-step overhead.
