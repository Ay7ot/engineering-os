# just-scrape command reference

Run `just-scrape --help` or `just-scrape <command> --help` for the option list
of the installed version.

## search

```bash
just-scrape search "query"
just-scrape search "query" --num-results 10
just-scrape search "query" -p "Extract provider names and prices"
just-scrape search "query" -p "..." --schema '<json-schema>'
just-scrape search "query" --format html
just-scrape search "query" --country us
just-scrape search "query" --time-range past_week
```

Time ranges: `past_hour`, `past_24_hours`, `past_week`, `past_month`,
`past_year`.

## scrape

```bash
just-scrape scrape "<url>"
just-scrape scrape "<url>" -f markdown
just-scrape scrape "<url>" -f markdown,html,links --json
just-scrape scrape "<url>" -f screenshot
just-scrape scrape "<url>" -f branding
just-scrape scrape "<url>" -f json -p "Extract all products"
just-scrape scrape "<url>" --html-mode reader
just-scrape scrape "<url>" --mode js --stealth --scrolls 5
just-scrape scrape "<url>" --country DE
```

Formats: `markdown`, `html`, `screenshot`, `branding`, `links`, `images`,
`summary`, `json`.

## extract

```bash
just-scrape extract "<url>" -p "Extract product names and prices"
just-scrape extract "<url>" -p "..." --schema '<json-schema>'
just-scrape extract "<url>" -p "Extract visible items" --scrolls 5
just-scrape extract "<url>" -p "..." --html-mode reader
just-scrape extract "<url>" -p "..." --country DE
```

`--cookies` and `--headers` accept JSON; pass them from environment variables,
for example `--headers "{\"Authorization\":\"Bearer $API_TOKEN\"}"`.

## crawl

```bash
just-scrape crawl "<url>"
just-scrape crawl "<url>" -f markdown,links
just-scrape crawl "<url>" --max-pages 50 --max-depth 3
just-scrape crawl "<url>" --max-links-per-page 20
just-scrape crawl "<url>" --allow-external
just-scrape crawl "<url>" --include-patterns '["^https://example\\.com/docs/.*"]'
just-scrape crawl "<url>" --exclude-patterns '[".*\\.pdf$"]'
```

## monitor

```bash
just-scrape monitor create --url "<url>" --interval 1h --name "Pricing tracker" -f markdown
just-scrape monitor create --url "<url>" --interval "0 * * * *" --webhook-url "$WEBHOOK_URL"
just-scrape monitor list
just-scrape monitor get --id <cronId>
just-scrape monitor update --id <cronId> --interval 30m
just-scrape monitor activity --id <cronId> --limit 50
just-scrape monitor pause --id <cronId>
just-scrape monitor resume --id <cronId>
just-scrape monitor delete --id <cronId>
```

Intervals accept cron expressions or shorthands such as `30m`, `1h`, `1d`.

## history, credits, validate

```bash
just-scrape history
just-scrape history scrape
just-scrape history extract --json
just-scrape history crawl --page-size 100 --json
just-scrape history scrape <request-id> --json
just-scrape credits --json
just-scrape validate --json
```

History services: `scrape`, `extract`, `search`, `crawl`, `monitor`.

## Reading results

```bash
wc -c .just-scrape/file.json && head -c 5000 .just-scrape/file.json
rg -n "keyword" .just-scrape/file.json
jq '.request_id // .id // .status' .just-scrape/file.json
jq -r '.. | objects | .url? // empty' .just-scrape/search.json
jq -r '.. | objects | select(has("status")) | .status' .just-scrape/crawl.json
```

Suggested naming:

```text
.just-scrape/search-{query}.json
.just-scrape/{site}-{path}-scrape.json
.just-scrape/{site}-{path}-extract.json
.just-scrape/{site}-{section}-crawl.json
.just-scrape/monitor-{name}.json
```

## Environment variables

| Variable | Meaning | Default |
|---|---|---|
| `SGAI_API_KEY` | ScrapeGraph API key | none |
| `SGAI_API_URL` | API base URL override | `https://v2-api.scrapegraphai.com` |
| `SGAI_TIMEOUT` | request timeout | `120` |
| `SGAI_DEBUG` | debug logs to stderr | `0` |

Legacy aliases are bridged: `JUST_SCRAPE_API_URL`, `JUST_SCRAPE_TIMEOUT_S` and
`SGAI_TIMEOUT_S`, `JUST_SCRAPE_DEBUG`.

## Worked examples

```bash
just-scrape search "query" --num-results 10
just-scrape search "query" -p "Extract provider names and prices"
just-scrape scrape "<url>" -f markdown,html,links --json
just-scrape scrape "<url>" --mode js --stealth --scrolls 5
just-scrape extract "<url>" -p "Extract product names and prices" --schema '<json-schema>'
just-scrape crawl "<url>" --max-pages 50 --max-depth 3
just-scrape monitor create --url "<url>" --interval 1h --name "Pricing tracker"
```

## Troubleshooting

- CLI not found: install it, or run `npx just-scrape@latest`.
- Auth fails: set `SGAI_API_KEY`, then run `just-scrape validate`.
- Empty or partial page: retry with `--mode js`, then add `--stealth` or
  `--scrolls <n>`.
- Extraction is loose: add `--schema '<json-schema>'`.
- Crawl too broad: add `--max-pages`, `--max-depth` and include or exclude
  patterns.
- Need an earlier result: `just-scrape history <service> --json`.

## Parallel fetching

```bash
just-scrape credits --json > .just-scrape/credits-before.json
just-scrape scrape "<url-1>" --json > .just-scrape/1.json &
just-scrape scrape "<url-2>" --json > .just-scrape/2.json &
just-scrape scrape "<url-3>" --json > .just-scrape/3.json &
wait
```

Stealth, branding, JS rendering, large crawls and repeated extraction all cost
more credits than a plain fetch.
