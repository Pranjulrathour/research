"""Compare the GloVe measurements across the attempts kept in this folder.

Attempt 2 (killed part-way, log only): run_second_attempt_killed_during_glove.log
Attempt 3 (completed under antivirus load, set aside):  run_third_attempt_glove_contended.json
Attempt 4 (the reported run, after the quiet-machine gate): results.json

Prints, for every GloVe configuration, recall, batched QPS, single-query p50/p99 and build time from each attempt, and the
spread, so that the paper can state how much the timings move between runs on the same laptop. Recall should agree to
three decimals (HNSW construction is multithreaded and not bit-reproducible, so it can differ slightly).
"""
import ast, json, pathlib, statistics
HERE = pathlib.Path(__file__).resolve().parent
KEYS = ("nlist", "nprobe", "M", "efSearch", "expansion_search")


def cfg(r):
    return (r["index"], tuple(sorted((k, v) for k, v in r["params"].items() if k in KEYS)))


def from_log(path):
    rows = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith("{") and "'dataset'" in line:
            try:
                rows.append(ast.literal_eval(line))
            except Exception:
                pass
    return [r for r in rows if r["dataset"] == "glove-100-angular"]


attempts = {
    "2": from_log(HERE / "run_second_attempt_killed_during_glove.log"),
    "3": json.load(open(HERE / "run_third_attempt_glove_contended.json"))["rows"],
    "4": [r for r in json.load(open(HERE / "results.json"))["rows"] if r["dataset"] == "glove-100-angular"],
}
by = {k: {cfg(r): r for r in v} for k, v in attempts.items()}
configs = sorted({c for v in by.values() for c in v}, key=lambda c: (c[0], c[1]))


def fmt(c):
    return c[0] + " " + ", ".join(f"{k} {v}" for k, v in c[1])


if __name__ == "__main__":
    print(f"{'configuration':44s} {'recall (2/3/4)':24s} {'QPS (2/3/4)':26s} {'single p99 ms (2/3/4)':24s} build s (2/3/4)")
    ratios = []
    for c in configs:
        rs = [by[a].get(c) for a in ("2", "3", "4")]
        rec = "/".join(f"{r['recall@10']:.3f}" if r else "  -  " for r in rs)
        qps = "/".join(f"{r['qps']:,.0f}" if r else "-" for r in rs)
        p99 = "/".join(f"{r['single_p99_ms']:.2f}" if r else "-" for r in rs)
        bld = "/".join(f"{r['build_s']:.0f}" if r else "-" for r in rs)
        print(f"{fmt(c):44s} {rec:24s} {qps:26s} {p99:24s} {bld}")
        q = [r["qps"] for r in rs if r]
        if len(q) >= 2 and rs[2]:
            ratios.append(max(q) / rs[2]["qps"])
    if ratios:
        print(f"\nbest-attempt QPS / reported (attempt 4) QPS: median {statistics.median(ratios):.2f}, max {max(ratios):.2f} over {len(ratios)} configurations")
