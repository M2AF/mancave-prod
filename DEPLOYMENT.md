# Mancave home base

Public hostname: https://mancave.chainlensnft.info/#home

The existing static site in `site/` is the home base for ChainLens, Magic Money Wallet, AfterGlow, and ChainLens Arcade. Only `site/` is published; project briefs, agent files and reports stay outside the hosting output.

Cloudflare Pages is used because it supports a custom subdomain with DNS hosted by Unstoppable Domains. The root domain and existing ChainLens Render service stay as they are.

## Publish

```powershell
npx --yes wrangler@4.136.1 pages deploy site --project-name mancave-productions --branch main
```

This is a direct-upload project. GitHub pushes alone do not deploy it. Sign in to the intended Cloudflare account before publishing.

## DNS

First associate `mancave.chainlensnft.info` with the Pages project. Then add this DNS record in Unstoppable Domains:

| Type | Host/name | Target | TTL |
| --- | --- | --- | --- |
| CNAME | mancave | mancave-productions.pages.dev | Default |

Do not change nameservers or the existing root/`www` records. HTTPS certificate activation follows domain validation. Until DNS is added and HTTPS is active, the custom hostname is not live.

Cloudflare instructions: https://developers.cloudflare.com/pages/configuration/custom-domains/

ChainLens's Back to home links point to `https://mancave.chainlensnft.info/#home` in the same tab, above the desktop sidebar logo and at the upper left on mobile.

Published preview: https://mancave-productions.pages.dev/#home (deployment 7670b619). Custom domain is active: Unstoppable CNAME verified, Cloudflare domain and certificate active, HTTPS200 and all five views verified on 2026-11-02. Verified locally with 324 browser assertions and on the published site at desktop/mobile widths.
