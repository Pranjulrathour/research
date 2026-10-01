"""Generate typographic e-book covers (1600 x 2560, Kindle/Play/Leanpub friendly) for both books.

Usage: python make_cover.py            -> writes <book>/cover/cover.png and a 600x960 preview for each book
Design: one typeface pair (Inter for titles, Instrument Serif italic for subtitles), one accent colour, one quiet
geometric motif per book, generous margins. No stock imagery, no gradients, no AI-art.
"""
from __future__ import annotations
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"
W, H = 1600, 2560
M = 128  # margin


def font(name: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONTS / name), size)
    if weight is not None:
        try:
            axes = f.get_variation_axes()
            vals = []
            for ax in axes:
                nm = ax["name"] if isinstance(ax["name"], str) else ax["name"].decode()
                if nm.lower().startswith("weight"):
                    vals.append(weight)
                elif nm.lower().startswith("optical"):
                    vals.append(min(max(size * 0.75, ax["minimum"]), ax["maximum"]))
                else:
                    vals.append(ax["default"])
            f.set_variation_by_axes(vals)
        except Exception as e:  # noqa
            print("variation not applied:", name, e)
    return f


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def cover_agi(out: Path):
    ink, paper, accent, muted = "#17161c", "#f4f2ec", "#ff4d2e", "#9a98a6"
    img = Image.new("RGB", (W, H), ink)
    d = ImageDraw.Draw(img)
    # motif: ten ascending ticks (a decade), bottom-left to upper-right, thin, in accent
    base_y, x0 = 1990, M
    for i in range(10):
        x = x0 + i * 92
        h = 40 + i * 26
        d.rectangle([x, base_y - h, x + 10, base_y], fill=accent if i == 9 else "#3a3944")
    # eyebrow
    eb = font("Inter-Variable.ttf", 40, 500)
    d.text((M, M + 8), "A FIELD GUIDE", font=eb, fill=muted)
    # title
    tf = font("Inter-Variable.ttf", 232, 760)
    y = M + 120
    for ln in ("The AGI", "Transition"):
        d.text((M - 10, y), ln, font=tf, fill=paper)
        y += 244
    # accent rule
    d.rectangle([M, y + 36, M + 160, y + 46], fill=accent)
    # subtitle
    sf = font("InstrumentSerif-Italic.ttf", 92)
    lines = wrap(d, "A Field Guide for the Next Decade", sf, W - 2 * M)
    text_block(d, M, y + 110, lines, sf, paper, 100)
    # descriptor
    df = font("Inter-Variable.ttf", 38, 400)
    desc = wrap(d, "Frameworks, not forecasts: capability, work, learning, governance, agents and your own career, 2026–2036. Written from India.", df, W - 2 * M - 120)
    text_block(d, M, 1560, desc, df, muted, 52)
    # author
    af = font("Inter-Variable.ttf", 56, 600)
    d.text((M, H - M - 140), "PRANJUL RATHOUR", font=af, fill=paper)
    sm = font("Inter-Variable.ttf", 34, 400)
    d.text((M, H - M - 60), "pranjulrathour.scult.in", font=sm, fill=muted)
    img.save(out / "cover.png", optimize=True)
    img.resize((600, 960), Image.LANCZOS).save(out / "cover-preview.png")


def cover_systems(out: Path):
    ink, paper, accent, muted = "#1c1b22", "#f4f3ef", "#1f6feb", "#6d6c78"
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)
    # motif: a long-tailed latency distribution, thin ink line with the tail in accent
    pts = []
    x0, x1, base, top = M, W - M, 2000, 1620
    for i in range(0, 801):
        t = i / 800
        # log-normal-ish shape: fast rise, long tail
        v = (t ** 1.6) * math.exp(-t * 7.5) * 7.5 ** 1.6 / 1.6 ** 1.6 * math.e ** 1.6
        pts.append((x0 + (x1 - x0) * t, base - (base - top) * v))
    peak_i = max(range(len(pts)), key=lambda i: -pts[i][1])
    d.line(pts[: peak_i + 120], fill=ink, width=7, joint="curve")
    d.line(pts[peak_i + 119:], fill=accent, width=7, joint="curve")
    d.line([(x0, base + 2), (x1, base + 2)], fill="#d8d7d2", width=3)
    # p50 / p99 markers
    mk = font("Inter-Variable.ttf", 30, 500)
    for frac, label in ((0.22, "p50"), (0.82, "p99")):
        x = x0 + (x1 - x0) * frac
        d.line([(x, base + 2), (x, base + 26)], fill=ink, width=3)
        d.text((x - 24, base + 34), label, font=mk, fill=muted)
    # eyebrow
    eb = font("Inter-Variable.ttf", 40, 500)
    d.text((M, M + 8), "ENGINEERING JUDGMENT, MEASURED", font=eb, fill=muted)
    # title
    tf = font("Inter-Variable.ttf", 220, 760)
    y = M + 120
    for ln in ("Systems", "That Scale"):
        d.text((M - 10, y), ln, font=tf, fill=ink)
        y += 232
    d.rectangle([M, y + 36, M + 160, y + 46], fill=accent)
    sf = font("InstrumentSerif-Italic.ttf", 84)
    lines = wrap(d, "The Engineering Judgment Behind Reliable, Low-Latency Software", sf, W - 2 * M)
    text_block(d, M, y + 110, lines, sf, ink, 92)
    af = font("Inter-Variable.ttf", 56, 600)
    d.text((M, H - M - 140), "PRANJUL RATHOUR", font=af, fill=ink)
    sm = font("Inter-Variable.ttf", 34, 400)
    d.text((M, H - M - 60), "pranjulrathour.scult.in", font=sm, fill=muted)
    img.save(out / "cover.png", optimize=True)
    img.resize((600, 960), Image.LANCZOS).save(out / "cover-preview.png")


if __name__ == "__main__":
    for slug, fn in (("agi-transition", cover_agi), ("systems-that-scale", cover_systems)):
        out = HERE / slug / "cover"; out.mkdir(exist_ok=True)
        fn(out); print("wrote", out / "cover.png")
