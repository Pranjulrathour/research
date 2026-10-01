# Chapter 4 — Data structures at scale

Every computer-science student learns that a hash table looks up in constant time and a balanced tree in logarithmic time, and that constant beats logarithmic. Every engineer who has profiled a real system has watched a hash table lose to a sorted array, a tree beat a hash table, and a theoretically slower structure win by a factor of ten because of where its bytes sat in memory. Both groups are right. Big-O describes how cost grows; it says nothing about what the cost is, and at scale the constants, the memory hierarchy and the access pattern decide the result.

This chapter is about the structures that large systems are actually built from, what each buys and costs in practice rather than in asymptotics, and a modern case, approximate nearest-neighbour search, in which the trade-off between accuracy and speed is explicit, measurable and, in the companion study, measured.

## The principle

**Asymptotic complexity is necessary and not sufficient. Choose structures by the access pattern and the memory hierarchy, measure the constants on your data, and when exactness is not required, trade it deliberately for speed along a curve you have measured.**

## Why Big-O is not enough

Three facts about hardware dominate data-structure performance at scale, and none of them appears in an asymptotic analysis.

**Memory is a hierarchy with cliffs.** A load from a register takes under a nanosecond; from the first-level cache, about one; from main memory, around a hundred; from a local SSD, around a hundred thousand; from a disk or a network, millions.[^1] Each level is roughly a hundred times slower than the one above. A structure whose operations touch memory in a pattern that stays in cache can be a hundred times faster than one with the same Big-O that does not, and a structure that fits in memory is a thousand times faster than the same structure spilled to disk. "O(log n) comparisons" says nothing about how many of those comparisons miss cache.

**Sequential beats random.** Hardware prefetches memory and disk in blocks; reading the next byte is nearly free, reading a random one is a full miss. A linear scan over a contiguous array can beat a pointer-chasing tree even when the tree does asymptotically less work, up to surprisingly large sizes, because the scan's accesses are predictable and the tree's are not. This is why columnar storage, log-structured storage and sorted runs appear throughout large systems: they turn random access into sequential.

**Constants are large and differ by a hundred.** Hashing a key, following a pointer, comparing two strings, allocating a node: each has a cost that depends on the language, the allocator and the data, and the differences between implementations of the "same" structure are routinely tenfold. The only way to know a constant is to measure it on your data on your hardware.

The practical conclusion is not to abandon complexity analysis. It is to use it to rule out structures that cannot scale, and then to choose among the survivors by measurement.

## The structures large systems are built from

A short field guide. Each entry says what the structure is for, what it costs, and the question that decides whether it fits.

**Hash tables.** Point lookup by exact key; the default in-memory index. Expected constant time, with the constant dominated by the hash function and the cache miss to the bucket. Costs: no ordering (range queries are impossible), resize pauses (a table that doubles must rehash everything, which is a latency spike in a serving system unless done incrementally), and memory overhead for load factor and pointers. *Question: do I only ever look up by exact key?*

**B-trees and their variants.** Ordered storage with logarithmic lookup, range scans and in-place updates; the structure beneath most relational database indexes and many file systems. Wide nodes (hundreds of keys) sized to a disk or memory page keep the tree shallow (three or four levels for billions of keys) so that a lookup is a handful of page reads. Costs: write amplification (an insert may rewrite a page), fragmentation, and random writes on disk. *Question: do I need range queries or ordered iteration, with reads dominating?*

**Log-structured merge trees (LSM).** Writes go to an in-memory structure and are flushed as sorted runs to disk; reads consult several runs; background compaction merges them. The structure beneath most write-heavy stores (LevelDB, RocksDB and the databases built on them, Cassandra, HBase). Buys sequential writes and very high write throughput; costs read amplification (a read may check several levels; Bloom filters mitigate), compaction's background IO and the latency spikes it can cause, and space amplification during merges.[^2] *Question: is this write-heavy, and can reads tolerate a few extra lookups?*

**Skip lists.** A probabilistic ordered structure with logarithmic operations and simple concurrent implementation; used where an ordered in-memory structure must be modified by many threads (the memtable in several LSM stores, sorted sets in Redis). Costs: pointer-chasing (cache-unfriendly) and memory for the extra levels. *Question: ordered, in memory, concurrent?*

**Bloom filters.** A compact probabilistic set that answers "definitely not present" or "probably present" with a tunable false-positive rate, in a few bits per element. Used to avoid expensive lookups (does this key exist in that run on disk? is this URL in the malware list? has this item been seen?). Costs: no deletion in the basic form, no enumeration, and false positives that must be acceptable. *Question: can I afford occasional false positives to skip most lookups?*

**HyperLogLog.** Counts distinct elements in a stream to within a few per cent using about a kilobyte, regardless of how many billions of distinct items there are. Used for cardinality (unique visitors, distinct queries) where an exact count would require storing every item. *Question: is approximately-right distinct counting good enough?*

**Inverted indexes.** Map each term to the list of documents containing it; the structure beneath every search engine. Buys fast text query; costs index build time, update complexity, and size comparable to the corpus. *Question: do I search by content rather than by key?*

**Vector indexes.** Find the items whose embedding vectors are nearest to a query vector; the structure beneath semantic search, recommendation and retrieval-augmented AI systems. The subject of the rest of this chapter, because it is the clearest modern example of a structure whose correctness is a dial rather than a guarantee.

## A modern case: approximate nearest-neighbour search

Represent each item (a document, an image, a product, a user) as a vector of a few hundred numbers, produced by a model so that similar items have nearby vectors. Retrieval becomes geometry: given a query vector, find the *k* items whose vectors are closest. Every semantic search, every "similar items" feature and every retrieval step in an AI application does this, often over millions or billions of vectors, often within a latency budget of tens of milliseconds.

**Exact search is a scan.** Comparing a query against a million 128-dimensional vectors is 128 million multiply-adds: a few tens of milliseconds on one core, and linear in the collection size. For a single query against a million vectors it is tolerable; against a billion, or at thousands of queries a second, it is not. There is no exact index that escapes this in high dimensions; the "curse of dimensionality" means tree structures that work in two or three dimensions degrade to scans in a hundred.

**Approximate search trades recall for speed.** An approximate index returns *k* neighbours that are mostly, but not always, the true *k* nearest. The quality measure is **recall@k**: the fraction of the true *k* that the index found. The price measure is throughput (queries per second) or per-query latency, plus build time and memory. Every approximate index has a knob (how much of the structure to explore per query), and turning it traces a **frontier**: a curve of recall against speed, along which the engineer picks a point.

Two families dominate.[^3]

*Inverted-file (IVF) indexes* cluster the vectors (say into 1,024 or 4,096 cells with k-means), and at query time search only the cells nearest the query. The knob is the number of cells probed. Build is fast; memory is close to the raw vectors; recall rises with probes and so does cost. Compression of the vectors within cells (product quantisation) trades further accuracy for memory, which is how billion-scale indexes fit in RAM.

*Graph indexes*, of which HNSW (Hierarchical Navigable Small World) is the standard, connect each vector to a few dozen neighbours and search by greedy walking from an entry point toward the query, with a beam of candidates. The knob is the beam width (often called `ef`). Graph indexes typically reach high recall at lower per-query cost than IVF; they cost more to build (minutes to hours for millions of vectors) and more memory (the graph's edges), and they are harder to update incrementally.[^4]

## What the measurements show

The companion study (Appendix A; paper P4) built exact, IVF and HNSW indexes (the last in two independent implementations) over two standard public datasets, one million 128-dimensional SIFT descriptors and 1.18 million 100-dimensional GloVe word vectors, and measured, for each configuration, recall@10 against the shipped ground truth, batched throughput, single-query latency on one thread (the number an online service sees), build time and memory.

<!-- P4 numbers: fill from papers/p4-ann-frontiers/results.json after the run -->

Three features of the frontiers are worth carrying away regardless of the exact numbers.

The frontier is steep near the top. Going from 90 to 95 per cent recall is cheap; from 99 to 99.9 is expensive; and exact search (100 per cent) is a different regime entirely. The engineer's job is to decide how much recall the application needs, which is a product question (does a user notice if one of ten results is the eleventh-nearest rather than the tenth?) before it is an engineering one.

Batched throughput and single-query latency are different numbers for the same index. Batched search over thousands of queries amortises overheads and uses every core; a service answering one query at a time on one thread sees a latency that can be an order of magnitude less favourable per query. Quoting one when the workload is the other is the most common error in vector-search capacity planning.

Build time and memory are part of the trade. The index that searches fastest may take longest to build and most to hold, which matters for an index that must be rebuilt as data changes or that must fit on a given machine. Chapter 11's cost lens applies.

## The question you will be asked

*"Design a system that finds the 10 most similar items among a billion in under 50 ms."*

Start with the arithmetic. A billion vectors of 128 32-bit floats is 512 GB: too large for one machine's memory, so compression (product quantisation to 16–64 bytes per vector brings it to 16–64 GB) or partitioning across machines, or both. Exact search is out: a billion distance computations per query is seconds, not milliseconds. So an approximate index, and the first question back to the interviewer is *what recall do you need*, because it decides everything downstream.

Then the design. Partition the collection (by IVF cell or by hash) across a few dozen machines so each holds a shard that fits in memory. On each shard, an IVF index with product-quantised vectors (memory-efficient at this scale) or an HNSW graph over quantised vectors (faster per query, more memory). A query is broadcast to the shards (or to the shards owning the nearest cells), each returns its top candidates in a few milliseconds, a coordinator merges them, and the final *k* are re-ranked against full-precision vectors fetched for only those candidates. Budget: network fan-out and merge, 5–10 ms; per-shard search, 10–20 ms at p99; re-rank, a few ms; headroom for the tail (chapter 1), because the user's latency is the slowest shard's.

Then operations: how new vectors are added (IVF accepts appends cheaply; graphs less so; most systems batch inserts and rebuild periodically), how recall is monitored in production (sample queries, compute exact neighbours offline, track recall over time as the data drifts), and what degrades under load (probe fewer cells, lower the beam width: the frontier is also a load-shedding dial). An answer that states the recall question, does the memory arithmetic, and knows that the frontier can be turned down under load is an answer from someone who has built one.

## The trade-off, stated

Choosing a structure by Big-O alone buys a defensible argument and costs the tenfold factors that memory hierarchy and constants impose. Measuring on your data costs an afternoon and buys the actual number. Approximate structures (Bloom filters, HyperLogLog, vector indexes) buy orders of magnitude in speed and memory and cost exactness, which must be given up deliberately, measured and monitored, because an approximation whose error nobody tracks is a bug nobody can find.

## Run this yourself

Run the P4 benchmark (or, for a quicker experiment, its first dataset only). Then do two things. First, take the HNSW results and plot single-query p99 latency against recall; find the point where the curve turns upward and ask what the application you have in mind would lose at that recall. Second, write a twenty-line exact search with NumPy over the same million vectors and time it for one query and for a batch of a thousand; compare with the flat index's numbers in the results, and notice how much of the difference is the library's use of your cores. Then, with the frontier in front of you, write down the recall you would choose for a product search, a near-duplicate detector and a retrieval step for an AI assistant, and why they differ. That reasoning, with the measured curve to back it, is the chapter.

---

[^1]: The "latency numbers every programmer should know", originally compiled by Jeff Dean and Peter Norvig and updated by others for current hardware; the ratios matter more than the absolute figures, which shift every few years.
[^2]: O'Neil, P., Cheng, E., Gawlick, D. & O'Neil, E. (1996), "The Log-Structured Merge-Tree (LSM-Tree)", *Acta Informatica* 33(4).
[^3]: Aumüller, M., Bernhardsson, E. & Faithfull, A. (2020), "ANN-Benchmarks: A benchmarking tool for approximate nearest neighbor algorithms", *Information Systems* 87 — the public benchmark and datasets the companion study uses.
[^4]: Malkov, Y. A. & Yashunin, D. A. (2018), "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs", *IEEE TPAMI* 42(4); Johnson, J., Douze, M. & Jégou, H. (2019), "Billion-scale similarity search with GPUs", *IEEE Transactions on Big Data* 7(3) — FAISS, including product quantisation at billion scale.

### Sources for this chapter
- Dean & Norvig, "Latency numbers every programmer should know" (various updated versions).
- O'Neil et al. (1996) — LSM trees; Bayer, R. & McCreight, E. (1972), "Organization and Maintenance of Large Ordered Indexes", *Acta Informatica* 1(3) — B-trees.
- Bloom, B. H. (1970), "Space/time trade-offs in hash coding with allowable errors", *CACM* 13(7); Flajolet, P. et al. (2007), "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm", *AofA 2007*.
- Pugh, W. (1990), "Skip Lists: A Probabilistic Alternative to Balanced Trees", *CACM* 33(6).
- Malkov & Yashunin (2018) — HNSW; Jégou, H., Douze, M. & Schmid, C. (2011), "Product Quantization for Nearest Neighbor Search", *IEEE TPAMI* 33(1); Johnson, Douze & Jégou (2019) — FAISS; Aumüller et al. (2020) — ANN-Benchmarks.
- Kleppmann (2017), *Designing Data-Intensive Applications*, chapter 3 — storage engines (B-trees vs LSM) for practitioners.
- Paper P4 in the companion repository (Appendix A) — the measurements referred to in this chapter.
