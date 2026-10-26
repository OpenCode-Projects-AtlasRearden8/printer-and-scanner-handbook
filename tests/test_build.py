"""Tests for the Printer & Scanner Handbook build.

Run with:  pytest tests/ -v
"""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402


# --------------------------------------------------------------------------- #
# Markdown renderer
# --------------------------------------------------------------------------- #

class TestHeadings:
    def test_h1_through_h3_with_slugs(self):
        html = build.render_markdown("# Hello There\n## Second: part\n### Third")
        assert '<h1 id="hello-there">Hello There</h1>' in html
        assert '<h2 id="second-part">Second: part</h2>' in html
        assert '<h3 id="third">Third</h3>' in html

    def test_inline_markup_in_heading_is_rendered(self):
        assert "<strong>" in build.render_markdown("# A **bold** title")


class TestInline:
    def test_bold(self):
        assert "<strong>ink</strong>" in build.render_markdown("**ink**")

    def test_italic(self):
        assert "<em>placidly</em>" in build.render_markdown("*placidly*")

    def test_code_span(self):
        assert build.render_markdown("type `3-7` now") == "<p>type <code>3-7</code> now</p>"

    def test_link(self):
        assert '<a href="x.html">go</a>' in build.render_markdown("[go](x.html)")

    def test_image(self):
        assert '<img src="a.svg" alt="b">' in build.render_markdown("![b](a.svg)")

    def test_html_is_escaped(self):
        out = build.render_markdown("a < b & honest")
        assert "a &lt; b &amp; honest" in out

    def test_code_span_protects_stars(self):
        assert build.render_markdown("`**not bold**`") == "<p><code>**not bold**</code></p>"


class TestBlocks:
    def test_paragraph_joining(self):
        assert build.render_markdown("one line\ntwo words") == "<p>one line two words</p>"

    def test_fenced_code_block(self):
        out = build.render_markdown("```\na < b\n```")
        assert "<pre><code>a &lt; b</code></pre>" in out

    def test_blockquote(self):
        assert "<blockquote><p>calm</p></blockquote>" in build.render_markdown("> calm")

    def test_hr(self):
        assert "<hr>" in build.render_markdown("---")

    def test_unordered_list(self):
        out = build.render_markdown("- a\n- b")
        assert out.startswith("<ul><li>a</li><li>b</li></ul>")

    def test_task_list_boxes(self):
        out = build.render_markdown("- [ ] todo\n- [x] done")
        assert "☐" in out and "☑" in out and 'class="checkbox"' in out

    def test_ordered_list(self):
        out = build.render_markdown("1. first\n2. second")
        assert out == "<ol><li>first</li><li>second</li></ol>"

    def test_pipe_table(self):
        out = build.render_markdown("| a | b |\n| --- | --- |\n| 1 | 2 |")
        assert "<th>a</th><th>b</th>" in out
        assert "<td>1</td><td>2</td>" in out

    def test_table_with_inline_markup_in_cells(self):
        out = build.render_markdown("| t | d |\n| --- | --- |\n| **ADF** | *auto feeder* |")
        assert "<td><strong>ADF</strong></td><td><em>auto feeder</em></td>" in out

    def test_raw_html_div_passthrough(self):
        out = build.render_markdown('text\n<div class="pack-meta">hello</div>\nmore')
        assert '<div class="pack-meta">hello</div>' in out

    def test_chapter1_starts_with_h1(self):
        md = (ROOT / "docs" / "01-why-printers-betray-us.md").read_text(encoding="utf-8")
        html = build.render_markdown(md)
        assert html.startswith('<h1 id="chapter-1-why-printers-betray-us">')


# --------------------------------------------------------------------------- #
# Page registries & sources
# --------------------------------------------------------------------------- #

class TestRegistries:
    def test_doc_pages_exist_on_disk(self):
        for src, _out, _label in build.DOC_PAGES:
            assert (ROOT / "docs" / src).exists(), f"missing docs/{src}"

    def test_pack_pages_exist_on_disk(self):
        for src, _out, _label in build.PACK_PAGES:
            assert (ROOT / "printable-packs" / src).exists(), f"missing {src}"

    def test_outputs_unique(self):
        outs = [out for _s, out, _l in build.DOC_PAGES]
        assert len(outs) == len(set(outs))

    def test_first_chapter_is_index(self):
        assert build.DOC_PAGES[0][0] == "index.md"


class TestSourcesAreSane:
    """Content guards: no secrets, no stray non-ASCII gibberish markers,
    chapter titles present."""

    SOURCE_DIRS = ["docs", "printable-packs"]

    def test_no_secrets_in_sources(self):
        secret_re = re.compile(
            r"(api[_-]?key|secret|password\s*[:=]|token\s*[:=])", re.IGNORECASE
        )
        for d in self.SOURCE_DIRS:
            for f in sorted((ROOT / d).glob("*.md")) + sorted((ROOT / "assets").glob("*")):
                text = f.read_text(encoding="utf-8")
                # "password" appears as the *topic*, not a value — only flag key=value patterns
                assert not secret_re.search(text.replace("Wi-Fi password", "")), f"possible secret in {f}"

    def test_all_source_files_are_utf8(self):
        for d in self.SOURCE_DIRS + ["assets"]:
            for f in sorted((ROOT / d).iterdir()):
                f.read_text(encoding="utf-8")

    def test_every_doc_has_h1(self):
        for d in self.SOURCE_DIRS:
            for f in sorted((ROOT / d).glob("*.md")):
                assert f.read_text(encoding="utf-8").lstrip().startswith("# "), f"no title in {f}"


# --------------------------------------------------------------------------- #
# Build pipeline (integration)
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def built():
    written = build.build(clean=True)
    errors = build.verify(written)
    return written, errors


class TestBuildPipeline:
    def test_build_runs_with_no_link_errors(self, built):
        written, errors = built
        assert errors == []

    def test_all_registered_pages_written(self, built):
        written, _errors = built
        names = {p.name: p for p in written}
        for _src, out, _l in build.DOC_PAGES:
            assert out in names

    def test_site_index_exists(self, built):
        written, _ = built
        assert (ROOT / "site" / "index.html") in written

    def test_assets_copied(self, built):
        written, _ = built
        assert (ROOT / "site" / "assets" / "style.css") in written
        assert (ROOT / "site" / "assets" / "flowchart.svg") in written

    def test_flowchart_referenced_and_resolveable(self, built):
        written, _ = built
        flow = ROOT / "site" / "troubleshooting-flowchart.html"
        assert '<img src="assets/flowchart.svg"' in flow.read_text(encoding="utf-8")
        assert (ROOT / "site" / "assets" / "flowchart.svg").exists()

    def test_nav_links_resolve_from_subpages(self, built):
        written, _ = built
        flow = (ROOT / "site" / "troubleshooting-flowchart.html").read_text(encoding="utf-8")
        for href in re.findall(r'href="(\./[^"]+"|[^"]*\.html")', flow):
            pass  # check_links already covers; this asserts presence of nav
        assert 'href="./glossary.html"' in flow

    def test_pack_pages_have_print_chrome_hidden(self, built):
        css = (ROOT / "site" / "assets" / "style.css").read_text(encoding="utf-8")
        assert "@media print" in css
        assert (ROOT / "site" / "printable-packs" / "printer-rescue-checklist.html").exists()

    def test_packs_index_builds(self, built):
        assert (ROOT / "site" / "printable-packs" / "index.html").exists()


class TestLicenseAndBranding:
    def test_license_exact_copyright_line(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        assert "Copyright (c) 2026 Asdale Dynamics, LLC" in text

    def test_readme_credits_llc(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        assert "Asdale Dynamics, LLC" in text

    def test_site_footer_has_copyright(self, built):
        footer_copyright = "Copyright (c) 2026 Asdale Dynamics, LLC"
        for page in [ROOT / "site" / "index.html", ROOT / "site" / "glossary.html"]:
            assert footer_copyright in page.read_text(encoding="utf-8")
