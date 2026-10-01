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

import h5py
import numpy as np
import faiss
from usearch.index import Index as UIndex

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
K = 10
THREADS = os.cpu_count() or 4
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
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    colors = {"flat": "#1c1b22", "ivf_flat": "#5b5a66", "hnsw_faiss": "#ff4d2e", "hnsw_usearch": "#c9602e"}
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, ds in zip(axes, DATASETS):
        for family in ("ivf_flat", "hnsw_faiss", "hnsw_usearch"):
            pts = sorted([(r["recall@10"], r["qps"]) for r in rows if r["dataset"] == ds and r["index"] == family])
            if pts: ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", ms=3, lw=1, color=colors[family], label=family)
        flat = [r for r in rows if r["dataset"] == ds and r["index"] == "flat"]
        if flat: ax.axhline(flat[0]["qps"], color=colors["flat"], ls="--", lw=0.9, label="flat (exact)")
        ax.set_yscale("log"); ax.set_xlabel("recall@10"); ax.set_ylabel("queries / second (batched, log)"); ax.set_title(ds); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "fig1_recall_qps_frontiers.png", dpi=160); plt.close(fig)
    # 2. serving-style single-query p99 vs recall
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, ds in zip(axes, DATASETS):
        for family in ("ivf_flat", "hnsw_faiss", "hnsw_usearch"):
            pts = sorted([(r["recall@10"], r["single_p99_ms"]) for r in rows if r["dataset"] == ds and r["index"] == family and "single_p99_ms" in r])
            if pts: ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", ms=3, lw=1, color=colors[family], label=family)
        flat = [r for r in rows if r["dataset"] == ds and r["index"] == "flat" and "single_p99_ms" in r]
        if flat: ax.axhline(flat[0]["single_p99_ms"], color=colors["flat"], ls="--", lw=0.9, label="flat (exact)")
        ax.set_yscale("log"); ax.set_xlabel("recall@10"); ax.set_ylabel("single-query p99 latency (ms, 1 thread, log)"); ax.set_title(ds); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "fig2_recall_vs_single_query_p99.png", dpi=160); plt.close(fig)
    # 3. build time and memory per index family (one bar per built index)
    built = []
    seen = set()
    for r in rows:
        key = (r["dataset"], r["index"], json.dumps({k: v for k, v in r["params"].items() if k in ("nlist", "M", "connectivity")}, sort_keys=True))
        if key not in seen:
            seen.add(key); built.append((f"{r['dataset'].split('-')[0]}\n{r['index']}\n{key[2].strip('{}')}", r["build_s"], r["mem_mb"]))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(range(len(built)), [b[1] for b in built], color="#5b5a66"); axes[0].set_ylabel("build time (s)"); axes[0].set_title("Index build time")
    axes[1].bar(range(len(built)), [b[2] for b in built], color="#ff4d2e"); axes[1].set_ylabel("resident memory added (MB)"); axes[1].set_title("Index memory")
    for ax in axes:
        ax.set_xticks(range(len(built))); ax.set_xticklabels([b[0] for b in built], fontsize=6)
    fig.tight_layout(); fig.savefig(FIG / "fig3_build_time_memory.png", dpi=160); plt.close(fig)


def main() -> None:
    import psutil
    meta = {"machine": platform.machine(), "processor": platform.processor(), "cpu_count": os.cpu_count(), "threads_used": THREADS,
            "ram_gb": round(psutil.virtual_memory().total / 2**30, 1), "python": platform.python_version(), "faiss": faiss.__version__,
            "usearch": __import__("usearch").__version__, "run_utc": time.strftime("%Y-%m-%dT%H:%M", time.gmtime()),
            "datasets": "ann-benchmarks.com sift-128-euclidean.hdf5, glove-100-angular.hdf5 (downloaded 2026-10-01)"}
    rows = []
    for ds in DATASETS:
        rows += run_dataset(ds)
        json.dump({"meta": meta, "rows": rows}, open(HERE / "results.json", "w"), indent=1)
    plots(rows)
    print("done:", len(rows), "configurations")


if __name__ == "__main__":
    main()
