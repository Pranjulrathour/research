# Chapter 3 — Caching: the fastest request is the one you don't make

Every performance conversation eventually arrives at a cache, and most production incidents involving a cache were caused by someone who added one without asking what it would do when it was wrong, empty or shared. A cache is the single most effective latency tool in the engineer's kit and the single most common source of the bugs that are hardest to reproduce, and both facts come from the same property: a cache is a deliberate decision to serve data that might be stale.

This chapter is about making that decision well: when a cache pays, what it costs, how it fails, and the few rules that prevent the failures that recur.

## The principle

**A cache trades freshness for latency and load. Decide how stale is acceptable before you build it, make invalidation part of the design rather than an afterthought, and never cache anything under a key that does not include everything the value depends on.**

## The arithmetic of a hit rate

A cache in front of a slow source is described by three numbers: the hit latency *h*, the miss latency *m* (which includes the source's latency plus the cache's own overhead), and the hit rate *p*. The average latency is

> *p* × *h* + (1 − *p*) × *m*.

Suppose *h* = 1 ms (an in-memory lookup over a local network) and *m* = 50 ms (a database query). At a 50 per cent hit rate the average is 25.5 ms, a halving. At 90 per cent, 5.9 ms. At 99 per cent, 1.5 ms. The curve is steep near the top, which has two consequences.

The last few per cent of hit rate are worth more than the first fifty. Moving from 90 to 99 per cent cuts the average four times further; moving from 0 to 50 only halves it. This is why cache tuning is about the long tail of keys, not the popular ones, which are hits anyway.

The *tail* latency is still the miss latency. Chapter 1 made the case that users experience percentiles, not averages, and a cache does nothing for the request that misses. If your p99 target is 20 ms and your source takes 50 ms, a 99 per cent hit rate does not meet the target: one request in a hundred still takes 50 ms, and that is exactly the p99. A cache improves the average and the load. It improves the tail only if the hit rate is high enough that misses fall outside the percentile you care about, or if the misses themselves are made faster.

Load is often the real reason. If the source can serve 1,000 queries a second and the application needs 10,000, a 90 per cent hit rate is not a latency optimisation; it is the difference between a working system and a fallen-over one. When a cache is doing this job, the question to ask is what happens when it is empty.

## Three places to cache, and what each costs in truth

**In the process.** A dictionary in memory, bounded by size and perhaps by age. Hit latency is nanoseconds to microseconds. The costs: each process has its own copy, so the same key may hold different values on different servers, and a deployment starts cold. Use for small, slowly-changing data (configuration, feature flags, reference tables) and for memoising pure computations.

**In a shared cache (Redis, Memcached and their managed forms).** One copy, shared by all processes, over a network hop: hit latency of a few hundred microseconds to a millisecond or two. The costs: a network dependency that can fail or slow down, a new component to operate, and the consistency question becomes real because now the cache is a second system of record that the first does not know about. Use for session state, rendered fragments, query results, rate-limit counters, anything read far more often than written.

**At the edge (CDN, browser).** Copies close to the user, hit latency dominated by the last mile. The costs: invalidation is slow and partial (a purge propagates in seconds to minutes), the cache is controlled by headers you set once and cannot easily take back, and anything personal cached at the edge under a shared key is a data breach waiting to happen. Use for static assets and for public content that can tolerate minutes of staleness.

Each level further from the source is faster, more shared, and harder to keep truthful. A design that uses all three must answer, at each level, the same question: when the source changes, how does this copy find out?

## Invalidation: the two hard things

The joke that there are only two hard problems in computer science, cache invalidation and naming things, endures because invalidation really is hard, and the reason is that it requires the system of record to know about every copy. There are only a few strategies, and each has a well-known failure.

**Time to live (TTL).** Each entry expires after a fixed period. Simple, needs no coordination, and bounds staleness: a 60-second TTL means data is at most a minute old. The failure is that it is at most a minute old *always*, including the second after the source changed, so a TTL is a statement that a minute of staleness is acceptable for this data. If that statement is false, no TTL is short enough: a one-second TTL on a balance still shows the wrong balance for a second.

**Explicit invalidation.** When the source changes, delete the cached entry (or update it). Fresh data immediately, at the cost of coupling: every code path that writes the source must know every key that depends on it. The failure is the path somebody forgot, usually a batch job or a migration, which leaves stale entries that no TTL will clear. The standard mitigation is to combine the two: invalidate explicitly and keep a long TTL as the safety net.

**Write-through.** Writes go to the cache and the source together, so the cache is never stale for data written through it. The failure is data written by anything else, and the extra write latency.

**Event-driven invalidation.** The source publishes change events (a change-data-capture stream from the database, a message on a bus) and the caches subscribe. Decouples writers from caches and scales to many caches. The failure is the delay and the dropped event, so it too wants a TTL behind it.

Whichever strategy, two rules hold.

*The key must contain everything the value depends on.* A rendered page cached under `/products/42` is wrong the moment it depends on the user's currency, language, permissions or A/B test group, and the symptom is one user seeing another's data, which is the most serious category of caching bug and entirely preventable. If the value depends on it, it is in the key. If that makes the key space too large to be useful, the data should not be cached at this level.

*Delete, don't update, on invalidation.* Updating a cache entry with a new value races with concurrent reads that may write an older value back; deleting forces the next reader to fetch fresh. The race still exists in a narrow window (a reader fetches the old value from the source, a writer updates the source and deletes the cache, the reader writes the old value into the cache), and the full fix is either a short TTL to bound the damage or a version check on write. Know that the window exists.

## The stampede

Here is the failure that takes down otherwise healthy systems. A popular key expires. In the next ten milliseconds, a thousand requests miss, and all thousand go to the source for the same value. The source, which was comfortably serving the trickle of misses, receives a thousand identical queries at once, slows down, and the slowdown causes more entries to expire before they can be refilled, which sends more traffic to the source. The cache that was protecting the database becomes the mechanism that overloads it. This is a *cache stampede* (or thundering herd, or dog-pile), and every engineer who has run a cache at scale has either prevented it or been paged by it.

There are three standard defences, and good systems use more than one.

*Request coalescing (single flight).* When a key misses, one request fetches from the source and the others wait for its result instead of fetching themselves. A thousand misses become one query. This is a small amount of code in the cache client and it eliminates the worst of the problem.

*Probabilistic early expiration.* Instead of every request treating the TTL as a hard edge, each request has a small, rising probability of refreshing the entry as it approaches expiry, so popular entries are refreshed by one request shortly before they would have expired, and nobody ever sees a cold key.[^1]

*Serve stale while revalidating.* Keep the expired value and serve it while one request fetches a fresh one in the background. Bounded extra staleness, no stampede, and the user never waits for the miss. HTTP standardised this behaviour for edge caches.

Combine with the general rule for anything that protects a dependency: when the cache is unavailable, the application must degrade (serve from the source with a concurrency limit, or serve a default) rather than fail open and pass full load downstream.

## A special case: caching the output of a model

AI systems make caching newly interesting because the source (a model call) is slow, expensive and often non-deterministic, and because requests that are different as strings may be the same in meaning.

Exact-match caching of model outputs works where the same prompt recurs (templated requests, popular questions) and fails where every request differs by a word. *Semantic caching* addresses the second case by embedding the request, searching for a nearby previous request, and returning its answer if the distance is small enough. It can cut cost and latency sharply for workloads with many near-duplicate requests, and it introduces a failure mode that ordinary caches do not have: a *false hit*, where two requests that are close in embedding space need different answers ("flights from Delhi to Mumbai on the 3rd" and "on the 4th"). The threshold is a precision–recall trade-off, the key-must-contain-dependencies rule applies with force (the cache key must include the user, the context and anything the answer depends on, not just the question), and the stale-value problem becomes a wrong-value problem. Chapter 4 covers the nearest-neighbour search that semantic caches are built on.

The second place caching applies in AI systems is inside the model serving stack itself: reusing computation for a shared prefix of a prompt (a long system instruction, a document many users ask about) across requests. This is a cache in the strict sense, the dependencies are exact, and it is one of the larger levers on both latency and cost in serving large models. The mechanism differs by system; the principle is the one this chapter started with.

## The question you will be asked

*"How do you invalidate a cache when the source of truth changes?"*

The answer is a design, not a word. Say what the data is and how stale it may acceptably be, because that decides everything. Say which strategy fits (TTL for bounded staleness, explicit or event-driven invalidation for data that must be fresh on change) and why. Say what the key contains and confirm it contains every dependency. Say how you prevent the stampede when a hot key invalidates. Say what happens when the cache is down. And say how you would know the cache is wrong: a metric for hit rate, for staleness, and an occasional comparison of cached and source values. An interviewer who hears those six things has heard someone who has operated a cache; one who hears "use a TTL" has not.

## The trade-off, stated

A cache buys latency and load relief, and costs freshness, a new failure mode (the stampede), a new class of bug (the wrong-key leak), and a second place where the truth lives. For data that tolerates staleness and is read far more than written, the trade is overwhelmingly favourable. For data that does not, the cache belongs closer to the source (a materialised view, a replica with a session guarantee, chapter 5) or not at all. The engineer's job is to know which kind of data they are holding before they reach for the cache.

## Run this yourself

Put a small HTTP service in front of a slow function (sleep 50 ms to simulate a query). Measure p50 and p99 under a closed-loop load of 32 concurrent clients requesting from a set of 1,000 keys with a skewed (Zipf) popularity distribution. Add an in-process cache with a 10-second TTL and measure again; note that the average falls far more than the p99. Then make one key hot (half the requests) and watch what happens at the ten-second mark: the stampede is visible as a latency spike and a burst of calls to the slow function. Add single-flight coalescing and watch it disappear. The harness from chapter 1 is sufficient for all of this, and the whole exercise fits in an afternoon.

---

[^1]: Vattani, A., Chierichetti, F. & Lowenstein, K. (2015), "Optimal Probabilistic Cache Stampede Prevention", *VLDB* 8(8) — the "XFetch" method.

### Sources for this chapter
- Vattani, Chierichetti & Lowenstein (2015), *VLDB* 8(8) — probabilistic early expiration.
- RFC 5861 (2010), "HTTP Cache-Control Extensions for Stale Content" — stale-while-revalidate and stale-if-error.
- RFC 9111 (2022), "HTTP Caching" — the current HTTP caching specification.
- Nishtala, R. et al. (2013), "Scaling Memcache at Facebook", *NSDI 2013* — leases (single flight), stale sets, and invalidation at scale; the best single paper on operating a shared cache.
- Fitzpatrick, B. (2004), "Distributed Caching with Memcached", *Linux Journal* — the original design rationale.
- Bang, F. (2023), "GPTCache: An Open-Source Semantic Cache for LLM Applications", *NLP-OSS 2023* — semantic caching and its false-hit problem.
- Kwon, W. et al. (2023), "Efficient Memory Management for Large Language Model Serving with PagedAttention", *SOSP 2023* — prefix sharing in model serving.
