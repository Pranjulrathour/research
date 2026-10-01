"""Build a paper's paper.md into HTML and PDF (single-column by default; --two-column for an IEEE-style layout).

Usage: python build_paper.py p1-fat-tails [--two-column]
Writes papers/<id>/build/<id>.html and <id>.pdf (via headless Chrome/Edge). Figures referenced as figures/*.png resolve
relative to the paper folder.
"""
from __future__ import annotations
import re, shutil, subprocess, sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
FONTS = (HERE.parent / "books" / "assets" / "fonts").as_posix()

CSS = """
@font-face {{ font-family: "Body"; src: url("file:///{fonts}/SourceSerif4-Variable.ttf"); font-weight: 200 900; }}
@font-face {{ font-family: "Body"; src: url("file:///{fonts}/SourceSerif4-Italic-Variable.ttf"); font-weight: 200 900; font-style: italic; }}
@font-face {{ font-family: "Head"; src: url("file:///{fonts}/Inter-Variable.ttf"); font-weight: 100 900; }}
@font-face {{ font-family: "Mono"; src: url("file:///{fonts}/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
@page {{ size: A4; margin: 22mm 20mm 24mm 20mm; @bottom-center {{ content: counter(page); font-family: "Head"; font-size: 9pt; color: #666; }} }}
html {{ font-size: {base}pt; }}
body {{ font-family: "Body", Georgia, serif; color: #1c1b22; line-height: 1.42; margin: 0; }}
.title {{ font-family: "Head"; font-weight: 700; font-size: 1.9em; letter-spacing: -0.015em; line-height: 1.15; margin: 0 0 0.5em; }}
.author {{ font-family: "Head"; font-weight: 600; font-size: 1.05em; margin: 0; }}
.affil {{ font-family: "Head"; font-size: 0.85em; color: #555; margin: 0.2em 0 0; }}
.date {{ font-family: "Head"; font-size: 0.85em; color: #555; margin: 0.2em 0 1.4em; }}
.kw {{ font-family: "Head"; font-size: 0.82em; color: #444; margin: 0 0 1.6em; }}
.kw b {{ font-weight: 600; }}
.body {{ {columns} }}
h2 {{ font-family: "Head"; font-weight: 650; font-size: 1.12em; margin: 1.5em 0 0.5em; break-after: avoid; }}
h3 {{ font-family: "Head"; font-weight: 600; font-size: 0.98em; margin: 1.2em 0 0.4em; break-after: avoid; }}
h2#abstract {{ margin-top: 0; }}
p {{ margin: 0 0 0.7em; text-align: justify; hyphens: auto; orphans: 3; widows: 3; }}
.body > p:first-of-type, h2 + p {{ text-indent: 0; }}
table {{ border-collapse: collapse; width: 100%; font-family: "Head"; font-size: 0.76em; margin: 0.6em 0 1em; break-inside: avoid; }}
th, td {{ text-align: left; padding: 0.3em 0.45em; border-bottom: 1px solid #ddd; vertical-align: top; }}
th {{ border-bottom: 1.5px solid #1c1b22; font-weight: 600; }}
tr:first-child th {{ border-top: 1.5px solid #1c1b22; }}
img {{ max-width: 100%; height: auto; display: block; margin: 0.6em auto; }}
.fig {{ break-inside: avoid; margin: 0.8em 0 1.2em; }}
.fig p.cap {{ font-family: "Head"; font-size: 0.78em; color: #444; text-align: left; margin: 0.3em 0 0; }}
code {{ font-family: "Mono"; font-size: 0.86em; }}
blockquote {{ margin: 0.6em 1em; color: #333; }}
em.tbl {{ font-family: "Head"; font-size: 0.85em; font-style: normal; font-weight: 600; display: block; margin-top: 0.8em; }}
ul, ol {{ margin: 0 0 0.7em; padding-left: 1.3em; }}
li {{ margin: 0 0 0.25em; }}
.refs p, .refs li {{ font-size: 0.86em; text-align: left; }}
.footnote {{ font-size: 0.82em; color: #333; border-top: 1px solid #ddd; margin-top: 1.5em; padding-top: 0.5em; }}
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


def build(pid: str, two_column: bool) -> None:
    folder = HERE / pid
    meta, body_md = parse_front_matter((folder / "paper.md").read_text(encoding="utf-8"))
    # figures: ![caption](figures/x.png) -> figure block
    body_md = re.sub(r"!\[(.*?)\]\((figures/[^)]+)\)", lambda m: f'<div class="fig"><img src="../{m.group(2)}" alt=""><p class="cap">{m.group(1)}</p></div>', body_md)
    html = markdown.markdown(body_md, extensions=["footnotes", "tables", "smarty", "sane_lists", "attr_list", "toc"])
    # italic table captions like *NIFTY 50, 95% (...)* on their own line -> styled label
    html = re.sub(r"<p><em>([^<]{3,120})</em></p>\s*(?=<table>)", r'<em class="tbl">\1</em>', html)
    # references section styling
    html = re.sub(r'(<h2 id="references">.*?)(?=<h2|$)', r'<div class="refs">\1</div>', html, flags=re.S)
    columns = "column-count: 2; column-gap: 7mm;" if two_column else ""
    css = CSS.format(fonts=FONTS, base=10.0 if two_column else 10.8, columns=columns)
    head = (f'<p class="title">{meta.get("title", pid)}</p><p class="author">{meta.get("author", "")}</p>'
            f'<p class="affil">{meta.get("affiliation", "")}</p><p class="date">{meta.get("date", "")}</p>'
            + (f'<p class="kw"><b>Keywords:</b> {meta["keywords"]}' + (f' &nbsp;·&nbsp; <b>JEL:</b> {meta["jel"]}' if meta.get("jel") else "") + "</p>" if meta.get("keywords") else ""))
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{meta.get("title", pid)}</title>'
           f'<meta name="author" content="{meta.get("author", "")}"><style>{css}</style></head><body>{head}<div class="body">{html}</div></body></html>')
    out = folder / "build"; out.mkdir(exist_ok=True)
    suffix = "-2col" if two_column else ""
    html_path = out / f"{pid}{suffix}.html"; html_path.write_text(doc, encoding="utf-8")
    pdf_path = out / f"{pid}{suffix}.pdf"
    for exe in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                shutil.which("chrome"), shutil.which("msedge")):
        if exe and Path(exe).exists():
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                            f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()], check=False, timeout=180, capture_output=True)
            break
    print("wrote", html_path.name, pdf_path.name if pdf_path.exists() else "(no pdf)", f"{pdf_path.stat().st_size // 1024 if pdf_path.exists() else 0} KB")


if __name__ == "__main__":
    build(sys.argv[1], "--two-column" in sys.argv)
