# Systems That Scale: The Engineering Judgment Behind Reliable, Low-Latency Software
### Pranjul Rathour

**Promise to the reader.** The judgment behind system design, taught through measurement. Every chapter states a principle,
shows it with a number you can reproduce, names the trade-off, and ends with the question an interviewer or an incident
review will ask. No framework-of-the-month; the principles predate the cloud and will outlast it.

**Design rules.** Every quantitative claim is either measured in the companion research repository (papers P3 and P4) or
cited to a primary source with a year. Each chapter ends with "The question you will be asked" and "Run this yourself".
Target ~45,000 words; 12 chapters.

---

## Part I — Latency

### 1. Latency is a distribution, not a number
- Why averages lie: p50, p95, p99, p99.9 and who experiences each; the "tail at scale" problem (Dean & Barroso 2013)
- Latency budgets: decomposing an end-to-end target into stage budgets; where time actually goes in a request
- Measuring correctly: coordinated omission, warm-up, repeated runs, confidence intervals (P3's method as the worked example)
- *Run this*: the P3 harness; *Question*: "Your p50 is 20 ms and your p99 is 2 s. What is happening?"

### 2. Concurrency models and the price of blocking
- Threads, event loops, hybrids; what blocks what; the GIL and its equivalents; why CPU-bound work on an event loop is the classic self-inflicted outage
- P3 results: how p99 diverges across threaded / async / hybrid designs as concurrency rises, on IO-, CPU- and mixed workloads
- Backpressure, bounded queues and load shedding: the system that says no survives
- *Question*: "When would you choose threads over async?"

### 3. Caching: the fastest request is the one you don't make
- Cache hit rate economics; TTL vs invalidation; cache stampedes and how to prevent them; what must never be cached under a shared key
- Multi-level caches (process, Redis, CDN) and the consistency price of each
- Semantic caches for AI workloads as a special case
- *Question*: "How do you invalidate a cache when the source of truth changes?"

### 4. Data structures at scale
- Why Big-O is necessary and not sufficient: constants, cache lines, memory bandwidth
- Hash tables, B-trees, LSM trees, skip lists, bloom filters, HyperLogLog: what each buys and costs
- Approximate nearest-neighbour search as a modern case: P4's recall-vs-QPS frontiers for flat, IVF and HNSW indexes
- *Question*: "Design a system that finds the 10 most similar items among a billion in under 50 ms."

## Part II — Correctness under failure

### 5. Consistency, availability and what you actually get
- CAP as a statement about partitions, not a menu; PACELC; linearizability vs eventual consistency in plain terms
- Read-your-writes, monotonic reads, causal consistency: which user-visible promises each model keeps
- Where the big systems sit and why (DynamoDB, Spanner, Cassandra, Postgres replication) with years
- *Question*: "A user updates their profile and immediately sees the old value. Where did it come from?"

### 6. Replication, partitioning and the two hard problems
- Leader-follower, multi-leader, leaderless; quorums; failover and split-brain
- Partitioning keys, hot spots, rebalancing; secondary indexes across partitions
- Distributed transactions, sagas, idempotency keys, exactly-once as a lie and at-least-once as a discipline
- *Question*: "Design a payment system that never double-charges."

### 7. Failure is the normal case
- Timeouts, retries with jitter, circuit breakers, bulkheads; retry storms and how they take down healthy systems
- Graceful degradation: deciding in advance what to drop; fallbacks that are tested, not assumed
- Chaos testing, game days, blameless post-mortems; the five whys and the one why
- *Question*: "Your dependency's latency doubled. What happens to your service in the next 60 seconds?"

### 8. Queues, streams and asynchrony
- When to make something asynchronous and when it is a mistake; queue depth as the health metric; dead-letter queues
- Ordering guarantees, partitions, consumer groups; log-based systems (Kafka-style) vs message queues
- Workflows and background jobs: the difference between "fire and forget" and a job that must complete
- *Question*: "A job queue is growing. Is the system healthy?"

## Part III — Operating and deciding

### 9. Observability: you cannot fix what you cannot see
- Logs, metrics, traces; the request ID that follows a call everywhere; cardinality and cost
- SLIs, SLOs, error budgets: turning reliability into a decision rule, not a slogan
- Alerting on symptoms not causes; alert fatigue
- *Question*: "Define an SLO for a search API and say what you would do when the budget is spent."

### 10. Capacity planning and performance testing
- Little's law and why it answers most capacity questions; utilisation vs latency (the knee of the curve)
- Load testing that means something: open vs closed loop, realistic mixes, soak tests
- Headroom, autoscaling lag, and why "it scales" is a claim that needs a number
- *Question*: "Traffic will triple for a launch. What do you check, in what order?"

### 11. Cost is a design constraint
- The cost model of compute, storage, egress and managed services; where money leaks (idle, over-provisioning, chatty services)
- Performance per rupee: when the slower design is the right one; free tiers and their cliffs
- Build vs buy vs rent, decided with numbers
- *Question*: "Cut this system's bill by 40% without changing its SLO."

### 12. Judgment: how to make and document a design decision
- Requirements before architecture: the questions to ask first (chapter 1's budget, chapter 5's guarantees, chapter 11's cost)
- Architecture decision records; stating the trade-off you accepted and what would change your mind
- The system-design interview as a compressed version of the real job: a method that works in both
- A closing checklist: twelve questions to ask of any design

---

## Front and back matter
- Preface: why measurement, why now (cheap plausibility makes checkable engineering more valuable)
- Appendix A: the P3 and P4 methods and how to re-run them
- Appendix B: a latency-budget worksheet and an SLO worksheet
- Appendix C: reading list (Dean & Barroso 2013; Kleppmann 2017; Google SRE books 2016/2018; Jeff Dean's numbers every engineer should know, updated; Hellerstein et al. on consistency; Gray & Reuter on transactions)
- Sources by chapter; about the author

## Measurements this book depends on (from the research repo)
- P3 `results.json`: p50/p95/p99 by server design x workload x concurrency, with machine spec
- P4 `results.json`: recall@10 vs QPS, build time and memory for flat / IVF / HNSW on SIFT-128 and GloVe-100
- All other numbers cited with year and source; none invented.
