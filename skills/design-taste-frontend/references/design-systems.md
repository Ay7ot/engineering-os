# Design Systems: Foundation Map, Installs, Sources

When the brief reads as one of these, install the official package and use it.
Do not recreate its CSS by hand, and do not import its tokens then override most
of them. One system per project.

| Brief reads as | Reach for |
|---|---|
| Microsoft, enterprise SaaS, dashboards | `@fluentui/react-components` or `@fluentui/web-components` |
| Google-like product, Material-flavoured | `@material/web` plus Material 3 tokens |
| IBM-style B2B, enterprise analytics | `@carbon/react` plus `@carbon/styles` |
| Shopify app surfaces | Polaris web components or Polaris React |
| Atlassian, Jira-style product | `@atlaskit/*` plus `@atlaskit/tokens` |
| GitHub-style devtool or community page | `@primer/css` or `@primer/react-brand` |
| UK public-sector service | `govuk-frontend` |
| US public-sector, trust-first | `uswds` |
| Fast local-business or agency MVP | Bootstrap 5.3 |
| Modern accessible React foundation | `@radix-ui/themes` |
| Modern SaaS where you own the components | shadcn/ui (see `shadcn`) |
| Tailwind-based modern SaaS or AI marketing | Tailwind v4 utilities (see `tailwind-design-system`) |

## Install commands

```bash
npm install @fluentui/react-components           # Fluent UI React v9
npm install @fluentui/web-components @fluentui/tokens
npm install @material/web                        # Material 3
npm install @carbon/react @carbon/styles         # IBM Carbon
npm install @radix-ui/themes
npx shadcn@latest init                           # shadcn/ui
npm install --save @primer/css                   # Primer product UI
npm install @primer/react-brand                  # Primer marketing UI
npm install govuk-frontend
npm install uswds
npm install bootstrap
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/card
```

Shopify Polaris web components are added per app in the document head:

```html
<meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
<script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## Canonical sources
Read these before reinventing anything in this area.

- Fluent UI: https://fluent2.microsoft.design/get-started/develop and
  https://learn.microsoft.com/en-us/fluent-ui/web-components/
- Material: https://m3.material.io/develop/web and
  https://material-web.dev/theming/material-theming/
- Carbon: https://carbondesignsystem.com/
- Polaris: https://shopify.dev/docs/api/app-home/web-components
- Atlassian: https://atlassian.design/get-started/develop and
  https://atlassian.design/tokens/design-tokens
- Primer: https://primer.style/ and https://github.com/primer/brand
- GOV.UK: https://design-system.service.gov.uk/components/button/
- USWDS: https://designsystem.digital.gov/documentation/developers/
- Bootstrap: https://getbootstrap.com/docs/5.3/layout/grid/
- Tailwind: https://tailwindcss.com/docs/dark-mode and
  https://tailwindcss.com/blog/tailwindcss-v4
- Radix Themes: https://www.radix-ui.com/themes/docs/components/theme
- shadcn/ui: https://ui.shadcn.com/docs
- Native CSS and standards:
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
  and https://drafts.csswg.org/scroll-animations-1/
- Apple Liquid Glass (Apple platforms only):
  https://developer.apple.com/design/human-interface-guidelines/materials

## Aesthetic briefs with no official package
Glassmorphism, bento, brutalism, editorial, dark tech, aurora and mesh
gradients, kinetic typography. Build with native CSS, Tailwind and a maintained
component library. Say in a comment which part is borrowed inspiration.

For glass: go beyond `backdrop-filter` with a 1px inner border and an inner
highlight, and provide a solid-fill fallback under
`prefers-reduced-transparency: reduce`. Note that this media feature has uneven
support, so keep contrast sufficient even without blur. Apple documents Liquid
Glass for Apple platforms only; there is no official web CSS package, so label
any web implementation as an approximation.
