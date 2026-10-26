#!/usr/bin/env python3
"""Build the Printer & Scanner Handbook site.

Converts Markdown sources (docs/, printable-packs/) to a static HTML site
in site/. Standard library only — no dependencies, fully local.

Usage:
    python3 build.py            # build (or rebuild) the site
    python3 build.py --clean    # remove site/ first, then build
    python3 build.py --check    # build, then verify: pages exist, links resolve
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DOCS = ROOT / "docs"
PACKS = ROOT / "printable-packs"
ASSETS = ROOT / "assets"

SITE_TITLE = "The Printer & Scanner Handbook"
SITE_TAGLINE = "A manual for the machine everyone loathes, explained kindly."
FOOTER = (
    "Copyright (c) 2026 Asdale Dynamics, LLC · "
    "Part of the beginner-friendly guides at dylanasdale.github.io · "
    "MIT License"
)

# (source markdown, output html name, nav label)
DOC_PAGES = [
    ("index.md", "index.html", "Home"),
    ("quick-start.md", "quick-start.html", "Quick start"),
    ("01-why-printers-betray-us.md", "01-why-printers-betray-us.html", "Ch 1 · Why printers betray us"),
    ("02-choosing-a-printer.md", "02-choosing-a-printer.html", "Ch 2 · Choosing sensibly"),
    ("03-wifi-printing.md", "03-wifi-printing.html", "Ch 3 · Wi-Fi printing"),
    ("04-scan-to-pdf.md", "04-scan-to-pdf.html", "Ch 4 · Scan to PDF"),
    ("05-ink-cost-math.md", "05-ink-cost-math.html", "Ch 5 · Ink-cost math"),
    ("06-double-sided-and-booklets.md", "06-double-sided-and-booklets.html", "Ch 6 · Duplex & booklets"),
    ("07-driver-and-spooler-fixes.md", "07-driver-and-spooler-fixes.html", "Ch 7 · Driver & spooler fixes"),
    ("08-printing-printable-packs.md", "08-printing-printable-packs.html", "Ch 8 · Printable packs"),
    ("troubleshooting-flowchart.md", "troubleshooting-flowchart.html", "Flowchart"),
    ("glossary.md", "glossary.html", "Glossary"),
    ("about.md", "about.html", "About"),
]

PACK_PAGES = [
    ("printer-rescue-checklist.md", "printer-rescue-checklist.html", "Printer Rescue Checklist"),
    ("ink-budget-planner.md", "ink-budget-planner.html", "Ink & Toner Budget Planner"),
    ("weekend-maintenance.md", "weekend-maintenance.html", "Weekend Maintenance Tick-Sheet"),
]


# --------------------------------------------------------------------------- #
# Minimal Markdown renderer (stdlib only)
# --------------------------------------------------------------------------- #

INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*(?!\s)([^*\n]+?)\*(?!\*)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def _slugify(text: str) -> str:
    text = re.sub(r"[*`_]", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "section"


def render_inline(text: str) -> str:
    """Convert inline Markdown to HTML. Markup chars are pre-escaped."""
    placeholders: list[str] = []

    def stash(html_frag: str) -> str:
        placeholders.append(html_frag)
        return f"\x00{len(placeholders) - 1}\x00"

    text = html.escape(text, quote=False)
    # code spans first, protected from further processing
    text = INLINE_CODE_RE.sub(lambda m: stash(f"<code>{m.group(1)}</code>"), text)
    text = IMAGE_RE.sub(lambda m: stash(f'<img src="{m.group(2)}" alt="{m.group(1)}">'), text)
    text = LINK_RE.sub(lambda m: stash(f'<a href="{m.group(2)}">{m.group(1)}</a>'), text)
    text = BOLD_RE.sub(lambda m: stash(f"<strong>{m.group(1)}</strong>"), text)
    text = ITALIC_RE.sub(lambda m: stash(f"<em>{m.group(1)}</em>"), text)
    # restore
    for i, frag in enumerate(placeholders):
        text = text.replace(f"\x00{i}\x00", frag)
    return text


def render_markdown(md: str) -> str:
    """Render the Markdown subset used in this handbook to HTML."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def flush_para(buf: list[str]) -> None:
        if buf:
            out.append(f"<p>{render_inline(' '.join(buf))}</p>")
            buf.clear()

    para: list[str] = []
    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        # fenced code block
        if stripped.startswith("```"):
            flush_para(para)
            lang = stripped[3:].strip()
            i += 1
            code_lines: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # closing fence
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        # raw HTML passthrough (used by printable packs)
        if re.match(r"^</?div", stripped):
            flush_para(para)
            out.append(stripped)
            i += 1
            continue

        # blank line
        if not stripped:
            flush_para(para)
            i += 1
            continue

        # horizontal rule (standalone dashes/asterisks, surrounded by blank-ish)
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped) and (not out or out[-1].startswith("<")):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para(para)
            level = len(m.group(1))
            inner = m.group(2).strip()
            out.append(f'<h{level} id="{_slugify(inner)}">{render_inline(inner)}</h{level}>')
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            flush_para(para)
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote><p>{render_inline(' '.join(quote))}</p></blockquote>")
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|", lines[i + 1]) and set(lines[i + 1].replace("|", "").replace(" ", "").replace(":", "").replace("-", "")) == set():
            flush_para(para)
            header_cells = [c.strip() for c in stripped.strip("|").split("|")]
            i += 1  # past header
            i += 1  # past separator row
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                # pad/truncate to header length
                cells = (cells + [""] * len(header_cells))[: len(header_cells)]
                rows.append(cells)
                i += 1
            head = "".join(f"<th>{render_inline(c)}</th>" for c in header_cells)
            body_rows = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in r) + "</tr>" for r in rows
            )
            out.append(
                "<table><thead><tr>" + head + "</tr></thead><tbody>" + body_rows + "</tbody></table>"
            )
            continue

        # unordered list (incl. task-list checkboxes)
        if re.match(r"^[-*]\s+", stripped):
            flush_para(para)
            items: list[str] = []
            while i < n:
                cur = lines[i].strip()
                lm = re.match(r"^[-*]\s+(.*)$", cur)
                if not lm:
                    break
                item = lm.group(1)
                tm = re.match(r"^\[( |x|X)\]\s*(.*)$", item)
                if tm:
                    box = "☑" if tm.group(1).lower() == "x" else "☐"
                    items.append(f'<li><span class="checkbox">{box}</span> {render_inline(tm.group(2))}</li>')
                    i += 1
                    continue
                items.append(f"<li>{render_inline(item)}</li>")
                i += 1
                # soft continuation lines (indented, non-list)
                while i < n and lines[i].strip() and not re.match(r"^[-*]\s+", lines[i].strip()) and lines[i].startswith(("    ", "\t")):
                    items[-1] = items[-1][:-len("</li>")] + " " + render_inline(lines[i].strip()) + "</li>"
                    i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        # ordered list
        if re.match(r"^\d+[\.\)]\s+", stripped):
            flush_para(para)
            oitems: list[str] = []
            while i < n:
                cur = lines[i].strip()
                om = re.match(r"^\d+[\.\)]\s+(.*)$", cur)
                if not om:
                    break
                oitems.append(f"<li>{render_inline(om.group(1))}</li>")
                i += 1
            out.append("<ol>" + "".join(oitems) + "</ol>")
            continue

        # paragraph (accumulate until blank line or block start)
        para.append(stripped)
        i += 1

    flush_para(para)
    return "\n".join(out)


def first_heading(md: str) -> str | None:
    for line in md.splitlines():
        m = re.match(r"^\s*#\s+(.*)$", line)
        if m:
            return re.sub(r"[*`]", "", m.group(1)).strip()
    return None


# --------------------------------------------------------------------------- #
# Templates
# --------------------------------------------------------------------------- #

def page_template(title: str, body_html: str, depth: int, label: str = "") -> str:
    """Standard handbook page. depth = number of dirs between page and site root."""
    up = "./" if depth == 0 else "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {SITE_TITLE}</title>
<meta name="description" content="{html.escape(SITE_TAGLINE)}">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{up}index.html">{SITE_TITLE}</a>
    <p class="tagline">{SITE_TAGLINE}</p>
  </div>
</header>
<nav class="site-nav" aria-label="Handbook chapters">
  <div class="wrap">
    <ul>
      {"".join(nav_links(depth))}
    </ul>
  </div>
</nav>
<main id="content" class="wrap">
{f'<p class="eyebrow">{label}</p>' if label else ""}
<article class="card">
{body_html.strip()}
</article>
<nav class="pn" aria-label="Chapter navigation"></nav>
</main>
<footer class="site-footer">
  <div class="wrap"><p>{FOOTER}</p></div>
</footer>
</body>
</html>
"""


def pack_template(title: str, body_html: str) -> str:
    """Printable-pack page: minimal chrome, dedicated print stylesheet."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Printable pack</title>
<meta name="description" content="Printable pack from The Printer & Scanner Handbook.">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body class="pack-page">
<header class="site-header slim">
  <div class="wrap">
    <a class="brand" href="../index.html">{SITE_TITLE}</a>
    <p class="tagline">Printable pack — press Ctrl+P / Cmd+P, choose 100% scale.</p>
  </div>
</header>
<main class="wrap">
<article class="pack">
{body_html.strip()}
</article>
<nav class="pn"></nav>
</main>
<footer class="site-footer">
  <div class="wrap"><p>{FOOTER}</p></div>
</footer>
</body>
</html>
"""


def nav_links(depth: int = 0) -> list[str]:
    up = "./" if depth == 0 else "../" * depth
    links = []
    current = getattr(nav_links, "_current", None)
    for _src, out, label in DOC_PAGES:
        extra = ' class="current"' if current == out else ""
        links.append(f'<li><a href="{up}{out}"{extra} data-page="{out}">{label}</a></li>')
    return links


# --------------------------------------------------------------------------- #
# Link verification
# --------------------------------------------------------------------------- #

HREF_RE = re.compile(r'(?:href|src)="([^"]+)"')
LOCAL_SKIP = ("#", "http://", "https://", "mailto:")


def check_links(html_text: str, page_path: Path) -> list[str]:
    errors = []
    for href in HREF_RE.findall(html_text):
        if href.startswith(LOCAL_SKIP):
            continue
        target = (page_path.parent / href).resolve()
        if not target.exists():
            errors.append(f"{page_path.relative_to(SITE)}: broken link -> {href}")
    return errors


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def build(clean: bool = False) -> list[Path]:
    if clean and SITE.exists():
        shutil.rmtree(SITE)
    written: list[Path] = []

    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    (SITE / "printable-packs").mkdir(parents=True, exist_ok=True)

    # copy assets
    if ASSETS.exists():
        for asset in sorted(ASSETS.iterdir()):
            shutil.copy2(asset, SITE / "assets" / asset.name)
            written.append(SITE / "assets" / asset.name)

    # docs pages
    for src_name, out_name, _label in DOC_PAGES:
        src = DOCS / src_name
        if not src.exists():
            sys.exit(f"build error: missing source {src.relative_to(ROOT)}")
        md = src.read_text(encoding="utf-8")
        body = render_markdown(md)
        title = first_heading(md) or SITE_TITLE
        nav_links._current = out_name  # type: ignore[attr-defined]
        page = page_template(title, body, depth=0)
        out = SITE / out_name
        out.write_text(page, encoding="utf-8")
        written.append(out)
    nav_links._current = None  # type: ignore[attr-defined]

    # printable packs
    for src_name, out_name, _label in PACK_PAGES:
        src = PACKS / src_name
        if not src.exists():
            sys.exit(f"build error: missing source {src.relative_to(ROOT)}")
        md = src.read_text(encoding="utf-8")
        body = render_markdown(md)
        title = first_heading(md) or out_name
        out = SITE / "printable-packs" / out_name
        out.write_text(pack_template(title, body), encoding="utf-8")
        written.append(out)

    # packs index (small generated page)
    pack_links = "".join(
        f'<li><a href="{out}">{label}</a></li>' for _s, out, label in PACK_PAGES
    )
    packs_index = page_template(
        "Printable packs",
        (
            "<h1>Printable packs</h1>"
            '<p class="lead">One-page paper tools from the handbook. </p>'
            "<p>Each opens in your browser with a built-in print stylesheet: press "
            "<em>Ctrl+P</em> (or <em>Cmd+P</em>), choose <em>100% scale</em>, and print. "
            "See <a href=\"../08-printing-printable-packs.html\">Chapter 8</a> for the settings.</p>"
            f"<ul>{pack_links}</ul>"
        ),
        depth=1,
    )
    out = SITE / "printable-packs" / "index.html"
    nav_links._current = None  # type: ignore[attr-defined]
    out.write_text(packs_index, encoding="utf-8")
    written.append(out)

    return written


def verify(written: list[Path]) -> list[str]:
    errors: list[str] = []
    for page in written:
        if page.suffix == ".html":
            errors.extend(check_links(page.read_text(encoding="utf-8"), page))
    # every page title heading present
    for page in written:
        if page.suffix == ".html" and "<h1" not in page.read_text(encoding="utf-8"):
            errors.append(f"{page.relative_to(SITE)}: missing <h1>")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="remove site/ before building")
    parser.add_argument("--check", action="store_true", help="verify links after building")
    args = parser.parse_args()

    written = build(clean=args.clean)
    html_pages = [p for p in written if p.suffix == ".html"]
    print(f"Built {len(html_pages)} HTML pages + "
          f"{len(written) - len(html_pages)} assets into site/")

    # always verify; cheap and catches mistakes
    errors = verify(written)
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("Link check: OK (all internal links resolve)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
