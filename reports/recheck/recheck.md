# Site recheck after fixes

**Verdict: five original defects PASS; functional checks PASS (324/324). One remaining design-spacing issue FAIL: desktop Arcade row gaps.**

Run: 2026-11-02T03:46:03.312Z. Chromium 156.0.8078.4, Playwright 1.64.1, headless, CSS pixels, viewport height 900 and device scale factor 1. Used only the existing Playwright at C:/Users/balla/Documents/agent-office/node_modules/playwright; installed nothing. All writes stayed under reports/recheck/. No commits. The protected-folder SHA-256 manifests in results.json match before/after. Earlier reports, site/, content/ and brief/ were not edited. The handoff board was read (owner none); it was left unchanged to respect the output-only scope.

## Five defect results

| Defect | Result | Current evidence |
|---|---|---|
| 1. Home DUO / Swarm HTML labels | PASS | Both names are visible figcaptions below their respective artwork at 1440, 1024, 768, 390 and 320; [Home 320](visual-320-home.png), [Home 1024](visual-1024-home.png). |
| 2. Phone 24px and tablet 32px gaps | PASS | Phone hero, product-index, game-grid and feature-list rules use 24px; 768px Home product and Arcade game rows measure 32px. Screenshots show the tighter rhythm. [Measurements](visual-measurements.json), [Home 390](visual-390-home.png), [Arcade 768](visual-768-arcade.png). Desktop spacing exception recorded separately below. |
| 3. Compact Magic Money icon + full HTML identity | PASS | Home heading is Magic Money Wallet. Dedicated 768/390/320 treatment pairs a 56px icon with a readable 24px HTML title before the main heading; fits even at 320. [Magic Money 320](visual-320-magic-money.png), [Home 768](visual-768-home.png). Navigation retains Magic Money. |
| 4. Magic Money heading order at 768 | PASS | Single-column hero puts icon/title and main heading above the introduction and actions; no empty upper-left column. [Magic Money 768](visual-768-magic-money.png). |
| 5. Wordmark reserved for >=1024 | PASS | PNG display is none at 768/390/320, visible at 1024+. Actual image widths: 928px at 1024, 960px at 1056, 999px at 1095, 1000px at 1440. Personally inspected the outlined lettering: readable at all three boundary samples, with intact source proportions. [1024 crop](wordmark-1024.png), [1056 crop](wordmark-1056.png), [1095 crop](wordmark-1095.png). |

## Functional checks

All five views (Home, ChainLens, Magic Money, AfterGlow, Arcade) passed at each of 1440, 768, 390 and 320: 20/20 view-width cases. Reused the existing reports/tests/run-tests.cjs harness by copying it into this folder; did not run it in its original output directory.

| Check | Result | Passed / cases |
|---|---|---:|
| Tab semantics and selection | PASS | 20/20 |
| Inactive panels excluded | PASS | 20/20 |
| Keyboard arrows/wrap/Home/End/Enter/Space | PASS | 20/20 |
| Skip link | PASS | 20/20 |
| Focus rings | PASS | 20/20 |
| Tap targets >=44px | PASS | 20/20 |
| Keyboard tab order isolation | PASS | 20/20 |
| No horizontal overflow | PASS | 20/20 |
| No broken images | PASS | 20/20 |
| Deep links and back/forward | PASS | 20/20 |
| Reduced motion | PASS | 20/20 |
| No console/page errors | PASS | 20/20 |
| Loopback-only requests | PASS | 20/20 |
| No HTTP errors or failed requests | PASS | 20/20 |
| JavaScript disabled: content and header anchors | PASS | 20/20 |
| JavaScript disabled: overflow/network/images | PASS | 20/20 |
| Exact outbound links | PASS | 1/1 |
| AfterGlow has no link/button | PASS | 1/1 |
| DUO Arcade exactly once beside Play | PASS | 1/1 |
| Protected files unchanged | PASS | 1/1 |

Detailed assertions and evidence: [results.json](results.json), [network log](requests.json), [environment](environment.json), [copied harness](run-tests.cjs), [generated functional report and per-view matrix](test-pass.md).

- ARIA reciprocation, selected state, roving tabindex, hidden-panel accessibility-tree exclusion and failed focus into hidden panels all passed. Actual keyboard events cover arrows, both wrap directions, Home/End, Enter/Space, skip link, Tab isolation, deep links and Back/Forward.
- All visible links/buttons measure at least 44 by 44 CSS px. All checked controls have keyboard focus-visible outlines >=2px; representative light/dark screenshots personally reviewed: [phone Home focus](320-home-action-focus.png), [tablet wallet focus](768-magic-money-action-focus.png). This is not a formal focus contrast certification.
- Zero page/console errors, external requests, HTTP >=400 responses or failed requests in the functional matrix. Every visible image loaded with nonzero natural dimensions. JS-off fallback exposes all five views, each header anchor navigates to its panel, with no overflow or broken images. Reduced-motion styles and running animations passed.
- Exact raw outbound href set: https://www.chainlensnft.info ; https://github.com/M2AF/Magic-Money-Wallet ; https://github.com/M2AF/Magic-Money-Wallet/releases/latest ; https://duo.magicmoney.dev ; https://discord.gg/26uxjad8uT . Discord occurs in Home and footer. Destinations were inspected, never fetched.
- AfterGlow content has zero anchors/buttons or link/button roles; shared navigation/footer are excluded from that assertion.
- Recursive case-insensitive source search over every file in site/ found DUO Arcade exactly once, in site/index.html line 345, in the Play action container. See the exact recorded line in results.json if source line numbering changes. rg is unavailable; the harness uses /duo arcade/gi over all source files.

## Visual regression checks and remaining issue

**FAIL — desktop Arcade row spacing, low priority.** At 1024px, .game-grid measures row-gap 64px and column-gap 48px. The 1024–1439 layout direction specifies 48px gaps. The first row ends at y=1109.67 and the second starts at y=1173.67, confirming an actual 64px separation. At 1440 the same 64px row gap persists (row one bottom 1029.66, row two start 1093.66). It looks orderly, with no collision, but the 1024px measurement misses the stated spacing target. [Arcade 1024](visual-1024-arcade.png), [Arcade 1440](visual-1440-arcade.png), [measured geometry](visual-measurements.json). The same desktop 64px row-gap rule is present on Home product-index; its 1024px grid also differs from the 48px table target. This desktop discrepancy is separate from the resolved phone/tablet defect.

**PASS — clipping, overlap, alignment and media:** personally opened full-page Home and Magic Money captures at every requested width (1440/1024/768/390/320), Arcade and AfterGlow at 768/320, plus Arcade 1024/1440 and three wordmark crops. No clipped text/control, overlapping visible artwork, unintentional misalignment or persistent blank media found. At 1024 the wallet retains the existing bottom-aligned desktop columns; the heading-first tablet correction works at 768. Wordmark thin strokes remain stylistically fine but readable at the tested boundary samples. Blue/amber panel borders in the visual captures are the focused panel outline from fragment navigation.

Initial fast visual captures showed several blank Arcade logos despite complete images and nonzero natural dimensions. The functional screenshots rendered all six correctly. Refreshed visual captures with explicit image.decode() and a 250ms paint wait; personally reopened Arcade 768/320 and confirmed Pool, Clash and World all render. This was a screenshot readiness issue, not a persistent missing asset. The final files linked here contain the complete artwork.

Fact-removal spot check: AfterMarket is now a name-only heading; the previously flagged onchain/EVM/public-address/passkey definitions and key-to-everything phrase are absent. This was a targeted removal check, not a new full fact audit.

## Screenshot inventory

- Home: [1440](visual-1440-home.png), [1024](visual-1024-home.png), [768](visual-768-home.png), [390](visual-390-home.png), [320](visual-320-home.png).
- Magic Money: [1440](visual-1440-magic-money.png), [1024](visual-1024-magic-money.png), [768](visual-768-magic-money.png), [390](visual-390-magic-money.png), [320](visual-320-magic-money.png).
- Arcade: [768](visual-768-arcade.png), [320](visual-320-arcade.png), plus desktop evidence above.
- AfterGlow: [768](visual-768-afterglow.png), [320](visual-320-afterglow.png).
- Other functional, JS-off and focus captures are alongside this report. [Visual capture script](visual.cjs).

## Could not test / boundaries

Chromium only. No Firefox/WebKit, physical touch device, OS screen reader/manual spoken output, production hosting, browser-extension behavior, external destination availability, formal contrast audit, or zoom/text-scaling audit. Wordmark boundary review samples 1024/1056/1095px, not every intermediate pixel. CSS >=1024 desktop row behavior was measured at 1024/1440, not every width. No deployment or real wallet operation was attempted. Both browser jobs and their loopback servers have closed.
