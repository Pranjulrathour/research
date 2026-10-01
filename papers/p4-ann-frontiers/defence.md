# P4 — Defence notes
## Recall–latency frontiers of approximate nearest-neighbour indexes on public datasets

*Private preparation notes for talking about this paper in an interview, a workshop or a review. Not part of the manuscript.*

## The three findings, in one breath each

1. **On SIFT the graph index wins everywhere, and the top of the frontier is steep.** FAISS HNSW: 99% recall at 8,500 batched queries/s (22× exact search) with a single-query p99 of 1.25 ms; IVF-Flat 1,800/s (5×) and 5.3 ms at the same recall. Going from 91% to 99% recall cost HNSW 3.4× in throughput; 99% to 99.9% cost another 4.3×. The last point is as expensive as the previous eight.

2. **On GloVe the frontier collapses into exact search.** Nothing reached 99% recall. At 90% the approximate indexes were 3× faster than brute force; at 95% they were slower (689 and 627 queries/s vs 747 for exact search on eight cores). They still answered a single query 5–6× faster (p99 6.8–8.4 ms vs 42.9). "Approximate is faster" is a hypothesis to test at the recall you need, not a premise.

3. **Batched throughput overstates serving capacity by a factor of four to six.** Single-query p50 on one thread was 2.5–15× the batched per-query cost (median 6.4× on SIFT, 4.3× on GloVe), and the ordering of configurations shifts in places. Size a service from single-query latency, not a leaderboard.

Bonus finding: **machine state is part of the measurement.** Three GloVe attempts within three hours on one laptop: recall identical to three decimals; throughput differed by up to 5.9× (median 2.5×), builds by 2.4–3.9×. I report the best timing per configuration, keep every attempt (Appendix B), and say so.

## The method in sixty seconds

Two ann-benchmarks datasets (SIFT-128 1M Euclidean; GloVe-100 1.18M angular, normalised). Exact (FAISS flat), IVF-Flat (nlist 1024/4096 × nprobe 1…128), FAISS HNSW (M 16/32, efConstruction 200, efSearch 16…512), USearch HNSW (connectivity 16, ef 16…512). Per configuration: recall@10 vs shipped ground truth; batched QPS over 10,000 queries with 8 OpenMP threads (one per physical core), best of three; single-query p50/p99 on one thread (500 queries); build time; resident memory added. Quiet-machine gate before each run; background load recorded. 70 configurations.

## Questions I expect, and answers

**"Best-of-attempts is cherry-picking."** It is the same rule the harness already uses within a run (best of three timings), applied across runs, and it is stated in Section 3.3 with every raw attempt in the repo and Appendix B listing all three side by side. The quantity a benchmark wants is what the hardware does when unoccupied; the minimum is the standard estimator for that. Recall didn't move at all. The alternative, reporting a throttled laptop's numbers as if they described the algorithm, would be worse.

**"Why only 8 threads on a 12-thread CPU?"** The first attempt used 12 and batched search collapsed ~10× whenever another process took a core: OpenMP's static schedule waits for the slowest thread. One thread per physical core fixed it. That abandoned run is kept and described.

**"GloVe: HNSW only reaching 0.965 looks wrong."** It's consistent with ann-benchmarks for glove-100-angular, which is the hard dataset in that suite: high intrinsic dimension, angular neighbourhoods that are hard to navigate. ef 512 is where the standard sweeps stop; wider ef would raise recall at even lower QPS.

**"Exact search at 747 QPS batched on a million vectors?"** 1.18M × 100 dims is a dense matrix product; FAISS hands it to BLAS on eight cores: ~1.3 ms per query batched. That's why the approximate frontier collapses into it at high recall on this scale. At 100M vectors, or with quantisation, the balance changes.

**"USearch is slower than FAISS, so USearch is bad?"** Same algorithm, different implementation and binding; USearch ran at 55–60% of FAISS's batched QPS at equal ef on SIFT with recall within a point, and single-query latencies about 2×, partly from the Python binding's per-call cost. The point isn't a verdict on a library; it's that "HNSW" names an algorithm, not a performance level, so measure.

**"Why no product quantisation / filtering / updates?"** Flat vectors only, by design, to measure the two basic families cleanly. Each of those is a separate study and is listed in Limitations.

**"What would you do next?"** Open the GloVe case: wider ef and larger M to find where HNSW reaches 0.99 and at what cost; quantised variants at 10–100M vectors; a Linux server with fixed clocks to put error bars on the timings; filtered search.

**"How does this connect to the job?"** Retrieval is in every LLM application I build; choosing and sizing a vector index at the right recall is routine work, and most teams size it from a leaderboard number that's 4–6× too optimistic. This paper is the measurement I'd want before making that call, plus the discipline to notice when the laptop, not the index, is what you're measuring.

## Numbers to have memorised

- SIFT exact: 383 QPS, 2.6 ms/q batched; single 35.9/57.8 ms. HNSW M16 ef128: 0.990, 8,504 QPS (22×), single 0.76/1.25 ms. IVF 4096/128: 0.993, 1,797 (5×), 3.22/5.29 ms.
- SIFT HNSW 91→99% recall: 28,497→8,504 QPS (3.4×); 99→99.9%: →1,991 (4.3×).
- GloVe exact: 747 QPS, 1.34 ms/q; single 34.6/42.9. Max recall 0.9645 (HNSW M32 ef512) at 627 QPS; IVF 1024/128 0.963 at 689. At ≥0.9: IVF 4096/128 2,360 QPS (3.2×).
- Single/batched ratio: SIFT 3.4–15.5× (median 6.4); GloVe 2.5–8.2× (median 4.3).
- Builds: SIFT HNSW M16 177 s vs IVF-1024 4.8 s; M32 adds 771 MB vs 494 MB raw (+56%). GloVe HNSW M32 330 s vs IVF-4096 21 s; USearch 731 s.
- Attempts: best/attempt-4 QPS median 2.47×, max 5.86×; recall identical.

## Where everything is

`papers/p4-ann-frontiers/benchmark.py` (design in the docstring; `--resume`, `--plots-only`), `results.json` (70 rows; `meta.glove_reported` and per-row `reported_from_attempts`), `compare_attempts.py` and `merge_glove_attempts.py`, raw attempts `run_first_attempt_contended.log`, `run_second_attempt_killed_during_glove.log`, `run_third_attempt_glove_contended.{log,json}`, `run_fourth_attempt_glove_throttled.json`, `figures/fig0_indexes.png` (Figure 1), `fig1_recall_qps_frontiers.png` (Figure 2), `fig2_recall_vs_single_query_p99.png` (Figure 3), `fig3_build_time_memory.png` (Figure 4), `paper.md`.
