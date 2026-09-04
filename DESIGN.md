# Design record: the four playgrounds

What this documents is what shipped, read back off the built pages, not what was intended.
Shipped 2026-09-03 to four GitHub Pages sites: PulseHTTP, GitEngine, JSON-LP and wc-Go.
Source of truth for each page is `playgrounds/<site>/index.template.html`; `playgrounds/build.py` writes the single-file `index.html` that deploys.

## The program

Each playground is one HTML file. It loads the repository's own artifact, runs it in the visitor's tab, and draws the mechanism working. JSON-LP fetches `lexer.py` and `parser.py` from its repository and runs them unmodified in CPython through Pyodide. GitEngine computes real SHA-1 over Git's exact serialization, so its hashes match native Git for the same bytes. PulseHTTP and wc-Go re-run their shipped algorithms in the browser and check every result against a reference in the same tab. The demo is the code, so nothing on these pages is a mockup of a result.

### What the four share

They share authorship of approach, not a skin. There is no common component set, no shared symbol library, and no palette carried between them.

1. **The mechanism owns the first viewport.** Every page opens on a full-bleed drawing of the thing working. No hero, no headline block over a screenshot.
2. **The visitor touches the mechanism directly.** Controls are objects in the world: levers in a signal box, a command line and a notebook, mail sacks, a chunk-size rail. There are no range sliders anywhere.
3. **Dark, and committed to a color.** Each ground is a specific dark surface with real color in it, chosen from the world rather than from a category default.
4. **Mixed case throughout.** No all-caps label systems. Verdict words read as words: Valid, Refused, Sealed, Returned.
5. **Below the fold, each world keeps its own form.** The accounts are a route card and a departures board, survey notes with contour dividers, a posted ledger with postmark rings, a counting rubric with bead tallies. None of them is a row of cards.
6. **Numbers are measured, and say where from.** Every figure names the harness that produced it and how to re-run it.
7. **No em dashes** in any page copy or in this document.

## PulseHTTP, a midnight metro control board

The request path of an HTTP/1.1 server drawn as a transit line. A request is a train; each stage of the server is a station.

**Ground and color.** Enamel `#0b1d3a`, deeper enamel `#0e2448`, steel `#33415c` and `#223150` for panels. Cobalt `#3a86ff` is the request line, scarlet `#e63946` the response line, amber `#ffb703` signals and holds, green `#2dc653` the cache short turn, sky `#8ecae6` a train already answered. Cream `#f1f3ea` ink, `#b9c1cf` secondary, `#8d99ad` faint.

**Type.** Overpass at 400, 600 and 800; Overpass Mono for token counts and codes.

**Mark.** A two-lamp signal head, drawn in the page. Nothing borrowed from a transit authority.

**Mechanism.** Six stations along one abstract line: Source, Router, Auth barrier, Limiter, Cache, Origin. Each carries a descriptor beneath its name. Refused traffic leaves on a diagonal stub to a No entry stop; rate-limited traffic parks in a Siding and stacks there. The limiter is a signal block of twenty lamps, one per token, going red when the bucket starves. The cache is a green loop that short turns a repeat URL.

**Controls.** A signal box of six levers: rate, ticketed share, repeat URLs, refill, capacity, cache slots. Each is a drag, wheel and keyboard control with an ARIA slider role, drawn as a lever plate rather than a track and thumb. Two push buttons: Surge and Hold all signals.

**States.** A service board reads Good service, or names the fault with a count of held trains. Tallies run per outcome: 200 origin, 200 cache, 304, 401, 403, 429.

**Below the fold.** A route card, one vertical cobalt line with a disc per stop, then a station by station account. Measured numbers sit on a departures board: 178,996 req/s at p99 2.2 ms, 19.5x cache lift, 78,341 req/s through the balancer, 39 raw-TCP conformance tests.

## GitEngine, a braided river survey

A repository drawn as a river system. Branches are channels, commits are confluences, the object store is sediment.

**Ground and color.** Water `#071a2c`, chart `#0a2540`, chart2 `#0e3254`, rule `#1d4a72`. Channel blue `#2e8fe6` with `#6fc6ff` for highlights, gold `#f2c14e` for confluences, coral `#ff6b57` for rapids, sand `#c9a86a` for contours and survey marks. Ink `#e8f1fb`, dim `#a3b9d6`, faint `#7f9ab8`.

**Type.** Alegreya Sans for text, Alegreya italic for water names and headings, Fira Mono for hashes.

**Mechanism.** Headwaters are the working tree, one labelled rail entry per file, stroked by state: gold for changed, blue for staged, faint for in sync. Beyond six files the rail pages. The staging pool is the index, its level a fill clipped to the pool's own outline with a wave surface. The channels carry five lanes and a window of the newest twelve commits, with an upstream note for everything older. Rebased-away commits stay drawn as a dashed oxbow, unreachable but still in the store. The delta mouth carries a flag per ref.

**Controls.** A survey console: command buttons, a field notebook that edits the selected file, a command line with seventeen commands including merge and rebase, and a core sample panel that prints an object exactly as Git serializes it, with the `git hash-object` line that reproduces the hash.

**Records.** The object store is three separate scrolling cores under the chart. Commits show message, hash, parents and branch tags. Trees show entry counts. Blobs show the file path and byte size. Any stratum opens in the core sample.

**Motion.** Water flows as particles along the path a command actually took, easing out and settling. Fresh objects hold a gold rim for one step.

**Below the fold.** Survey notes separated by contour rules, headings marked with a benchmark disc, gauge readings drawn as water levels, a key inset with a scale bar, and a survey stamp in the footer.

## JSON-LP, a night mail sorting office

A JSON lexer and parser drawn as a mail room. Characters are letters, token types are pigeonholes, the parser is the address reader.

**Ground and color.** Navy `#0f1a2e`, `#15223a`, `#1c2d4a`, rule `#2a3d5e`, under a lamp glow `#f5d9a6`. Kraft `#c8a87a` and `#8f7551` for the sack and dashed frames. Postmark red `#d7263d`, stamp green `#3aa655`, airmail blue `#2b6ce6`, yellow `#f2c94c`, violet `#9b6cf2`. Ink `#f3efe6`, dim `#b7b1a4`.

**Type.** Archivo for text, Archivo Black for counts and headings, Special Elite for anything the office types: stamps, verdicts, the seal.

**Mechanism.** A drawn sack with a gathered neck, a tie, a seam and one letter showing. Twelve pigeonholes, one per token type the repository's lexer actually emits. The lexer has no number type, so a number is filed as a string and the hole says so. Sorted letters ride a belt to the reader's desk, where the recursive-descent parser returns a verdict. Two inspectors stamp it: the repository parser and RFC-strict `json.loads`. Agreement applies a wax seal, disagreement returns the letter.

**States.** Boot, sorting, sealed, returned, and a refused-but-agreed state that still seals. Stamps are double-ring rubber stamps with the word inside, rotated a few degrees.

**Below the fold.** A posted ledger, each entry marked by a postmark ring and cancellation bars, a stamp sheet for the token colors, and a manifest whose values are stamped: 572K tokens/s over a 12 MB corpus, 98 differential cases with zero disagreements, 8 documented deviations across 3 policies, 8 error classes. The known weak spot is published with them.

## wc-Go, a soroban

The shipped counting algorithm worked on a Japanese abacus. Counts are beads, chunk seams are the reason the carry exists.

**Ground and color.** Black lacquer `#120e0c`, `#1b1512`, `#241c17`. Brass frame `#c9a15a` and `#8a6d3b`, rods `#5a4636`. Vermilion heaven beads `#c0392b`, bone earth beads `#e8d8b8`. Ink `#f4ecdc`, seam blue `#7fb3d5`, gold `#f2c14e` for agreement.

**Type.** Shippori Mincho for the counts, Zen Kaku Gothic New for text, Noto Sans Mono for hex.

**Mechanism.** Four frames in a two by two grid, one per count: lines, words, bytes, characters. Each frame carries thirteen rods, so a count reads exactly into the trillions. A heaven bead worth five drops to just above the beam; the topmost earth beads rise to just under it, so nothing overlaps at any digit. Above the frames a feed tray shows the chunks with their seams; the carry bead sits on the seam with its hex bytes. Below, the whole-string reference prints its four numbers and the frame says whether the streamed counts agree.

**Controls.** A chunk-size rail at 4, 8, 16, 32 and 64 bytes, presets that stress the seams, and file upload or drop.

**Large inputs.** Anything over 4 KB is counted at the real 32 KB chunk size with progress logged, and the reference still runs, so agreement is proved rather than skipped. Uploaded text is shown in the panel in full up to 2 MB and as the first 64 KB beyond that, with a note saying so.

**Below the fold.** A counting rubric with bead marks for headings, the seam problem explained, and the tally as bead rows: 59 of 59 agreement with coreutils, 5.6 GB/s, 0.8 times the speed of the one honest loss.

## Surfaces the browser would otherwise style

Each world themes its own selection color, focus ring, scrollbars and caret from its palette. Scrollable regions inside the pages, the records cores, the stream log and the text panels, carry a themed thumb and track rather than the platform default.

## Responsive behavior

Every board carries a second geometry, chosen by frame width rather than viewport width, so the drawing reflows instead of scrolling sideways. Under 700 px the metro line runs vertically with its levers in a grid, the river stacks headwaters, pool, a vertical channel and the mouth, the sorting office splits into two tiers, and the soroban stacks its four frames.

## Accessibility

Interactive marks in the drawings are buttons with labels and keyboard handlers. The lever frame exposes ARIA slider semantics with arrow-key control. Live regions announce the service board, the gauge, the stamp box and the counting status. Body text meets 4.5:1 on its ground, and `prefers-reduced-motion` stops the belt, the trains and the bead transitions.

## How each page is verified

1. `python3 playgrounds/build.py` writes the four `index.html` files.
2. `node playgrounds/tools/verify-all.mjs <outDir> [site] [baseUrl]` drives each page headlessly to its signature moment, records the evidence, and captures desktop, full page and mobile.
3. `node playgrounds/tools/stress.mjs <outDir> [baseUrl] [wcgo]` runs the cases a visitor will actually try: a 1.6 MB file on the soroban, a crowded repository on the river, a refused letter in the office.
4. `node ~/.claude/skills/impeccable/scripts/detect.mjs <index.html...>` reports zero anti-patterns.
5. `playgrounds/deploy.sh "message"` copies each built page onto its repository's gh-pages branch through a temporary worktree.

The same verification runs against the live origin by passing `https://brickster241.github.io` as the base URL.
