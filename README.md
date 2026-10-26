# The Printer & Scanner Handbook

*A manual for the printer everyone loathes, explained kindly.*

Beginner-friendly, warm, step-by-step guidance for the least loved machine in the house: why printers misbehave, how to choose one sensibly, Wi-Fi printing, scan-to-PDF, the real math of ink vs. toner, duplex and booklets, driver and spooler repairs — plus a troubleshooting flowchart, a glossary, and printable packs you can keep in the drawer under the printer.

Published by **Asdale Dynamics, LLC** (Dylan Asdale — [dylanasdale.github.io](https://dylanasdale.github.io)), part of a series of guides that explain technology "like a friend would": plain English, step by step, never condescending.

## What's inside

| | |
| --- | --- |
| `docs/` | The handbook, in Markdown: 8 chapters, quick start, flowchart, glossary, about page |
| `printable-packs/` | Three one-page printable tools (checklist, ink budget planner, maintenance tick-sheet) |
| `assets/` | Site stylesheet and the troubleshooting flowchart (SVG) |
| `build.py` | Dependency-free build script (Python standard library only) |
| `site/` | The built, static HTML site — fully offline, no tracking, no accounts |
| `tests/` | pytest suite covering the renderer, build, and link check |

## Build & run

Requires Python 3.10+ (standard library only — nothing to install).

```bash
python3 build.py --clean     # build the static site into site/
python3 build.py             # rebuild (same, unless you want site/ wiped first)
```

Then open `site/index.html` in any browser. Everything works offline.

Printable packs: open `site/printable-packs/index.html`, press `Ctrl+P` (or `Cmd+P`), choose **100% scale**, print.

## Tests

```bash
pytest tests/ -v
```

The suite covers the Markdown renderer (headings, tables, lists, checkboxes, code, links), the build pipeline (all pages generated, titles present, assets copied), and the internal-link check (no broken relative links). `build.py` also self-verifies links on every run.

## Project philosophy

- **Local-first**: built with the standard library, served from a folder, read from disk. No telemetry, no accounts, no secrets.
- **Calm humor**: printers are exasperating; checklists and a little warmth beat panic.
- **Tested**: the build verifies itself, and the tests are part of the repo.
- **Printable**: the packs carry their own `@media print` stylesheet and print beautifully at 100% scale on Letter or A4.

## License

MIT — see [LICENSE](LICENSE): Copyright (c) 2026 Asdale Dynamics, LLC.

Print it, photocopy it for your library or community group, teach from it. Educational content only; no printer manufacturers were harmed (or consulted).

*No medical advice in here either — just the sensible kind of advice about not losing money on ink.*
