# P3 — Defence notes
## Tail latency under load: threaded, event-loop and hybrid API server designs

*Private preparation notes for talking about this paper in an interview, a workshop or a review. Not part of the manuscript.*

## The three findings, in one breath each

1. **Fairness, not capacity, makes the threaded tail.** At 256 clients on CPU-bound work, the threaded server and the inline event loop had almost the same throughput (116 vs 152 rps) and medians (1.5 vs 1.6 s), but p99s of 8.2 s vs 2.2 s, and the threaded server's worst request took 16.7 s. The loop serves in arrival order; 256 OS threads under the GIL are scheduled unfairly.

2. **Under the GIL, a thread pool keeps the loop responsive and buys no throughput.** The thread-pool hybrid matched the inline loop on CPU-bound and mixed work (~115–160 rps for all three lock-bound designs) and was slightly worse at moderate concurrency (p99 349 vs 237 ms at 32 clients, mixed). It only helps I/O requests stuck behind CPU requests.

3. **The process pool pays a hand-off tax, then wins, then hits the dispatcher.** 7.6 ms vs 2.9 ms at one client (about 4.7 ms per hand-off, more than the 2.8 ms of work). From 8 clients the fastest: 2× throughput and ¼ the p99 of the lock-bound designs at 128 clients. Plateau ~310 rps on 8 cores: the serial dispatch work in the loop process is the ceiling.

Signature to volunteer: **p99/p50 at full load: 1.2–1.6 for every event-loop design on every workload; 3.1, 4.3, 5.4 for threads.** Independent of the machine, invisible in throughput.

## The method in sixty seconds

Four minimal Python 3.13 HTTP/1.1 servers, identical except for the concurrency model (ThreadingHTTPServer; asyncio with CPU inline; asyncio + ThreadPoolExecutor; asyncio + ProcessPoolExecutor, pre-warmed). Three workloads: 20 ms sleep, ~2.8 ms BLAKE2b loop, both. Closed-loop asyncio load generator in a separate process: 1/8/32/128/256 keep-alive clients × 40 requests, three repeats, median-p99 repeat reported, all three p99s kept. Quiet-machine gate before the run and background load sampled after each server. Everything in one file; 53 minutes.

## Questions I expect, and answers

**"Why is the async I/O floor 31 ms when the sleep is 20?"** Windows: `asyncio.sleep` resolves to the 15.6 ms system timer, so 20 ms becomes ~31; `time.sleep` in the threaded server uses a high-resolution timer. It's a platform artefact, stated in the paper, and it doesn't touch any comparison at high concurrency. On Linux it would be 20.

**"Why does the threaded server take 10 ms for 2.8 ms of work at one client?"** The stdlib server has ~7 ms of fixed per-request overhead (separate header/body writes, bookkeeping). A production threaded server would do better. The seconds-scale differences at 256 clients don't depend on it.

**"Throughput of the lock-bound designs halves from 1 client to 32. Why?"** Per-request cost roughly doubles under load: interpreter overhead of multiplexing many connections, and probably the laptop dropping clock speed under sustained single-core load. The harness doesn't record frequency, so I can't separate them; it's listed as a limitation and it affects all three designs equally.

**"Only 2× from a process pool on 8 cores? Isn't that a bug?"** It's the finding. The dispatcher (parse, pickle to a worker, unpickle, respond) is serial Python under the GIL and costs ~3.2 ms per request, which caps throughput near 310 rps. That's why you measure instead of reasoning: "uses the cores" used one.

**"Closed loop understates the tail (coordinated omission)."** Yes. The paper says so and cites Schroeder et al. It measures what each of C connected clients experiences, not capacity at a fixed arrival rate. An open-loop variant is the natural follow-up, and Book 2's chapter 10 exercise is exactly that.

**"The hybrid_thread spreads are wide."** 1,684–2,610 ms at 256 clients (CPU). The background-load sample after that server read 1.85 cores vs ~0.5 for the others: something woke up during its run. Reported, not hidden; no conclusion depends on those cells.

**"What about the backlog of 5?"** The first full run failed at 256 clients with connection refusals: `socketserver` asks for a listen backlog of 5 and Windows refuses when it's full. Raised to 1,024 to match asyncio's. The failed log is in the repo. It's a lesson in itself: every queue has a size, chosen by someone who didn't know your load.

**"What would you do next?"** Open-loop load; Linux and the free-threaded 3.13 build (GIL off) to see the thread results change; a worker model without pickling to raise the process-pool ceiling; record CPU frequency.

**"How does this connect to the job?"** Choosing and operating services at the tail is the daily work of platform and infrastructure teams. The paper shows I measure distributions, control the environment, keep failed runs, and explain mechanisms rather than quote folklore.

## Numbers to have memorised

- CPU work 2.82 ms; I/O 20 ms (31 ms floor for asyncio on Windows); 60 settings; 53 minutes; background 0.70 cores at start.
- I/O at 256: threaded p50 99 / p99 307 ms / 2,079 rps; event loops p99 44–49 ms / 7,433–7,829 rps.
- CPU at 256: threaded 1,518 / 8,244 ms / 116 rps (max 16,715); async 1,559 / 2,240 / 152; hybrid_thread 1,570 / 2,192 / 155; hybrid_proc 896 / 1,153 / 279.
- CPU at 128: hybrid_proc p99 532 ms / 311 rps vs 957–4,049 ms / 118–158 rps.
- One client, CPU: async 2.9 ms, hybrid_thread 3.0, hybrid_proc 7.6, threaded 10.1.
- Mixed at 256: hybrid_proc p99 946 ms vs 2,366–2,480 (loop designs) vs 6,367 (threaded).
- p99/p50 at 256: threaded 3.1 / 5.4 / 4.3 (io / cpu / mixed); event-loop designs 1.2–1.6.

## Where everything is

`papers/p3-tail-latency/harness.py` (servers, load generator, gate, plots), `results.json` (all 60 settings with p99 spreads and background samples), `figures/fig0_servers.png` (Figure 1), `fig1_p99_vs_concurrency.png` (Figure 2), `fig2_throughput_vs_concurrency.png` (Figure 3), `fig3_tail_ratio.png` (Figure 4), `run_first_attempt_backlog5.log` (the failed run), `paper.md`.
