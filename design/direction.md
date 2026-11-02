# ManCave Productions — art direction

Design proposal for the first HTML/CSS/JS site. Product statements must come exclusively from `brief/FACTS.md`; logo permissions come from `brief/LOGOS.md`. This document defines presentation, not new company facts. No remote assets, fonts, tracking, forms, sign-in or wallet connection.

## The company comes first

Use a light, editorial company shell: clear typography, deliberate whitespace, strong alignment, a small blue company mark and a compact product navigation. ManCave Productions is the parent; the four products are peers in the navigation. Keep the company name and header constant across all five views. Home introduces that relationship and provides four product entries; it is not a wallet dashboard or game lobby.

Prefer a single strong heading, a short factual description and one relevant action per product. Use broad sections and thin rules rather than piles of rounded cards. Avoid decorative dashboards, fictitious screenshots, badges, testimonials, stock people, invented metrics and animated coin fields. Treat the supplied logos as the expressive artwork. Shared composition, typography and navigation provide the family resemblance.

## Measured palette

`node design/sample-logos.cjs` uses the existing Playwright installation at `C:/Users/balla/Documents/agent-office/node_modules/playwright`, starts a loopback server and decodes every supplied PNG and SVG in Chromium. It draws each image at its natural dimensions into an sRGB canvas, reads RGBA pixels, and counts exact RGB triplets for alpha >= 250. The chromatic histogram excludes pixels where max(R,G,B) - min(R,G,B) <= 60, removing the white matte and neutral colours. No resizing or colour quantisation is used. Counts, dimensions, SHA-256 hashes and extra hue samples are in `logo-samples.json`.

**Exact ManCave blue: `#0033B9` (RGB 0, 51, 185), 29,357 qualifying pixels.** It is the most frequent chromatic RGB triplet in the 1254 × 1254 source. The logo has several nearby blues; this is a measured representative token, not a claim that its artwork is flat colour. Keep those variations in the raster. Do not replace the logo with a CSS drawing.

| Token | Value | Role |
|---|---|---|
| Company blue | `#0033B9` | Active navigation, primary buttons, links on light surfaces |
| Paper | `#FFFFFF` | Main canvas, ManCave tile |
| Mist | `#F5F7FA` | Alternating sections, quiet geometry |
| Ink | `#182230` | Headings and body on light |
| Muted ink | `#526071` | Supporting copy on white/mist |
| Rule | `#DFE5ED` | Decorative separators only |
| Control edge | `#7A8799` | Essential outlines on white or dark; never small text |
| Dark surface | `#101827` | Magic Money and Arcade media fields |
| Black | `#000000` | ChainLens image panel; exact source backdrop match |
| Pale violet | `#F0EDF8` | AfterGlow, Poker and World logo insets |
| Focus amber | `#FFCE66` | Keyboard ring on dark surfaces; chosen UI colour, not a logo sample |

Product accent colours below are exact source pixel values, not suggested logo recolourings:

| Product/source | Sampled colours | Use outside the logo |
|---|---|---|
| ChainLens | `#000000` (692,224 pixels); `#E9E9E9` (147,700) | Monochrome panels; company blue remains its UI accent |
| Magic Money PNG | `#FFFFFF` (1,398); `#62FAD3` (3); `#2465F8` (3) | Mint details on dark; blue only for nonessential decoration on dark |
| Magic Money SVG, rasterised at 1000 × 1000 | `#2567FA` (223); `#5FFACD` (63) | Confirms blue/mint character; preserve the actual SVG gradient |
| AfterGlow | `#534ADE` (11,972); `#DEB766` (7,205) | Violet accent on white, warm gold as sparse decoration |
| Arcade / DUO | `#5CE1E6` (149,232); `#FFA7E4` (149,560); `#FF66C4` (6,964) | Cyan primary accent on dark, pink secondary detail |
| Poker | `#0C0059` (2,291,507); `#0094FF` (295,731); `#14C876` (194,342) | Retain within game artwork; avoid a second global palette |
| Pool | `#00C0FD` (193), `#00D5FE` (168) | Cyan glow already supplies its character |
| Swarm | `#0FB8CE` (142,042); `#580DA3` (56,851) | Cyan/purple confined to game identity |
| Clash | `#00F4FC` (610), `#FFFFFF` (10,943) | White outline and cyan stroke remain intact |
| World | `#5CE1E6` (191,142); `#0F3222` (93,078) | Cyan canopy lettering and deep green remain intact |

Gradient colours with small counts are literal pixel samples, not predominant flat fills. The sampler's optional hue categories simply choose the most frequent qualifying exact colour within each stated channel comparison; the complete rules are in its source. All interface colours still require suitable foreground/background pairings.

## Typography

No font downloads. System fonts provide the finish through proportion and spacing.

```css
:root {
  --font-heading: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  --font-body: system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", Consolas,
    "Liberation Mono", monospace;
}
```

| Style | Size | Leading / weight | Tracking |
|---|---|---|---|
| Display / one page h1 | `clamp(2.25rem, 1.25rem + 3vw, 4.5rem)` | 1.06 / 650 (600 fallback) | -0.035em |
| Section h2 | `clamp(1.75rem, 1.2rem + 1.5vw, 3rem)` | 1.15 / 650 | -0.025em |
| Item h3 | 1.5rem | 1.25 / 600 | -0.015em |
| Lead | `clamp(1.125rem, 1rem + .4vw, 1.375rem)` | 1.5 / 400 | normal |
| Body | 1rem | 1.6 / 400 | normal |
| Navigation / action | .9375rem | 1.4 / 600 | normal |
| Caption | .875rem | 1.5 / 400 | normal |
| Mono label | .75rem | 1.5 / 500 | .04em |

Use rems with a browser-default 16px root, never lock user text scaling. Reserve mono for small structural labels, not paragraphs or manufactured technical jargon. Sentence case; no stretched uppercase navigation. Keep body measures at 60–68ch and hero headings around 16–22ch. Limit lead copy to about 45ch. Use real headings and readable HTML product names alongside the logo images.

## Spacing and layout

Spacing tokens in pixels at the default root: **4, 8, 12, 16, 24, 32, 48, 64, 96, 128** (implement in rem). Use 8/12 within controls, 16/24 within content groups, 32/48 between groups, 64/96 between sections. Section vertical padding: 48px phone, 64px tablet, 96px desktop. Buttons have at least 44px block size. Corners: 4px for media panels, 6px for controls; use circles only where an existing mark requires them. No routine drop shadows.

| Viewport | Outer gutter | Content organisation |
|---|---|---|
| 320–479px | 16px | Single column; logo/media after introductory copy; 24px gaps |
| 480–767px | 24px | Single column; two compact entries only when labels fit comfortably |
| 768–1023px | 32px | Two-column product/index sections; 32px gaps |
| 1024–1439px | 48px | Twelve-column grid, 48px gaps; intro 5 columns and media 7 |
| 1440px and up | at least 64px | Centred container capped at 1280px; no indefinite text expansion |

Container: `width: min(1280px, calc(100% - 2 * var(--gutter))); margin-inline: auto`. Keep prose narrower than the container. Media may reach the container edge but never viewport overflow. Logos always use intrinsic aspect ratio, `object-fit: contain`, and uncropped source images (except the permitted new ManCave derivative). Allow space for built-in padding: Poker has substantial empty margins. Do not stretch that canvas to make letters fill a fixed square.

Company mark target height: 36px phone / 44px desktop with a readable HTML company name. Keep at least half the visible mark's width clear on all sides in hero placements; compact header spacing may be one quarter. In dark contexts put the mark on an opaque white tile with at least 12px padding. On the supplied source, the cleaned copy's aspect ratio is 689:869, not square.

## Navigation, selected state and focus

Five labels, in order: **Home, ChainLens, Magic Money, AfterGlow, ChainLens Arcade**. The same labels and positions persist across views. Use page links and `aria-current="page"` if each view is a document; for genuine in-page tabs use buttons with `role="tab"`, a labelled tablist, `aria-selected`, `aria-controls` and one roving tab stop. Implement Left/Right, Home/End and Enter/Space consistently. Do not apply tab roles to ordinary page links. Unselected panels must be hidden from keyboard and accessibility navigation.

White header, ink default labels; hover mist background and blue text. Selected tab has blue text, semibold weight and a 3px blue bottom rule, so colour alone does not identify it. Keep the header brand distinct from the product identity. On phones place all five labels in a separate wrapping nav below the company row (two or three rows as needed), with each target at least 44 × 44px and no clipped labels or horizontal scrolling. On desktop use one row when it fits, otherwise wrap before squeezing text. Avoid a sticky header in v1; it can obscure focused controls and costs phone space.

Primary action: white on company blue; secondary: blue on white with a visible edge. Underline body links. On dark product surfaces, use white body copy and mint/cyan for links, with underlines. Never put company-blue small text on dark. Do not use gold or pastel accents for small text on white. Essential control outlines use `#7A8799`; `#DFE5ED` is only a decorative rule.

```css
:focus-visible {
  outline: 3px solid #0033b9;
  outline-offset: 3px;
}
.surface-dark :focus-visible {
  outline-color: #ffce66;
}
@media (forced-colors: active) {
  :focus-visible { outline: 3px solid Highlight; }
}
```

Never remove focus. Leave at least 6px around targets for the ring; avoid clipping ancestors. On a blue button use a white 2px outer box-shadow separator under the blue outline; this separates the ring from the blue fill. Provide a visible-on-focus skip link to main content. Keep text selectable, link names explicit and image alternatives meaningful; use empty alt for a repeated decorative logo next to the same linked product name.

Calculated sRGB contrast ratios (`verification.json`, WCAG relative luminance formula):

| Pair | Ratio | Intended use |
|---|---|---|
| Blue / white | 9.66:1 | Text, primary button inverse, focus |
| Blue / mist | 9.00:1 | Text and focus |
| Ink / white | 16.03:1 | Body and headings |
| Muted ink / white; mist | 6.42:1; 5.98:1 | Supporting text |
| White / dark | 17.77:1 | Product text |
| Cyan `#5CE1E6` / dark | 11.31:1 | Arcade links / indicators |
| Mint `#62FAD3` / dark | 13.65:1 | Magic Money links / indicators |
| Violet `#534ADE` / white | 6.17:1 | AfterGlow links |
| Focus amber / dark | 12.07:1 | Dark-surface keyboard ring |
| Control edge / white; dark | 3.65:1; 4.87:1 | Essential non-text edges |
| Blue / dark | **1.84:1** | Reject direct functional use; company logo needs white tile |

Normal UI text must meet 4.5:1; large text at least 3:1; meaningful control boundaries and state indicators at least 3:1. Logos are artwork, but their exemptions do not make low-contrast placement desirable. These calculations cover specified colour pairs, not a certification of the eventual website. Keyboard behaviour, zoom/reflow and the implemented navigation still need site-level testing.

## Product character within the shared shell

**ChainLens:** monochrome identity, black media panel, generous containment around the white circle. Use calm rectangular divisions and factual feature descriptions. Keep headings and navigation in the shared system type; retain the company blue for actions on the surrounding light surface. No invented market charts or wallet balances. The black panel should be intentionally bounded, not a black square accidentally floating over another dark colour.

**Magic Money:** a dark `#101827` feature field, quiet mint details sampled from its coin/wand, white copy. Keep the blue/mint gradient inside the original asset. White wordmark only on dark; it is thin outlined artwork and becomes weak at small sizes. Reserve the full PNG for a wide hero slot, ideally 1000px image width, and use the supplied icon plus HTML “Magic Money Wallet” in compact cards and phone headers. The PNG's built-in transparent margins remain intact. At widths below 768px prefer icon + HTML title instead of shrinking the wordmark. No simulated connect/unlock controls. Product capability text must retain the fact sheet's chain/route qualifications.

**AfterGlow:** pale violet `#F0EDF8` media inset, violet UI accents on white, small warm gold decorative details. Its bubbly lettering and black extrusion provide sufficient personality; avoid turning the entire site into that lettering style. Never set this logo directly on black: the deep black extrusion merges into it. Use the local/private workspace description from the facts; no public download action has been provided.

**ChainLens Arcade:** set the name as ordinary styled HTML text in the shared heading stack, paired with the untouched ChainLens mark in its own black inset. There is no Arcade logo. Use a dark gallery field, cyan selection/link details and occasional pink decoration derived from DUO. Each game receives an intact logo and a separate readable HTML name. Keep company header/navigation light and unchanged. The supplied game artwork may say DUO; retain it in the files, while every arcade-level label says “ChainLens Arcade”. No invented Arcade emblem and no typographic imitation of the game marks.

## Logo backgrounds and six-game review

All originals were opened as images, including the supplied SVG icon rendered by Chromium. Final placements are shown in `logo-review.html` and screenshots. Panel defaults: 24px padding, 240px review height, centred `object-fit: contain`. These are presentation panels, not modified logo files.

| Asset | Intended background | Observations / constraints |
|---|---|---|
| ManCave derivative | White or mist; white tile on dark | Cutout keeps door openings transparent. White and dark checks show no retained white rectangle. Direct dark placement is clean but too low contrast; white tile is the final dark-context treatment. Original white-backed PNG remains untouched. |
| ChainLens | Exactly `#000000` | Solid black original merges with matching panel. Grey `#E9E9E9` / black is 17.30:1; white ring remains distinct. Keep panel padding: ring approaches the source edges. White would expose a hard black square; do not remove its black background. |
| Magic Money wordmark | `#101827` or black | White outline requires dark; not suitable on white. At card/mobile size the fine strokes are visibly weak even on dark. Final compact treatment is the supplied icon + real text; full wordmark gets a wide hero only. White's theoretical 17.77:1 does not establish thin-stroke legibility. |
| Magic Money SVG icon | `#101827` | Gradient coin/wand clearly separates at review size. Lowest blue portions are quieter than mint; don't use the gradient as functional text colour. No white matte. |
| AfterGlow | `#F0EDF8` or white | Black extrusion remains visible, purple/gold face retains its colour. Black background would swallow the extrusion. Preserve full height and shadow; no cropping. |
| DUO | `#101827` | Both cyan and pink marks remain readable. File includes two stacked colour versions; use the complete file, not an unauthorised crop. This makes its panel composition taller than wordmark-style games. |
| Poker | **`#F0EDF8` inset** in dark gallery | Initial dark test made purple/green fills recede; outlines carried most recognition. Pale inset restores dark lettering separation. Source has large margins; logo appears smaller than peers with contain. Keep accompanying “Poker” text; do not crop margins or rewrite its DUO text. |
| Pool | `#101827` | Neon lettering, cues and ball separate clearly. Soft coloured glow is part of the transparent image, not a rectangular opaque background. Maintain padding around cue ends; avoid other decorative lights behind it. |
| Swarm | `#101827` | Cyan border separates silhouette; purple letterforms remain distinguishable against cyan. Distressed details soften at phone size. Keep plain-text “Swarm” as the accessible name, not logo-only navigation. |
| Clash | `#101827` | White outline clearly separates dark letters. Far blue stroke ends are subdued and fine distressed edges soften at small sizes; preserve whole canvas and give it a wide slot. |
| World | **`#F0EDF8` inset** in dark gallery | Dark test weakened green WORLD letters; pale inset restores their silhouette and retains cyan DUO and foliage. Green foliage details remain busy at small sizes. Keep separate HTML “World”; preserve the existing DUO artwork. |

Background CSS to implement without loading an SVG:

```css
.logo-panel { padding: 24px; border-radius: 4px; }
.logo-panel--chainlens { background: #000; }
.logo-panel--magic-money, .logo-panel--arcade { background: #101827; }
.logo-panel--afterglow, .logo-panel--poker,
.logo-panel--world { background: #f0edf8; }
.logo-panel img { display: block; max-width: 100%; height: auto; object-fit: contain; }
.company-tile { background: #fff; padding: 12px; border-radius: 4px; }
```

## Original background art and motion

`assets/generated/company-grid.svg` is a hand-built field of rectangular lines and offset planes using company blue, mist and a quiet rule. It is decorative geometry, not a new mark or product diagram. Use it once on Home or in a company introduction, with copy in its quiet left half. At phone sizes omit it or show it below copy. Never use it behind a logo panel or body text. Set decorative background images through CSS or empty alt and `aria-hidden="true"` where appropriate.

`chainlens-panel.svg` is a solid black 1200 × 720 backdrop; `magic-money-panel.svg` is a solid `#101827` backdrop at the same size. Both are self-contained; no scripts, fonts or external references. Their CSS equivalents above are usually preferable. The geometric field has a 1600 × 900 viewBox. Do not animate these assets.

Motion is optional and secondary: 120–160ms colour/opacity transitions for hover/focus, no parallax, marquee, auto-carousel, pulsing logos or constant particles. Tab content should switch without a sliding layout. Respect `prefers-reduced-motion: reduce`: disable transitions, animations and smooth scrolling. Content must remain fully visible when scripts or animation are disabled. Do not delay keyboard focus for an animation.

## Generation and verification

The only derivative is `mancave-trimmed-transparent.png`, **689 × 869 RGBA**. `verify-assets.cjs` decodes the source with Chromium canvas. Neutral white matte pixels are cleared; blue pixels require B−R > 12 and B−G > 10. Interior pixels with R <= 20 retain their RGB values (248,499 pixels). The 10,344 lighter edge pixels are unmatted against white using alpha=(255−R)/255 and RGB channel recovery, preventing a white fringe on dark. This edge treatment removes the background contribution; it does not flatten or recolour the blue interior. Crop bounds, inclusive in original coordinates: x=283..971, y=151..1019, including two pixels of transparent clearance. Do not apply this colour key to any other logo.

Commands run from the project root:

```text
node --version
node design/sample-logos.cjs
node design/verify-assets.cjs
```

Node reported v24.14.1. Playwright is required by absolute path from the user-authorised existing installation; nothing was installed. The scripts read only this project's assets plus that tool dependency and serve only project paths over loopback. `verification.json` records successful decoding of all 11 original assets and all four generated assets (the cutout is repeated in three comparison panels), checks all 11 original SHA-256 hashes against the pre-edit samples, computes contrast and captures 1440, 768, 390 and 320px wide screenshots. Final run: no browser console/page errors, no external requests, no horizontal overflow at those four sizes, all original hashes match. Reduced-motion media was enabled during capture; the static fixture has no animations.

The saved cutout was decoded again and its alpha checked: 339,898 fully transparent pixels, 10,344 partially transparent pixels, 248,499 opaque pixels, and zero visible near-white pixels (all RGB channels > 240). The first generation pass reported a missing cutout image during bootstrap before that file existed. Subsequent runs decoded the completed files and passed. Visual review found the dark ManCave contrast issue, small Magic Money wordmark issue and dark Poker/World fill issue; the final background recommendations above incorporate them. The cutout was visually checked on white, dark and a white tile in dark context. All SVGs were rendered as browser images. This is asset and direction validation in a review fixture, not a test of `site/`, a functional navigation implementation, a complete accessibility audit or a deployed site.

## File inventory

- `assets/generated/mancave-trimmed-transparent.png` — permitted new company derivative.
- `assets/generated/company-grid.svg` — original geometric background.
- `assets/generated/chainlens-panel.svg` — exact black backdrop.
- `assets/generated/magic-money-panel.svg` — dark backdrop.
- `design/direction.md` — this implementation direction and review notes.
- `design/logo-samples.json` — measured source pixels, dimensions and hashes.
- `design/sample-logos.cjs` — reproducible sampler, using existing Playwright.
- `design/logo-review.html` — local visual review sheet; no site changes.
- `design/verify-assets.cjs` — derivative generation, browser checks and screenshots.
- `design/verification.json` — final machine-readable check results.
- `design/review-1440.png`, `design/review-768.png`, `design/review-390.png`, `design/review-320.png` — final review screenshots.

No original logo was edited. No changes were made to `site/`, `content/`, `HANDOFF.md` or `HANDOFF_LOG.md`. No commit, push, publication or deployment was performed.
