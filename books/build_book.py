"""Build a book from its markdown chapters into HTML, EPUB and PDF.

Usage:  python build_book.py agi-transition
        python build_book.py systems-that-scale

Reads  <book>/00-front-matter.md, <book>/ch*.md (sorted), <book>/99-back-matter.md
Writes <book>/build/<slug>.html, <slug>.epub, <slug>.pdf  (PDF via headless Chrome/Edge)
Cover  <book>/cover/cover.png (1600x2560) if present, embedded in the EPUB and as the PDF's first page.

Typography: Source Serif 4 for body, Inter for headings and UI, JetBrains Mono for code (all OFL, in assets/fonts).
"""
from __future__ import annotations
import re, shutil, subprocess, sys, uuid
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"

META = {
    "agi-transition": {
        "title": "The AGI Transition",
        "subtitle": "A Field Guide for the Next Decade",
        "author": "Pranjul Rathour",
        "lang": "en",
        "description": "Frameworks, not forecasts: how to reason about AI capability, work, learning, governance and your own career between 2026 and 2036. Written from India.",
        "accent": "#ff4d2e",
    },
    "systems-that-scale": {
        "title": "Systems That Scale",
        "subtitle": "The Engineering Judgment Behind Reliable, Low-Latency Software",
        "author": "Pranjul Rathour",
        "lang": "en",
        "description": "System design taught through measurement: latency, concurrency, caching, consistency, failure, queues, observability, capacity, cost and judgment, each with a reproducible number and the question you will be asked.",
        "accent": "#1f6feb",
    },
}

CSS = """
@font-face {{ font-family: "Body"; src: url("{fonts}/SourceSerif4-Variable.ttf"); font-weight: 200 900; }}
@font-face {{ font-family: "Body"; src: url("{fonts}/SourceSerif4-Italic-Variable.ttf"); font-weight: 200 900; font-style: italic; }}
@font-face {{ font-family: "Head"; src: url("{fonts}/Inter-Variable.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: "Mono"; src: url("{fonts}/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
:root {{ --ink: #1c1b22; --muted: #5b5a66; --rule: #e4e4ea; --accent: {accent}; }}
html {{ font-size: 11.5pt; }}
body {{ font-family: "Body", Georgia, serif; color: var(--ink); line-height: 1.5; max-width: 38em; margin: 0 auto; padding: 0 1.5em; font-variant-numeric: oldstyle-nums; }}
h1, h2, h3, h4 {{ font-family: "Head", system-ui, sans-serif; font-weight: 600; letter-spacing: -0.01em; line-height: 1.2; color: var(--ink); }}
h1 {{ font-size: 2.1em; margin: 2.2em 0 0.6em; page-break-before: always; break-before: page; }}
h1:first-of-type {{ page-break-before: avoid; break-before: avoid; }}
h2 {{ font-size: 1.35em; margin: 1.8em 0 0.5em; }}
h3 {{ font-size: 1.1em; margin: 1.4em 0 0.4em; }}
h4 {{ font-size: 1em; margin: 1.2em 0 0.3em; color: var(--muted); font-weight: 500; }}
p {{ margin: 0 0 0.85em; orphans: 3; widows: 3; }}
p + p {{ text-indent: 0; }}
blockquote {{ margin: 1em 0; padding: 0.2em 0 0.2em 1em; border-left: 2px solid var(--accent); color: var(--ink); font-style: italic; }}
blockquote p {{ margin: 0; }}
hr {{ border: 0; border-top: 1px solid var(--rule); margin: 2em 0; }}
table {{ border-collapse: collapse; width: 100%; font-family: "Head", system-ui, sans-serif; font-size: 0.85em; margin: 1em 0 1.4em; page-break-inside: avoid; }}
th, td {{ text-align: left; padding: 0.45em 0.6em; border-bottom: 1px solid var(--rule); vertical-align: top; }}
th {{ font-weight: 600; border-bottom: 1.5px solid var(--ink); }}
code, pre {{ font-family: "Mono", ui-monospace, monospace; font-size: 0.88em; }}
pre {{ background: #f6f6f8; padding: 0.8em 1em; overflow-x: auto; border-radius: 4px; }}
a {{ color: var(--ink); text-decoration: underline; text-decoration-color: var(--accent); text-underline-offset: 2px; }}
sup {{ font-size: 0.7em; line-height: 0; }}
.footnote {{ font-size: 0.85em; color: var(--muted); border-top: 1px solid var(--rule); margin-top: 2em; padding-top: 0.8em; }}
.footnote ol {{ padding-left: 1.4em; }}
.footnote-ref, .footnote-backref {{ text-decoration: none; }}
.titlepage {{ text-align: left; padding-top: 30vh; page-break-after: always; break-after: page; }}
.titlepage .t {{ font-family: "Head"; font-weight: 700; font-size: 3em; letter-spacing: -0.02em; line-height: 1.05; margin: 0; }}
.titlepage .s {{ font-family: "Body"; font-style: italic; font-size: 1.4em; color: var(--muted); margin: 0.6em 0 2em; }}
.titlepage .a {{ font-family: "Head"; font-weight: 500; font-size: 1.1em; letter-spacing: 0.08em; text-transform: uppercase; }}
.titlepage .rule {{ width: 3em; height: 4px; background: var(--accent); margin: 1.5em 0; }}
.cover {{ page-break-after: always; break-after: page; margin: 0; padding: 0; text-align: center; }}
.cover img {{ display: block; width: 100%; height: auto; }}
@page {{ size: 6in 9in; margin: 0.85in 0.8in 0.9in 0.8in; }}
@page cover {{ size: 6in 9in; margin: 0; }}
@media print {{ html {{ font-size: 10.5pt; }} body {{ max-width: none; padding: 0; }} a {{ text-decoration: none; }} .cover {{ page: cover; }} .cover img {{ width: 6in; height: 9in; }} }}
"""


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["footnotes", "tables", "smarty", "sane_lists", "attr_list"],
                             extension_configs={"footnotes": {"PLACE_MARKER": "///FOOTNOTES///"}})


def chapters(book: Path) -> list[Path]:
    front = sorted(book.glob("00-*.md"))
    body = sorted(book.glob("ch*.md"), key=lambda p: int(re.match(r"ch(\d+)", p.name).group(1)))
    back = sorted(book.glob("99-*.md"))
    return front + body + back


def build(slug: str) -> None:
    book = HERE / slug
    meta = META[slug]
    out = book / "build"; out.mkdir(exist_ok=True)
    files = chapters(book)
    print("chapters:", [f.name for f in files])
    # Each chapter rendered separately so footnotes stay per chapter
    parts = []
    for f in files:
        html = md_to_html(f.read_text(encoding="utf-8"))
        # markdown's footnote extension puts the list where the marker is, or at the end; wrap it
        html = html.replace('<div class="footnote">', '<div class="footnote">')
        parts.append(f'<section id="{f.stem}">\n{html}\n</section>')
    cover_png = book / "cover" / "cover.png"
    cover_html = f'<div class="cover"><img src="../cover/cover.png" alt="cover"></div>' if cover_png.exists() else ""
    title_html = (f'<div class="titlepage"><p class="t">{meta["title"]}</p><p class="s">{meta["subtitle"]}</p>'
                  f'<div class="rule"></div><p class="a">{meta["author"]}</p></div>')
    fonts_rel = Path("..") / ".." / "assets" / "fonts"
    css = CSS.format(fonts=fonts_rel.as_posix(), accent=meta["accent"])
    doc = (f'<!doctype html><html lang="{meta["lang"]}"><head><meta charset="utf-8"><title>{meta["title"]}: {meta["subtitle"]}</title>'
           f'<meta name="author" content="{meta["author"]}"><meta name="description" content="{meta["description"]}">'
           f'<style>{css}</style></head><body>{cover_html}{title_html}{"".join(parts)}</body></html>')
    html_path = out / f"{slug}.html"
    html_path.write_text(doc, encoding="utf-8")
    print("wrote", html_path, f"{len(doc)/1024:.0f} KB")
    build_epub(slug, meta, files, out, cover_png)
    build_pdf(html_path, out / f"{slug}.pdf")


def build_epub(slug, meta, files, out, cover_png):
    from ebooklib import epub
    bk = epub.EpubBook()
    bk.set_identifier(f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'https://pranjulrathour.scult.in/books/' + slug)}")
    bk.set_title(f"{meta['title']}: {meta['subtitle']}")
    bk.set_language(meta["lang"])
    bk.add_author(meta["author"])
    bk.add_metadata("DC", "description", meta["description"])
    bk.add_metadata("DC", "publisher", meta["author"])
    bk.add_metadata("DC", "date", "2026-10")
    if cover_png.exists():
        bk.set_cover("cover.png", cover_png.read_bytes())
    # fonts
    font_items = []
    for fn in ("SourceSerif4-Variable.ttf", "SourceSerif4-Italic-Variable.ttf", "Inter-Variable.ttf", "JetBrainsMono-Variable.ttf"):
        p = FONTS / fn
        if p.exists():
            it = epub.EpubItem(uid=fn.replace(".", "_"), file_name=f"fonts/{fn}", media_type="font/ttf", content=p.read_bytes())
            bk.add_item(it); font_items.append(it)
    css = CSS.format(fonts="fonts", accent=meta["accent"])
    css = re.sub(r"@page[^}]*}\s*", "", css)  # not valid in EPUB CSS
    style = epub.EpubItem(uid="style", file_name="style/book.css", media_type="text/css", content=css.encode("utf-8"))
    bk.add_item(style)
    items, toc = [], []
    for f in files:
        html = md_to_html(f.read_text(encoding="utf-8"))
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = re.sub("<[^>]+>", "", m.group(1)) if m else f.stem
        ch = epub.EpubHtml(title=title, file_name=f"{f.stem}.xhtml", lang=meta["lang"])
        ch.content = f'<html><head><title>{title}</title></head><body>{html}</body></html>'
        ch.add_item(style)
        bk.add_item(ch); items.append(ch); toc.append(ch)
    bk.toc = toc
    bk.add_item(epub.EpubNcx()); bk.add_item(epub.EpubNav())
    bk.spine = ["nav"] + items
    path = out / f"{slug}.epub"
    epub.write_epub(str(path), bk)
    print("wrote", path, f"{path.stat().st_size/1024:.0f} KB")


def build_pdf(html_path: Path, pdf_path: Path):
    for exe in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                shutil.which("chrome"), shutil.which("google-chrome"), shutil.which("msedge")):
        if exe and Path(exe).exists():
            cmd = [exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                   f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
            subprocess.run(cmd, check=False, timeout=300, capture_output=True)
            if pdf_path.exists():
                print("wrote", pdf_path, f"{pdf_path.stat().st_size/1024:.0f} KB"); return
    print("no headless browser found; PDF skipped")


if __name__ == "__main__":
    build(sys.argv[1])
