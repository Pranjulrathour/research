# Chapter 1 — Latency is a distribution, not a number

Ask an engineer how fast their service is and you will usually get one number: "about 40 milliseconds". Ask a user how fast it is and you will get a story: "mostly fine, but sometimes it just hangs". Both are describing the same system. The engineer is quoting an average; the user is describing a tail. The whole discipline of performance engineering begins with understanding that the user is right.

This chapter is about why a single number misleads, what to measure instead, how to divide a latency target into pieces that can be engineered, and how to measure latency so that the number you get is the number users feel. It ends, like every chapter, with the question you will be asked and an experiment you can run in an afternoon.

## The principle

**Latency is a distribution. Report and engineer its percentiles, not its mean; budget it stage by stage against a target the user would recognise; and measure it in a way that cannot hide the slow requests.**

## Why averages lie

Suppose a service answers 99 requests in 10 ms each and one in 1,000 ms. The mean is 19.9 ms. Nobody experienced 19.9 ms: ninety-nine people experienced 10 and one experienced a full second. The mean describes a request that did not happen.

Latency distributions in real systems are almost never symmetric. They have a floor (the fastest a request can possibly be served), a body where most requests sit, and a long right tail of requests delayed by garbage collection, a lock, a cache miss, a slow disk, a retry, a network hiccup or a neighbouring process. The tail is where the user's "sometimes it hangs" lives, and the mean is pulled toward it just enough to misrepresent the body without describing the tail.

The vocabulary that replaces the mean is **percentiles**. The p50 (median) is the latency that half of requests beat. The p95 is the latency that 95 per cent beat: one request in twenty is slower. The p99: one in a hundred. The p99.9: one in a thousand. Each percentile answers a precise question (*how slow is the experience for the unluckiest one-in-N user?*), and a service is described by several of them together, never by one.

Which percentile matters depends on who is counting. A page that makes one request to a service cares about that service's p99 roughly once per hundred page loads. A page that makes a hundred requests to a hundred services, which is how modern applications are built, hits *some* service's p99 on almost every load. This is the observation at the centre of Dean and Barroso's "The Tail at Scale" (2013): when a user request fans out to many servers and waits for all of them, the user's latency is the *maximum* of many samples, and the maximum of a hundred samples lives in the tail of each.[^1] With a hundred servers each at p99 = 1 s, the probability that a given user request avoids every server's slowest 1 per cent is 0.99¹⁰⁰ ≈ 37 per cent. Nearly two-thirds of users wait for someone's tail. The tail is not a corner case at scale. It *is* the user experience.

Three practical consequences.

*Dashboards show percentiles, not means.* A latency graph with one line is a graph of the wrong thing. Plot p50, p95 and p99 together; the gap between them is the shape of the distribution, and a widening gap is an early warning that the mean will miss.

*Service-level targets are set on percentiles.* "99 per cent of requests under 300 ms" is a promise a user can recognise. "Average under 100 ms" is not, because it is compatible with a tenth of users waiting a second.

*The tail is engineered separately from the body.* Making the median faster (a tighter loop, a smaller payload) does not touch the causes of the tail (pauses, contention, retries). Chapter 7's techniques for tolerating slow dependencies, and the hedged requests and timeouts in Dean and Barroso, are tail engineering, and they often make the median slightly worse in exchange for a much better p99. That trade is almost always right.

## Where the time goes: the latency budget

A target such as "p99 under 300 ms" is useless until it is decomposed, because no single component is responsible for 300 ms. The decomposition is a **latency budget**: the end-to-end target divided among the stages a request passes through, so that each stage has a number it can be engineered and measured against.

A typical interactive request passes through, at least: the client's own processing; the network from the user to the edge; a load balancer or gateway; authentication; the service's own logic; one or more dependency calls (a database, a cache, another service, a model); serialisation; the network back; rendering. Appendix B has a worksheet. Filled in for a real system, it usually produces three surprises.

The network is a fixed cost you do not control. A round trip from a user in Kanpur to a server in Mumbai is around 20–40 ms on a good connection; to Singapore, 60–90 ms; to the eastern United States, 200 ms or more.[^2] A budget of 300 ms with a 200 ms round trip leaves 100 ms for everything else. Placement (where the servers are) is a latency decision before any code is written.

Sequential dependency calls add; parallel ones take the maximum. A service that calls three dependencies one after another at 30 ms each spends 90 ms; the same service calling them concurrently spends about 30 ms plus the cost of the slowest tail. Finding the sequential calls that could be parallel is, in many services, the largest single latency improvement available, and it costs no infrastructure.

The p99 of the whole is not the sum of the p99s of the parts. Summing the stage p99s gives the worst case, in which every stage is slow on the same request; that is rarer than any single stage's p99. Summing the p50s gives something close to the median of the whole. The true end-to-end p99 lies between, and the only way to know it is to measure end to end, which chapter 9's traces make possible. The budget is a planning tool, not a prediction; the measurement is the fact.

## Measuring correctly

Latency numbers are easy to produce and easy to get wrong, and the three classic errors each flatter the system.

**Coordinated omission.** Most load-testing tools work like this: send a request, wait for the response, record its latency, send the next. If the system stalls for two seconds, the tool waits two seconds, records one slow request, and resumes. But in that two seconds, a real user population would have *sent* two seconds' worth of requests, all of which would have waited; the tool recorded one slow request where there should have been hundreds. The measurement omitted the slow requests in exact coordination with the system's slowness, which is the worst possible bias.[^3] The correction is to decide when each request *should* have been sent, on a fixed schedule, and to measure from the scheduled time, so that a stall shows up as hundreds of delayed requests rather than one. Tools that do not do this (and many popular ones do not) under-report p99 by an order of magnitude in exactly the conditions that matter. Chapter 10 returns to this under open- versus closed-loop testing.

**No warm-up, too short.** Just-in-time compilers, caches, connection pools and operating-system page caches all start cold. The first seconds of any measurement are of a different system from the one that runs in steady state. Discard a warm-up period, then run long enough for periodic events (garbage collection, log rotation, cache expiry) to occur several times; a five-second test measures the cold start and misses the tail.

**One run.** Latency varies between runs on the same machine for reasons that have nothing to do with the code: background processes, thermal throttling, where memory happened to be allocated. One run is one sample from that distribution too. Repeat, and report the spread (a range, or the median of several runs with the others shown), so that a 5 per cent improvement is not mistaken for signal when run-to-run variation is 10 per cent. The companion benchmark to this chapter does exactly this and reports the spread of its p99 across repeats alongside the value it keeps.

Two further habits. Measure at the right place: the service's own view of its latency omits the queueing in front of it and the network behind it, and the user's view is the one that matters, so measure as close to the user as the system allows (chapter 9). And record the whole distribution, not summary statistics computed on the fly: percentiles cannot be averaged across machines or time windows (the average of two p99s is not the p99 of the union), so keep histograms with enough resolution in the tail, and compute percentiles from them.[^3]

## What this looks like when measured

The companion study to this book (Appendix A, paper P3 in the research repository) built three minimal HTTP servers that differ only in their concurrency model, ran identical workloads against them at rising concurrency, and recorded every request's latency. Chapter 2 is about *why* the designs differ; here the point is only what a latency distribution looks like when you actually measure one.

<!-- P3 numbers: fill from papers/p3-tail-latency/results.json after the run -->

Three features of the measured distributions recur in every system this author has measured, and they are the features the mean would have hidden.

The floor is set by physics and the body by design. On the IO-bound workload, no design can beat the 20 ms simulated downstream wait, and at low concurrency all three designs sit within a millisecond or two of it. The design choice shows up only when the system is loaded.

The tail opens before the body moves. As concurrency rises, the p50 stays near the floor long after the p99 has begun to climb: the system is serving most requests fine and a growing minority badly. A dashboard showing the mean would show a gentle rise; the users in the p99 would be describing a system that hangs.

The ratio p99/p50 is a design signature. For a well-behaved server under a load it can handle, the ratio stays small (two or three). When a design hits its structural limit (a CPU-bound task blocking an event loop; a thread pool exhausted), the ratio jumps by an order of magnitude while the median barely changes. The ratio is a single number worth putting on a dashboard precisely because it captures the shape that the mean throws away.

## The question you will be asked

*"Your p50 is 20 ms and your p99 is 2 seconds. What is happening?"*

The ratio of a hundred says the body and the tail are produced by different mechanisms: most requests take a fast path and one in a hundred takes a slow one. Name the candidates, in the order you would check them. A dependency with its own heavy tail (a database query that occasionally hits a slow plan, a cache miss falling through to a slow source, a downstream service's p99). Pauses in the process itself (garbage collection, a lock held by a slow operation, a thread pool momentarily exhausted so requests queue). Something periodic (a batch job, a log rotation, a cache expiring all at once and stampeding, chapter 3). Infrastructure (a noisy neighbour, a load balancer health check, DNS). Then say how you would find out: traces of the slow requests (chapter 9) to see which stage held them; correlation of the slow timestamps with GC logs, deploys and batch schedules; the dependency's own percentiles. And say what you would *not* conclude: that the service is "about 20 ms". An answer that lists the mechanisms, says how to distinguish them and refuses the mean is the answer that shows you have operated a service.

## The trade-off, stated

Measuring percentiles costs more than measuring means: histograms instead of counters, more storage, more care in aggregation, load tests that are harder to write correctly. It buys the only latency numbers that correspond to what users experience and the only ones on which reliability promises can be made. Engineering the tail costs median latency and complexity (timeouts, hedging, redundancy). It buys the difference between a system that is fast on average and one that is fast. In neither case is the cheaper option actually cheaper; it merely moves the cost from the engineer's dashboard to the user's experience, where it is paid without being counted.

## Run this yourself

The harness from the research repository (`papers/p3-tail-latency/harness.py`) is a single Python file: three servers, three workloads, a load generator, and a results file. Run it on an idle machine; it takes under half an hour. Then open the results and, for one server and one workload, plot the full latency histogram at the highest concurrency rather than the percentiles. Look at its shape: the floor, the body, the tail. Compute the mean and mark it on the plot; notice how few requests are near it. Then change one thing (halve the simulated IO wait, or double the CPU work) and run again; watch which part of the distribution moves. One afternoon with the actual distribution in front of you will do more for your intuition than any number of percentile tables, including the ones in this book.

---

[^1]: Dean, J. & Barroso, L. A. (2013), "The Tail at Scale", *Communications of the ACM* 56(2), 74–80.
[^2]: Typical figures from public round-trip-time measurements between major Indian and regional cloud regions (2025–2026); your numbers depend on the route and should be measured, not quoted.
[^3]: Tene, G. (2013–2015), "How NOT to Measure Latency", talks and the HdrHistogram documentation, hdrhistogram.org — coordinated omission and the case for recording full histograms.

### Sources for this chapter
- Dean & Barroso (2013), "The Tail at Scale", *CACM* 56(2).
- Tene (2013–2015), "How NOT to Measure Latency"; HdrHistogram.
- Schroeder, B., Wierman, A. & Harchol-Balter, M. (2006), "Open Versus Closed: A Cautionary Tale", *NSDI 2006* — why the load model changes the tail you measure.
- Gregg, B. (2020), *Systems Performance*, 2nd ed., chapter 2 (methodologies) — latency as the primary metric and how to decompose it.
- Beyer et al. (2016), *Site Reliability Engineering*, chapter 4 — percentile-based service-level objectives.
- Paper P3 in the companion repository (Appendix A) — the measurements referred to in this chapter.
