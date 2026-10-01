"""Typeset a paper's paper.md as a journal-style preprint PDF (single column, A4) or an IEEE-style two-column PDF.

Usage: python build_paper.py p1-fat-tails [--two-column]
Writes papers/<id>/build/<id>.pdf (and -2col.pdf). Figures referenced as figures/*.png resolve from the paper folder.

Layout follows the conventions of a typeset preprint: STIX Two text, centred title block, indented abstract,
numbered sections, table captions above tables and figure captions below figures, hanging-indent references, a
running head and page numbers.
"""
from __future__ import annotations
import glob, os, re, subprocess, sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
FONTS = (HERE.parent / "books" / "assets" / "fonts").as_uri()

CSS = """
@font-face {{ font-family: "Paper"; src: url("{fonts}/STIXTwoText-Regular.ttf"); font-weight: 400; font-style: normal; }}
@font-face {{ font-family: "Paper"; src: url("{fonts}/STIXTwoText-Bold.ttf"); font-weight: 700; font-style: normal; }}
@font-face {{ font-family: "Paper"; src: url("{fonts}/STIXTwoText-Italic.ttf"); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: "Paper"; src: url("{fonts}/STIXTwoText-BoldItalic.ttf"); font-weight: 700; font-style: italic; }}
@font-face {{ font-family: "Mono"; src: url("{fonts}/JetBrainsMono-Regular.ttf"); }}
@page {{ size: A4; margin: 24mm 22mm 24mm 22mm;
         @top-left {{ content: "{runhead}"; font-family: "Paper"; font-style: italic; font-size: 8.5pt; color: #555; }}
         @top-right {{ content: "Preprint · {date}"; font-family: "Paper"; font-size: 8.5pt; color: #555; }}
         @bottom-center {{ content: counter(page); font-family: "Paper"; font-size: 9pt; color: #333; }} }}
@page :first {{ @top-left {{ content: none; }} @top-right {{ content: none; }} }}
html {{ font-size: {base}pt; }}
body {{ font-family: "Paper", "Times New Roman", serif; color: #111; line-height: 1.36; margin: 0;
       text-align: justify; hyphens: auto; -webkit-hyphens: auto; font-variant-numeric: lining-nums; }}
.title {{ font-size: 1.62em; font-weight: 700; line-height: 1.2; text-align: center; margin: 0.4em 0 0.7em; hyphens: manual; text-wrap: balance; }}
.author {{ text-align: center; font-size: 1.1em; margin: 0; }}
.affil {{ text-align: center; font-style: italic; font-size: 0.9em; margin: 0.25em 0 0; color: #222; }}
.email {{ text-align: center; font-size: 0.86em; margin: 0.15em 0 0; font-family: "Mono"; color: #333; }}
.date {{ text-align: center; font-size: 0.9em; margin: 0.5em 0 1.4em; color: #333; }}
.abstract {{ margin: 0 2.4em 1.1em; font-size: 0.93em; line-height: 1.34; }}
.abstract h2 {{ text-align: center; font-size: 1em; margin: 0 0 0.4em; font-variant-caps: small-caps; letter-spacing: 0.04em; }}
.abstract p {{ text-indent: 0; }}
.kw {{ margin: 0 2.4em 1.6em; font-size: 0.88em; text-align: left; }}
.kw b {{ font-weight: 700; }}
.body {{ {columns} }}
h2 {{ font-size: 1.12em; font-weight: 700; margin: 1.3em 0 0.45em; break-after: avoid; text-align: left; hyphens: manual; }}
h2 .n {{ display: inline-block; min-width: 1.6em; }}
h3 {{ font-size: 1em; font-weight: 700; font-style: normal; margin: 0.95em 0 0.3em; break-after: avoid; text-align: left; hyphens: manual; }}
h3 .n {{ display: inline-block; min-width: 2.2em; }}
p {{ margin: 0; text-indent: 1.5em; orphans: 2; widows: 2; }}
h2 + p, h3 + p, figure + p, table + p, ul + p, ol + p, .tcap + table + p, blockquote + p, .tsub + p {{ text-indent: 0; }}
ul, ol {{ margin: 0.35em 0 0.5em; padding-left: 1.5em; }}
li {{ margin: 0 0 0.18em; }}
li p {{ text-indent: 0; }}
code {{ font-family: "Mono"; font-size: 0.84em; }}
blockquote {{ margin: 0.5em 1.5em; }}
blockquote p {{ text-indent: 0; }}
table {{ border-collapse: collapse; width: 100%; font-size: 0.82em; line-height: 1.25; margin: 0.25em 0 0.9em; break-inside: avoid; text-align: left; hyphens: manual; }}
th, td {{ padding: 0.22em 0.45em; vertical-align: top; text-align: left; }}
thead th {{ border-top: 1.1px solid #111; border-bottom: 0.6px solid #111; font-weight: 700; }}
tbody tr:last-child td {{ border-bottom: 1.1px solid #111; }}
td:not(:first-child), th:not(:first-child) {{ text-align: right; font-variant-numeric: tabular-nums; }}
.tcap {{ text-indent: 0; font-size: 0.86em; margin: 0.9em 0 0.25em; text-align: left; break-after: avoid; }}
.tcap b {{ font-weight: 700; }}
.tsub {{ text-indent: 0; font-size: 0.84em; font-style: italic; margin: 0.6em 0 0.15em; break-after: avoid; }}
figure {{ margin: 0.9em 0 1em; break-inside: avoid; text-align: center; }}
figure img {{ max-width: 100%; height: auto; }}
figcaption {{ font-size: 0.86em; line-height: 1.3; text-align: left; margin-top: 0.4em; }}
figcaption b {{ font-weight: 700; }}
.refs p, .refs li {{ text-indent: -1.5em; padding-left: 1.5em; text-align: left; font-size: 0.88em; margin-bottom: 0.25em; }}
.refs ul {{ list-style: none; padding-left: 0; }}
.footnote {{ font-size: 0.82em; border-top: 0.5px solid #999; margin-top: 1.2em; }}
.footnote p {{ text-indent: 0; }}
a {{ color: inherit; text-decoration: none; }}
"""


def parse_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


def build(pid: str, two_column: bool) -> Path:
    folder = HERE / pid
    meta, body_md = parse_front_matter((folder / "paper.md").read_text(encoding="utf-8"))
    # figures: ![Figure N. caption](figures/x.png)
    def fig(m):
        cap = m.group(1)
        cap = re.sub(r"^(Figure \d+\.)", r"<b>\1</b>", cap)
        cap = re.sub(r"\*(.+?)\*", r"<i>\1</i>", cap)
        # print each figure at its drawn size (figures are drawn at 300 dpi with 9 pt text), so type size is the
        # same in every figure; wide figures are capped at the column width
        style, wide = "", False
        try:
            from PIL import Image
            with Image.open(folder / m.group(2)) as im:
                dpi = (im.info.get("dpi") or (300, 300))[0] or 300
                w_in = im.size[0] / dpi
            style, wide = f' style="width: min(100%, {w_in:.2f}in)"', w_in > 3.6
        except Exception:
            pass
        cls = ' class="wide"' if wide else ""
        return f'\n<figure{cls}><img src="../{m.group(2)}" alt=""{style}/><figcaption>{cap}</figcaption></figure>\n'
    body_md = re.sub(r"!\[(.*?)\]\((figures/[^)]+)\)", fig, body_md)
    html = markdown.markdown(body_md, extensions=["footnotes", "tables", "smarty", "sane_lists", "attr_list"])
    # abstract block
    html = re.sub(r'<h2>Abstract</h2>\s*(<p>.*?</p>)', r'<div class="abstract"><h2>Abstract</h2>\1</div>', html, count=1, flags=re.S)
    # section numbers: "1. Introduction" -> numbered span
    html = re.sub(r"<h2>(\d+)\.\s+", r'<h2><span class="n">\1</span>', html)
    html = re.sub(r"<h3>(\d+\.\d+)\s+", r'<h3><span class="n">\1</span>', html)
    # table captions and sub-captions
    html = re.sub(r"<p><strong>(Table \d+\.)(.*?)</strong></p>", r'<p class="tcap"><b>\1</b>\2</p>', html, flags=re.S)
    html = re.sub(r"<p><em>([^<]{3,160})</em></p>(\s*<table>)", r'<p class="tsub">\1</p>\2', html)
    # references block
    html = re.sub(r'(<h2>(?:<span class="n">\d+</span>)?References</h2>)(.*?)(?=<h2|$)', r'\1<div class="refs">\2</div>', html, flags=re.S)
    kw = ""
    if meta.get("keywords"):
        kw = f'<p class="kw"><b>Keywords:</b> {meta["keywords"]}' + (f'. <b>JEL:</b> {meta["jel"]}' if meta.get("jel") else "") + "</p>"
    abs_end = html.find("</div>") + len("</div>") if 'class="abstract"' in html else 0
    html = html[:abs_end] + kw + f'<div class="body">{html[abs_end:]}</div>'
    affil = meta.get("affiliation", "")
    parts = [s.strip() for s in affil.split("·")]
    title = meta.get("title", pid).replace("-", "‑")  # non-breaking hyphens: no line break inside "Out-of-Sample"
    head = (f'<p class="title">{title}</p><p class="author">{meta.get("author", "")}</p>'
            + (f'<p class="affil">{parts[0]}</p>' if parts else "")
            + "".join(f'<p class="email">{p}</p>' for p in parts[1:])
            + f'<p class="date">{meta.get("date", "")}</p>')
    runhead = meta.get("runhead") or (meta.get("author", "") + " · " + meta.get("short", meta.get("title", ""))[:70])
    columns = ("column-count: 2; column-gap: 6mm; column-fill: auto; } "
               ".body figure.wide, .body table, .body .tcap, .body .tsub { column-span: all; ") if two_column else ""
    css = CSS.format(fonts=FONTS, base=9.6 if two_column else 10.6, columns=columns, runhead=runhead.replace('"', "'"), date=meta.get("date", ""))
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{meta.get("title", pid)}</title>'
           f'<meta name="author" content="{meta.get("author", "")}"><style>{css}</style></head><body>{head}{html}</body></html>')
    out = folder / "build"; out.mkdir(exist_ok=True)
    suffix = "-2col" if two_column else ""
    html_path = out / f"{pid}{suffix}.html"; html_path.write_text(doc, encoding="utf-8")
    pdf_path = out / f"{pid}{suffix}.pdf"
    if pdf_path.exists():
        pdf_path.unlink()
    shells = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-*\chrome-headless-shell-win64\chrome-headless-shell.exe"))
    for exe, extra in [(s, []) for s in shells] + [(r"C:\Program Files\Google\Chrome\Application\chrome.exe", ["--headless=new"])]:
        if Path(exe).exists():
            try:
                subprocess.run([exe, *extra, "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                                "--virtual-time-budget=6000", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                               check=False, timeout=300, capture_output=True)
            except subprocess.TimeoutExpired:
                continue
            if pdf_path.exists():
                break
    print("wrote", pdf_path.name if pdf_path.exists() else "(no pdf)", f"{pdf_path.stat().st_size // 1024 if pdf_path.exists() else 0} KB")
    return pdf_path


if __name__ == "__main__":
    build(sys.argv[1], "--two-column" in sys.argv)
