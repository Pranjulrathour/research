# Chapter 10 — Capacity planning and performance testing

"It scales" is the most common claim in system design and the least often accompanied by a number. Scaling is not a property a system has; it is a measured relationship between load and some resource, valid over a range, with a point beyond which it stops holding. This chapter is about finding that relationship before users do: the one equation that answers most capacity questions, the shape of the curve that every queue follows, how to run a load test that means something, and how much headroom to buy.

## The principle

**Capacity is a measured number with a date on it. Find the constraining resource, measure the load at which it saturates, keep utilisation below the knee of the latency curve, and re-measure whenever the system or the traffic changes.**

## Little's law

The most useful equation in systems engineering was proved by John Little in 1961 and takes one line:[^1]

> *L* = *λ* × *W*

The average number of items in a system (*L*) equals the average arrival rate (*λ*) times the average time each item spends in the system (*W*). It holds for any stable system regardless of the arrival distribution, the service distribution or the queueing discipline, which is why it is so useful: it needs no model.

Applied to a service: the average number of requests in flight equals the request rate times the average latency. A service handling 2,000 requests a second with an average latency of 50 ms has, on average, 2,000 × 0.05 = 100 requests in flight. If each in-flight request holds a thread, the service needs at least 100 threads; if it holds a database connection, at least 100 connections; if latency doubles because a dependency slows (chapter 7), in-flight requests double and so does every resource they hold. This is the arithmetic behind chapter 2's blocking argument and chapter 7's cascade, in one line.

Applied backwards: a connection pool of 50 and a request rate of 2,000 per second can sustain an average latency of at most 50 / 2,000 = 25 ms before the pool is the bottleneck. If the database's p50 is 30 ms, the pool is undersized, and no amount of application tuning will fix it.

Applied to a queue (chapter 8): the average depth equals the arrival rate times the average time a message waits. A depth of 10,000 at 500 messages a second means each message waits twenty seconds. Depth is a latency measurement in disguise.

Most capacity questions reduce to Little's law plus a measurement of one of the three quantities. Memorise it.

## The knee of the curve

Little's law says how many requests are in the system. Queueing theory says what happens to latency as the system fills, and the shape is the same for every resource that serves requests one at a time: a CPU core, a disk, a database connection, a thread pool, a network link.

Define utilisation *ρ* as the fraction of the resource's capacity in use. For the simplest queue (random arrivals, random service times, one server, the M/M/1 model) the average time in system is

> *W* = *S* / (1 − *ρ*)

where *S* is the service time with no queue. At 50% utilisation, latency is twice the bare service time. At 80%, five times. At 90%, ten times. At 95%, twenty. At 99%, a hundred. The curve is flat and then vertical, and the transition, the *knee*, sits around 70–80% for this model, with the exact point depending on how variable the arrivals and service times are: more variability moves the knee left.[^2]

Three consequences govern capacity planning.

**Running a resource "hot" is running it slow.** A CPU at 90% is not 90% as fast as one at 10%; its queue is ten times longer. The cheapest latency improvement available to most systems is to add capacity until the constraining resource sits below its knee.

**Headroom is latency insurance, not waste.** A team that provisions to 60% utilisation is not wasting 40%; it is buying the flat part of the curve, and the ability to absorb a traffic spike or a lost instance without crossing the knee. Chapter 11 puts a price on this; the price is almost always worth paying for the resource that constrains user-facing latency.

**The tail is where the knee bites first.** The equation above is the average. Percentiles rise faster, because the requests that arrive during a burst are the ones that queue, and a resource that looks fine on average at 75% may already be producing a p99 several times its p50. Chapter 1's insistence on distributions is, here, the difference between seeing the knee coming and discovering it.

## Finding the constraining resource

Every system has one resource that saturates first, and capacity planning is the discipline of knowing which. The method is to measure utilisation of each candidate (CPU, memory, disk I/O, network, connection pools, thread pools, locks, downstream rate limits, a single hot partition) under rising load and watch which one approaches its knee first. It is frequently not the one people assume: web services are often bound by a connection pool or a downstream dependency long before CPU; databases by disk I/O or lock contention rather than CPU; data pipelines by a single partition or a serial step.

When the constraint is found, there are exactly four responses: add more of it (scale up or out), use less of it per request (optimise), move work off it (cache, precompute, make asynchronous), or shed the load that would exceed it (chapter 7). Which one is right is a cost question (chapter 11) and a correctness question (chapters 5 and 6), and the constraint moves to the next resource as soon as the first is relieved. Capacity planning is therefore not a project but a loop.

## Load testing that means something

A load test is an experiment: apply controlled load, measure the response. Most load tests are badly designed experiments, and the common faults are known.

**Open versus closed loop.** A *closed-loop* generator runs *N* virtual users, each sending a request, waiting for the response, then sending the next. The arrival rate adapts to the system: when the system slows, users wait, arrivals fall, and the system is protected from the very overload the test was meant to measure. An *open-loop* generator sends requests at a fixed rate regardless of responses, as real traffic does (users arriving at a website do not wait for other users' pages to load). Open-loop tests show the knee; closed-loop tests hide it, and report a flattering throughput at a latency that would never occur under real load.[^3] Closed-loop testing has a place (it answers "what is the maximum throughput with *N* concurrent clients?", which is the question chapter 1's harness asked); it does not answer "what happens at 3,000 requests a second?". Know which question you are asking.

**Coordinated omission.** The subtle cousin of the closed-loop fault. If a generator records latency only for requests it managed to send, and it could not send during a stall because it was waiting, the stall is omitted from the measurements exactly when the system was slowest. The cure is to schedule sends on a fixed timetable and measure from the *intended* send time, so that a request delayed by a stall carries the stall in its latency. Tools that do not do this (and many do not) under-report tails by an order of magnitude in exactly the conditions that matter.[^4]

**Realistic mix.** A test that hits one cheap endpoint with one cached key measures the cache. The request mix, the key distribution (chapter 3: Zipf, not uniform), the payload sizes and the ratio of reads to writes should resemble production, which means deriving them from production logs rather than guessing.

**Warm-up and duration.** JIT compilers, caches, connection pools and autoscalers all take time to reach steady state; the first minute of any test measures the cold start. Discard it. Then run long enough for the slow things to happen: garbage collection cycles, log rotation, cache expiry, the autoscaler's reaction time. A *soak test* (hours at moderate load) finds leaks and slow degradation that a five-minute test never will.

**Repeat and report the spread.** One run is one sample. Chapter 1's method applies: several runs, and a confidence interval or at least a range, so that a 5% improvement is not mistaken for signal when the run-to-run variation is 10%.

**Test the failure modes too.** A load test at 120% of capacity is the only way to see whether load shedding works, whether the system recovers when load falls, and whether the recovery is fast or slow (a backlog that must drain, a cache that must refill). Chapter 7's exercises are load tests with failures injected.

## Autoscaling and its lag

Elastic infrastructure makes capacity a dial, and the dial has a delay. An autoscaler observes a metric (CPU, request rate, queue depth), decides to add instances, and the instances take time to start, warm up and join the pool. The delay is typically one to several minutes; traffic can double in seconds. During the gap the existing instances absorb the spike, and if they were already near the knee, they cross it.

Three practices follow. Scale on a *leading* indicator (request rate or queue depth) rather than a *lagging* one (CPU, which rises after the queue has already formed). Keep enough headroom on the existing instances to cover the scaling delay at the steepest plausible traffic ramp. And test the autoscaler as part of the load test: ramp traffic at the production rate of change and watch whether capacity arrives before the knee.

Autoscaling also does not help a resource that does not scale horizontally: a single-leader database, a hot partition, a downstream rate limit. For those, capacity is planned the old way, with a measured ceiling and a date by which it will be reached.

## The headroom decision

How much spare capacity to carry is a trade between cost (idle resources) and risk (crossing the knee under a spike or a failure). A defensible rule: provision so that the constraining resource stays below its knee when (a) traffic is at the highest level seen in the planning window plus the growth expected before the next review, and (b) one unit of capacity (an instance, a zone) has failed. The "N + 1" discipline from infrastructure engineering is the second clause; the first is the forecast. Both are numbers with dates, and both are re-measured at every review.

## The question you will be asked

*"Traffic will triple for a launch. What do you check, in what order?"*

First, the constraining resource today: which pool, store or dependency is closest to its knee at current peak, from the utilisation dashboards (chapter 9). Tripling load will take it past the knee unless something changes; say what. Second, the resources that do not scale horizontally (the primary database, hot partitions, third-party rate limits): measure their current peak utilisation, estimate the tripled load, and decide now whether they need a bigger instance, a cache in front, or a rate limit of your own. Third, run an open-loop load test at three times current peak with the production request mix, watch every utilisation metric, and find the new knee. Fourth, check the autoscaler's lag against the launch's expected ramp (a launch announcement produces a step, not a ramp). Fifth, confirm the degradation and shedding paths (chapter 7) work at four times, because launches overshoot. Sixth, agree what you will watch during the launch and who can roll back. Then say what you would not do: trust "it scales" from anyone, including yourself, without the test.

## The trade-off, stated

Headroom costs money every day; its absence costs latency, incidents and lost users on the days that matter most. Load testing costs engineering time and a realistic environment; its absence means the production launch *is* the load test. Autoscaling costs lag and complexity; it buys capacity that follows demand. In every case the decision should be made with the numbers (utilisation, the knee, the ramp, the lag) rather than with adjectives, and the numbers should be dated, because traffic grows and systems change.

## Run this yourself

Use chapter 1's harness in open-loop mode (fixed send rate, latency measured from the scheduled send time). Run the CPU-bound workload against a single-process server at 10, 20, 40, 60, 70, 80, 90 and 95% of the throughput you measured as its maximum in chapter 2. Plot p50 and p99 against utilisation. You will see the flat region, the knee somewhere between 70 and 85%, and the vertical region beyond, and you will see the p99 leave the floor well before the p50 does. Then switch the generator to closed-loop with a fixed number of clients and repeat; note how the closed loop refuses to show you the vertical part, because it slows down instead. Finally apply Little's law to one of your runs: multiply the rate by the average latency and compare with the in-flight count the server reports. The three numbers agree, which is reassuring, and the shape of the curve is the thing to carry into every capacity conversation for the rest of your career.

---

[^1]: Little, J. D. C. (1961), "A Proof for the Queuing Formula: L = λW", *Operations Research* 9(3), 383–387.
[^2]: Kleinrock, L. (1975), *Queueing Systems, Volume 1: Theory*, Wiley — the M/M/1 result; Gunther, N. J. (2007), *Guerrilla Capacity Planning*, Springer — the practitioner's treatment, including the Universal Scalability Law for the effect of contention and coherence on throughput.
[^3]: Schroeder, B., Wierman, A. & Harchol-Balter, M. (2006), "Open Versus Closed: A Cautionary Tale", *NSDI 2006*.
[^4]: Tene, G. (2013–2015), "How NOT to Measure Latency", talks and the HdrHistogram documentation — the coordinated-omission problem and its correction.

### Sources for this chapter
- Little (1961); Kleinrock (1975); Gunther (2007) — the theory and its application.
- Schroeder, Wierman & Harchol-Balter (2006) — open vs closed loop.
- Tene (2013–2015) — coordinated omission; HdrHistogram.
- Beyer et al. (2016), *Site Reliability Engineering*, chapter 18 (software engineering in SRE, on capacity planning tooling) and chapter 21 (handling overload).
- Dean & Barroso (2013), "The Tail at Scale" — tail behaviour under load.
- Brendan Gregg (2020), *Systems Performance*, 2nd ed., Addison-Wesley — the USE method (utilisation, saturation, errors) for finding the constraining resource.
