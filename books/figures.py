"""Figures for both books: one visual system (Inter, ink + one accent, hairline strokes, generous white space).

Usage:  python figures.py [agi|systems|all]   -> books/<book>/figures/*.png

Charts plot exact formulas (stated in each function). Schematics carry no numbers unless a number is quoted in the
text with its source; the captions in the chapters say which is which.
"""
from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
import matplotlib.text
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
# Drawn at roughly the printed size (text block 4.5 in) so labels print at 6.5-8.5 pt and stay legible on a phone.
# Schematic layouts use a 0-100 coordinate grid whose height is defined against a 7.2 in reference width (REF_W).
W_IN, DPI, REF_W, FS = 5.0, 320, 7.2, 0.93

plt.rcParams.update({
    "font.family": "Inter", "font.size": 9.5, "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": MID, "ytick.color": MID, "axes.linewidth": 0.8, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "xtick.major.size": 3, "ytick.major.size": 3, "axes.spines.top": False, "axes.spines.right": False,
    "savefig.facecolor": PAPER, "figure.facecolor": PAPER, "axes.facecolor": PAPER, "legend.frameon": False,
})


HEADLINES = {
    # Book 1
    "fig01_levels_map": ("\u201cAGI\u201d is a grid, not a finishing line", "performance against breadth, with 2023 systems placed by the framework's authors"),
    "fig02_saturation": ("A benchmark stops informing before it reaches 100%", "scores spread out early, then crowd into the instrument's own noise"),
    "fig03_four_channels": ("Automation works through four channels, and only one shows on day one", "the other three take years, and historically they decide the outcome"),
    "fig04_entry_ladder": ("The tools are strongest exactly where careers begin", "the routine work that trains juniors is the work the tools do best"),
    "fig05_proof_and_practice": ("Practice and proof have come apart", "the essay still teaches; it no longer proves anything"),
    "fig06_bottleneck": ("Speed up the start of the pipeline and the bottleneck moves", "to the stages that need hands, instruments and judgement"),
    "fig07_five_questions": ("Four jurisdictions, five questions, one shared answer", "everyone requires labelling; almost nothing else is agreed"),
    "fig08_lethal_trifecta": ("Any two are safe. All three is a leak.", "the three properties that let an AI system exfiltrate what it knows"),
    "fig09_reliability": ("99% per step is 37% per hundred steps", "chance of finishing an n-step task when each step succeeds with probability p"),
    "fig10_three_layers": ("What compounds with the tools sits underneath them", "judgement, systems understanding and domain knowledge are what the tools can't supply"),
    "fig11_dpi_stack": ("Build on shared rails and inherit the plumbing", "identity, payments and consented data, already connected"),
    "fig12_diffusion": ("Twenty to forty years from available to transformative", "three earlier general-purpose technologies, and the open question"),
    "fig13_operators": ("The first job vanished. The first-timers found another. The incumbents paid.", "the automation of telephone switching, 1920\u20131940"),
    "fig14_horses_and_cars": ("Twenty-six million horses, then three", "horses and mules against motor vehicles in the United States, 1900\u20131960"),
    "fig15_engels_pause": ("Sixty years of growth the average worker never saw", "Britain, output per worker and the real wage, index 1780 = 100"),
    "fig16_electrification": ("Forty years from the power station to the productivity statistics", "share of US factory mechanical drive supplied by electric motors"),
    "fig17_books": ("Forty-six years of printing out-produced a century of scribes", "books produced in Western Europe, log scale"),
    "fig18_containers": ("A 97% cost cut, and a deal about who kept it", "loading cost per ton, and the 1960 West Coast agreement"),
    "fig19_wheat": ("The seed arrived in 1966. The harvest moved in 1968.", "India's wheat production, million tonnes"),
    "fig20_upi": ("From three million to 140 billion in eight years", "UPI transactions per calendar year, log scale"),
    "fig21_forecasts": ("Human-level machines have been twenty years away for seventy years", "predicted arrival against the year of the prediction"),
    # Book 2
    "fig01_tail_at_scale": ("Fan out to 100 servers and most requests wait for someone's slowest 1%", "share of requests that touch at least one server's tail"),
    "fig02_concurrency_models": ("What a server does while it waits", "three concurrency models on the same three requests"),
    "fig03_hit_rate": ("A cache fixes the average long before it fixes the tail", "average and p99 latency against hit rate, h = 1 ms, m = 50 ms"),
    "fig04_memory_hierarchy": ("Every level down is a cliff", "approximate access times, 2020s hardware, log scale"),
    "fig05_consistency_spectrum": ("Stronger promises, more coordination, less availability", "the consistency models in common use, from strongest to weakest"),
    "fig06_idempotency": ("The retry is harmless because the key makes it the same request", "an idempotent payment, with the response lost once"),
    "fig07_availability": ("Ten dependencies at 99.9% make a 99% service", "best-case availability against the number of dependencies every request needs"),
    "fig08_queue_depth": ("Arrivals above capacity grow a queue without limit", "messages waiting under three arrival patterns"),
    "fig09_error_budget": ("At burn rate 14.4, a month's budget lasts two days", "error budget remaining for a 99.9% SLO over 30 days"),
    "fig10_knee": ("Past about 80% busy, waiting explodes", "time in system as a multiple of service time, single queue"),
    "fig11_cost_crossover": ("Count the people and the crossover moves", "managed against self-hosted cost as volume grows"),
    "fig12_decision_loop": ("Decide, record, measure, repeat", "the design loop that turns opinions into evidence"),
}


def headline(fig, name: str):
    if name not in HEADLINES:
        return
    title, sub = HEADLINES[name]
    fig.text(0.0, 1.075, title, fontsize=10.6, fontweight=600, color=INK, ha="left", va="bottom", transform=fig.transFigure, wrap=False)
    if sub:
        fig.text(0.0, 1.02, sub, fontsize=8.4, color=MID, ha="left", va="bottom", transform=fig.transFigure)


def save(fig, book: str, name: str):
    headline(fig, name)
    for t in fig.findobj(matplotlib.text.Text):
        t.set_fontsize(t.get_fontsize() * FS)
    out = HERE / ("agi-transition" if book == "agi" else "systems-that-scale") / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("wrote", out / f"{name}.png")


def blank(h_in: float):
    fig = plt.figure(figsize=(W_IN, h_in * W_IN / REF_W))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100 * h_in / REF_W); ax.axis("off")
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.80))
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
    fig, ax = blank(3.6)
    box(ax, 1, 21, 19, 12, "A task is\nautomated", fc="#f7f6f8", ec=INK, size=9.6, weight=600)
    rows = [("Displacement", "less demand for people on it", "−", "at once"),
            ("Productivity", "the tasks around it gain value", "+", "months"),
            ("New tasks", "work that did not exist", "+", "years"),
            ("Demand", "cheaper output, more bought", "+", "years")]
    for i, (name, desc, sign, when) in enumerate(rows):
        y = 40 - i * 9.4
        arrow(ax, 20, 27, 27, y + 3.6, MID, 0.8)
        box(ax, 27, y, 52, 7.6, "", fc=PAPER, ec=RULE if i else A, lw=0.9 if i else 1.1)
        label(ax, 29.5, y + 5.0, name, 9.2, INK, 600)
        label(ax, 29.5, y + 2.2, desc, 7.9, MID)
        label(ax, 77, y + 3.8, sign, 12, A if sign == "−" else INK, 600, ha="right")
        label(ax, 82, y + 3.8, when, 7.8, MID)
    label(ax, 82, 49.5, "shows up", 7.6, MID, 600)
    box(ax, 27, 1.0, 52, 6.4, "net effect = the sum of all four", fc=T, ec=A, size=8.6, weight=600)
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
    label(ax, 1, 9.5, "how juniors\nhave always\nlearned", 7.6, MID)
    arrow(ax, 14.5, 9.5, x0 - 1.0, 9.5, MID, 0.8)
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
    fig, ax = blank(4.1)
    qs = ["Which uses get stricter rules?", "What must be disclosed?", "Who checks?", "Is there a size threshold?", "Who pays when it fails?"]
    cols = ["EU", "US", "China", "India"]
    # 2 = binding rule in force or enacted; 1 = partial / sectoral / state-level / voluntary; 0 = no AI-specific rule
    grid = [[2, 1, 1, 0], [2, 1, 2, 1], [2, 1, 2, 1], [2, 1, 0, 0], [1, 0, 1, 1]]
    notes = [["risk tiers", "state laws", "by service", "—"], ["docs, labels", "state laws", "labels, filing", "synthetic media"],
             ["conformity", "NIST, voluntary", "state review", "voluntary"], ["10²⁵ FLOP", "CA: 10²⁶", "—", "—"],
             ["PLD 2024", "existing law", "civil code", "existing law"]]
    x0, cw, top, rh = 44, 14, 45, 7.6
    label(ax, 99, top + 6.8, "as of October 2026", 7.4, MID, ha="right")
    for j, c in enumerate(cols):
        label(ax, x0 + j * cw + cw / 2, top + 2.6, c, 9.2, INK, 600, ha="center")
    for i, q in enumerate(qs):
        y = top - (i + 1) * rh
        ax.plot([1, 99], [y + rh, y + rh], color=RULE, lw=0.7)
        label(ax, 1, y + rh / 2, q, 8.4, INK, 500)
        for j, v in enumerate(grid[i]):
            cx = x0 + j * cw + cw / 2
            cy = y + rh / 2 + 1.2
            ax.add_patch(Circle((cx, cy), 1.3, fc=INK if v == 2 else PAPER, ec=INK, lw=0.9))
            if v == 1:
                ax.add_patch(Wedge((cx, cy), 1.3, 90, 270, fc=INK, ec="none"))
            label(ax, cx, y + rh / 2 - 1.9, notes[i][j], 6.6, MID, ha="center")
    ax.plot([1, 99], [top - 5 * rh, top - 5 * rh], color=RULE, lw=0.7)
    for k, (v, t) in enumerate([(2, "binding rule"), (1, "partial, state-level or voluntary"), (0, "none specific to AI")]):
        cx = 2.2 + [0, 26, 70][k]
        ax.add_patch(Circle((cx, 2.6), 1.1, fc=INK if v == 2 else PAPER, ec=INK, lw=0.8))
        if v == 1:
            ax.add_patch(Wedge((cx, 2.6), 1.1, 90, 270, fc=INK, ec="none"))
        label(ax, cx + 2.2, 2.6, t, 7.4, MID)
    save(fig, "agi", "fig07_five_questions")


def agi_trifecta():
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(4.4)
    centres = [(38, 40), (58, 40), (48, 23.5)]
    for (cx, cy) in centres:
        ax.add_patch(Circle((cx, cy), 15, fc="none", ec=INK, lw=1.0))
    label(ax, 30, 58.2, "private data", 8.8, INK, 600, ha="center")
    label(ax, 66, 58.2, "untrusted content", 8.8, INK, 600, ha="center")
    label(ax, 48, 4.6, "external communication", 8.8, INK, 600, ha="center")
    ax.add_patch(Circle((48, 34.5), 4.4, fc=T, ec=A, lw=1.1))
    label(ax, 48, 34.5, "leak\nrisk", 7.8, A, 600, ha="center")
    label(ax, 76, 26, "Any two can be\nmade safe. All three\ntogether is a design\ndecision to revisit.", 8.0, MID)
    save(fig, "agi", "fig08_lethal_trifecta")


def agi_reliability():
    A = ACCENT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 2.97))
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
    fig, ax = blank(3.9)
    box(ax, 4, 42, 92, 7, "AI applications for Indian users, in Indian languages", fc=T, ec=A, lw=1.1, size=9.0, weight=600, color=INK)
    rows = [("Commerce", "ONDC", "open network for trade"),
            ("Data", "Account Aggregator,\nDigiLocker", "consented data sharing"),
            ("Payments", "UPI", "≈18–20 bn a month (2025)"),
            ("Identity", "Aadhaar", "1.3 bn+ enrolments")]
    for i, (layer, name, note) in enumerate(rows):
        y = 32 - i * 8.6
        box(ax, 4, y, 92, 7, "", fc="#f7f6f8", ec=RULE, lw=0.8)
        label(ax, 7, y + 3.5, layer.upper(), 7.2, MID, 600)
        label(ax, 28, y + 3.5, name, 8.8, INK, 600)
        label(ax, 93, y + 3.5, note, 7.8, MID, ha="right")
    label(ax, 4, 1.8, "Figures from UIDAI and NPCI; see chapter sources.", 7.2, MID)
    save(fig, "agi", "fig11_dpi_stack")


def agi_diffusion():
    A = ACCENT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.0))
    rows = [("Electricity", 1882, 1925, "power stations → factory productivity"),
            ("Computing", 1970, 1997, "business computers → late-1990s surge"),
            ("Internet", 1993, 2008, "commercial web → search, cloud, phones"),
            ("Generative AI", 2022, None, "")]
    for i, (name, a, b, note) in enumerate(rows):
        y = len(rows) - 1 - i
        if b:
            ax.plot([a, b], [y, y], color=INK, lw=6, solid_capstyle="butt")
            ax.text(b + 1.8, y, f"~{b - a} yr", va="center", fontsize=8.4, color=INK, fontweight=600)
            ax.text(a, y - 0.3, note, fontsize=7.5, color=MID, va="top")
        else:
            ax.plot([a, a + 12], [y, y], color=A, lw=2.0, ls=(0, (1, 1.6)))
            ax.plot([a], [y], "o", color=A, ms=6)
            ax.text(a + 13.5, y, "?", va="center", fontsize=11, color=A, fontweight=600)
    ax.set_xlim(1876, 2045); ax.set_ylim(-0.75, 3.45)
    ax.set_yticks([3, 2, 1, 0]); ax.set_yticklabels([r[0] for r in rows], fontsize=8.8, fontweight=600, color=INK)
    ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
    ax.set_xticks([1880, 1920, 1960, 2000, 2040])
    ax.text(2045, 3.35, "dates approximate", ha="right", fontsize=7.4, color=MID)
    save(fig, "agi", "fig12_diffusion")


# ================================================================================================ Book 2
def sys_tail_at_scale():
    A = ACCENT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 2.80))
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.71))
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.80))
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
    ax.text(3, 6.6, "approximate, 2020s hardware; log scale", ha="right", fontsize=7.5, color=MID)
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.80))
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.71))
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.71))
    budget = 0.001 * 30 * 24 * 60
    d = np.linspace(0, 30, 600)
    for rate, c, lw, name in ((1, INK, 1.4, "burn rate 1: budget lasts the window"), (2, MID, 1.2, "burn rate 2: gone in 15 days"),
                              (14.4, A, 1.8, "burn rate 14.4: ~2 days")):
        rem = np.clip(budget - budget * rate * d / 30, 0, None)
        ax.plot(d, rem, color=c, lw=lw)
        pos = {1: (17.5, 24.0), 2: (15.5, 1.4), 14.4: (2.6, 1.4)}[rate]
        ax.text(*pos, name, fontsize=8.0, color=c)
    ax.set_xlim(0, 30); ax.set_ylim(0, budget * 1.08)
    ax.set_xlabel("days into the 30-day window", color=MID, fontsize=8.5); ax.set_ylabel("error budget left (minutes)", color=MID, fontsize=8.5)
    ax.text(0.3, budget * 1.03, f"SLO 99.9% over 30 days → {budget:.1f} minutes of budget", fontsize=8.2, color=INK)
    ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    save(fig, "systems", "fig09_error_budget")


def sys_knee():
    A, T = ACCENT["systems"], TINT["systems"]
    fig, ax = plt.subplots(figsize=(W_IN, 2.80))
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
    fig, ax = plt.subplots(figsize=(W_IN, 2.63))
    v = np.linspace(0, 10, 200)
    ax.plot(v, 1.0 * v, color=A, lw=1.8, label="managed / pay per use")
    ax.plot(v, 3 + 0.35 * v, color=INK, lw=1.4, label="self-hosted, infrastructure only")
    ax.plot(v, 5.2 + 0.35 * v, color=INK, lw=1.2, ls=(0, (4, 3)), label="self-hosted, counting the engineers who run it")
    ax.legend(loc="lower right", fontsize=7.8, handlelength=2.4)
    for x in (3 / 0.65, 5.2 / 0.65):
        ax.plot([x], [x], "o", color=A, ms=4)
    ax.annotate("the crossover moves right\nonce people are counted", xy=(5.2 / 0.65, 5.2 / 0.65), xytext=(0.4, 9.0), fontsize=8.0, color=INK,
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



# ================================================================================================ Book 1: history
def agi_operators():
    """Feigenbaum & Gross (2020): after a city's cutover to dial, operators among women 16-25 fell 50-80%; the next
    cohort's employment rate was unchanged; incumbents were less likely to be working a decade later."""
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.3)
    panels = [(4, "The job", "women 16\u201325 working\nas operators"), (37, "The next cohort", "employment rate of young\nwomen who came after"),
              (70, "The incumbents", "operators, ten years\nafter the cutover")]
    for x, t, sub in panels:
        label(ax, x, 42.5, t, 9.4, INK, 600)
        label(ax, x, 38.6, sub, 7.8, MID, va="top")
    # panel 1: before 100, after 20-50 (the 50-80% fall)
    ax.add_patch(Rectangle((6, 8), 8, 22, fc=INK, ec="none")); label(ax, 10, 5.3, "before", 7.6, MID, ha="center")
    ax.add_patch(Rectangle((18, 8), 8, 22 * 0.5, fc=T, ec=A, lw=0.8)); ax.add_patch(Rectangle((18, 8), 8, 22 * 0.2, fc=A, ec="none"))
    label(ax, 22, 5.3, "after", 7.6, MID, ha="center")
    ax.annotate("down 50\u201380%,\nimmediately and\npermanently", xy=(26.3, 8 + 22 * 0.35), xytext=(28.5, 22), fontsize=7.6, color=A, va="center",
                arrowprops=dict(arrowstyle="-", color=A, lw=0.6))
    # panel 2: equal bars
    ax.add_patch(Rectangle((39, 8), 8, 22, fc=INK, ec="none")); label(ax, 43, 5.3, "manual cities", 7.2, MID, ha="center")
    ax.add_patch(Rectangle((51, 8), 8, 22, fc=INK, ec="none")); label(ax, 55, 5.3, "dial cities", 7.2, MID, ha="center")
    label(ax, 61, 19, "no difference:\nsecretarial, typing\nand service jobs\nabsorbed them", 7.6, INK, va="center")
    # panel 3: two downward markers
    for i, t in enumerate(["less likely to be\nworking at all", "if working, more likely\nin a lower-paid job"]):
        y = 27 - i * 11
        arrow(ax, 73, y + 3.2, 73, y - 2.8, A, 1.0, ms=8)
        label(ax, 75.5, y, t, 7.8, INK, va="center")
    label(ax, 2, 0.6, "Schematic. Magnitudes from Feigenbaum & Gross (2020), NBER WP 28061.", 7.4, MID)
    save(fig, "agi", "fig13_operators")


def agi_horses_and_cars():
    """Horses and mules (USDA via Ensminger 1969 / Kilby 2007) and motor-vehicle registrations (FHWA Table MV-200), millions."""
    A = ACCENT["agi"]
    years = [1900, 1905, 1910, 1915, 1920, 1925, 1930, 1935, 1940, 1945, 1950, 1955, 1960]
    horses = [21.531635, 22.077, 24.042882, 26.493, 25.199552, 22.08152, 18.885856, 16.676, 13.931531, 11.629, 7.604, 4.309, 3.089]
    cars = [0.008, 0.0788, 0.4685, 2.490932, 9.239161, 20.068543, 26.749853, 26.546126, 32.453233, 31.03542, 49.161691, 62.688792, 73.857768]
    fig, ax = plt.subplots(figsize=(W_IN, 2.9))
    ax.plot(years, horses, color=INK, lw=1.7, marker="o", ms=3.2)
    ax.plot(years, cars, color=A, lw=1.7, marker="o", ms=3.2)
    ax.text(1960.6, 3.1, "horses and\nmules", color=INK, fontsize=8.2, va="center")
    ax.text(1960.6, 73.9, "motor\nvehicles", color=A, fontsize=8.2, va="center")
    ax.annotate("1915: 26.5 million animals,\n2.5 million vehicles", xy=(1915, 26.5), xytext=(1901, 46), fontsize=8.0, color=INK,
                arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.annotate("1930: 26.7 million vehicles,\n18.9 million animals", xy=(1930, 26.75), xytext=(1931.5, 11), fontsize=8.0, color=INK,
                arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(1899, 1961); ax.set_ylim(0, 80); ax.set_xticks(range(1900, 1961, 10))
    ax.set_ylabel("millions", color=MID, fontsize=8.5); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    fig.subplots_adjust(right=0.84)
    save(fig, "agi", "fig14_horses_and_cars")


def agi_engels_pause():
    """Allen (2009): output per worker +46% and real wage +12% over 1780-1840; +90% and +123% over 1840-1900. Index 1780 = 100."""
    A, T = ACCENT["agi"], TINT["agi"]
    yrs = [1780, 1840, 1900]
    out = [100, 146, 146 * 1.90]
    wage = [100, 112, 112 * 2.23]
    fig, ax = plt.subplots(figsize=(W_IN, 2.75))
    ax.axvspan(1780, 1840, color=T, lw=0)
    ax.plot(yrs, out, color=INK, lw=1.7, marker="o", ms=3.5)
    ax.plot(yrs, wage, color=A, lw=1.7, marker="o", ms=3.5)
    ax.text(1901, out[-1], "output per worker", color=INK, fontsize=8.2, va="center")
    ax.text(1901, wage[-1], "real wage", color=A, fontsize=8.2, va="center")
    ax.text(1810, 262, "Engels\u2019 pause: sixty years in which\noutput per worker rose 46%\nand the real wage rose 12%", ha="center", fontsize=8.0, color=INK)
    ax.text(1870, 118, "after 1840 the two\nmove together", ha="center", fontsize=8.0, color=MID)
    ax.set_xlim(1778, 1902); ax.set_ylim(90, 300); ax.set_xticks([1780, 1800, 1820, 1840, 1860, 1880, 1900])
    ax.set_ylabel("index, 1780 = 100", color=MID, fontsize=8.5); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    fig.subplots_adjust(right=0.80)
    save(fig, "agi", "fig15_engels_pause")


def agi_electrification():
    """Three anchors: under 5% in 1899, about half two decades later, over 75% by 1929 (David 1990; Devine 1983 via
    Atkeson & Kehoe 2001). Drawn as anchors joined by a dotted line, not as a measured curve."""
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 2.7))
    xs, ys, labs = [1899, 1920, 1929], [5, 50, 76], ["under 5%", "about half", "over 75%"]
    ax.axvspan(1920, 1930, color=T, lw=0)
    ax.plot(xs, ys, color=LIGHT, lw=1.0, ls=(0, (2, 3)), zorder=1)
    ax.plot(xs, ys, "o", color=A, ms=5, zorder=3)
    for x, y, l in zip(xs, ys, labs):
        ax.text(x, y + 6, f"{x}: {l}", ha="center", fontsize=8.2, color=INK)
    ax.axvline(1882, color=MID, lw=0.7)
    ax.text(1883, 92, "1882: Edison\u2019s Pearl Street\nstation, New York", fontsize=7.8, color=MID, va="top")
    ax.text(1925, 22, "1920s: factories rebuilt\naround unit drive; manufacturing\nproductivity growth responds", ha="center", fontsize=7.8, color=A)
    ax.set_xlim(1878, 1935); ax.set_ylim(0, 100); ax.set_xticks([1880, 1890, 1900, 1910, 1920, 1930])
    ax.set_ylabel("share of factory mechanical drive (%)", color=MID, fontsize=8.5); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    save(fig, "agi", "fig16_electrification")


def agi_books():
    """Buringh & van Zanden (2009): ~5 million manuscript books in the 15th century; 12.6 million printed books 1454-1500.
    Febvre & Martin (1958): 150-200 million copies in the 16th century."""
    A = ACCENT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 2.2))
    rows = [("manuscripts copied by hand,\n1400s (a hundred years)", 5.0e6, INK), ("printed books, 1454\u20131500\n(forty-six years)", 12.6e6, A),
            ("printed books, 1500s\n(a hundred years)", 175e6, A)]
    for i, (name, v, c) in enumerate(rows[::-1]):
        ax.barh(i, v, color=c, height=0.55)
        ax.text(1.6e5, i, name, va="center", ha="right", fontsize=8.2, color=INK)
    ax.plot([150e6, 200e6], [0, 0], color=PAPER, lw=1.2)
    ax.plot([150e6, 200e6], [0, 0], color=INK, lw=0.8); ax.plot([150e6, 150e6], [-0.14, 0.14], color=INK, lw=0.8); ax.plot([200e6, 200e6], [-0.14, 0.14], color=INK, lw=0.8)
    for i, (name, v, c) in enumerate(rows[::-1]):
        ax.text(v * 1.25 if i else 2.1e8 * 1.1, i, "5 million" if i == 2 else ("12.6 million" if i == 1 else "150\u2013200 million"), va="center", fontsize=8.2, color=INK)
    ax.set_xscale("log"); ax.set_xlim(2e5, 2e9); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xticks([1e6, 1e7, 1e8, 1e9]); ax.set_xticklabels(["1 million", "10 million", "100 million", "1 billion"])
    fig.subplots_adjust(left=0.40)
    save(fig, "agi", "fig17_books")


def agi_containers():
    """Levinson (2006): $5.83 a ton to load loose cargo by hand, 15.8 cents a ton for the Ideal-X's containers.
    ILWU-PMA Mechanization and Modernization Agreement, 18 Oct 1960; $29 million paid into the fund by 1966."""
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = blank(3.0)
    ax.add_patch(Rectangle((8, 12), 14, 26, fc=INK, ec="none")); label(ax, 15, 40.5, "$5.83 a ton", 9.0, INK, 600, ha="center")
    label(ax, 15, 8.5, "loose cargo,\nloaded by hand", 7.8, MID, ha="center", va="top")
    ax.add_patch(Rectangle((28, 12), 14, 26 * 0.158 / 5.83, fc=A, ec="none")); label(ax, 35, 16.5, "16 cents a ton", 9.0, A, 600, ha="center")
    label(ax, 35, 8.5, "the Ideal-X\u2019s\nfifty-eight boxes, 1956", 7.8, MID, ha="center", va="top")
    # timeline
    x0, x1 = 54, 97
    ax.plot([x0, x1], [20, 20], color=RULE, lw=1.0)
    for yr, text, dy in ((1956, "26 April 1956\nIdeal-X sails,\nNewark to Houston", 1), (1960, "18 October 1960\nunion and employers sign\nthe M&M Agreement", -1),
                         (1966, "by 1966\n$29 million paid for\nretirements and\nguaranteed pay", 1)):
        x = x0 + (yr - 1955) / (1967 - 1955) * (x1 - x0)
        ax.add_patch(Circle((x, 20), 0.9, fc=A if yr == 1960 else INK, ec="none"))
        label(ax, x, 20 + dy * 3.2, text, 7.4, INK if yr == 1960 else MID, ha="center", va="bottom" if dy > 0 else "top", linespacing=1.3)
    save(fig, "agi", "fig18_containers")


def agi_wheat():
    """India wheat production, USDA PSD series (market years), 1960-1985, million tonnes."""
    A, T = ACCENT["agi"], TINT["agi"]
    years = list(range(1960, 1986))
    mt = [10.320, 10.995, 12.076, 10.779, 9.854, 12.258, 10.394, 11.393, 16.540, 18.651, 20.093, 23.832, 26.410, 24.735, 21.778, 24.104,
          28.846, 29.010, 31.749, 35.508, 31.830, 36.313, 37.452, 42.794, 45.476, 44.069]
    fig, ax = plt.subplots(figsize=(W_IN, 2.75))
    ax.plot(years, mt, color=INK, lw=1.7, marker="o", ms=2.8)
    ax.axvline(1966, color=A, lw=0.9, ls=(0, (3, 2)))
    ax.text(1966.4, 44, "1966: 18,000 tonnes of\nMexican seed imported", fontsize=8.0, color=A, va="top")
    ax.annotate("1968: 16.5 million tonnes,\nup from 11.4", xy=(1968, 16.54), xytext=(1969.5, 9), fontsize=8.0, color=INK,
                arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.annotate("1964\u201366: two failed\nmonsoons", xy=(1966, 10.39), xytext=(1960.2, 20), fontsize=8.0, color=MID,
                arrowprops=dict(arrowstyle="-", color=MID, lw=0.7))
    ax.set_xlim(1959.5, 1985.5); ax.set_ylim(0, 50); ax.set_xticks(range(1960, 1986, 5))
    ax.set_ylabel("million tonnes", color=MID, fontsize=8.5); ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True)
    save(fig, "agi", "fig19_wheat")


def agi_upi():
    """UPI transactions per calendar year, NPCI product statistics (millions)."""
    A = ACCENT["agi"]
    years = list(range(2016, 2025))
    vol = [2.65, 418.8, 3746.32, 10787.54, 18880.89, 38744.55, 74044.48, 117675.97, 139995.98]
    fig, ax = plt.subplots(figsize=(W_IN, 2.75))
    ax.bar(years, vol, color=[INK] + [A] * 8, width=0.62)
    for y, v in zip(years, vol):
        lab = f"{v/1000:.0f} bn" if v >= 1000 else (f"{v:.0f} m" if v >= 10 else f"{v:.2f} m")
        ax.text(y, v * 1.25, lab, ha="center", fontsize=7.8, color=INK)
    ax.set_yscale("log"); ax.set_ylim(1, 1e6); ax.set_xlim(2015.4, 2024.6)
    ax.set_yticks([1, 10, 100, 1e3, 1e4, 1e5, 1e6]); ax.set_yticklabels(["1 m", "10 m", "100 m", "1 bn", "10 bn", "100 bn", "1 tn"])
    ax.text(2016, 0.45 * 1e6, "launched April 2016,\n21 banks; most paper\ncurrency withdrawn\nthat November", fontsize=7.8, color=MID, va="top", ha="left")
    ax.grid(axis="y", color=RULE, lw=0.6); ax.set_axisbelow(True); ax.tick_params(axis="x", length=0)
    save(fig, "agi", "fig20_upi")


def agi_forecasts():
    """Predicted arrival of human-level machines against the year of the forecast. Sources in chapter 12."""
    A, T = ACCENT["agi"], TINT["agi"]
    fig, ax = plt.subplots(figsize=(W_IN, 3.0))
    x = np.array([1950, 2030])
    ax.fill_between(x, x + 15, x + 25, color=T, lw=0, label="15\u201325 years out")
    ax.plot(x, x, color=LIGHT, lw=0.9, ls=(0, (3, 2)))
    ax.axhline(2026, color=MID, lw=0.7)
    ax.text(1950.8, 2027, "2026: forecasts below this line have come due", fontsize=7.8, color=MID, va="bottom")
    ax.text(2004, 2036.5, "15\u201325 years out:\nthe most common\nhorizon (Armstrong\n& Sotala, 2012)", fontsize=7.6, color=A, ha="center", va="center")
    pts = [(1955, 1956, 1956, "Dartmouth proposal:\n\u201ca summer\u201d"), (1965, 1985, 1985, "Simon: \u201cwithin\ntwenty years\u201d"),
           (1970, 1973, 1978, "Minsky: \u201cthree to\neight years\u201d"), (2013, 2023, 2033, "Frey & Osborne:\n\u201ca decade or two\u201d"),
           (2016, 2021, 2021, "Hinton: radiologists,\nfive years")]
    for yr, lo, hi, text in pts:
        if lo != hi:
            ax.plot([yr, yr], [lo, hi], color=INK, lw=1.4)
        ax.plot([yr], [(lo + hi) / 2], "o", color=INK, ms=4.6, zorder=3)
    for yr in (2016, 2019, 2022):
        ax.plot([yr], [yr + 1], "o", color=A, ms=4.0, zorder=3)
    ax.text(2023.2, 2019.5, "full self-driving\n\u201cnext year\u201d,\n2016\u20132023", fontsize=7.6, color=A, va="center")
    offs = {1955: (1957, 1949.5), 1965: (1959, 1991.5), 1970: (1972, 1969), 2013: (1998, 2010.5), 2016: (2000.5, 2027.5)}
    for yr, lo, hi, text in pts:
        tx, ty = offs[yr]
        ax.annotate(text, xy=(yr, (lo + hi) / 2), xytext=(tx, ty), fontsize=7.6, color=INK, va="center", ha="left",
                    arrowprops=dict(arrowstyle="-", color=LIGHT, lw=0.6, shrinkA=2, shrinkB=3))
    ax.set_xlim(1950, 2030); ax.set_ylim(1945, 2045); ax.set_xticks(range(1950, 2031, 10)); ax.set_yticks(range(1950, 2041, 10))
    ax.set_xlabel("year the forecast was made", color=MID, fontsize=8.5); ax.set_ylabel("year it said the change would arrive", color=MID, fontsize=8.5)
    ax.grid(color=RULE, lw=0.5); ax.set_axisbelow(True)
    save(fig, "agi", "fig21_forecasts")


AGI = [agi_levels_map, agi_saturation, agi_four_channels, agi_entry_ladder, agi_proof_practice, agi_bottleneck,
       agi_five_questions, agi_trifecta, agi_reliability, agi_three_layers, agi_dpi_stack, agi_diffusion,
       agi_operators, agi_horses_and_cars, agi_engels_pause, agi_electrification, agi_books, agi_containers, agi_wheat, agi_upi, agi_forecasts]
SYSTEMS = [sys_tail_at_scale, sys_concurrency, sys_hit_rate, sys_memory_hierarchy, sys_consistency, sys_idempotency,
           sys_availability, sys_queue_depth, sys_error_budget, sys_knee, sys_cost_crossover, sys_decision_loop]

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    fns = AGI if which == "agi" else SYSTEMS if which == "systems" else AGI + SYSTEMS
    if which == "history":
        fns = [agi_operators, agi_horses_and_cars, agi_engels_pause, agi_electrification, agi_books, agi_containers, agi_wheat, agi_upi, agi_forecasts]
    for f in fns:
        f()
