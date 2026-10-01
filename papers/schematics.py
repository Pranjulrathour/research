"""Method diagrams (one per paper): python schematics.py  ->  papers/<id>/figures/fig0_*.png

These show study design, not results. P5's diagram is drawn from the real dataset (transaction counts per hour and the
fraud cases, with the split boundaries the analysis uses).
"""
from __future__ import annotations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np

import plotstyle as ps

HERE = Path(__file__).resolve().parent
ps.apply(9.0)
INK, MID, LIGHT, RULE, A, B = ps.INK, ps.MID, ps.LIGHT, ps.RULE, ps.ACCENT, ps.ACCENT2


def out(pid, name):
    d = HERE / pid / "figures"; d.mkdir(exist_ok=True)
    return d / name


def p1_model_grid():
    fig, ax = plt.subplots(figsize=(6.3, 3.0)); ax.set_xlim(0, 100); ax.set_ylim(0, 49); ax.axis("off")
    ax.text(31, 47.5, "Volatility held constant\nover the 500-day window", ha="center", va="top", fontsize=9, fontweight="bold")
    ax.text(73, 47.5, "Volatility time-varying\n(EWMA, λ = 0.94)", ha="center", va="top", fontsize=9, fontweight="bold")
    ax.text(5, 31.25, "Normal\ntails", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(5, 13.75, "Fat\ntails", ha="center", va="center", fontsize=9, fontweight="bold")
    cells = {(0, 0): (["Gaussian"], False), (1, 0): (["EWMA-Gaussian"], False),
             (0, 1): (["Historical simulation", "Student-t"], False), (1, 1): (["Filtered Student-t", "Filtered historical simulation"], True)}
    for (c, r), (names, hl) in cells.items():
        x, y = 12 + c * 42, 23.5 - r * 17.5
        ax.add_patch(FancyBboxPatch((x, y), 38, 15.5, boxstyle="round,pad=0,rounding_size=0.8", fc="#fbf3f0" if hl else "#f6f6f8",
                                    ec=A if hl else RULE, lw=1.1 if hl else 0.8))
        for k, n in enumerate(names):
            ax.text(x + 19, y + 7.75 + (len(names) - 1) * 2.4 - k * 4.8, n, ha="center", va="center", fontsize=9)
    ax.text(12 + 42 + 19, 2.6, "the only cell that addresses both effects", ha="center", va="center", fontsize=8, color=A, style="italic")
    fig.savefig(out("p1-fat-tails", "fig0_model_grid.png")); plt.close(fig)


def p2_protocol():
    fig, ax = plt.subplots(figsize=(6.3, 3.2))
    years = np.arange(2005, 2027)
    tests = [2012, 2016, 2020, 2024, 2026]
    for i, Y in enumerate(tests):
        y = len(tests) - i + 1.4
        ax.barh(y, (Y - 2) - 2005, left=2005, height=0.5, color=LIGHT)
        ax.barh(y, 2, left=Y - 2, height=0.5, color=ps.SERIES[2])
        ax.barh(y, 1 if Y < 2026 else 0.75, left=Y, height=0.5, color=A)
        ax.text(2004.6, y, f"test {Y}", ha="right", va="center", fontsize=8.5)
    ax.text(2004.6, 0.8, "shuffled\n5-fold CV", ha="right", va="center", fontsize=8.5)
    rng = np.random.default_rng(1)
    for yr in range(2005, 2027):
        for m in range(12):
            if yr == 2026 and m > 8:
                continue
            ax.add_patch(Rectangle((yr + m / 12, 0.55), 1 / 12, 0.5, fc=A if rng.random() < 0.2 else LIGHT, ec="white", lw=0.3))
    ax.set_xlim(2001.5, 2027.3); ax.set_ylim(0.2, 7.2); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xticks([2005, 2010, 2015, 2020, 2025])
    handles = [Rectangle((0, 0), 1, 1, fc=LIGHT), Rectangle((0, 0), 1, 1, fc=ps.SERIES[2]), Rectangle((0, 0), 1, 1, fc=A)]
    ax.legend(handles, ["training (expanding)", "validation (last 24 months)", "test"], loc="upper center", ncol=3,
              bbox_to_anchor=(0.55, 1.08), handlelength=1.2, fontsize=8)
    ax.text(2027.2, 1.2, "test folds drawn from every period: look-ahead", ha="right", va="bottom", fontsize=7.5, color=MID, style="italic")
    fig.savefig(out("p2-ml-returns", "fig0_protocol.png")); plt.close(fig)


def p3_servers():
    fig, ax = plt.subplots(figsize=(6.3, 3.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")
    X0 = 53

    def blk(x0, x1, y, kind):
        fc = {"io": "white", "cpu": A, "net": INK}[kind]
        ax.add_patch(Rectangle((X0 + x0 + 0.15, y - 1.0), x1 - x0 - 0.3, 2.0, fc=fc, ec=LIGHT if kind == "io" else "none", lw=0.5,
                               hatch="////" if kind == "io" else None))

    def lane(y, label=""):
        ax.plot([X0, 99], [y, y], color=RULE, lw=0.5, zorder=0)
        if label:
            ax.text(X0 - 1, y, label, fontsize=6.8, color=MID, ha="right", va="center")

    def title(y, name, l1, l2):
        ax.text(1, y + 1.4, name, fontsize=9, fontweight="bold")
        ax.text(1, y - 1.6, l1, fontsize=7.2, color=MID)
        ax.text(1, y - 4.0, l2, fontsize=7.2, color=MID)
    # threaded: two threads, CPU work serialised by the GIL
    title(55, "threaded", "one OS thread per connection;", "the GIL lets one thread compute at a time")
    lane(56, "thread 1"); lane(52, "thread 2")
    blk(0, 3, 56, "net"); blk(3, 15, 56, "io"); blk(15, 21, 56, "cpu")
    blk(1, 4, 52, "net"); blk(4, 16, 52, "io"); blk(21, 27, 52, "cpu")
    # async inline
    title(41, "async", "one event loop; CPU work runs inline", "and every other connection waits behind it")
    lane(42, "loop")
    blk(0, 3, 42, "net"); blk(3, 6, 42, "net"); blk(15, 21, 42, "cpu"); blk(21, 27, 42, "cpu"); blk(27, 30, 42, "net")
    # hybrid thread
    title(27, "hybrid_thread", "event loop + thread pool; the loop stays free,", "but CPU work is still serialised by the GIL")
    lane(30, "loop"); lane(25, "pool")
    for k in range(6):
        blk(k * 3, k * 3 + 3, 30, "net")
    blk(15, 21, 25, "cpu"); blk(21, 27, 25, "cpu"); blk(27, 33, 25, "cpu")
    # hybrid proc
    title(11, "hybrid_proc", "event loop + process pool; CPU work runs", "in parallel across cores")
    lane(16, "loop"); lane(12, "proc 1"); lane(8, "proc 2"); lane(4, "proc 3")
    for k in range(6):
        blk(k * 3, k * 3 + 3, 16, "net")
    blk(15, 21, 12, "cpu"); blk(16, 22, 8, "cpu"); blk(17, 23, 4, "cpu")
    for k, (kind, t) in enumerate([("net", "parse / respond"), ("io", "20 ms wait"), ("cpu", "~3 ms CPU")]):
        x = [0, 18, 34][k]
        blk(x, x + 2.4, 0.2 if False else -0.6, kind)
        ax.text(X0 + x + 3.2, -0.6, t, fontsize=7, color=MID, va="center")
    ax.annotate("", xy=(99, 59.2), xytext=(91, 59.2), arrowprops=dict(arrowstyle="-|>", color=MID, lw=0.7))
    ax.text(90.5, 59.2, "time", fontsize=7.2, color=MID, ha="right", va="center")
    ax.set_ylim(-2.5, 61)
    fig.savefig(out("p3-tail-latency", "fig0_servers.png")); plt.close(fig)


def p4_indexes():
    rng = np.random.default_rng(3)
    pts = rng.normal(size=(260, 2)) * [1.0, 0.8] + rng.choice([[-1.6, 0.9], [1.4, 1.2], [0.2, -1.4], [1.8, -0.8], [-1.5, -1.2]], 260)
    q = np.array([0.6, 0.15])
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.0))
    # IVF: k-means cells, probe the nearest few
    from scipy.cluster.vq import kmeans2
    from scipy.spatial import Voronoi, voronoi_plot_2d
    cents, lab = kmeans2(pts, 9, seed=4, minit="++")
    order = np.argsort(((cents - q) ** 2).sum(1))
    probed = set(order[:3])
    ax = axes[0]
    vor = Voronoi(np.vstack([cents, [[-20, -20], [20, -20], [-20, 20], [20, 20]]]))
    voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False, line_colors=LIGHT, line_width=0.7)
    for k in range(len(cents)):
        m = lab == k
        ax.scatter(pts[m, 0], pts[m, 1], s=5, color=A if k in probed else LIGHT, lw=0)
    ax.scatter(cents[:, 0], cents[:, 1], s=16, color=INK, marker="+", lw=0.9)
    ax.scatter([q[0]], [q[1]], s=36, color=B, marker="*", zorder=5)
    ax.set_title("IVF: search only the probed cells", fontsize=9)
    ax.set_xlim(-4.2, 4.2); ax.set_ylim(-3.8, 3.6); ax.axis("off")
    # HNSW-like: proximity graph, greedy walk
    ax = axes[1]
    from scipy.spatial import cKDTree
    tree = cKDTree(pts)
    _, nn = tree.query(pts, k=5)
    for i in range(len(pts)):
        for j in nn[i, 1:]:
            ax.plot(pts[[i, j], 0], pts[[i, j], 1], color=RULE, lw=0.4, zorder=0)
    ax.scatter(pts[:, 0], pts[:, 1], s=4, color=LIGHT, lw=0)
    cur = int(np.argmax(pts[:, 0] * -1 + pts[:, 1]))
    path = [cur]
    for _ in range(30):
        cand = nn[cur, 1:]
        best = cand[np.argmin(((pts[cand] - q) ** 2).sum(1))]
        if ((pts[best] - q) ** 2).sum() >= ((pts[cur] - q) ** 2).sum():
            break
        cur = int(best); path.append(cur)
    ax.plot(pts[path, 0], pts[path, 1], color=A, lw=1.3, zorder=3)
    ax.scatter(pts[path, 0], pts[path, 1], s=10, color=A, zorder=4)
    ax.scatter([q[0]], [q[1]], s=36, color=B, marker="*", zorder=5)
    ax.set_title("Graph (HNSW): greedy walk toward the query", fontsize=9)
    ax.set_xlim(-4.2, 4.2); ax.set_ylim(-3.8, 3.6); ax.axis("off")
    fig.savefig(out("p4-ann-frontiers", "fig0_indexes.png")); plt.close(fig)


def p5_split():
    import pandas as pd
    df = pd.read_csv(HERE / "p5-fraud-imbalance" / "data" / "creditcard.csv", usecols=["Time", "Class"]).sort_values("Time").reset_index(drop=True)
    n = len(df); a, b = int(0.7 * n), int(0.8 * n)
    t_a, t_b = df.Time.iloc[a] / 3600, df.Time.iloc[b] / 3600
    hours = df.Time / 3600
    fig, axes = plt.subplots(2, 1, figsize=(6.3, 3.3), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
    ax = axes[0]
    counts, edges = np.histogram(hours, bins=np.arange(0, 48.5, 0.5))
    ax.bar(edges[:-1], counts, width=0.5, align="edge", color=LIGHT, lw=0)
    for x, lab in ((t_a, "70%"), (t_b, "80%")):
        ax.axvline(x, color=INK, lw=0.8, ls=(0, (3, 2)))
        ax.text(x + 0.3, counts.max() * 0.97, lab, fontsize=7.5, va="top")
    ax.text(t_a / 2, counts.max() * 1.05, "train", ha="center", fontsize=8.5, fontweight="bold")
    ax.text((t_a + t_b) / 2, counts.max() * 1.05, "val.", ha="center", fontsize=8.5, fontweight="bold")
    ax.text((t_b + 48) / 2, counts.max() * 1.05, "test", ha="center", fontsize=8.5, fontweight="bold")
    ax.set_ylabel("transactions\nper half hour"); ax.set_ylim(0, counts.max() * 1.15)
    ax = axes[1]
    fr = hours[df.Class == 1]
    ax.vlines(fr, 0, 1, color=A, lw=0.6)
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 1.1)
    ax.set_ylabel("frauds", rotation=0, ha="right", va="center")
    for x in (t_a, t_b):
        ax.axvline(x, color=INK, lw=0.8, ls=(0, (3, 2)))
    ax.set_xlabel("hours since the first transaction"); ax.set_xlim(0, 48)
    fig.savefig(out("p5-fraud-imbalance", "fig0_split.png")); plt.close(fig)
    print(f"p5 split boundaries: {t_a:.2f} h, {t_b:.2f} h; frauds {int(df.Class.sum())}")


if __name__ == "__main__":
    for f in (p1_model_grid, p2_protocol, p3_servers, p4_indexes, p5_split):
        f(); print("wrote", f.__name__)

