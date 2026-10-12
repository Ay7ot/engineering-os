# Programmatic SEO playbooks

## The twelve playbooks

| Playbook | Pattern | Example |
|---|---|---|
| Templates | "[type] template" | "resume template" |
| Curation | "best [category]" | "best website builders" |
| Conversions | "[X] to [Y]" | "10 USD to GBP" |
| Comparisons | "[X] vs [Y]" | "webflow vs wordpress" |
| Examples | "[type] examples" | "landing page examples" |
| Locations | "[service] in [location]" | "dentists in austin" |
| Personas | "[product] for [audience]" | "crm for real estate" |
| Integrations | "[product A] [product B] integration" | "slack asana integration" |
| Glossary | "what is [term]" | "what is pSEO" |
| Translations | Content in several languages | Localised content |
| Directory | "[category] tools" | "ai copywriting tools" |
| Profiles | "[entity name]" | "stripe ceo" |

## Choosing one

| If you have | Consider |
|---|---|
| Proprietary data | Directories, profiles |
| A product with integrations | Integrations |
| A design or creative product | Templates, examples |
| A multi-segment audience | Personas |
| Local presence | Locations |
| A tool or utility product | Conversions |
| Content or expertise | Glossary, curation |
| A crowded competitor landscape | Comparisons |

Layer playbooks when they combine naturally, for example "best coworking spaces in San Diego".

## Keeping pages unique

- Build sections that only render when the underlying data supports them, so pages differ structurally, not just in wording.
- Add at least one original element per page: a computed statistic, a local note, a short analysis, or a comparison against a sibling entry.
- Pull user-generated or first-party content in where it exists; it is the hardest for competitors to copy.
- Refuse to generate a page whose data is empty or thin. Suppress it instead.

## Indexation strategy

- Submit high-volume, high-quality patterns first; let them index before adding long-tail tiers.
- `noindex` variations with no unique content or no meaningful demand, and keep them out of the sitemap.
- Split sitemaps by page type so indexation can be monitored per set.
- Watch crawl stats per set; a large failing set can drain crawl budget from the rest of the site.

## Common failure patterns

- Template that only interpolates a variable into an otherwise identical page.
- Several patterns accidentally targeting the same query, splitting internal signals.
- Generating the full combination space instead of the subset with demand.
- Launching without a hub, leaving spokes unreachable except via sitemap.
