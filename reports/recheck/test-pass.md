# Static site test pass

Run: 2026-11-02T03:47:13.103Z. Chromium headless; widths 1440, 768, 390, 320 CSS px, viewport height 900. Existing Playwright installation only. Loopback server: http://127.0.0.1:59577.

## Check summary

| Check | Result | Cases |
|---|---|---|
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

## Per-view / width matrix

| View | Width | Result | Failures |
|---|---:|---|---|
| home | 1440 | PASS | None |
| chainlens | 1440 | PASS | None |
| magic-money | 1440 | PASS | None |
| afterglow | 1440 | PASS | None |
| arcade | 1440 | PASS | None |
| home | 768 | PASS | None |
| chainlens | 768 | PASS | None |
| magic-money | 768 | PASS | None |
| afterglow | 768 | PASS | None |
| arcade | 768 | PASS | None |
| home | 390 | PASS | None |
| chainlens | 390 | PASS | None |
| magic-money | 390 | PASS | None |
| afterglow | 390 | PASS | None |
| arcade | 390 | PASS | None |
| home | 320 | PASS | None |
| chainlens | 320 | PASS | None |
| magic-money | 320 | PASS | None |
| afterglow | 320 | PASS | None |
| arcade | 320 | PASS | None |

## Failures


## Evidence and scope

- Detailed assertions and measured evidence: [results.json](results.json). HTTP response log: [requests.json](requests.json). Browser/version/time: [environment.json](environment.json). Re-run with `node reports/tests/run-tests.cjs`.
- Full-page screenshots: `<width>-<view>.png`; skip-focus and action-focus screenshots also saved for every applicable combination. No-JavaScript full-page screenshots: `<width>-no-javascript.png`.
- Tabs tested with real key events, automatic selection, both wrap directions, Home/End, Enter/Space; actual Tab traversal confirms one tab stop. CDP accessibility inspection confirms inactive panels are ignored; focus attempts into hidden panels fail.
- All visible links/buttons measured and checked in keyboard focus mode for a >=2px non-none focus outline. View panels and main use the same global focus rule; focus screenshots require visual review.
- All five panels render together without JavaScript. Every fallback header link tested at each width. Lazy images scrolled into view before checking load completion. Reduced-motion computed styles checked including pseudo-elements, plus running animation inspection after hover/focus.
- Outbound URLs inspected only; never followed. A route guard blocks unexpected external requests and records them as failures.
- No dependencies installed and no commits made. Protected folder file hashes compared before/after.

## Not tested / limitations

- Chromium only: Firefox, WebKit, physical touch devices, operating-system assistive technology and manual screen-reader output were not tested. Accessibility-tree results are Chromium CDP evidence.
- Target-size measurements use CSS pixels at device scale factor 1. Focus checks combine computed outlines with screenshot review; they are not a formal contrast audit. External site availability intentionally not tested.
- History tested by clicking tabs then Back/Forward for every starting view and width. No browser-extension or production-host behavior is implied.
