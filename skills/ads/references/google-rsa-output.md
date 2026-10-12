# Google responsive search ad output contract

Apply this whenever the request is for Google responsive search ads. Do not ship a partial or malformed ad.

## Hard limits per ad

- Headlines: exactly 15, each 30 characters or fewer, counting spaces. Print the count beside each, for example `1. Ship Reports Faster (19 chars)`.
- Descriptions: exactly 4, each 90 characters or fewer.
- Paths: up to 2, each 15 characters or fewer.
- Final URL: present, https.
- Pinning: state any pinned positions explicitly; the default is unpinned unless the user asks.
- Guardrail: Google allows at most 3 responsive search ads per ad group. When more than 3 are requested, group them by ad group.

## Required sidecar artifacts

1. Ad group structure, labelled `Ad group structure:`: each ad group with its theme, target keywords and match types, and which ads map to it.
2. Negative keywords, labelled `Negative keywords:`: at least 8 entries, with group-level versus campaign-level called out.
3. Sitelinks, at least 4, each with title (25 characters), two description lines (35 characters each) and a URL.
4. Callouts, at least 4, each 25 characters or fewer.
5. Structured snippets where relevant.

## Compliance

Check the product context for regulated categories. Where a regulator forbids them, remove superlatives (`#1`, "best", "leading", "top", "reference") and outcome promises ("guaranteed", "cure", "100 percent", "pain free"), and avoid comparative claims against named competitors. Use neutral framing instead. Include a geographic qualifier where the offer is region-specific.

## Output order

Emit in this order so the most required sections survive any truncation:

1. Ad group structure.
2. Negative keywords (at least 8, before the ads).
3. Sitelinks.
4. Callouts.
5. The ads, last.

## Template

```
Ad group structure:
- AG1 [theme]: keywords (match types) -> RSA1, RSA2

Negative keywords:
  Campaign-level:
    - <keyword> (at least 4)
  Ad-group level:
    - AG1: <keyword>, <keyword> (at least 4 more, 8 total)

Sitelinks (at least 4):
  - <title, 25 max> | <description 1, 35 max> | <description 2, 35 max> | URL

Callouts (at least 4, 25 max each):
  - <callout>

RSA1, [ad group name]
  Final URL: https://...
  Path1: ...   Path2: ...
  Headlines (15, 30 max each):
    1. <headline> (NN chars)
    ...
    15. <headline> (NN chars)
  Descriptions (4, 90 max each):
    1. <description> (NN chars)
    ...
    4. <description> (NN chars)
  Pinning: H1=none; H2=none; ...

RSA2 ...
RSA3 ...
```

## Self-check before responding

- [ ] Each ad has exactly 15 headlines and exactly 4 descriptions
- [ ] Every headline is 30 characters or fewer and every description 90 or fewer, with counts printed
- [ ] Negative keyword list labelled with at least 8 entries
- [ ] Ad group structure labelled
- [ ] Sitelinks and callouts present, within their limits
- [ ] Compliance restrictions checked for the product category
- [ ] If any check fails, rewrite before responding
