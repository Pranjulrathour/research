# Appendix A — The benchmark methods and how to re-run them

The measurements in chapters 1, 2 and 4 come from two small, fully published benchmark studies in the companion repository (github.com/Pranjulrathour/research). This appendix records their methods so that a reader can judge the numbers and reproduce them. Absolute figures depend on the machine; the comparisons do not, and the machine is recorded with every result.

## A.1 Tail latency of API server designs (papers/p3-tail-latency)

**Question.** How do p50, p95 and p99 latency diverge across threaded, event-loop (async) and hybrid server designs as concurrency rises, on IO-bound, CPU-bound and mixed workloads?

**Servers.** Four minimal HTTP servers in Python, identical in protocol and response, differing only in concurrency model: (a) a thread-per-connection server; (b) a single event loop with CPU-bound work run inline (the classic mistake); (c) an event loop that hands CPU-bound work to a thread pool (responsive, but still serialised by the interpreter lock); (d) an event loop that hands CPU-bound work to a process pool (the pattern that uses the cores). No framework; the point is the model, not the library. Whether the interpreter had its global lock enabled is recorded with the results.

**Workloads.** *IO-bound*: each request awaits a simulated 20 ms downstream call. *CPU-bound*: each request performs a fixed hashing loop calibrated to about 3 ms on one core (the measured value is recorded with the results). *Mixed*: the 20 ms wait followed by the same computation.

**Load.** A closed-loop asynchronous load generator with *N* concurrent keep-alive clients, *N* ∈ {1, 8, 32, 128, 256}, each sending 40 requests one after another. Every path is warmed up first; each cell is run three times, the repeat with the median p99 is kept, and all three p99s are recorded. The closed-loop choice is deliberate, and chapter 10 explains what it does and doesn't measure: it answers "with *N* concurrent clients, what latency does each one see?" and isn't a fixed-rate capacity test.

**Metrics.** p50, p95, p99 and maximum latency, throughput, and the ratio p99/p50 as a one-number measure of tail heaviness.

**Reproduce.** `cd papers/p3-tail-latency && python harness.py`. It writes `results.json` (whose `meta` records the processor, core count, Python version, whether the interpreter lock was enabled, and the background load on the machine at the start and after each server) and three figures. The harness waits for a quiet machine before it starts, because background programs inflate tails unevenly across designs; on the first attempt, an emulator running in the background was enough to distort the results.

## A.2 Recall–latency frontiers of approximate nearest-neighbour indexes (papers/p4-ann-frontiers)

**Question.** For vector similarity search at the scale of a million vectors, how do exact search, inverted-file (IVF) and graph (HNSW) indexes trade recall for throughput, build time and memory?

**Datasets.** The standard public ann-benchmarks sets: SIFT-128 (one million 128-dimensional vectors, Euclidean) and GloVe-100 (about 1.18 million 100-dimensional word vectors, angular distance), each with 10,000 held-out queries and precomputed exact 100-nearest-neighbour ground truth.

**Indexes.** Flat (exact, brute force) as the recall-1.0 reference; IVF-Flat with a range of cluster counts and probe counts; HNSW in two implementations (FAISS and usearch) with a range of graph and search parameters. Each configuration is built once (build time and memory recorded) and queried at several search-effort settings to trace its frontier.

**Metrics.** Recall@10 against the ground truth; batched queries per second over all 10,000 queries, using one thread per physical core; single-query latency (p50 and p99 over 500 queries, one at a time, on one thread), which is what an online service actually experiences; build time; and index memory. The frontier for each index family is the set of (recall, speed) points not beaten on both axes by another point of the same family.

**Reproduce.** Download the two HDF5 files from ann-benchmarks.com into `papers/p4-ann-frontiers/data/` (about 1 GB; the URLs are in `data/SNAPSHOT.json`), then `cd papers/p4-ann-frontiers && python benchmark.py`. It builds every configuration and writes `results.json` and the figures. Like P3, it waits for a quiet machine and records the background load. Expect an hour or two on a laptop.

## A.3 Reading the numbers

Three cautions apply to both studies, and to any benchmark you read.

The first is that each study ran on a single machine, my laptop, which is specified in each `results.json`. A server-class machine, a different Python build or a different operating system will move every absolute number. The comparisons within each study are the finding.

The second is that the workloads are synthetic. The IO wait is a sleep, the computation is a loop, the vectors are a public dataset. Real workloads are messier and their tails heavier, so the studies show the shape of the trade-offs rather than their size in your system.

The third is that both designs were fixed before running, and every configuration that was run is reported. Where something was changed along the way (a socket default that made one server refuse connections, a thread count that made results hostage to background load), the script's docstring and comments say so. Hold other people's benchmarks to the same standard.

---

# Appendix B — Two worksheets

## B.1 Latency budget

For one user-facing operation. Fill in measured values where you have them and estimates, marked as such, where you do not. The budget is the target at the percentile that matters, and the sum of the stages must fit inside it with headroom.

| Stage | p50 (ms) | p99 (ms) | Measured or estimated? | Can it be removed, cached, parallelised? |
|---|---|---|---|---|
| Client processing before request | | | | |
| Network to edge (user's connection) | | | | |
| Edge / CDN / load balancer | | | | |
| Service: authentication, routing | | | | |
| Service: dependency call 1 | | | | |
| Service: dependency call 2 | | | | |
| Service: database query | | | | |
| Service: serialisation, response | | | | |
| Network back to client | | | | |
| Client rendering | | | | |
| **Total** | | | | |
| **Budget (target)** | | | | |
| **Headroom** | | | | |

Rules of thumb while filling it in: the p99 total is not the sum of the stage p99s (that is the worst case) nor the sum of the p50s (that is the median); it lies between, and the only way to know it is to measure end to end. The stages that are sequential add; stages that can run in parallel contribute their maximum. The stage with the largest p99 is where the work is.

## B.2 SLO definition

One sheet per service, two or three SLOs per service.

| | SLO 1 | SLO 2 | SLO 3 |
|---|---|---|---|
| Indicator (what is measured, as a ratio) | | | |
| Measured where (edge, client, server)? | | | |
| What counts as "good"? (status codes, latency threshold) | | | |
| What is excluded (health checks, bots)? | | | |
| Target (percentage) | | | |
| Window (days) | | | |
| Error budget in the window (minutes or request count) | | | |
| Fast burn alert: burn rate, lookback, action | | | |
| Slow burn alert: burn rate, lookback, action | | | |
| Policy when budget is exhausted | | | |
| Owner, review date | | | |

Two checks before you adopt it: a user who experienced exactly the target would describe the service as acceptable (if not, the target is too loose); and the team can state what it would do differently with the budget at 100% versus at 0% (if not, the budget is a number, not a decision rule).

---

# Appendix C — Reading list

Primary sources and the handful of books that practitioners actually return to. Roughly in the order this book draws on them.

**Latency and performance**
- Dean, J. & Barroso, L. A. (2013), "The Tail at Scale", *Communications of the ACM* 56(2).
- Gregg, B. (2020), *Systems Performance: Enterprise and the Cloud*, 2nd ed., Addison-Wesley.
- Tene, G., "How NOT to Measure Latency" (talks, 2013–2015) and the HdrHistogram documentation.
- Schroeder, B., Wierman, A. & Harchol-Balter, M. (2006), "Open Versus Closed: A Cautionary Tale", *NSDI 2006*.
- Little, J. D. C. (1961), "A Proof for the Queuing Formula: L = λW", *Operations Research* 9(3).

**Data systems and consistency**
- Kleppmann, M. (2017), *Designing Data-Intensive Applications*, O'Reilly. If you read one book from this list, read this one.
- Gilbert, S. & Lynch, N. (2002), "Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services", *ACM SIGACT News* 33(2); Brewer, E. (2012), "CAP Twelve Years Later", *IEEE Computer*.
- Abadi, D. (2012), "Consistency Tradeoffs in Modern Distributed Database System Design", *IEEE Computer* 45(2).
- Terry, D. B. et al. (1994), "Session Guarantees for Weakly Consistent Replicated Data", *PDIS 1994*.
- DeCandia, G. et al. (2007), "Dynamo: Amazon's Highly Available Key-value Store", *SOSP 2007*.
- Corbett, J. C. et al. (2012), "Spanner: Google's Globally-Distributed Database", *OSDI 2012*.
- Ongaro, D. & Ousterhout, J. (2014), "In Search of an Understandable Consensus Algorithm", *USENIX ATC 2014*.
- Gray, J. & Reuter, A. (1993), *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann.
- Garcia-Molina, H. & Salem, K. (1987), "Sagas", *SIGMOD 1987*.
- Helland, P. (2012), "Idempotence Is Not a Medical Condition", *ACM Queue* 10(4).

**Caching and search**
- Nishtala, R. et al. (2013), "Scaling Memcache at Facebook", *NSDI 2013*.
- Malkov, Y. A. & Yashunin, D. A. (2018), "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs", *IEEE TPAMI* 42(4).
- Johnson, J., Douze, M. & Jégou, H. (2019), "Billion-scale similarity search with GPUs", *IEEE Transactions on Big Data* 7(3) — the FAISS paper.
- Aumüller, M., Bernhardsson, E. & Faithfull, A. (2020), "ANN-Benchmarks: A benchmarking tool for approximate nearest neighbor algorithms", *Information Systems* 87.

**Failure, operations and reliability**
- Nygard, M. T. (2018), *Release It!*, 2nd ed., Pragmatic Bookshelf.
- Beyer, B. et al. (eds.) (2016), *Site Reliability Engineering*, O'Reilly; and (2018), *The Site Reliability Workbook*, O'Reilly. Both free to read online.
- Basiri, A. et al. (2016), "Chaos Engineering", *IEEE Software* 33(3).
- Hamilton, J. (2007), "On Designing and Deploying Internet-Scale Services", *LISA 2007*.
- Majors, C., Fong-Jones, L. & Miranda, G. (2022), *Observability Engineering*, O'Reilly.
- Sigelman, B. H. et al. (2010), "Dapper, a Large-Scale Distributed Systems Tracing Infrastructure", Google.

**Streams and messaging**
- Kreps, J. (2013), "The Log: What every software engineer should know about real-time data's unifying abstraction", LinkedIn Engineering.
- Hohpe, G. & Woolf, B. (2003), *Enterprise Integration Patterns*, Addison-Wesley.

**Judgment**
- Lampson, B. W. (1983), "Hints for Computer System Design", *SOSP 1983*.
- Brooks, F. P. (1995), *The Mythical Man-Month*, anniversary ed., Addison-Wesley.
- Nygard, M. (2011), "Documenting Architecture Decisions".
- Gunther, N. J. (2007), *Guerrilla Capacity Planning*, Springer.

---

# About the author

**Pranjul Rathour** is a generative-AI engineer from Kanpur, India. He builds production systems around large language models (retrieval, evaluation, agents and the reliability engineering that holds them together) and has won first prize at three hackathons for applied AI work. He has mentored more than two hundred students in India and abroad on careers in software and AI.

His research, including the two benchmark studies behind this book and three further empirical papers in finance and machine learning, is published with code and data at github.com/Pranjulrathour/research. He writes at pranjulrathour.com. *The AGI Transition: A Field Guide for the Next Decade*, the companion to this volume, takes the wider view of what capable AI means for work, learning and institutions.

He can be reached at pranjulrathour41@gmail.com, and he is easy to find online:

- Website: [pranjulrathour.com](https://pranjulrathour.com)
- GitHub: [github.com/Pranjulrathour](https://github.com/Pranjulrathour)
- LinkedIn: [linkedin.com/in/pranjul-rathour](https://www.linkedin.com/in/pranjul-rathour/)
- X: [x.com/PranjulRathourx](https://x.com/PranjulRathourx)
- Instagram: [instagram.com/pranjulrathour.in](https://www.instagram.com/pranjulrathour.in/)
- Threads: [threads.com/@pranjulrathour.in](https://www.threads.com/@pranjulrathour.in)
- Bluesky: [bsky.app/profile/pranjulrathour.bsky.social](https://bsky.app/profile/pranjulrathour.bsky.social)
- Facebook: [facebook.com/profile.php?id=1377591238763842](https://www.facebook.com/profile.php?id=1377591238763842)
- Dev.to: [dev.to/pranjulrathour](https://dev.to/pranjulrathour)
- Hashnode: [pranjulrathour.hashnode.dev](https://pranjulrathour.hashnode.dev)
- Blogger: [pranjulrathourtechguru.blogspot.com](https://pranjulrathourtechguru.blogspot.com)
