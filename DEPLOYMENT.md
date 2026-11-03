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

Published preview: https://mancave-productions.pages.dev/#home (current deployment fc44e9f6, 2026-11-02; earlier 39337ba1, 7670b619). Custom domain is active: Unstoppable CNAME verified, Cloudflare domain and certificate active, HTTPS200 and all five views verified on 2026-11-02. Verified locally with 324 browser assertions and on the published site at desktop/mobile widths.

Arcade card published, 2026-11-02: deployment `39337ba1` (https://39337ba1.mancave-productions.pages.dev). Before publishing, all 15 `site/` files matched the tested gate hashes. Wrangler uploaded 2 changed files (13 already uploaded). Live verification passed on both `mancave.chainlensnft.info` and `mancave-productions.pages.dev` at 1440 and 390: six labelled game logos (DUO, Poker, Pool, Swarm, Clash, World), no ChainLens mark, all five views, no overflow, broken images, page errors or failed requests. That is 28/28 checks. Evidence: `.local-artifacts/arcade-20261102/deploy.log` and `live/` (results.json and screenshots).

Magic Money button fix published, 2026-11-02: deployment `fc44e9f6` (https://fc44e9f6.mancave-productions.pages.dev), commit `71e8939`. At >=1024px the wordmark image overlapped the Download latest release and View on GitHub buttons and took their clicks; `.wordmark img` now has `pointer-events: none`. Wrangler uploaded 1 changed file (14 already uploaded). Live click checks on both hosts at 1440, 1024, 768 and 390 confirmed each external button navigates to its FACTS.md URL, and `verify.cjs live` passed 28/28. Evidence: `.local-artifacts/links-20261102/` (deploy.log, results and screenshots).

Wrangler auth note: if `C:\Users\<user>\.wrangler\` exists, Wrangler uses it as its config directory. It then ignores the stored login in `%APPDATA%\xdg.config\.wrangler\config\default.toml` and fails in a non-interactive shell. Fix this without touching any credentials: run Wrangler with `USERPROFILE` and `HOME` pointed at an empty temporary directory, only for that process. Wrangler then reads the stored OAuth login and refreshes it itself.

Earlier blocked attempt (superseded by the publish above), 2026-11-02: no new deployment ID confirmed. The predecessor's `.local-artifacts/arcade-20261102/deploy.log` is absent. All 15 current `site/` files match the saved passing gate hashes (324 harness assertions and 28 targeted checks). The publish command above failed before Wrangler could run: npm registry access returned `EACCES`. Authentication lookup was not reached; no credentials were read or supplied. Both public home URLs at 1440 and 390 failed Chromium navigation with `ERR_NETWORK_ACCESS_DENIED`, so the six-game card, five live views, page errors and live screenshots remain unverified. The earlier deployment ID `7670b619` is historical, not a confirmation of this update. Evidence: `.local-artifacts/arcade-20261102/deploy-resume.log` and `resume-results.json`. Resume from a session with network access: check Pages deployment history first, deploy only if needed, then run `node .local-artifacts/arcade-20261102/verify.cjs live` and review the screenshots.
