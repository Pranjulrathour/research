---
title: "Recall–Latency Frontiers of Approximate Nearest-Neighbour Indexes on Public Datasets"
author: "Pranjul Rathour"
affiliation: "Independent researcher, Kanpur, India · pranjulrathour41@gmail.com · https://pranjulrathour.scult.in"
date: "October 2026"
keywords: "approximate nearest neighbour search, vector search, HNSW, IVF, FAISS, usearch, recall, latency, ann-benchmarks, retrieval-augmented generation"
---

## Abstract

Vector similarity search underlies semantic search, recommendation and the retrieval step of most AI applications, and the index that performs it is chosen along a curve: recall traded against speed, build time and memory. This paper measures that curve for the two index families in common use on two standard public datasets. Exact search, inverted-file (IVF-Flat, two cluster counts, eight probe settings) and graph (HNSW, two implementations, two graph degrees, six search-width settings) indexes were built over SIFT-128 (one million 128-dimensional vectors, Euclidean) and GloVe-100 (1.18 million 100-dimensional vectors, cosine), and each configuration was measured for recall@10 against the shipped ground truth, batched throughput over the 10,000-query test sets, single-query latency on one thread (the number an online service sees), build time and resident memory.

<!-- RESULTS SUMMARY: fill from results.json -->

The study follows the ann-benchmarks methodology at a scale an individual can reproduce, adds the serving-style single-query measurement that the batched-throughput convention omits, and reports every configuration run. Code and data provenance are public; the benchmark reproduces with one command.

## 1. Introduction

A nearest-neighbour query asks, for a query vector, which *k* vectors in a collection are closest under some metric. Exact answers require comparing the query with every vector (or with a large fraction of them: in high dimensions, tree indexes degrade to scans), which at a million vectors costs tens of milliseconds per query on one core and grows linearly. Approximate indexes return mostly-correct neighbours in a fraction of the time, and the engineering decision is where on the recall–speed curve to sit.

The ann-benchmarks project (Aumüller, Bernhardsson and Faithfull, 2020) standardised the comparison: public datasets with precomputed ground truth, recall@k against queries per second, and a published harness. Its leaderboards are comprehensive and they report batched throughput on dedicated hardware. Two things a practitioner designing a service needs are less visible there: the *single-query* latency at one thread, which is what a request-serving system pays, and the build-time and memory cost of each point on the curve, which decides whether the index can be rebuilt as data changes and whether it fits on the machine.

This paper measures all of those for the two dominant families on two standard datasets, on one laptop, with a design fixed in advance. Its purpose is a clear, reproducible reference for the trade-off, not a new index.

## 2. Data

Two datasets from ann-benchmarks.com in their distributed HDF5 form, downloaded on 1 October 2026 (provenance and byte counts in `data/SNAPSHOT.json`):

- **sift-128-euclidean**: 1,000,000 base vectors and 10,000 queries of 128-dimensional SIFT image descriptors (Jégou, Douze and Schmid, 2011), Euclidean distance.
- **glove-100-angular**: 1,183,514 base vectors and 10,000 queries of 100-dimensional GloVe word embeddings (Pennington, Socher and Manning, 2014), angular distance; vectors are L2-normalised so that inner product equals cosine similarity.

Each file ships the 100 exact nearest neighbours of every query; recall@10 is computed against the first ten.

## 3. Method

### 3.1 Indexes

- **flat**: exact search (FAISS `IndexFlatL2` / `IndexFlatIP`); the recall-1.0 reference.
- **ivf_flat**: FAISS `IndexIVFFlat`, *nlist* ∈ {1024, 4096} clusters trained on a fixed random sample of 50 × *nlist* vectors (seed 0), *nprobe* ∈ {1, 2, 4, 8, 16, 32, 64, 128}.
- **hnsw_faiss**: FAISS `IndexHNSWFlat`, *M* ∈ {16, 32}, *efConstruction* = 200, *efSearch* ∈ {16, 32, 64, 128, 256, 512}.
- **hnsw_usearch**: usearch HNSW, connectivity 16, expansion_add 200, expansion_search ∈ {16, 32, 64, 128, 256, 512}; an independent implementation of the same algorithm (Malkov and Yashunin, 2018).

Parameter ranges are the standard ann-benchmarks sweeps; nothing was tuned after seeing results.

### 3.2 Measurements

For each configuration: **recall@10**; **batched QPS**, the full 10,000-query set searched in one call with all cores, best of three timings; **single-query latency**, 500 queries (100 for the exact index) searched one at a time on one thread, reported as p50 and p99; **build time**; and **resident memory added** by the index. Thread count, library versions, processor, core count and RAM are recorded in `results.json`.

### 3.3 Reproducibility

`python benchmark.py` with the two HDF5 files in `data/` reproduces every number and figure. FAISS 1.15 (CPU), usearch 2.26, h5py, NumPy, psutil; Python 3.13. Expect one to two hours on a laptop, dominated by HNSW construction.

## 4. Results

<!-- RESULTS: fill from results.json
  Table 1: machine metadata
  Table 2: flat reference per dataset (recall 1.0, QPS, single p50/p99, memory)
  Table 3: for each family, the configuration reaching recall >= 0.95 and >= 0.99 at the highest QPS, with its single p99,
           build time and memory
  Figure 1: recall vs batched QPS frontiers; Figure 2: recall vs single-query p99; Figure 3: build time and memory
  Text: shape of frontiers; IVF vs HNSW crossover; the two HNSW implementations compared; batched vs single-query gap;
        build/memory cost; dataset differences (SIFT easier than GloVe)
-->

## 5. Discussion

<!-- fill after results -->

## 6. Limitations

*One machine.* Absolute QPS and latency belong to the test laptop; the frontiers' shapes and the relative positions of index families are the transferable result.

*Two datasets, one million scale.* Both are standard and both are small by production standards. Behaviour at a hundred million or a billion vectors, where compression (product quantisation) becomes necessary, is not measured.

*No quantisation, no filtering, no updates.* Flat vectors only; no metadata filtering, which changes graph-index behaviour substantially; no insertions or deletions after build. Each is a separate study.

*Library defaults.* Beyond the swept parameters, everything is each library's default. Both libraries have further knobs that a tuned deployment would use.

*Recall@10 only.* Applications that need recall@100, or that re-rank a larger candidate set, face a different curve.

## 7. Conclusion

<!-- fill after results -->

## References

- Aumüller, M., Bernhardsson, E. & Faithfull, A. (2020). ANN-Benchmarks: A benchmarking tool for approximate nearest neighbor algorithms. *Information Systems*, 87, 101374.
- Malkov, Y. A. & Yashunin, D. A. (2018). Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 42(4), 824–836.
- Johnson, J., Douze, M. & Jégou, H. (2019). Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data*, 7(3), 535–547.
- Douze, M. et al. (2024). The Faiss library. arXiv:2401.08281.
- Jégou, H., Douze, M. & Schmid, C. (2011). Product quantization for nearest neighbor search. *IEEE TPAMI*, 33(1), 117–128.
- Pennington, J., Socher, R. & Manning, C. D. (2014). GloVe: Global vectors for word representation. *EMNLP 2014*.
- Vardanian, A. (2023). USearch: Smaller & faster single-file vector search engine. Software, version 2.x.
- Li, W. et al. (2020). Approximate nearest neighbor search on high dimensional data: Experiments, analyses, and improvement. *IEEE TKDE*, 32(8), 1475–1488.

## Data and code availability

Code, `results.json`, figures and `data/SNAPSHOT.json` are at https://github.com/Pranjulrathour/research under `papers/p4-ann-frontiers/`. The HDF5 datasets are redistributed by ann-benchmarks.com and are not committed here (1 GB).

## Declaration

The author has no competing interests and received no funding for this work.
