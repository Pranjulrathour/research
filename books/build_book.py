"""Build a book from its markdown chapters into HTML, EPUB and PDF.

Usage:  python build_book.py agi-transition
        python build_book.py systems-that-scale

Reads  <book>/00-front-matter.md, <book>/ch*.md (sorted), <book>/99-back-matter.md, <book>/figures/*.png
Writes <book>/build/<slug>.html, <slug>.epub, <slug>.pdf  (PDF via headless Chromium)
Cover  <book>/cover/cover.png (1600x2560), embedded in the EPUB and as the PDF's first page.

Typography follows book conventions rather than web ones: indented paragraphs with no gap between them, chapter
openers set a third of the way down the page, numbered figures with captions, page numbers. Body in Source Serif 4,
headings in Inter, title page in the cover's display face. Fonts are OFL and live in assets/fonts; the EPUB embeds
static instances because e-readers handle variable fonts unevenly.
"""
from __future__ import annotations
import glob, os, re, shutil, subprocess, sys, uuid
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"

META = {
    "agi-transition": {
        "title": "The AGI Transition", "subtitle": "A Field Guide for the Next Decade", "author": "Pranjul Rathour",
        "lang": "en", "accent": "#c8432b",
        "description": "Frameworks, not forecasts: how to reason about AI capability, work, learning, governance and your own career between 2026 and 2036. Written from India.",
        "display_font": "BodoniModa-Text-540.ttf", "display_weight": 500, "display_track": "0.14em", "display_case": "uppercase",
    },
    "systems-that-scale": {
        "title": "Systems That Scale", "subtitle": "The Engineering Judgment Behind Reliable, Low-Latency Software",
        "author": "Pranjul Rathour", "lang": "en", "accent": "#c27a07",
        "description": "System design taught through measurement: latency, concurrency, caching, consistency, failure, queues, observability, capacity, cost and judgment, each with a reproducible number and the question you will be asked.",
        "display_font": "Archivo-Condensed-800.ttf", "display_weight": 800, "display_track": "0em", "display_case": "uppercase",
    },
}

CSS = """
@font-face {{ font-family: "Body"; src: url("{fonts}/SourceSerif4-Regular.ttf"); font-weight: 400; font-style: normal; }}
@font-face {{ font-family: "Body"; src: url("{fonts}/SourceSerif4-SemiBold.ttf"); font-weight: 600; font-style: normal; }}
@font-face {{ font-family: "Body"; src: url("{fonts}/SourceSerif4-Italic.ttf"); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: "Head"; src: url("{fonts}/Inter-Regular.ttf"); font-weight: 400; }}
@font-face {{ font-family: "Head"; src: url("{fonts}/Inter-Medium.ttf"); font-weight: 500; }}
@font-face {{ font-family: "Head"; src: url("{fonts}/Inter-SemiBold.ttf"); font-weight: 600; }}
@font-face {{ font-family: "Mono"; src: url("{fonts}/JetBrainsMono-Regular.ttf"); font-weight: 400; }}
@font-face {{ font-family: "Display"; src: url("{fonts}/{display_font}"); font-weight: 100 900; }}
:root {{ --ink: #1b1a1f; --muted: #5d5b64; --rule: #dedce2; --accent: {accent}; }}
html {{ font-size: 11.5pt; }}
body {{ font-family: "Body", Georgia, serif; color: var(--ink); line-height: 1.52; max-width: 36em; margin: 0 auto; padding: 0 1.5em;
       font-variant-numeric: oldstyle-nums proportional-nums; hyphens: auto; -webkit-hyphens: auto; text-align: justify; }}
h1, h2, h3, h4 {{ font-family: "Head", system-ui, sans-serif; color: var(--ink); text-align: left; hyphens: manual; }}
h1 {{ font-weight: 600; font-size: 1.95em; line-height: 1.15; letter-spacing: -0.012em; margin: 5.5em 0 1.6em; break-before: page; page-break-before: always; }}
section:first-of-type h1, h1.first {{ break-before: auto; page-break-before: auto; }}
h1 .chnum {{ display: block; font-size: 0.4em; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.9em; }}
h2 {{ font-weight: 600; font-size: 1.18em; line-height: 1.25; margin: 2.1em 0 0.7em; break-after: avoid; }}
h3 {{ font-weight: 600; font-size: 1.02em; margin: 1.6em 0 0.5em; break-after: avoid; }}
h4 {{ font-weight: 500; font-size: 0.95em; margin: 1.3em 0 0.4em; color: var(--muted); break-after: avoid; }}
p {{ margin: 0; text-indent: 1.4em; orphans: 2; widows: 2; }}
h1 + p, h2 + p, h3 + p, h4 + p, figure + p, blockquote + p, ul + p, ol + p, table + p, hr + p, .lede, div + p {{ text-indent: 0; }}
h1 + p::first-line {{ font-variant-caps: all-small-caps; letter-spacing: 0.04em; }}
ul, ol {{ margin: 0.7em 0 0.9em; padding-left: 1.4em; }}
li {{ margin: 0 0 0.35em; }}
li p {{ text-indent: 0; }}
blockquote {{ margin: 1em 1.4em; font-style: italic; text-align: left; }}
blockquote p {{ text-indent: 0; }}
hr {{ border: 0; margin: 1.6em 0; text-align: center; }}
hr::after {{ content: "·  ·  ·"; color: var(--muted); letter-spacing: 0.3em; }}
table {{ border-collapse: collapse; width: 100%; font-family: "Head", system-ui, sans-serif; font-size: 0.8em; margin: 1.1em 0 1.3em; break-inside: avoid; text-align: left; hyphens: manual; }}
th, td {{ text-align: left; padding: 0.42em 0.55em; border-bottom: 1px solid var(--rule); vertical-align: top; }}
th {{ font-weight: 600; border-bottom: 1.2px solid var(--ink); }}
code, pre {{ font-family: "Mono", ui-monospace, monospace; font-size: 0.86em; }}
pre {{ background: #f5f4f6; padding: 0.8em 1em; overflow-x: auto; }}
a {{ color: inherit; text-decoration: none; }}
sup {{ font-size: 0.68em; line-height: 0; font-variant-numeric: lining-nums; }}
figure {{ margin: 1.5em 0 1.6em; break-inside: avoid; page-break-inside: avoid; }}
figure img {{ display: block; width: 100%; height: auto; }}
figcaption {{ font-family: "Head", system-ui, sans-serif; font-size: 0.74em; line-height: 1.45; color: var(--muted); margin-top: 0.7em; text-align: left; hyphens: manual; }}
figcaption .fn {{ color: var(--ink); font-weight: 600; margin-right: 0.45em; }}
.footnote {{ font-size: 0.82em; line-height: 1.45; color: var(--muted); margin-top: 2.2em; padding-top: 0.6em; border-top: 1px solid var(--rule); text-align: left; }}
.footnote hr {{ display: none; }}
.footnote ol {{ padding-left: 1.3em; }}
.footnote p {{ text-indent: 0; }}
.footnote-backref {{ display: none; }}
section.back h1, section.front h2 {{ text-align: left; }}
.titlepage {{ text-align: center; padding-top: 2.4in; break-after: page; page-break-after: always; position: relative; height: 7.2in; box-sizing: border-box; }}
.titlepage .t {{ font-family: "Display", serif; font-weight: {display_weight}; font-size: 2.6em; letter-spacing: {display_track}; text-transform: {display_case}; line-height: 1.12; margin: 0; text-indent: 0; }}
.titlepage .s {{ font-family: "Body"; font-style: italic; font-size: 1.15em; color: var(--muted); margin: 0.9em 0 0; text-indent: 0; }}
.titlepage .a {{ font-family: "Display", serif; font-weight: {display_weight}; font-size: 1.0em; letter-spacing: 0.24em; text-transform: uppercase; position: absolute; left: 0; right: 0; bottom: 0.5in; margin: 0; text-indent: 0; }}
.cover {{ break-after: page; page-break-after: always; margin: 0; padding: 0; }}
.cover img {{ display: block; width: 100%; height: auto; }}
@page {{ size: 6in 9in; margin: 0.8in 0.75in 0.85in 0.75in;
         @bottom-center {{ content: counter(page); font-family: "Head"; font-size: 8pt; color: #77757d; }} }}
@page cover {{ size: 6in 9in; margin: 0; @bottom-center {{ content: none; }} }}
@page title {{ @bottom-center {{ content: none; }} }}
@media print {{ html {{ font-size: 10.4pt; }} body {{ max-width: none; padding: 0; }} .cover {{ page: cover; }} .cover img {{ width: 6in; height: 9in; }} .titlepage {{ page: title; }} }}
"""


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["footnotes", "tables", "smarty", "sane_lists", "attr_list"])


def chapters(book: Path) -> list[Path]:
    front = sorted(book.glob("00-*.md"))
    body = sorted(book.glob("ch*.md"), key=lambda p: int(re.match(r"ch(\d+)", p.name).group(1)))
    back = sorted(book.glob("99-*.md"))
    return front + body + back


def inline_md(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def polish(html: str, chap: int | None, img_prefix: str) -> tuple[str, list[str]]:
    """Chapter-opener markup, numbered figures with captions, and the list of figure files used."""
    used: list[str] = []
    m = re.match(r"\s*<h1>Chapter (\d+) [—–-] (.*?)</h1>", html, re.S)
    if m:
        html = html.replace(m.group(0), f'<h1><span class="chnum">Chapter {m.group(1)}</span>{m.group(2)}</h1>', 1)
    k = 0

    def fig(mm):
        nonlocal k
        k += 1
        alt, src = mm.group(1), mm.group(2)
        used.append(src)
        num = f"Figure {chap}.{k}" if chap else f"Figure {k}"
        cap = inline_md(alt.replace("&quot;", '"'))
        return f'<figure><img src="{img_prefix}{src}" alt="{num}"/><figcaption><span class="fn">{num}</span>{cap}</figcaption></figure>'

    html = re.sub(r'<p>\s*<img alt="(.*?)" src="(figures/[^"]+)"\s*/?>\s*</p>', fig, html, flags=re.S)
    return html, used


def build(slug: str) -> None:
    book = HERE / slug
    meta = META[slug]
    out = book / "build"; out.mkdir(exist_ok=True)
    files = chapters(book)
    parts, figs = [], []
    for f in files:
        cm = re.match(r"ch(\d+)", f.name)
        html, used = polish(md_to_html(f.read_text(encoding="utf-8")), int(cm.group(1)) if cm else None, "../")
        figs += used
        kind = "front" if f.name.startswith("00") else "back" if f.name.startswith("99") else "chapter"
        parts.append(f'<section class="{kind}" id="{f.stem}">\n{html}\n</section>')
    cover_png = book / "cover" / "cover.png"
    cover_html = '<div class="cover"><img src="../cover/cover.png" alt="Cover"/></div>' if cover_png.exists() else ""
    title_html = (f'<div class="titlepage"><p class="t">{meta["title"]}</p><p class="s">{meta["subtitle"]}</p>'
                  f'<p class="a">{meta["author"]}</p></div>')
    css = CSS.format(fonts=(Path("..") / ".." / "assets" / "fonts").as_posix(), accent=meta["accent"], display_font=meta["display_font"],
                     display_weight=meta["display_weight"], display_track=meta["display_track"], display_case=meta["display_case"])
    doc = (f'<!doctype html><html lang="{meta["lang"]}"><head><meta charset="utf-8"><title>{meta["title"]}: {meta["subtitle"]}</title>'
           f'<meta name="author" content="{meta["author"]}"><meta name="description" content="{meta["description"]}">'
           f'<style>{css}</style></head><body>{cover_html}{title_html}{"".join(parts)}</body></html>')
    html_path = out / f"{slug}.html"
    html_path.write_text(doc, encoding="utf-8")
    missing = [f for f in figs if not (book / f).exists()]
    print(f"html: {len(doc)/1024:.0f} KB, {len(figs)} figures" + (f", MISSING {missing}" if missing else ""))
    build_epub(slug, meta, files, out, cover_png, book)
    build_pdf(html_path, out / f"{slug}.pdf")


def build_epub(slug, meta, files, out, cover_png, book):
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
    for fn in ("SourceSerif4-Regular.ttf", "SourceSerif4-SemiBold.ttf", "SourceSerif4-Italic.ttf", "Inter-Regular.ttf",
               "Inter-Medium.ttf", "Inter-SemiBold.ttf", "JetBrainsMono-Regular.ttf", meta["display_font"]):
        p = FONTS / fn
        if p.exists():
            bk.add_item(epub.EpubItem(uid="font_" + fn.replace(".", "_").replace("-", "_"), file_name=f"fonts/{fn}",
                                      media_type="font/ttf", content=p.read_bytes()))
    css = CSS.format(fonts="../fonts", accent=meta["accent"], display_font=meta["display_font"], display_weight=meta["display_weight"],
                     display_track=meta["display_track"], display_case=meta["display_case"])
    css = re.sub(r"@page[^{]*\{(?:[^{}]|\{[^{}]*\})*\}\s*", "", css)   # paged-media rules are not valid in EPUB
    css = re.sub(r"@media print\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*", "", css)
    css = css.replace("max-width: 36em; margin: 0 auto; padding: 0 1.5em;", "margin: 0;").replace("margin: 5.5em 0 1.6em", "margin: 2.4em 0 1.4em")
    style = epub.EpubItem(uid="style", file_name="style/book.css", media_type="text/css", content=css.encode("utf-8"))
    bk.add_item(style)
    added_imgs = set()
    items = []
    for f in files:
        cm = re.match(r"ch(\d+)", f.name)
        html, used = polish(md_to_html(f.read_text(encoding="utf-8")), int(cm.group(1)) if cm else None, "")
        for src in used:
            if src not in added_imgs and (book / src).exists():
                bk.add_item(epub.EpubImage(uid="img_" + Path(src).stem, file_name=src, media_type="image/png", content=(book / src).read_bytes()))
                added_imgs.add(src)
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = re.sub("<[^>]+>", " ", m.group(1)).strip() if m else ("Front matter" if f.name.startswith("00") else f.stem)
        title = re.sub(r"\s+", " ", title)
        ch = epub.EpubHtml(title=title, file_name=f"{f.stem}.xhtml", lang=meta["lang"])
        ch.content = f'<html><head><title>{title}</title></head><body>{html}</body></html>'
        ch.add_item(style)
        bk.add_item(ch); items.append(ch)
    bk.toc = items
    bk.add_item(epub.EpubNcx()); bk.add_item(epub.EpubNav())
    bk.spine = ["cover", "nav"] + items if cover_png.exists() else ["nav"] + items
    path = out / f"{slug}.epub"
    epub.write_epub(str(path), bk)
    print("wrote", path.name, f"{path.stat().st_size/1024:.0f} KB, {len(added_imgs)} images")


def build_pdf(html_path: Path, pdf_path: Path):
    shells = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-*\chrome-headless-shell-win64\chrome-headless-shell.exe"))
    for exe, headless in [(s, None) for s in shells] + [(r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new")]:
        if not Path(exe).exists():
            continue
        if pdf_path.exists():
            pdf_path.unlink()
        cmd = [exe] + ([headless] if headless else []) + ["--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                                                         "--virtual-time-budget=8000", f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
        try:
            subprocess.run(cmd, check=False, timeout=600, capture_output=True)
        except subprocess.TimeoutExpired:
            continue
        if pdf_path.exists():
            print("wrote", pdf_path.name, f"{pdf_path.stat().st_size/1024:.0f} KB"); return
    print("PDF failed")


if __name__ == "__main__":
    build(sys.argv[1])
