"""Front covers for both books, typeset as HTML + SVG and rendered by headless Chrome at 1600 x 2560 (KDP's recommended
ratio). Real fonts, real kerning, vector geometry, and a light paper/print texture.

Usage:  python make_cover.py            -> <book>/cover/cover.png (+ cover-thumb.png at Amazon thumbnail size)

Book 1, The AGI Transition: the title letters carry the idea. A is a type designer's construction drawing (guides,
overshoot lines, a compass circle), G is half-finished engraver's hatching, I is finished ink. Drafted to done.
Book 2, Systems That Scale: one square partitioned again and again through eight orders of magnitude, with a single
tiny square in the accent colour: the one that fails, which at scale is never zero.
"""
from __future__ import annotations
import glob
import os
import subprocess
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image

HERE = Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"
W, H = 1600, 2560
# Playwright's headless-shell Chromium renders large SVG pages reliably; full Chrome's --screenshot hung on this machine.
CHROME = (glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-*\chrome-headless-shell-win64\chrome-headless-shell.exe"))
          or [r"C:\Program Files\Google\Chrome\Application\chrome.exe"])[0]
# Display text uses static instances built with overlaps removed (fontTools + skia-pathops); the variable Bodoni's
# overlapping contours made Chrome drop the thick stroke of "A".


def font_face(family: str, file: str, style: str = "normal", weight: str = "100 900") -> str:
    return (f'@font-face{{font-family:"{family}";src:url("{(FONTS / file).as_uri()}");'
            f'font-style:{style};font-weight:{weight};}}')


def glyphs(font_file: str, axes: dict | None, text: str) -> dict:
    """Outline path (font units, y up), advance and ink bounds for each character, from a static, overlap-free font."""
    f = TTFont(FONTS / font_file)
    if axes:
        f = instancer.instantiateVariableFont(f, axes, overlap=instancer.OverlapMode.REMOVE)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    out = {"upm": f["head"].unitsPerEm, "cap": f["OS/2"].sCapHeight, "xh": f["OS/2"].sxHeight, "g": {}}
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs); gs[name].draw(pen)
        bp = BoundsPen(gs); gs[name].draw(bp)
        out["g"][ch] = {"d": pen.getCommands(), "adv": f["hmtx"][name][0], "bounds": bp.bounds}
    return out


PAPER_FILTERS = """
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" result="n"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.1 0.62"/>
</filter>
<filter id="mottle" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.0035" numOctaves="3" seed="3"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -0.9 0.5"/>
</filter>
<filter id="ink" x="-2%" y="-2%" width="104%" height="104%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="11" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="2.2"/>
</filter>
"""


def page(body_svg: str, css: str, bg: str) -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}'
            f'html,body{{margin:0;padding:0;background:{bg};}}svg{{display:block}}</style></head><body>'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{PAPER_FILTERS}</defs>{body_svg}</svg></body></html>')


def textures(dark: bool) -> str:
    grain_op, mottle_op = (0.10, 0.045) if not dark else (0.15, 0.07)
    blend = "multiply" if not dark else "screen"
    return (f'<rect width="{W}" height="{H}" filter="url(#mottle)" opacity="{mottle_op}" style="mix-blend-mode:{blend}"/>'
            f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="{grain_op}" style="mix-blend-mode:{blend}"/>')


def spaced(text: str, x: float, y: float, size: float, family: str, fill: str, track: float, weight: int = 400,
           style: str = "normal", anchor: str = "middle", extra: str = "") -> str:
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" font-style="{style}" letter-spacing="{track}em" fill="{fill}" {extra}>{text}</text>')


# ------------------------------------------------------------------------------------------------ Book 1
def cover_agi() -> str:
    paper, ink, grey, verm = "#f1ebdf", "#141312", "#a59e92", "#c8432b"
    fam = "BodoniD"
    # text lines use a small optical size: the display cut's hairlines are ~1px and vanish at thumbnail size
    css = (font_face(fam, "BodoniModa-Text-540.ttf", weight="400 700")
           + font_face(fam, "BodoniModa-TextItalic-440.ttf", "italic", "400 700")
           + font_face("Plex Mono", "IBMPlexMono-Regular.ttf", weight="400"))
    G = glyphs("BodoniModa-Display-680.ttf", None, "AGI")
    upm, cap, xh = G["upm"], G["cap"], G["xh"]
    # lay out A G I with hand-tuned spacing (no GPOS kerning for three letters)
    gap = [0, -40, 30]          # extra font-unit spacing before A, G, I
    xs, pen = [], 0
    for ch, g in zip("AGI", gap):
        pen += g; xs.append(pen); pen += G["g"][ch]["adv"]
    width_units = pen
    target_w = 1260
    s = target_w / width_units
    x0 = (W - target_w) / 2
    base = 1235                                  # baseline y in px
    capy = base - cap * s
    xhy = base - xh * s
    over = 14 * s                                # overshoot band for round letters
    parts = []
    # --- construction guides spanning the word (drawn first, behind the letters)
    gx0, gx1 = x0 - 70, x0 + target_w + 70
    for y, label in ((capy, "cap height"), (xhy, "x-height"), (base, "baseline")):
        parts.append(f'<line x1="{gx0}" y1="{y:.1f}" x2="{gx1}" y2="{y:.1f}" stroke="{grey}" stroke-width="1.6"/>')
        parts.append(f'<text x="{gx0}" y="{y - 12:.1f}" font-family="Plex Mono" font-size="21" fill="{grey}" letter-spacing="0.06em">{label}</text>')
    for y in (capy - over, base + over):
        parts.append(f'<line x1="{gx0 + 200}" y1="{y:.1f}" x2="{gx1}" y2="{y:.1f}" stroke="{grey}" stroke-width="1" stroke-dasharray="6 7"/>')
    # sidebearing verticals for each glyph
    for ch, xu in zip("AGI", xs):
        for xx in (x0 + xu * s, x0 + (xu + G["g"][ch]["adv"]) * s):
            parts.append(f'<line x1="{xx:.1f}" y1="{capy - 60:.1f}" x2="{xx:.1f}" y2="{base + 60:.1f}" stroke="{grey}" stroke-width="1" stroke-dasharray="2 6"/>')
    # --- the letters
    hatch = (f'<pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)">'
             f'<line x1="0" y1="0" x2="0" y2="14" stroke="{ink}" stroke-width="4.4"/></pattern>')
    parts.insert(0, f"<defs>{hatch}</defs>")
    for ch, xu in zip("AGI", xs):
        tr = f'translate({x0 + xu * s:.2f},{base}) scale({s:.5f},{-s:.5f})'
        d = G["g"][ch]["d"]
        sw = 3.2 / s
        if ch == "A":
            parts.append(f'<path d="{d}" transform="{tr}" fill="none" stroke="{ink}" stroke-width="{sw:.2f}" stroke-linejoin="round"/>')
        elif ch == "G":
            parts.append(f'<path d="{d}" transform="{tr}" fill="url(#hatch)" stroke="none" opacity="0.92"/>')
            parts.append(f'<path d="{d}" transform="{tr}" fill="none" stroke="{ink}" stroke-width="{sw:.2f}"/>')
        else:
            parts.append(f'<g filter="url(#ink)"><path d="{d}" transform="{tr}" fill="{ink}"/></g>')
    # compass circle on the G's bowl, and the compass point
    b = G["g"]["G"]["bounds"]; gx = x0 + (xs[1] + (b[0] + b[2]) / 2) * s; gy = base - ((b[1] + b[3]) / 2) * s
    r = ((b[3] - b[1]) / 2) * s + 6
    parts.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{r:.1f}" fill="none" stroke="{verm}" stroke-width="2.2"/>')
    parts.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="5" fill="{verm}"/>')
    parts.append(f'<line x1="{gx - 26:.1f}" y1="{gy:.1f}" x2="{gx + 26:.1f}" y2="{gy:.1f}" stroke="{verm}" stroke-width="2"/>'
                 f'<line x1="{gx:.1f}" y1="{gy - 26:.1f}" x2="{gx:.1f}" y2="{gy + 26:.1f}" stroke="{verm}" stroke-width="2"/>')
    # apex mark on the A
    ab = G["g"]["A"]["bounds"]; ax = x0 + (xs[0] + (ab[0] + ab[2]) / 2) * s
    parts.append(f'<path d="M{ax - 34:.1f},{capy - 46:.1f} L{ax:.1f},{capy - 18:.1f} L{ax + 34:.1f},{capy - 46:.1f}" fill="none" stroke="{verm}" stroke-width="2.2"/>')
    hero = "".join(parts)

    body = [f'<rect width="{W}" height="{H}" fill="{paper}"/>']
    body.append(spaced("FRAMEWORKS, NOT FORECASTS", W / 2 + 10, 300, 30, "Plex Mono", "#6f685d", 0.34, 400))
    body.append(spaced("THE", W / 2, 620, 92, fam, ink, 0.42, 500))
    body.append(hero)
    body.append(spaced("TRANSITION", W / 2 + 18, 1520, 132, fam, ink, 0.17, 560))
    # subtitle between two hairlines
    body.append(f'<line x1="{W/2 - 430}" y1="1640" x2="{W/2 + 430}" y2="1640" stroke="{ink}" stroke-width="1.6"/>')
    body.append(spaced("A Field Guide for the Next Decade", W / 2, 1735, 74, fam, ink, 0.01, 400, "italic"))
    body.append(f'<line x1="{W/2 - 430}" y1="1800" x2="{W/2 + 430}" y2="1800" stroke="{ink}" stroke-width="1.6"/>')
    body.append(spaced("PRANJUL RATHOUR", W / 2 + 14, 2330, 84, fam, ink, 0.26, 500))
    body.append(textures(False))
    return page("".join(body), css, paper)


# ------------------------------------------------------------------------------------------------ Book 2
def cover_systems() -> str:
    bg, ink, dim, amber = "#121519", "#ece8df", "#59606b", "#f0a21a"
    css = (font_face("ArchivoC", "Archivo-Condensed-800.ttf", weight="400 900")
           + font_face("ArchivoS", "Archivo-SemiBold-600.ttf", weight="400 900")
           + font_face("Bodoni Moda", "BodoniModa-TextItalic-440.ttf", "italic", "400 700")
           + font_face("Plex Mono", "IBMPlexMono-Regular.ttf", weight="400"))
    body = [f'<rect width="{W}" height="{H}" fill="{bg}"/>']
    # title: heavy condensed grotesque, stacked, optically centred
    body.append(spaced("SYSTEMS", W / 2, 560, 300, "ArchivoC", ink, -0.005, 800))
    body.append(spaced("THAT SCALE", W / 2, 830, 248, "ArchivoC", ink, 0.0, 800))
    # the partition: a square subdivided into quadrants, recursing into one corner eight times
    side = 840; sx = (W - side) / 2; sy = 960
    lines = [f'<rect x="{sx}" y="{sy}" width="{side}" height="{side}" fill="none" stroke="{ink}" stroke-width="4"/>']
    x, y, sz = sx, sy, side
    corner = [(1, 1), (0, 1), (1, 0), (1, 1), (0, 0), (1, 1), (0, 1)]  # which quadrant to recurse into, 7 levels
    for level, (cx, cy) in enumerate(corner, start=1):
        half = sz / 2
        w = max(1.0, 3.6 - 0.4 * level)
        lines.append(f'<line x1="{x + half:.2f}" y1="{y:.2f}" x2="{x + half:.2f}" y2="{y + sz:.2f}" stroke="{ink}" stroke-width="{w:.2f}"/>')
        lines.append(f'<line x1="{x:.2f}" y1="{y + half:.2f}" x2="{x + sz:.2f}" y2="{y + half:.2f}" stroke="{ink}" stroke-width="{w:.2f}"/>')
        x, y, sz = x + cx * half, y + cy * half, half
    lines.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{sz:.2f}" height="{sz:.2f}" fill="{amber}"/>')
    n_cells = 4 ** len(corner)
    lines.append(f'<text x="{sx}" y="{sy + side + 58}" font-family="Plex Mono" font-size="24" fill="{dim}" letter-spacing="0.04em">1 of {n_cells:,}</text>')
    lines.append(f'<line x1="{x + sz + 3:.1f}" y1="{y + sz:.1f}" x2="{sx + side - 6}" y2="{sy + side + 26}" stroke="{amber}" stroke-width="1.6"/>')
    lines.append(f'<text x="{sx + side}" y="{sy + side + 58}" font-family="Plex Mono" font-size="24" fill="{amber}" text-anchor="end" letter-spacing="0.04em">the one that fails</text>')
    body.append("".join(lines))
    # subtitle between hairlines
    body.append(f'<line x1="{W/2 - 520}" y1="2045" x2="{W/2 + 520}" y2="2045" stroke="{dim}" stroke-width="1.6"/>')
    body.append(spaced("The Engineering Judgment Behind", W / 2, 2112, 58, "Bodoni Moda", ink, 0.01, 400, "italic"))
    body.append(spaced("Reliable, Low-Latency Software", W / 2, 2182, 58, "Bodoni Moda", ink, 0.01, 400, "italic"))
    body.append(f'<line x1="{W/2 - 520}" y1="2230" x2="{W/2 + 520}" y2="2230" stroke="{dim}" stroke-width="1.6"/>')
    body.append(spaced("PRANJUL RATHOUR", W / 2 + 12, 2395, 78, "ArchivoS", ink, 0.28, 600))
    body.append(textures(True))
    return page("".join(body), css, bg)


def render(html: str, out_png: Path) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    src = out_png.with_suffix(".html"); src.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", f"--window-size={W},{H}", "--virtual-time-budget=4000",
                    f"--screenshot={out_png}", src.as_uri()], check=False, capture_output=True, timeout=300)
    im = Image.open(out_png).convert("RGB")
    if im.size != (W, H):
        im = im.crop((0, 0, W, H))
    im.save(out_png, optimize=True)
    im.resize((200, 320), Image.LANCZOS).save(out_png.with_name("cover-thumb.png"))
    im.resize((600, 960), Image.LANCZOS).save(out_png.with_name("cover-preview.png"))
    print("wrote", out_png, im.size)


if __name__ == "__main__":
    render(cover_agi(), HERE / "agi-transition" / "cover" / "cover.png")
    render(cover_systems(), HERE / "systems-that-scale" / "cover" / "cover.png")
