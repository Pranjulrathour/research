"""Shared figure style for the papers: STIX Two (the journal serif used for the text), ink plus one accent, hairlines.
Import and call apply() before plotting; every figure in every paper uses it so the set reads as one piece of work."""
from pathlib import Path

import matplotlib
from matplotlib import font_manager as fm

FONTS = Path(__file__).resolve().parent.parent / "books" / "assets" / "fonts"
INK, MID, LIGHT, RULE = "#1a1a1d", "#66646c", "#b8b6bd", "#e4e3e7"
ACCENT, ACCENT2 = "#b8401f", "#2f5d8a"
SERIES = [INK, ACCENT, "#7a7880", ACCENT2, "#c9a227", "#9a9aa2"]


def apply(base_size: float = 9.0) -> None:
    for f in ("STIXTwoText-Regular.ttf", "STIXTwoText-Bold.ttf", "STIXTwoText-Italic.ttf", "STIXTwoText-BoldItalic.ttf"):
        p = FONTS / f
        if p.exists():
            fm.fontManager.addfont(str(p))
    matplotlib.rcParams.update({
        "font.family": "STIX Two Text", "mathtext.fontset": "stix", "font.size": base_size,
        "axes.titlesize": base_size + 0.5, "axes.labelsize": base_size, "xtick.labelsize": base_size - 0.5,
        "ytick.labelsize": base_size - 0.5, "legend.fontsize": base_size - 0.5, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.7, "axes.edgecolor": INK,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.8, "ytick.major.size": 2.8,
        "axes.prop_cycle": matplotlib.cycler(color=SERIES), "axes.grid": False, "grid.color": RULE, "grid.linewidth": 0.5,
        "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.05, "figure.dpi": 100,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": MID, "ytick.color": MID,
    })
