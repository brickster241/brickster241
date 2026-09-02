# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: a senior engineer or hiring manager at a Google- or Rubrik-class company, arriving cold from the resume's "Live demo" link or the GitHub profile, deciding within a minute whether the systems on the resume are real and whether this person built them. Their job is a poke test: touch the mechanism, change an input, watch the real code respond, and leave convinced.

Secondary (confirmed): a non-technical recruiter skimming. The first viewport must land for them without interaction; depth is for the engineer.

Both audiences arrive alone, on a laptop, mid-screening, with no patience for reading before seeing.

## Product Purpose

Four interactive playgrounds, one per from-scratch systems repository, each running the repository's real logic in the visitor's browser tab:

- **PulseHTTP**: the HTTP/1.1 request path (router, bearer auth, token-bucket limiter, LRU+ETag cache, origin) animated as live traffic, with the real route table and role rules.
- **GitEngine**: a content-addressed repository in memory with real SHA-1 hashing (WebCrypto), real tree serialization, three-way merge with diff3-style conflicts, a commit graph and object-store view, and a command line.
- **JSON-LP**: the repository's actual `lexer.py` and `parser.py`, fetched unmodified from GitHub and executed by Pyodide, with a token stream and a differential verdict against RFC-strict `json.loads`.
- **wc-Go**: the shipped wc algorithm (chunked read, incomplete-tail carry, word-state across chunks) streaming visibly through chunk boundaries, with a whole-string differential reference.

Success: the visitor concludes "he built this, and it works," and can verify that conclusion themselves inside the page.

## Positioning

**The demo is the code.** Nothing on these pages is a mock-up of the system; the page runs the system. Pyodide executes the repo's Python byte for byte. The git hashes match native git and the page prints the `git hash-object` command that proves it. Every run of JSON-LP and wc-Go is a differential test against a reference. This is the interactive form of the profile's standing line, "Measured, not claimed." A competitor's portfolio can show screenshots of a system; it cannot truthfully let a visitor run it.

## Operating Context

- Each playground is one self-contained `index.html` on its repository's `gh-pages` branch, served at `brickster241.github.io/<repo>/`. No build step, no framework, no bundler. Vanilla HTML, CSS, and ES modules.
- External loads that already exist and are acceptable: Google Fonts, the Pyodide CDN (jsdelivr, ~10 MB on first visit), and `raw.githubusercontent.com` for the repo's Python source.
- Each page auto-demonstrates itself until the visitor's first pointer or key event, then hands over control.
- File upload and drag-and-drop feed real files through the real logic (wc-Go counts real files at real 32 KB chunks and reports throughput; JSON-LP parses uploaded JSON; GitEngine imports files into the worktree).
- The profile README embeds a screenshot of each playground linking to it; the resume links each as "Live demo." Screenshots are recaptured after any redesign.

## Capabilities and Constraints

Preserve, exactly, on every page: every mechanism above, the auto-demo handoff, uploads and drop, the differential verdicts, and the URLs. Redesign replaces the presentation, never the machinery.

Binding constraints from the owner:

- Dark presentation only.
- **No em dashes anywhere on any page.** The owner reads them as a tell that a model wrote the copy.
- **No range sliders or stock form controls as the way to drive the mechanism.** Controls must feel like part of the instrument, not a settings panel beside it.
- No typefaces that read as the AI-default stack. The owner named "the same weird font" as a tell.
- No generic AI front-end grammar: eyebrow label above a big headline above a lede above a card grid; three equal cards; glowing edges; middle-dot metadata strips; hero-then-sections page shape.
- Must work on a phone; the engineer may open it from a message.

Undecided, deliberately: whether the pages share a nav or cross-link to each other at all.

## Brand Commitments

- Author: Ashish Verma, `brickster241`. Standing line: **"Measured, not claimed."**
- **Four distinct visual worlds, one per playground** (owner's decision, 2026-09-02, reversing the earlier "one house style" call in his own words: "that was incorrect of me"). Each repository gets its own concept from its own subject's world. What carries across all four is authorship of approach, not a shared skin: the machine leads the first viewport, the visitor touches the mechanism directly, nothing is a hero, a card, or a slider.
- **Dark and colorful, every one of them.** The owner wants dark themes that attract a recruiter or a demo visitor: deep blues, purples, and other committed dark palettes with real color in them. Light mode is not wanted. A grey-on-grey industrial panel was tried and rejected as "not ideal."
- **No all-caps label systems and no engraved or mono lettering as the page's voice.** The owner reads uniform capitalized labels as generated ("every capital text looks exactly the same"). Type must be chosen per world with a point of view; mixed case by default.
- **No symbol set shared across the four pages.** Repeated pushbuttons, valves, and pipe glyphs across sites read as one template stamped four times.
- The GitHub profile already speaks an "instrument" language (generated SVG gauges, a flight-data-recorder commit strip). That is evidence of the owner's taste, not visual authority over the playgrounds.
- Voice: plain, specific, measured. Numbers over adjectives. No hype verbs.

## Evidence on Hand

Real and citable on the pages:

- PulseHTTP: 178,996 req/s at p99 2.2 ms over 200K requests with 0 errors; 19.5x cache lift (8.2K to 160K req/s); 78,341 req/s through the balancer; 39 raw-TCP conformance tests. Source: the repo's own `pulsebench` harness and README.
- GitEngine: byte-for-byte hash parity with native git across commit chains, merge bases, merge commits, and rebased tips; 15/15 differential tests; fsck at 28,555 objects/s; 8 concurrent writers, 0 lost updates. Source: `go test ./difftest/`, `gebench`.
- JSON-LP: 572K tokens/s over a 12 MB corpus; 98-case differential conformance suite, 0 disagreements. Source: `bench.py`, `conformance.py`.
- wc-Go: 59/59 differential agreement with coreutils; 5.6 GB/s on lines by its own harness. Source: repo README and harness.
- The existing playground code for all four, which carries the mechanisms and is the only thing worth keeping from the incumbent pages.

Absences future work must not fabricate: no photography, no illustration assets, no logo beyond a circle favicon, no image-generation tool in this environment, no customer or usage claims.

## Product Principles

1. **The artifact leads; the interface recedes.** The running mechanism owns the first viewport at full scale. Page chrome earns its pixels or does not exist.
2. **Run it, never mock it.** If the real thing can execute in the tab, it does. Anything that cannot is labeled as illustration.
3. **Every number is measured.** Numbers on screen come from the page's own execution or the repo's harness, and say which.
4. **Controls are the mechanism.** The visitor changes the system by touching the system, not a panel beside it.
5. **One hand, four machines.** The same authorship is legible across all four; the subject changes, the author does not.

## Accessibility & Inclusion

Every control reachable and operable by keyboard. Motion honors `prefers-reduced-motion` with the mechanism still legible when still. Text contrast at WCAG AA against its actual ground. The auto-demo never traps focus or hijacks scroll.
