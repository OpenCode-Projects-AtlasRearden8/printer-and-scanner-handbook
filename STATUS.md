# STATUS.md — Printer & Scanner Handbook

Last updated: 2026-10-26 · Built and verified by Asdale Dynamics, LLC

## What was built

**The Printer & Scanner Handbook** — a complete beginner manual for printers and scanners, "explained like a friend would": plain English, step by step, with calm humor. Part of Dylan Asdale's beginner-friendly guide series.

### Contents

- **`docs/` — the handbook in Markdown (13 pages):**
  - `index.md` — handbook home & chapter map
  - `quick-start.md` — the 5-fix emergency page
  - `01-why-printers-betray-us.md` — printer economics & psychology
  - `02-choosing-a-printer.md` — inkjet vs. laser buying guide
  - `03-wifi-printing.md` — Wi-Fi setup & "offline" mysteries
  - `04-scan-to-pdf.md` — flatbed & phone scanning, signing
  - `05-ink-cost-math.md` — cost-per-page arithmetic, worked examples
  - `06-double-sided-and-booklets.md` — duplex, page ranges, booklet folding
  - `07-driver-and-spooler-fixes.md` — queue surgery, drivers, jams, quality table
  - `08-printing-printable-packs.md` — how to print the packs beautifully
  - `troubleshooting-flowchart.md` — decision path (SVG diagram + text version)
  - `glossary.md` — 27 terms in plain English
  - `about.md` — purpose, license, related guides

- **`printable-packs/` — three one-page printable tools (Markdown):**
  - `printer-rescue-checklist.md` — the calm path to a fix, with checkboxes
  - `ink-budget-planner.md` — chapter 5's math as a fill-in worksheet
  - `weekend-maintenance.md` — the monthly 5-minute ritual

- **`assets/` — `style.css`** (warm screen + dedicated `@media print` stylesheet, `@page` margins, hidden chrome) **and `flowchart.svg`** (hand-built, XML-valid, self-describing flowchart).

- **`build.py`** — dependency-free (Python stdlib only) static site generator: minimal Markdown renderer (headings w/ slugs, bold/italic/code, links, images, tables, ordered/unordered/task lists, blockquotes, fenced code, raw-HTML div passthrough), two page templates, asset copying, generated packs index, and an automatic internal link checker on every run.

- **`site/`** — the built output: 17 HTML pages + 2 assets, fully offline, no accounts/tracking/javascript.

- **`tests/test_build.py`** — 38 pytest tests: renderer units, content sanity (every source has an h1, no secret-looking strings, UTF-8), build integration (all pages written, nav/asset/link verification), and license/branding checks.

- **`README.md`, `LICENSE`** (MIT, © Asdale Dynamics, LLC), `.gitignore` (excludes generated `site/`, `__pycache__`, `.pytest_cache`).

## How to run it

```bash
python3 build.py --clean      # build site/ (self-verifies all internal links)
python3 build.py              # rebuild
python3 -m pytest tests/ -v   # run the test suite
open site/index.html          # read the handbook offline
open site/printable-packs/index.html   # printable packs (Ctrl+P, 100% scale)
```

Requires Python 3.10+ only. Zero third-party dependencies; pytest is used for tests only (not for the build).

## Verification results (all passing)

- `python3 build.py --clean` → `Built 17 HTML pages + 2 assets into site/` + `Link check: OK (all internal links resolve)`
- `python3 -m pytest tests/ -q` → **38 passed**
- `assets/flowchart.svg` parses as valid XML (18 boxes, 24 connector paths)
- Tag-balance audit across all 17 HTML pages: no mismatches (`html/head/body/main/table/article`)
- Rendered-content audit: no garbled text, no stray non-English fragments, all tables/lists/checkboxes render as intended
- `grep "Copyright (c) 2026 Asdale Dynamics, LLC" LICENSE` → exact match present
- README credits Asdale Dynamics, LLC; site footer carries the copyright line

### Issues found and fixed during verification

- Table parser consumed row data along with the separator (rows were dropped) → rewrote branch; all tables now render fully (glossary 28 rows, index 11, ch2 6)
- Task-list checkbox HTML was being HTML-escaped → injected after inline rendering
- Printable-pack index generated with root-relative links while living one dir deep → depth-aware template/nav links
- Content polish: fixed awkward/garbled phrases found by review + heuristic gibberish scans (chapter 1 "Software that…", ch2 cost line, ch6 "Folding trickers", ch2 "text nobody can't read", ch3 "AirPlay"→AirPrint, ch8 "egg the paper", ch5 stray non-language strings, etc.)

## Known gaps

- **No `sitemap.xml`/RSS** and no server-side search — deliberate (local-first, minimal), a client-side search could be added later.
- **Model-specific screenshots** are intentionally absent: menu names vary by brand, so steps are written to be brand-neutral and durable.
- **Printer "brand voice"**: all guidance is manufacturer-neutral; safety-sensitive steps (like never powering off mid-firmware-update) are flagged, but always follow your own model's manual for hardware-specific procedures.
- **Tests cover the build, not browser rendering** — layout verified structurally and via CSS review, not in a live browser matrix (no browser available in the build environment).
- **Printable packs** print beautifully from desktop Chrome/Firefox/Edge at 100% scale; mobile browser re-flow means the chapter 8 recommendation (Save as PDF from the mobile dialog) applies on small screens.
