"""Figures for both books: one visual system (Inter, ink + one accent, hairline strokes, generous white space).

Usage:  python figures.py [agi|systems|all]   -> books/<book>/figures/*.png

Charts plot exact formulas (stated in each function). Schematics carry no numbers unless a number is quoted in the
text with its source; the captions in the chapters say which is which.
"""
from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle, Wedge
import numpy as np

HERE = Path(__file__).resolve().parent
for n in ("Regular", "Medium", "SemiBold", "Bold"):
    fm.fontManager.addfont(str(HERE / "assets" / "fonts" / f"Inter-{n}.ttf"))
fm.fontManager.addfont(str(HERE / "assets" / "fonts" / "IBMPlexMono-Regular.ttf"))

INK, MID, LIGHT, RULE, PAPER = "#16161a", "#6e6c73", "#b9b7bd", "#e6e4e8", "#ffffff"
ACCENT = {"agi": "#c8432b", "systems": "#d4860b"}
TINT = {"agi": "#f6e3dd", "systems": "#f8ecd6"}
W_IN, DPI = 7.2, 250

plt.rcParams.update({
    "font.family": "Inter", "font.size": 9.5, "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": MID, "ytick.color": MID, "axes.linewidth": 0.8, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "xtick.major.size": 3, "ytick.major.size": 3, "axes.spines.top": False, "axes.spines.right": False,
    "savefig.facecolor": PAPER, "figure.facecolor": PAPER, "axes.facecolor": PAPER, "legend.frameon": False,
})


def save(fig, book: str, name: str):
    out = HERE / ("agi-transition" if book == "agi" else "systems-that-scale") / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("wrote", out / f"{name}.png")


def blank(h_in: float):
    fig = plt.figure(figsize=(W_IN, h_in))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100 * h_in / W_IN); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", fc=PAPER, ec=INK, lw=0.9, size=9.5, weight=500, color=INK, r=1.2, ha="center", **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if text:
        tx = x + w / 2 if ha == "center" else x + 1.6
        ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=size, fontweight=weight, color=color, linespacing=1.35, **kw)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=0.9, style="-|>", ms=8, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def label(ax, x, y, s, size=8.5, color=MID, weight=400, ha="left", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, **kw)


# ================================================================================================ Book 1
def agi_levels_map():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(4.6)
    levels = ["Superhuman", "Virtuoso", "Expert", "Competent", "Emerging"]
    pct = ["beats every person", "99th percentile", "90th percentile", "median skilled adult", "≈ unskilled person"]
    narrow = ["AlphaFold, AlphaZero, Stockfish", "Deep Blue, AlphaGo", "grammar checkers,\nimage generators",
              "voice assistants, LLMs on\nsome narrow tasks", "early rule-based systems"]
    general = ["not yet achieved", "not yet achieved", "not yet achieved", "not yet achieved", "2023 chatbots\n(ChatGPT, Gemini, Llama 2)"]
    x0, cw, rh, top = 31, 33, 10.2, 58
    label(ax, x0 + cw / 2, top + 3.2, "NARROW", 8.5, INK, 600, ha="center")
    label(ax, x0 + cw + 1.5 + cw / 2, top + 3.2, "GENERAL", 8.5, INK, 600, ha="center")
    label(ax, x0 + cw / 2, top + 0.6, "a clearly scoped task", 7.8, MID, ha="center")
    label(ax, x0 + cw + 1.5 + cw / 2, top + 0.6, "a wide range of non-physical tasks", 7.8, MID, ha="center")
    for i, (lv, p, n, g) in enumerate(zip(levels, pct, narrow, general)):
        y = top - 2 - (i + 1) * rh
        label(ax, 2, y + rh / 2 + 1.6, lv, 9.5, INK, 600)
        label(ax, 2, y + rh / 2 - 2.0, p, 7.8, MID)
        box(ax, x0, y + 0.6, cw, rh - 1.2, n, fc="#f7f6f8", ec=RULE, lw=0.8, size=8.2, weight=400)
        hit = g.startswith("2023")
        box(ax, x0 + cw + 1.5, y + 0.6, cw, rh - 1.2, g, fc=T if hit else PAPER, ec=A if hit else RULE, lw=1.0 if hit else 0.8,
            size=8.2, weight=500 if hit else 400, color=INK if hit else LIGHT)
    arrow(ax, 27.5, top - 2 - 5 * rh + 1, 27.5, top - 3, MID, 0.8)
    label(ax, 26.2, top - 2 - 2.5 * rh, "performance", 7.8, MID, ha="right", rotation=90)
    label(ax, 2, 2.2, "Placements as given by Morris et al. (2023). Autonomy is a separate, deployment-time choice.", 7.6, MID)
    save(fig, "agi", "fig01_levels_map")


def agi_saturation():
    A = ACCENT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.3))
    t = np.linspace(0, 10, 400)
    s = 25 + 68.5 / (1 + np.exp(-(t - 4.2) * 1.15))
    ax.plot(t, s, color=INK, lw=1.6)
    ax.axhline(100, color=LIGHT, lw=0.8)
    ax.axhspan(93.5, 100, color=TINT["agi"], lw=0)
    ax.text(9.95, 96.7, "label-error floor: questions with no right answer", ha="right", va="center", fontsize=8, color=A)
    ax.annotate("scores spread out:\ndifferences mean something", xy=(3.2, s[np.searchsorted(t, 3.2)]), xytext=(0.3, 72),
                fontsize=8.3, color=INK, arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.annotate("near the ceiling: gaps between systems\nare smaller than the instrument's noise", xy=(8.2, s[np.searchsorted(t, 8.2)]),
                xytext=(5.3, 58), fontsize=8.3, color=INK, arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(0, 10); ax.set_ylim(15, 104); ax.set_xticks([]); ax.set_yticks([25, 50, 75, 100])
    ax.set_xlabel("time since the benchmark was released", color=MID, fontsize=8.5)
    ax.set_ylabel("best reported score (%)", color=MID, fontsize=8.5)
    ax.text(0, 106, "Schematic", fontsize=7.5, color=MID)
    save(fig, "agi", "fig02_saturation")


def agi_four_channels():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.5)
    box(ax, 2, 20, 20, 12, "A task is\nautomated", fc="#f7f6f8", ec=INK, size=10, weight=600)
    rows = [("Displacement", "demand for people on that task falls", "−", "immediate"),
            ("Productivity", "the other tasks around it become worth more", "+", "months"),
            ("New tasks", "work that did not exist before", "+", "years"),
            ("Demand", "cheaper output, more of it bought", "+", "years")]
    for i, (name, desc, sign, when) in enumerate(rows):
        y = 39 - i * 9.4
        arrow(ax, 22, 26, 31, y + 3.6, MID, 0.8)
        box(ax, 31, y, 46, 7.4, "", fc=PAPER, ec=RULE if i else A, lw=0.9 if i else 1.1)
        label(ax, 33, y + 4.9, name, 9.4, INK, 600)
        label(ax, 33, y + 2.2, desc, 8.0, MID)
        label(ax, 74.8, y + 3.7, sign, 13, A if sign == "−" else INK, 600, ha="right")
        label(ax, 79, y + 3.7, when, 7.8, MID)
    box(ax, 31, 1.2, 46, 6.0, "net effect on workers = the sum of all four", fc=T, ec=A, size=8.8, weight=600)
    label(ax, 79, 47.6, "shows up", 7.6, MID, 600)
    save(fig, "agi", "fig03_four_channels")


def agi_entry_ladder():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.6)
    rungs = [("Accountability", "signing off, carrying the consequences"),
             ("Independent judgement", "deciding what to do, unsupervised"),
             ("Supervised judgement", "deciding, with someone checking"),
             ("Routine tasks", "document review, test writing, first drafts")]
    x0, w = 22, 46
    ax.plot([x0, x0], [4, 46], color=INK, lw=1.4); ax.plot([x0 + w, x0 + w], [4, 46], color=INK, lw=1.4)
    for i, (name, desc) in enumerate(rungs):
        y = 41 - i * 11
        bottom = i == 3
        yy = 6.0 if bottom else y
        ax.plot([x0, x0 + w], [yy, yy], color=A if bottom else INK, lw=1.1 if bottom else 2.2, ls=(0, (3, 2.5)) if bottom else "-")
        label(ax, x0 + w + 4, y + 1.5, name, 9.4, INK, 600)
        label(ax, x0 + w + 4, y - 1.6, desc, 7.9, MID)
    ax.add_patch(Rectangle((x0 + 0.6, 4), w - 1.2, 9.5, fc=T, ec="none"))
    label(ax, x0 + w / 2, 10.2, "where current tools are strongest", 8.2, A, 500, ha="center")
    label(ax, 2, 8.6, "how juniors\nhave always\nlearned", 8, MID)
    arrow(ax, 13.5, 8.6, x0 - 1.5, 8.6, MID, 0.8)
    save(fig, "agi", "fig04_entry_ladder")


def agi_proof_practice():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.4)
    label(ax, 2, 44, "Before 2022", 9.5, INK, 600)
    box(ax, 6, 20, 22, 11, "the essay", fc="#f7f6f8", size=10, weight=600)
    arrow(ax, 17, 31, 17, 39, MID); label(ax, 19, 37, "teaches the student", 8, INK)
    arrow(ax, 28, 25.5, 36, 25.5, MID); label(ax, 37, 25.5, "proves learning", 8, INK)
    label(ax, 37, 22.4, "to the teacher", 8, MID)
    ax.plot([50, 50], [4, 46], color=RULE, lw=0.9)
    label(ax, 54, 44, "After", 9.5, INK, 600)
    box(ax, 56, 31, 18, 8, "the essay", fc="#f7f6f8", size=9.5, weight=600)
    arrow(ax, 74, 35, 79, 35, MID); label(ax, 80, 36.2, "still teaches,", 8, INK); label(ax, 80, 33.4, "if you write it", 8, MID)
    label(ax, 56, 24.5, "proof now comes from elsewhere", 8.2, A, 500)
    for i, s in enumerate(["oral examination", "supervised work", "process evidence", "verifiable portfolio"]):
        box(ax, 56 + (i % 2) * 21.5, 13 - (i // 2) * 8.4, 20, 6.6, s, fc=T, ec=A, lw=0.8, size=8.1, weight=500)
    save(fig, "agi", "fig05_proof_and_practice")


def agi_bottleneck():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.45)
    stages = ["Literature", "Code", "Search &\nsimulation", "Experiment", "Verification", "Review &\npublication"]
    before = [6, 7, 8, 9, 8, 7]
    after = [1.3, 1.6, 1.4, 8.6, 9.5, 8.0]
    for i, (s, b, a) in enumerate(zip(stages, before, after)):
        x = 3 + i * 16
        box(ax, x, 4, 13.5, 8.5, s, fc="#f7f6f8" if i < 3 else PAPER, ec=RULE if i != 4 else A, lw=0.8 if i != 4 else 1.2, size=8.4, weight=500)
        if i < 5:
            arrow(ax, x + 13.5, 8.25, x + 16, 8.25, MID, 0.7, ms=6)
        ax.add_patch(Rectangle((x + 3.3, 15), 2.6, b * 2.6, fc=LIGHT, ec="none"))
        ax.add_patch(Rectangle((x + 7.3, 15), 2.6, a * 2.6, fc=A if i == 4 else INK, ec="none"))
    label(ax, 3, 46.5, "time each stage takes", 8.2, MID)
    ax.add_patch(Rectangle((30, 45.5), 2, 2, fc=LIGHT)); label(ax, 33, 46.5, "before", 8, MID)
    ax.add_patch(Rectangle((42, 45.5), 2, 2, fc=INK)); label(ax, 45, 46.5, "after", 8, MID)
    label(ax, 99, 46.5, "Schematic", 7.5, MID, ha="right")
    label(ax, 3 + 4 * 16 + 8.6, 15 + 9.5 * 2.6 + 2.2, "the bottleneck moves here", 8.2, A, 600, ha="center")
    save(fig, "agi", "fig06_bottleneck")


def agi_five_questions():
    A = ACCENT["agi"]
    fig, ax = blank(3.9)
    qs = ["Which uses are treated differently?", "What must be disclosed?", "Who checks?", "Is there a size threshold?", "Who pays when it fails?"]
    cols = ["EU", "US", "China", "India"]
    # 2 = binding rule in force or enacted; 1 = partial / sectoral / state-level / voluntary; 0 = no AI-specific rule
    grid = [[2, 1, 1, 0], [2, 1, 2, 1], [2, 1, 2, 1], [2, 1, 0, 0], [1, 0, 1, 1]]
    notes = [["four risk tiers", "state laws", "by service type", "—"], ["GPAI docs, labels", "state laws", "labels, filing", "synthetic-content rules"],
             ["conformity, AI Office", "NIST RMF (voluntary)", "state assessment", "voluntary"], ["10²⁵ FLOP", "CA SB 53: 10²⁶", "—", "—"],
             ["Product Liability Dir.", "existing law", "civil code", "existing law"]]
    x0, cw, top, rh = 36, 15.6, 42, 7.4
    for j, c in enumerate(cols):
        label(ax, x0 + j * cw + cw / 2, top + 3, c, 9.5, INK, 600, ha="center")
    for i, q in enumerate(qs):
        y = top - (i + 1) * rh
        ax.plot([2, 98], [y + rh, y + rh], color=RULE, lw=0.7)
        label(ax, 2, y + rh / 2, q, 8.8, INK, 500)
        for j, v in enumerate(grid[i]):
            cx = x0 + j * cw + cw / 2
            ax.add_patch(Circle((cx, y + rh / 2 + 1.1), 1.35, fc=PAPER, ec=INK, lw=0.9))
            if v == 2:
                ax.add_patch(Circle((cx, y + rh / 2 + 1.1), 1.35, fc=INK, ec=INK, lw=0.9))
            elif v == 1:
                ax.add_patch(Wedge((cx, y + rh / 2 + 1.1), 1.35, 90, 270, fc=INK, ec="none"))
            label(ax, cx, y + rh / 2 - 1.75, notes[i][j], 6.6, MID, ha="center")
    ax.plot([2, 98], [top - 5 * rh, top - 5 * rh], color=RULE, lw=0.7)
    y = 2.0
    for k, (v, t) in enumerate([(2, "binding rule in force or enacted"), (1, "partial, sectoral, state-level or voluntary"), (0, "no AI-specific rule")]):
        cx = 3.5 + k * 32
        ax.add_patch(Circle((cx, y), 1.1, fc=INK if v == 2 else PAPER, ec=INK, lw=0.8))
        if v == 1:
            ax.add_patch(Wedge((cx, y), 1.1, 90, 270, fc=INK, ec="none"))
        label(ax, cx + 2.2, y, t, 7.6, MID)
    label(ax, 98, top + 7.2, "as of October 2026", 7.5, MID, ha="right")
    save(fig, "agi", "fig07_five_questions")


def agi_trifecta():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.9)
    centres = [(40, 34), (60, 34), (50, 17.5)]
    names = [("access to\nprivate data", (27, 40)), ("exposure to\nuntrusted content", (73, 40)), ("ability to\ncommunicate outside", (50, 9.0))]
    for (cx, cy) in centres:
        ax.add_patch(Circle((cx, cy), 15, fc="none", ec=INK, lw=1.0))
    for s, (x, y) in names:
        label(ax, x, y, s, 8.8, INK, 500, ha="center")
    ax.add_patch(Circle((50, 28.5), 4.2, fc=T, ec=A, lw=1.1))
    label(ax, 50, 28.5, "leak\nrisk", 7.8, A, 600, ha="center")
    label(ax, 82, 18, "Any two can be\nmade safe. All three\nis a design decision\nto revisit.", 8.2, MID)
    save(fig, "agi", "fig08_lethal_trifecta")


def agi_reliability():
    A = ACCENT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.5))
    n = np.arange(1, 51)
    for p, c, lw in ((0.999, INK, 1.2), (0.99, INK, 1.2), (0.95, A, 1.8), (0.90, MID, 1.2)):
        ax.plot(n, p ** n * 100, color=c, lw=lw)
        ax.text(50.8, p ** 50 * 100, f"{p:.1%} per step".replace(".0%", "%"), fontsize=8.2, color=c, va="center")
    ax.plot([10], [0.95 ** 10 * 100], "o", color=A, ms=4.5)
    ax.annotate(f"10 steps at 95%: {0.95**10:.0%} of tasks finish correctly", xy=(10, 0.95 ** 10 * 100), xytext=(23, 52),
                fontsize=8.3, color=INK, arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(1, 50); ax.set_ylim(0, 102); ax.set_xticks([1, 10, 20, 30, 40, 50])
    ax.set_xlabel("steps in the task, n", color=MID, fontsize=8.5); ax.set_ylabel("tasks completed correctly (%)", color=MID, fontsize=8.5)
    ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    save(fig, "agi", "fig09_reliability")


def agi_three_layers():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.3)
    layers = [("Judgement", "framing the problem · verifying the output · taste"),
              ("Systems", "how the parts fit, fail and scale"),
              ("Domain depth", "knowing what the field actually needs")]
    for i, (name, desc) in enumerate(layers):
        y = 26 - i * 10.5
        box(ax, 22, y, 56, 8.6, "", fc="#f7f6f8", ec=INK if i == 0 else RULE, lw=1.0)
        label(ax, 25, y + 5.5, name, 10, INK, 600)
        label(ax, 25, y + 2.5, desc, 8.1, MID)
    box(ax, 22, 37.5, 56, 6.2, "AI tools", fc=T, ec=A, lw=1.0, size=9.5, weight=600, color=A)
    for x in (32, 50, 68):
        arrow(ax, x, 37.3, x, 35.0, A, 0.8, ms=6)
    label(ax, 80.5, 40.6, "amplify what is\nunderneath", 8.0, MID)
    label(ax, 80.5, 15, "the layers that\ncompound", 8.0, MID)
    save(fig, "agi", "fig10_three_layers")


def agi_dpi_stack():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.8)
    box(ax, 10, 41, 80, 7, "AI applications for Indian users, in Indian languages", fc=T, ec=A, lw=1.1, size=9.5, weight=600, color=INK)
    rows = [("Commerce", "ONDC", "open network for buying and selling"),
            ("Data", "Account Aggregator · DigiLocker", "consent-based sharing of records"),
            ("Payments", "UPI", "≈ 18–20 bn transactions a month (2025)"),
            ("Identity", "Aadhaar", "1.3 bn+ enrolments")]
    for i, (layer, name, note) in enumerate(rows):
        y = 31 - i * 8.6
        box(ax, 10, y, 80, 7, "", fc="#f7f6f8", ec=RULE, lw=0.8)
        label(ax, 13, y + 3.5, layer.upper(), 7.6, MID, 600)
        label(ax, 33, y + 3.5, name, 9.4, INK, 600)
        label(ax, 88, y + 3.5, note, 8.0, MID, ha="right")
    label(ax, 10, 1.6, "Figures from UIDAI and NPCI; see chapter sources.", 7.5, MID)
    save(fig, "agi", "fig11_dpi_stack")


def agi_diffusion():
    A = ACCENT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.4))
    rows = [("Electricity", 1882, 1925, "first central power stations → factory productivity gains"),
            ("Computing", 1970, 1997, "business computing → the late-1990s productivity surge"),
            ("The internet", 1993, 2008, "commercial web → search, platforms, cloud, smartphones"),
            ("Generative AI", 2022, None, "")]
    for i, (name, a, b, note) in enumerate(rows):
        y = len(rows) - 1 - i
        if b:
            ax.plot([a, b], [y, y], color=INK, lw=5, solid_capstyle="butt")
            ax.text(b + 1.5, y, f"~{b - a} years", va="center", fontsize=8.3, color=INK, fontweight=600)
        else:
            ax.plot([a, a + 14], [y, y], color=A, lw=5, solid_capstyle="butt", ls=(0, (1.2, 1.0)))
            ax.text(a + 15.5, y, "?", va="center", fontsize=11, color=A, fontweight=600)
        ax.plot([a], [y], "o", color=A if not b else INK, ms=5)
        ax.text(a, y - 0.34, note, fontsize=7.6, color=MID, va="top")
    ax.set_xlim(1876, 2045); ax.set_ylim(-0.8, 3.5)
    ax.set_yticks([3, 2, 1, 0]); ax.set_yticklabels([r[0] for r in rows], fontsize=9, fontweight=600, color=INK)
    ax.tick_params(axis="y", length=0)
    ax.set_xticks([1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020, 2040]); ax.spines["left"].set_visible(False)
    ax.text(2045, 3.4, "dates approximate", ha="right", fontsize=7.5, color=MID)
    save(fig, "agi", "fig12_diffusion")


# ================================================================================================ Book 2
def sys_tail_at_scale():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.3))
    n = np.arange(1, 201)
    ax.plot(n, (1 - 0.99 ** n) * 100, color=A, lw=1.8)
    ax.plot(n, (1 - 0.999 ** n) * 100, color=INK, lw=1.2)
    ax.text(201, (1 - 0.99 ** 200) * 100, "each server's p99 tail", fontsize=8.2, color=A, va="center")
    ax.text(201, (1 - 0.999 ** 200) * 100, "each server's p99.9 tail", fontsize=8.2, color=INK, va="center")
    ax.plot([100], [(1 - 0.99 ** 100) * 100], "o", color=A, ms=4.5)
    ax.annotate(f"fan out to 100 servers: {1 - 0.99**100:.0%} of requests\nwait for at least one slow reply",
                xy=(100, (1 - 0.99 ** 100) * 100), xytext=(112, 38), fontsize=8.3, color=INK, arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(1, 200); ax.set_ylim(0, 100); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("servers a request waits on (fan-out)", color=MID, fontsize=8.5)
    ax.set_ylabel("requests that hit a tail (%)", color=MID, fontsize=8.5)
    save(fig, "systems", "fig01_tail_at_scale")


def sys_concurrency():
    A, T = ACCENT["systems"], TINT["systems"]
    fig, ax = blank(3.9)

    def lane(y, segs, name=None):
        ax.plot([20, 98], [y, y], color=RULE, lw=0.6, zorder=0)
        if name:
            label(ax, 19, y, name, 7.8, MID, ha="right")
        for (a, b, kind) in segs:
            if kind == "work":
                ax.add_patch(Rectangle((a + 0.25, y - 1.3), b - a - 0.5, 2.6, fc=INK, ec="none"))
            elif kind == "cpu":
                ax.add_patch(Rectangle((a + 0.25, y - 1.3), b - a - 0.5, 2.6, fc=A, ec="none"))
            else:
                ax.add_patch(Rectangle((a, y - 1.3), b - a, 2.6, fc=PAPER, ec=LIGHT, lw=0.6, hatch="////"))
    label(ax, 2, 49, "Thread per request", 9.4, INK, 600)
    for k in range(3):
        lane(44 - k * 4, [(22 + k * 3, 25 + k * 3, "work"), (25 + k * 3, 45 + k * 3, "wait"), (45 + k * 3, 48 + k * 3, "work")], f"thread {k + 1}")
    label(ax, 2, 30, "Event loop", 9.4, INK, 600)
    lane(25, [(22, 25, "work"), (25, 28, "work"), (28, 31, "work"), (31, 55, "cpu"), (55, 58, "work"), (58, 61, "work"), (61, 64, "work")], "one loop")
    ax.annotate("CPU work inline: every other\nconnection waits behind it", xy=(43, 26.5), xytext=(66, 30.5), fontsize=7.9, color=A,
                arrowprops=dict(arrowstyle="-", color=A, lw=0.7))
    label(ax, 2, 16, "Hybrid", 9.4, INK, 600)
    lane(11, [(22, 25, "work"), (25, 28, "work"), (28, 31, "work"), (31, 34, "work"), (34, 37, "work"), (37, 40, "work"), (40, 43, "work"), (43, 46, "work"), (55, 58, "work")], "loop")
    lane(6, [(31, 55, "cpu")], "worker")
    arrow(ax, 32, 9.5, 32, 7.6, MID, 0.6, ms=5)
    for k, (kind, t) in enumerate([("work", "handling a request"), ("wait", "waiting on IO"), ("cpu", "CPU-bound work")]):
        x = 22 + k * 25
        if kind == "work":
            ax.add_patch(Rectangle((x, 0.6), 3, 2.2, fc=INK))
        elif kind == "cpu":
            ax.add_patch(Rectangle((x, 0.6), 3, 2.2, fc=A))
        else:
            ax.add_patch(Rectangle((x, 0.6), 3, 2.2, fc=PAPER, ec=LIGHT, lw=0.6, hatch="////"))
        label(ax, x + 4, 1.7, t, 7.8, MID)
    label(ax, 98, 49, "time →", 7.8, MID, ha="right")
    save(fig, "systems", "fig02_concurrency_models")


def sys_hit_rate():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.2))
    p = np.linspace(0, 0.999, 600); h, m = 1.0, 50.0
    ax.plot(p * 100, p * h + (1 - p) * m, color=INK, lw=1.6, label="average latency")
    p99 = np.where(p < 0.99, m, h)
    ax.plot(p * 100, p99, color=A, lw=1.8, drawstyle="steps-post", label="p99 latency")
    ax.text(98, 52.2, "p99 stays at the miss latency until misses fall below 1%", fontsize=8.2, color=A, ha="right")
    ax.text(1, 59.5, "average = p·h + (1 − p)·m,  with h = 1 ms (hit) and m = 50 ms (miss)", fontsize=8.2, color=INK)
    ax.set_xlim(0, 100); ax.set_ylim(0, 63); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("cache hit rate (%)", color=MID, fontsize=8.5); ax.set_ylabel("latency (ms)", color=MID, fontsize=8.5)
    ax.legend(loc="lower left", fontsize=8.2)
    save(fig, "systems", "fig03_hit_rate")


def sys_memory_hierarchy():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.3))
    rows = [("L1 cache reference", 1e-9), ("L2 cache reference", 4e-9), ("main memory reference", 100e-9),
            ("SSD random read", 16e-6), ("round trip in one datacentre", 500e-6), ("disk seek", 2e-3),
            ("packet round trip across continents", 150e-3)]
    for i, (name, t) in enumerate(rows[::-1]):
        ax.barh(i, t, color=A if "memory" in name else INK, height=0.52, left=0)
        lab = f"{t*1e9:.0f} ns" if t < 1e-6 else (f"{t*1e6:.0f} µs" if t < 1e-3 else f"{t*1e3:.0f} ms")
        ax.text(t * 1.4, i, lab, va="center", fontsize=8.2, color=INK)
        ax.text(3e-10 * 0.9, i, name, va="center", ha="right", fontsize=8.4, color=INK)
    ax.set_xscale("log"); ax.set_xlim(3e-10, 3); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xticks([1e-9, 1e-6, 1e-3, 1]); ax.set_xticklabels(["1 ns", "1 µs", "1 ms", "1 s"])
    ax.text(3, 6.6, "approximate, 2020s hardware; each step is roughly 100× the last", ha="right", fontsize=7.5, color=MID)
    fig.subplots_adjust(left=0.36)
    save(fig, "systems", "fig04_memory_hierarchy")


def sys_consistency():
    A, T = ACCENT["systems"], TINT["systems"]
    fig, ax = blank(3.1)
    models = ["Linearizable", "Sequential", "Causal", "Session\n(read-your-writes,\nmonotonic reads)", "Eventual"]
    promise = ["never stale", "one agreed order", "no effect before\nits cause", "you see your\nown writes", "copies agree\neventually"]
    examples = ["Spanner, etcd,\nZooKeeper", "", "COPS", "edge routing,\nversion tokens", "Dynamo-style stores,\nreplica reads"]
    for i, (m, pr, ex) in enumerate(zip(models, promise, examples)):
        x = 4 + i * 19
        ax.add_patch(Circle((x + 7, 27), 1.4, fc=INK if i == 0 else (A if i == 3 else PAPER), ec=INK, lw=0.9))
        label(ax, x + 7, 33.5, m, 8.6, INK, 600, ha="center", va="bottom")
        label(ax, x + 7, 21.5, pr, 7.9, INK, ha="center", va="top")
        label(ax, x + 7, 9.5, ex, 7.3, MID, ha="center", va="top")
    ax.plot([11, 87], [27, 27], color=INK, lw=0.9, zorder=0)
    arrow(ax, 82, 44, 18, 44, MID, 0.8)
    label(ax, 50, 46.5, "more coordination: more latency, less availability during a partition", 7.9, MID, ha="center")
    save(fig, "systems", "fig05_consistency_spectrum")


def sys_idempotency():
    A, T = ACCENT["systems"], TINT["systems"]
    fig, ax = blank(3.9)
    cols = [("Client", 12), ("Payment service", 50), ("Ledger + key table", 86)]
    for name, x in cols:
        box(ax, x - 11, 45, 22, 5.2, name, fc="#f7f6f8", ec=RULE, size=8.6, weight=600)
        ax.plot([x, x], [5, 45], color=LIGHT, lw=0.8, ls=(0, (2, 2)))
    def msg(y, a, b, text, color=INK, lost=False):
        arrow(ax, a, y, b, y, color, 0.9, ms=7)
        label(ax, (a + b) / 2, y + 1.5, text, 7.8, color, ha="center")
        if lost:
            label(ax, (a + b) / 2, y - 1.7, "× response lost", 7.8, A, 600, ha="center")
    msg(40, 12, 50, "charge ₹500, key K1")
    msg(35, 50, 86, "write charge + K1 atomically")
    msg(30, 50, 12, "200 OK", MID, lost=True)
    label(ax, 2, 24.5, "timeout, retry", 7.8, INK, 500)
    msg(20, 12, 50, "charge ₹500, key K1 (retry)")
    msg(15, 50, 86, "look up K1: already done")
    msg(10, 50, 12, "200 OK (the stored result)")
    box(ax, 62, 4, 36, 6.0, "charged once", fc=T, ec=A, size=8.6, weight=600)
    save(fig, "systems", "fig06_idempotency")


def sys_availability():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.3))
    n = np.arange(1, 51)
    for a, c, lw in ((0.9999, INK, 1.2), (0.9995, MID, 1.2), (0.999, A, 1.8)):
        ax.plot(n, a ** n * 100, color=c, lw=lw)
        ax.text(50.8, a ** 50 * 100, f"each {a*100:g}%", fontsize=8.2, color=c, va="center")
    v = 0.999 ** 10
    ax.plot([10], [v * 100], "o", color=A, ms=4.5)
    hours = (1 - v) * 30 * 24
    ax.annotate(f"10 required dependencies at 99.9%: {v:.1%}\n≈ {hours:.0f} hours of downtime a month", xy=(10, v * 100), xytext=(3, 95.0),
                fontsize=8.3, color=INK, arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(1, 50); ax.set_ylim(94.5, 100.05); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("dependencies every request needs", color=MID, fontsize=8.5); ax.set_ylabel("best-case availability (%)", color=MID, fontsize=8.5)
    save(fig, "systems", "fig07_availability")


def sys_queue_depth():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.2))
    t = np.arange(0, 301)
    ax.plot(t, 200 * t, color=A, lw=1.8)
    ax.text(8, 58000, "arrivals 1,000/s, service 800/s:\ngrows by 200 every second, forever", ha="left", va="top", fontsize=8.2, color=A)
    burst = np.zeros_like(t, dtype=float); q = 0.0
    for i in t:
        arr = 1500 if i < 60 else 600
        q = max(0.0, q + arr - 1000); burst[i] = q
    ax.plot(t, burst, color=INK, lw=1.4)
    ax.text(140, 9000, "a one-minute burst at 1,500/s against\n1,000/s of service: absorbed, then drained", fontsize=8.2, color=INK)
    ax.plot(t, np.zeros_like(t), color=MID, lw=1.2)
    ax.text(300, 1500, "service 1,200/s: stays near zero", ha="right", fontsize=8.2, color=MID)
    ax.set_xlim(0, 300); ax.set_ylim(-2000, 62000); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("seconds", color=MID, fontsize=8.5); ax.set_ylabel("messages waiting", color=MID, fontsize=8.5)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k" if v else "0"))
    save(fig, "systems", "fig08_queue_depth")


def sys_error_budget():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.2))
    budget = 0.001 * 30 * 24 * 60
    d = np.linspace(0, 30, 600)
    for rate, c, lw, name in ((1, INK, 1.4, "burn rate 1: budget lasts the window"), (2, MID, 1.2, "burn rate 2: gone in 15 days"),
                              (14.4, A, 1.8, "burn rate 14.4: gone in about 2 days")):
        rem = np.clip(budget - budget * rate * d / 30, 0, None)
        ax.plot(d, rem, color=c, lw=lw)
        pos = {1: (17.5, 24.0), 2: (15.5, 1.4), 14.4: (2.4, 4.0)}[rate]
        ax.text(*pos, name, fontsize=8.0, color=c)
    ax.set_xlim(0, 30); ax.set_ylim(0, budget * 1.08)
    ax.set_xlabel("days into the 30-day window", color=MID, fontsize=8.5); ax.set_ylabel("error budget left (minutes)", color=MID, fontsize=8.5)
    ax.text(0.3, budget * 1.03, f"SLO 99.9% over 30 days → {budget:.1f} minutes of budget", fontsize=8.2, color=INK)
    ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    save(fig, "systems", "fig09_error_budget")


def sys_knee():
    A, T = ACCENT["systems"], TINT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.3))
    rho = np.linspace(0, 0.97, 500)
    ax.axvspan(70, 85, color=T, lw=0)
    ax.plot(rho * 100, 1 / (1 - rho), color=INK, lw=1.7)
    for r in (0.5, 0.8, 0.9):
        ax.plot([r * 100], [1 / (1 - r)], "o", color=A, ms=4.2)
        ax.text(r * 100 - 1.2, 1 / (1 - r) + 1.3, f"{r:.0%} busy → {1/(1-r):.0f}×", ha="right", fontsize=8.2, color=INK)
    ax.text(77.5, 31, "the knee", ha="center", fontsize=8.4, color=A, fontweight=600)
    ax.text(2, 28, "time in system ÷ bare service time = 1 / (1 − ρ)\n(single queue, random arrivals and service)", fontsize=8.2, color=INK)
    ax.set_xlim(0, 100); ax.set_ylim(0, 34); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("utilisation ρ (%)", color=MID, fontsize=8.5); ax.set_ylabel("latency, multiples of service time", color=MID, fontsize=8.5)
    save(fig, "systems", "fig10_knee")


def sys_cost_crossover():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.1))
    v = np.linspace(0, 10, 200)
    ax.plot(v, 1.0 * v, color=A, lw=1.8, label="managed / pay per use")
    ax.plot(v, 3 + 0.35 * v, color=INK, lw=1.4, label="self-hosted, infrastructure only")
    ax.plot(v, 5.2 + 0.35 * v, color=INK, lw=1.2, ls=(0, (4, 3)), label="self-hosted, counting the engineers who run it")
    ax.legend(loc="upper left", fontsize=8.2, handlelength=2.6)
    for x in (3 / 0.65, 5.2 / 0.65):
        ax.plot([x], [x], "o", color=A, ms=4)
    ax.annotate("the crossover moves right\nonce people are counted", xy=(5.2 / 0.65, 5.2 / 0.65), xytext=(7.0, 2.2), fontsize=8.2, color=INK,
                arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("steady volume", color=MID, fontsize=8.5); ax.set_ylabel("cost per month", color=MID, fontsize=8.5)
    ax.text(0, 10.3, "Schematic", fontsize=7.5, color=MID)
    save(fig, "systems", "fig11_cost_crossover")


def sys_decision_loop():
    A, T = ACCENT["systems"], TINT["systems"]
    fig, ax = blank(3.7)
    steps = ["Requirements,\nas numbers", "At least two\noptions", "Decide, and state\nthe trade-off", "Record it\n(an ADR)", "Build", "Measure against\nthe prediction"]
    cx, cy, r = 50, 25, 18
    pts = []
    for i, s in enumerate(steps):
        ang = np.pi / 2 - i * 2 * np.pi / len(steps)
        x, y = cx + 2.1 * r * np.cos(ang), cy + r * np.sin(ang)
        pts.append((x, y))
    for i in range(len(steps)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(steps)]
        arrow(ax, x0 + (x1 - x0) * 0.32, y0 + (y1 - y0) * 0.32, x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.68, A if i == 5 else MID, 0.9, ms=7)
    for i, ((x, y), s) in enumerate(zip(pts, steps)):
        box(ax, x - 9.5, y - 3.8, 19, 7.6, s, fc=T if i in (2, 5) else "#f7f6f8", ec=A if i in (2, 5) else RULE, lw=0.9, size=8.0, weight=500)
    label(ax, cx, cy, "update the next\ndesign with what\nyou learned", 7.8, MID, ha="center")
    save(fig, "systems", "fig12_decision_loop")


AGI = [agi_levels_map, agi_saturation, agi_four_channels, agi_entry_ladder, agi_proof_practice, agi_bottleneck,
       agi_five_questions, agi_trifecta, agi_reliability, agi_three_layers, agi_dpi_stack, agi_diffusion]
SYSTEMS = [sys_tail_at_scale, sys_concurrency, sys_hit_rate, sys_memory_hierarchy, sys_consistency, sys_idempotency,
           sys_availability, sys_queue_depth, sys_error_budget, sys_knee, sys_cost_crossover, sys_decision_loop]

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for f in (AGI if which == "agi" else SYSTEMS if which == "systems" else AGI + SYSTEMS):
        f()
