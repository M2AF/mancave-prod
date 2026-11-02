# Website fact audit

Scope: `site/index.html`, `site/main.js`, and `site/styles.css`. Authority: `brief/FACTS.md` only. Only the requested report was written; no site or brief files were changed, and no commit was made. Line numbers below refer to the audited files and fact sheet as inspected.

## Findings

### Medium — AfterMarket is described beyond the approved name-only mention

- **File/quote:** `site/index.html:311` — “AfterMarket, a trait market, is related to AfterGlow.”
- **FACTS.md:** line 51 permits “AfterMarket, a trait market” in the fact sheet but explicitly says “Mention it only by name, with no details.” Calling it a trait market and explaining its relationship adds details. The heading at line 310 also says “Related: AfterMarket,” which conveys a relationship rather than only the name.

### Low — Explanatory definitions add facts not in the source

- **File/quote:** `site/index.html:128` — “\"Onchain\" means anything recorded on a blockchain, such as token balances, NFTs and transactions.”
- **FACTS.md:** lines 11–21 describe ChainLens and its supported features but do not define “onchain.” The definition is unsupported under the instruction that FACTS.md is the only source.

- **File/quote:** `site/index.html:149` — “EVM networks are the Ethereum-compatible family of blockchains.”
- **FACTS.md:** line 13 names 18 EVM networks but does not define EVM. This explanatory definition is unsupported by the permitted source.

- **File/quote:** `site/index.html:149` — “A public address is the shareable address of a wallet; entering one lets you look at its activity.”
- **FACTS.md:** line 15 says users can enter public addresses to see NFTs, tokens, balances and transaction activity, but does not define a public address as shareable. The definition is extra unsupported copy.

- **File/quote:** `site/index.html:161` — “A passkey is a sign-in method that uses your device instead of a password.”
- **FACTS.md:** line 18 lists passkeys as a sign-in option but does not define how they work. The definition is extra unsupported copy.

### Low — Self-custody explanation overstates what the phrase restores

- **File/quote:** `site/index.html:199` — “Your seed phrase (also called a recovery phrase, the list of words that restores your wallet) is the key to everything...”
- **FACTS.md:** lines 31 and 39 establish that the recovery phrase is encrypted at rest and the user is responsible for it; they do not say it is “the key to everything” or define it as a list of words that restores the wallet. “The key to everything” is broader than the supported recovery-phrase responsibility statement and may mislead.

## Checked and found fine

- All external links in `site/index.html` match the five approved URLs exactly: ChainLens (`https://www.chainlensnft.info`), Magic Money repository and latest release, Arcade play URL, and Discord invite. Discord appears on Home and in the footer; both use the approved invite. No other outbound URLs occur in the checked HTML, JS, or CSS.
- The tagline is exactly “One company. Four products.” (`index.html:54`). The parent-company framing and Microsoft/Alphabet analogy (`index.html:56`) match FACTS.md line 7.
- “DUO Arcade” appears once case-insensitively, only in the short note beside Play (`index.html:340`) that says the game site still shows the old name while the rename finishes. Other Arcade references use “ChainLens Arcade.” DUO, Poker, Pool, Swarm, Clash and World retain their names.
- “Free” is used only for the Arcade and its games, as approved by FACTS.md lines 58, 62–66 and 72. No banned superlatives (“best,” “#1,” “first,” “most secure”), “coming soon,” invented numerical or dated claims, people, partners, prices, roadmaps, awards or quotations were found.
- Discord copy identifies the community and invites users to join; it makes no member-count claim and promises no community offerings.
- Magic Money identifies itself as a self-custody wallet, states user responsibility for the recovery phrase, says swap/send support varies by chain and route, and gives no financial advice or return promise. No audited, unhackable, risk-free or guaranteed claim appears. Network, ecosystem, feature and platform copy checked against FACTS.md lines 25–40.
- ChainLens correctly gives 24 networks, including 18 EVM plus Solana, Polkadot, Tron and Cardano. Its Search, scanner, Market, Magic Swap, Profile, Messenger, Themes and web-platform descriptions match FACTS.md lines 11–21. (Definitions called out above are the exceptions.)
- AfterGlow has no website/download link, no button leading externally, and no “coming soon” copy. The feature descriptions checked match FACTS.md lines 45–50 and 53, apart from the AfterMarket over-description above.
- The audited site code contains no forms, sign-in or wallet-connect UI controls, or tracking/analytics code. Mentions of ChainLens sign-in and wallet connection are descriptive feature copy matching FACTS.md lines 15 and 18; they are not implemented prompts on this company site.
- Titles, meta descriptions, image alt text, aria labels, footer text, script-generated title/description behavior, and styles contain no other factual claims beyond those enumerated above. `main.js` and `styles.css` add no product claims or outbound URLs.

## Severity summary

- **High:** 0
- **Medium:** 1
- **Low:** 5

