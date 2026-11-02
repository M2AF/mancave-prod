# Static site visual review

**Verdict: needs fixes.** The shared shell, palette, logo backgrounds and responsive navigation are largely correct. Five issues remain: missing game names in the Home preview, phone spacing, incomplete compact Magic Money identity, the tablet Magic Money heading position, and tablet wordmark legibility. No clipped content, horizontal overflow, broken images or invented dashboard imagery was found in the 20 reviewed renders.

## Scope and evidence

Reviewed the rendered `site/` against `design/direction.md`, `brief/LOGOS.md` and `brief/FACTS.md`. Captured and personally opened **all 20 full-page screenshots** listed below, including every page's footer and all six Arcade games. Widths are CSS pixels; viewport height was 900px, device scale 1, reduced motion enabled. Chromium 156.0.8078.4 launched successfully in the sandbox using the existing Playwright at `C:/Users/balla/Documents/agent-office/node_modules/playwright`. Nothing was installed.

`capture.cjs` served only `site/` through a temporary `127.0.0.1` HTTP server, visited each hash view, scrolled through the entire page to trigger lazy loading, waited for visible images to decode, returned to the top and captured the page. Browser measurements are saved in [measurements.json](measurements.json). The browser and server were closed after capture. No external site, download or Discord destination was opened.

| View | 1440px | 768px | 390px | 320px |
|---|---|---|---|---|
| Home | [Reviewed](home-1440.png) | [Reviewed](home-768.png) | [Reviewed](home-390.png) | [Reviewed](home-320.png) |
| ChainLens | [Reviewed](chainlens-1440.png) | [Reviewed](chainlens-768.png) | [Reviewed](chainlens-390.png) | [Reviewed](chainlens-320.png) |
| Magic Money | [Reviewed](magic-money-1440.png) | [Reviewed](magic-money-768.png) | [Reviewed](magic-money-390.png) | [Reviewed](magic-money-320.png) |
| AfterGlow | [Reviewed](afterglow-1440.png) | [Reviewed](afterglow-768.png) | [Reviewed](afterglow-390.png) | [Reviewed](afterglow-320.png) |
| ChainLens Arcade | [Reviewed](arcade-1440.png) | [Reviewed](arcade-768.png) | [Reviewed](arcade-390.png) | [Reviewed](arcade-320.png) |

Deep links focus the tabpanel in this browser. The blue or amber outline around the full panel in these captures is its focus indicator; it is not a decorative panel border. It was retained during capture.

## Defects and suggested fixes

### 1. Home game preview has no individual HTML game names

**View / widths:** Home, 1440, 768, 390 and 320px. **Priority: medium.**

The ChainLens Arcade entry displays the ChainLens mark, DUO artwork and Swarm artwork, but the only HTML label is “ChainLens Arcade”. DUO and Swarm have no separate readable HTML names beside their logos. At 320px Swarm becomes particularly small. This falls short of the requirement that each depicted game have an HTML name alongside its artwork, even though the dedicated Arcade gallery does this correctly.

**Fix:** add HTML “DUO” and “Swarm” labels to the corresponding preview items and reflow the group at narrow widths, or simplify this product entry to the ChainLens inset and HTML Arcade name, leaving individual game artwork in the labelled gallery. Preserve complete source images.

**Evidence:** [Home 320](home-320.png), [Home 1440](home-1440.png), Arcade entry under “Our products”.

### 2. Phone group spacing exceeds the specified 24px gaps

**View / widths:** Home, ChainLens, Magic Money, AfterGlow and ChainLens Arcade at 390 and 320px. **Priority: low.**

The overall gutters and section padding are right, but content-group gaps are larger than the phone layout direction: Home product entries and Arcade game entries are separated by 48px; the ChainLens and AfterGlow copy-to-media gaps are 32px; feature lists use 32px; the Magic Money copy grid also uses 32px. The screenshots consequently have a looser, longer rhythm than the requested 24px phone gaps. At 768px the Home and Arcade grids also retain 48px row gaps, rather than the layout table's 32px tablet gaps.

**Fix:** set phone grid/group gaps to 1.5rem for `.hero`, `.product-index`, `.game-grid` and `.feature-list`; set tablet product/game row gaps to 2rem. Keep the existing 48px phone, 64px tablet and 96px desktop section padding. Intentional control spacing can stay distinct.

**Evidence:** [Home 390](home-390.png), [ChainLens 320](chainlens-320.png), [Magic Money 320](magic-money-320.png), [AfterGlow 390](afterglow-390.png), [Arcade 320](arcade-320.png); tablet row spacing is visible in [Home 768](home-768.png) and [Arcade 768](arcade-768.png).

### 3. Compact Magic Money treatment needs its full HTML identity grouped with the icon

**View / widths:** Home at 1440, 768, 390 and 320px; Magic Money at 390 and 320px. **Priority: low.**

Home correctly uses the supplied icon instead of a tiny wordmark, but its adjacent heading is only “Magic Money”; the specified compact title is “Magic Money Wallet”. On the dedicated phone view the full name exists as a 12px eyebrow and in the prose, while the 112px icon sits alone below both action buttons. The product remains identifiable, but this does not deliver the intended icon-plus-readable-HTML-title compact identity.

**Fix:** use “Magic Money Wallet” as the compact product heading, and group the phone icon with a readable HTML product title near the introduction. Retain the required “Magic Money” navigation label. Keep the original wordmark out of the phone treatment.

**Evidence:** [Home 390](home-390.png), [Magic Money 390](magic-money-390.png), [Magic Money 320](magic-money-320.png).

### 4. Tablet Magic Money hero puts its primary heading well below the introduction

**View / width:** Magic Money, 768px. **Priority: medium.**

The right column starts near the top of the section, while the left eyebrow and main heading sit much lower. Bottom alignment of unequal columns leaves a conspicuous empty upper-left area and causes the explanatory paragraph to be encountered visually before the primary heading. This is the weakest hierarchy among the five tablet views.

**Fix:** top-align the tablet `.hero--stacked` copy columns, or stack this hero at tablet width so the product heading comes first. Preserve the stronger wide-screen composition if desired.

**Evidence:** [Magic Money 768](magic-money-768.png), opening hero.

### 5. Tablet Magic Money wordmark is visibly weak

**View / width:** Magic Money, 768px. **Priority: medium.**

The PNG loads at 704 × 281.59px, including its substantial transparent margins. Its fine outlined letters are noticeably weaker than the surrounding HTML and the same artwork at the intended 1000px desktop image width. The background and aspect ratio are correct; this is a legibility issue, not a failed load or clipping. The direction specifically warns that theoretical white-on-dark contrast does not establish thin-stroke wordmark legibility.

**Fix:** keep the icon-plus-HTML identity through the tablet breakpoint and reserve the full PNG for a genuinely wide hero near the 1000px image target. Do not crop its transparent margins, thicken strokes or redraw the logo.

**Evidence:** compare [Magic Money 768](magic-money-768.png) with [Magic Money 1440](magic-money-1440.png).

## What looks right

- **Company-first shell:** the same white header, supplied blue company mark, readable company name and five peer navigation labels persist across all views. Broad sections and thin rules give the site the intended editorial character.
- **Palette and type:** rendered colours match the specified blue `#0033B9`, white, mist, ink, muted ink and product surfaces. System font stacks, heading sizes/weights/tracking, 16px body text, 15px semibold actions/nav, 14px captions and 12px mono labels follow the direction. No font download or substitute display face appeared.
- **Gutters and major layout:** at 1440px the centred 1280px container leaves 80px on each side, exceeding the 64px minimum; 768px uses 32px, and 390/320px use 16px. Home has two product columns at tablet/desktop and one on phones. The Arcade gallery moves from three columns to two to one. Phone media follows introductory copy.
- **Navigation:** desktop fits on one row; 768px wraps below the company row; both phone sizes fit all five labels on two rows without clipping or horizontal scrolling. Every captured selected tab computes to blue text, weight 600 and a 3px blue bottom rule. Targets measure at least 44px in each dimension. The header does not obscure content.
- **Company mark:** measured at 34.875 × 44px on desktop and 28.53125 × 36px on tablet/phones, preserving the derivative's 689:869 ratio. Header clearance exceeds one quarter of the visible mark width. There is no company mark in a dark section or hero, so the dark-context opaque white tile / 12px padding requirement and hero half-width clearspace are not exercised; no low-contrast direct-dark placement was found.
- **ChainLens:** the ring remains circular, complete and contained on exact `#000000`, including the Home preview and Arcade mark insets. No mismatched grey square or cropped edge appears.
- **Magic Money:** media stays on `#101827`. The 1440px hero PNG uses a 1000px image width with intact margins and original proportions. Both phone sizes load the supplied SVG icon rather than shrinking the wordmark. Swap/send qualifications by chain and route remain readable; no simulated unlock/connect UI or invented security claims appear.
- **AfterGlow:** all placements use `#F0EDF8`, with the entire black extrusion visible. None is on black. The HTML describes a local/private workspace and offers no invented public download action. Sparse violet/gold detail stays subordinate to the shared shell.
- **Arcade:** “ChainLens Arcade” is styled HTML next to the original ChainLens mark in a black inset. No new Arcade emblem is invented. In the dedicated gallery all six logos remain intact and have readable HTML game headings and descriptions. DUO retains both stacked colour variants; Poker retains its built-in margins; cue ends, Clash strokes and World foliage are contained. Poker and World have `#F0EDF8` insets; DUO, Pool, Swarm and Clash sit on `#101827`.
- **Home geometry:** `company-grid.svg` is used once, on the desktop Home hero, with its drawn geometry to the right of the copy. It is absent from the tablet/phone renders, product panels and other views; no logo or paragraph sits over the visible grid artwork.
- **Community and rename note:** Home has a clear Discord action in its Community section. The footer Discord link is underlined and wraps tidily, including the 320px layout. The single “DUO Arcade” note is readable immediately beside the Play button at 1440px and directly below it at smaller sizes, with white 14px text and a 16px action-group gap. It is clearly subordinate to the current Arcade name.
- **Contrast:** body/headings, muted footer copy, active navigation, white-on-blue actions, mint/cyan actions and violet labels use the direction's high-contrast pairs. No company-blue small functional text appears directly on a dark surface. Logo artwork retains its original colours; the thin wordmark issue is separately reported above. This is a visual/token review, not a full accessibility certification.
- **Rendering integrity:** every visible image decoded with nonzero natural dimensions, including the large Poker and AfterGlow PNGs. All 20 cases have document width equal to viewport width, no element outside the horizontal viewport, zero browser console/page/HTTP errors and zero external requests. Visual inspection found no overlapping text, clipped controls, blank media fields, decorative dashboards, fake screenshots, invented metrics, badges or testimonials.

## Boundaries

Only review artifacts were written under `reports/visual/`; `site/`, `content/` and `brief/` were not edited. No commit was made. Existing unrelated dirty files were left alone. The project memory index was read and contains no topics. The handoff board was read (`owner: none`); its helper could not run because the available `python.exe` is an inaccessible WindowsApps alias, so no handoff state was changed. This review covers the four requested widths in the local Chromium render; external destinations, other browsers, complete keyboard journeys and zoom/reflow beyond those widths are outside this pass.
