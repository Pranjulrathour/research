"""P4 -- Recall-latency frontiers of approximate nearest-neighbour indexes on public datasets.

Reproduce:  python benchmark.py            (reads data/*.hdf5 from ann-benchmarks.com, writes results.json + figures/)

Design, fixed before running:
  * Datasets: SIFT-128 (1,000,000 base / 10,000 queries, Euclidean) and GloVe-100 (1,183,514 / 10,000, angular -> vectors
    L2-normalised so inner product == cosine). Ground truth = the 100 true neighbours shipped in the files.
  * Indexes (CPU only, single machine, one process):
      flat        exact search (FAISS IndexFlat)                      -> the recall = 1.0 reference and the latency ceiling
      ivf         FAISS IVF-Flat, nlist in {1024, 4096}, sweep nprobe  -> the classic inverted-file family
      hnsw_faiss  FAISS HNSW-Flat, M in {16, 32}, efConstruction 200, sweep efSearch
      hnsw_usearch usearch HNSW, connectivity 16, sweep ef              -> a second, independent HNSW implementation
  * Metric: recall@10 (fraction of the true 10 nearest found in the returned 10) vs queries per second, batched queries of
    the full 10,000-query test set, best-of-3 timing per configuration; build time and index memory recorded.
  * Threads pinned to the machine's physical core count and recorded; everything else is library defaults.
No parameter is tuned after seeing results; the sweeps are the standard ranges from the ann-benchmarks project.
"""
from __future__ import annotations
import json, os, platform, time, gc
from pathlib import Path

import sys

import h5py
import numpy as np
import faiss
import psutil
from usearch.index import Index as UIndex

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import benchenv  # noqa: E402  (quiet-machine gate and background-load record, shared with P3)

FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
K = 10
# One OpenMP thread per physical core. Using every logical CPU (12 on the author's 4P+4E laptop) made batched search
# collapse ~10x whenever any other process took a core, because OpenMP's static schedule waits for the slowest thread.
THREADS = psutil.cpu_count(logical=False) or 4
faiss.omp_set_num_threads(THREADS)

DATASETS = {
    "sift-128-euclidean": {"metric": "l2"},
    "glove-100-angular": {"metric": "ip"},      # cosine via normalisation
}
IVF_NLIST = (1024, 4096)
IVF_NPROBE = (1, 2, 4, 8, 16, 32, 64, 128)
HNSW_M = (16, 32)
HNSW_EF = (16, 32, 64, 128, 256, 512)


def load(name: str):
    with h5py.File(HERE / "data" / f"{name}.hdf5", "r") as h:
        train = np.ascontiguousarray(h["train"][:], dtype=np.float32)
        test = np.ascontiguousarray(h["test"][:], dtype=np.float32)
        gt = h["neighbors"][:, :K]
    if DATASETS[name]["metric"] == "ip":
        faiss.normalize_L2(train); faiss.normalize_L2(test)
    return train, test, gt


def recall_at_k(found: np.ndarray, gt: np.ndarray) -> float:
    hits = 0
    for f, g in zip(found, gt):
        hits += len(set(f.tolist()) & set(g.tolist()))
    return hits / (gt.shape[0] * K)


def timed_search(fn, test, repeats=3):
    best = None; out = None
    for _ in range(repeats):
        t0 = time.perf_counter(); res = fn(test); dt = time.perf_counter() - t0
        if best is None or dt < best: best, out = dt, res
    return best, out


def mem_mb():
    import psutil
    return psutil.Process().memory_info().rss / 2**20


def single_query_latency(fn, test, n=500, faiss_threads=True):
    """Serving-style latency: one query at a time, one thread, n queries; returns p50 and p99 in ms.
    This is the number an online service sees; the batched QPS above is the number an offline job sees."""
    if faiss_threads: faiss.omp_set_num_threads(1)
    lat = []
    for i in range(min(n, len(test))):
        q = test[i:i + 1]
        t0 = time.perf_counter(); fn(q); lat.append((time.perf_counter() - t0) * 1e3)
    if faiss_threads: faiss.omp_set_num_threads(THREADS)
    lat.sort()
    return {"single_p50_ms": lat[len(lat) // 2], "single_p99_ms": lat[min(len(lat) - 1, int(0.99 * len(lat)))], "single_n": len(lat)}


def run_dataset(name: str) -> list[dict]:
    train, test, gt = load(name)
    d = train.shape[1]; metric = DATASETS[name]["metric"]
    rows = []
    base_mem = mem_mb()

    # --- flat (exact) ---
    idx = faiss.IndexFlatL2(d) if metric == "l2" else faiss.IndexFlatIP(d)
    t0 = time.perf_counter(); idx.add(train); build = time.perf_counter() - t0
    dt, (_, I) = timed_search(lambda q: idx.search(q, K), test)
    rows.append({"dataset": name, "index": "flat", "params": {}, "build_s": build, "mem_mb": mem_mb() - base_mem,
                 "recall@10": recall_at_k(I, gt), "qps": len(test) / dt, "latency_ms_per_query_batched": dt / len(test) * 1e3,
                 **single_query_latency(lambda q: idx.search(q, K), test, n=100)})
    print(rows[-1], flush=True); del idx; gc.collect()

    # --- IVF-Flat ---
    for nlist in IVF_NLIST:
        quant = faiss.IndexFlatL2(d) if metric == "l2" else faiss.IndexFlatIP(d)
        mt = faiss.METRIC_L2 if metric == "l2" else faiss.METRIC_INNER_PRODUCT
        idx = faiss.IndexIVFFlat(quant, d, nlist, mt)
        t0 = time.perf_counter(); idx.train(train[np.random.RandomState(0).choice(len(train), min(len(train), 50 * nlist), replace=False)]); idx.add(train); build = time.perf_counter() - t0
        m = mem_mb() - base_mem
        for nprobe in IVF_NPROBE:
            idx.nprobe = nprobe
            dt, (_, I) = timed_search(lambda q: idx.search(q, K), test)
            rows.append({"dataset": name, "index": "ivf_flat", "params": {"nlist": nlist, "nprobe": nprobe}, "build_s": build, "mem_mb": m,
                         "recall@10": recall_at_k(I, gt), "qps": len(test) / dt, "latency_ms_per_query_batched": dt / len(test) * 1e3,
                         **single_query_latency(lambda q: idx.search(q, K), test)})
            print(rows[-1], flush=True)
        del idx, quant; gc.collect()

    # --- HNSW (FAISS) ---
    for M in HNSW_M:
        idx = faiss.IndexHNSWFlat(d, M, faiss.METRIC_L2 if metric == "l2" else faiss.METRIC_INNER_PRODUCT)
        idx.hnsw.efConstruction = 200
        t0 = time.perf_counter(); idx.add(train); build = time.perf_counter() - t0
        m = mem_mb() - base_mem
        for ef in HNSW_EF:
            idx.hnsw.efSearch = max(ef, K)
            dt, (_, I) = timed_search(lambda q: idx.search(q, K), test)
            rows.append({"dataset": name, "index": "hnsw_faiss", "params": {"M": M, "efConstruction": 200, "efSearch": ef}, "build_s": build, "mem_mb": m,
                         "recall@10": recall_at_k(I, gt), "qps": len(test) / dt, "latency_ms_per_query_batched": dt / len(test) * 1e3,
                         **single_query_latency(lambda q: idx.search(q, K), test)})
            print(rows[-1], flush=True)
        del idx; gc.collect()

    # --- HNSW (usearch) ---
    uidx = UIndex(ndim=d, metric="l2sq" if metric == "l2" else "ip", connectivity=16, expansion_add=200, dtype="f32")
    keys = np.arange(len(train), dtype=np.uint64)
    t0 = time.perf_counter(); uidx.add(keys, train, threads=THREADS); build = time.perf_counter() - t0
    m = mem_mb() - base_mem
    for ef in HNSW_EF:
        uidx.expansion_search = max(ef, K)
        dt, res = timed_search(lambda q: uidx.search(q, K, threads=THREADS), test)
        I = np.asarray(res.keys).reshape(len(test), -1)[:, :K].astype(np.int64)
        rows.append({"dataset": name, "index": "hnsw_usearch", "params": {"connectivity": 16, "expansion_add": 200, "expansion_search": ef}, "build_s": build, "mem_mb": m,
                     "recall@10": recall_at_k(I, gt), "qps": len(test) / dt, "latency_ms_per_query_batched": dt / len(test) * 1e3,
                     **single_query_latency(lambda q: uidx.search(q, K, threads=1), test, faiss_threads=False)})
        print(rows[-1], flush=True)
    del uidx; gc.collect()
    return rows


def plots(rows: list[dict]) -> None:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    import plotstyle as ps
    ps.apply(9.0)
    fam_c = {"ivf_flat": ps.ACCENT2, "hnsw_faiss": ps.ACCENT, "hnsw_usearch": "#c9a227"}
    fam_l = {"flat": "Flat (exact)", "ivf_flat": "IVF-Flat (FAISS)", "hnsw_faiss": "HNSW (FAISS)", "hnsw_usearch": "HNSW (USearch)"}
    ds_l = {"sift-128-euclidean": "SIFT-128, Euclidean", "glove-100-angular": "GloVe-100, angular"}
    build_keys = ("nlist", "M", "connectivity")

    def bkey(r):
        return json.dumps({k: v for k, v in r["params"].items() if k in build_keys}, sort_keys=True)

    def frontier(ax, ds, ykey):
        sub = [r for r in rows if r["dataset"] == ds and ykey in r]
        for family in ("ivf_flat", "hnsw_faiss", "hnsw_usearch"):
            keys = sorted({bkey(r) for r in sub if r["index"] == family})
            for j, k in enumerate(keys):
                pts = sorted((r["recall@10"], r[ykey]) for r in sub if r["index"] == family and bkey(r) == k)
                lab = fam_l[family] if j == 0 else None
                ax.plot([q[0] for q in pts], [q[1] for q in pts], marker="o", ms=2.4, lw=0.8, color=fam_c[family], label=lab,
                        alpha=1.0 if j == 0 else 0.55, ls="-" if j == 0 else (0, (3, 1.5)))
        flat = [r for r in sub if r["index"] == "flat"]
        if flat:
            ax.axhline(flat[0][ykey], color=ps.INK, ls=(0, (3, 2)), lw=0.6)
            ax.text(0.02, flat[0][ykey], "exact search", transform=ax.get_yaxis_transform(), fontsize=7, color=ps.INK,
                    va="bottom" if ykey == "qps" else "top")
        ax.set_yscale("log"); ax.set_xlabel("recall@10")
        ax.set_title(ds_l.get(ds, ds), loc="left", fontsize=9.5, fontweight="bold", pad=6)

    # 1. recall vs batched throughput
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))
    for ax, ds in zip(axes, DATASETS):
        frontier(ax, ds, "qps")
    axes[0].set_ylabel("queries per second (batched)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.07), handlelength=1.4, columnspacing=1.4)
    fig.tight_layout(w_pad=1.8); fig.savefig(FIG / "fig1_recall_qps_frontiers.png"); plt.close(fig)
    # 2. recall vs single-query p99 latency
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))
    for ax, ds in zip(axes, DATASETS):
        frontier(ax, ds, "single_p99_ms")
    axes[0].set_ylabel("single-query p99 (ms, one thread)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.07), handlelength=1.4, columnspacing=1.4)
    fig.tight_layout(w_pad=1.8); fig.savefig(FIG / "fig2_recall_vs_single_query_p99.png"); plt.close(fig)
    # 3. build time and memory, one bar per built index
    built, seen = [], set()
    for r in rows:
        key = (r["dataset"], r["index"], bkey(r))
        if key in seen:
            continue
        seen.add(key)
        par = ", ".join(f"{k} {v}" for k, v in r["params"].items() if k in build_keys)
        built.append((f"{ds_l.get(r['dataset'], r['dataset']).split(',')[0]} · {fam_l[r['index']]}" + (f", {par}" if par else ""),
                      r["build_s"], r["mem_mb"], r["index"]))
    h = 0.24 * len(built) + 0.7
    fig, axes = plt.subplots(1, 2, figsize=(6.3, h), sharey=True)
    ys = np.arange(len(built))[::-1]
    cols = [fam_c.get(b[3], ps.INK) for b in built]
    axes[0].barh(ys, [b[1] for b in built], 0.62, color=cols); axes[0].set_xlabel("build time (s)")
    axes[1].barh(ys, [b[2] for b in built], 0.62, color=cols); axes[1].set_xlabel("memory added (MB)")
    for ax, k in zip(axes, (1, 2)):
        for y, b in zip(ys, built):
            ax.text(b[k], y, f" {b[k]:,.0f}" if b[k] >= 10 else f" {b[k]:.1f}", va="center", fontsize=6.8, color=ps.MID)
        ax.margins(x=0.18); ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(ys); axes[0].set_yticklabels([b[0] for b in built], fontsize=7.2)
    fig.tight_layout(w_pad=1.2); fig.savefig(FIG / "fig3_build_time_memory.png"); plt.close(fig)


def main() -> None:
    if "--plots-only" in sys.argv:
        plots(json.load(open(HERE / "results.json"))["rows"]); print("redrew figures"); return
    start_env = benchenv.wait_for_quiet()
    meta = {"machine": platform.machine(), "processor": platform.processor(), "cpu_count": os.cpu_count(),
            "physical_cores": psutil.cpu_count(logical=False), "threads_used": THREADS, "background_at_start": start_env,
            "ram_gb": round(psutil.virtual_memory().total / 2**30, 1), "python": platform.python_version(), "faiss": faiss.__version__,
            "usearch": __import__("usearch").__version__, "run_utc": time.strftime("%Y-%m-%dT%H:%M", time.gmtime()),
            "datasets": "ann-benchmarks.com sift-128-euclidean.hdf5, glove-100-angular.hdf5 (downloaded 2026-10-01)"}
    rows = []
    meta["background_after_dataset"] = {}
    done = set()
    if "--resume" in sys.argv and (HERE / "results.json").exists():
        # Explicit opt-in only: keep the datasets a previous run completed (results.json is written after each dataset)
        # and run the rest. Used once, on 2026-10-01, after the process was killed part-way through the second dataset.
        prev = json.load(open(HERE / "results.json"))
        rows = prev["rows"]
        done = {ds for ds in DATASETS if any(r["dataset"] == ds and r["index"] == "hnsw_usearch" for r in rows)}
        rows = [r for r in rows if r["dataset"] in done]
        meta["resumed"] = {"kept_datasets": sorted(done), "previous_run_utc": prev["meta"].get("run_utc"),
                           "previous_background_at_start": prev["meta"].get("background_at_start"),
                           "previous_background_after_dataset": prev["meta"].get("background_after_dataset")}
        print("resuming: keeping", sorted(done), flush=True)
    for ds in DATASETS:
        if ds in done:
            continue
        rows += run_dataset(ds)
        meta["background_after_dataset"][ds] = benchenv.sample_load()
        json.dump({"meta": meta, "rows": rows}, open(HERE / "results.json", "w"), indent=1)
    try:
        plots(rows)
    except Exception as e:  # results.json is already written; re-draw with --plots-only
        print("plotting failed:", repr(e))
    print("done:", len(rows), "configurations")


if __name__ == "__main__":
    main()
