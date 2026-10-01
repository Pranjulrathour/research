---
title: "Tail Latency Under Load: An Empirical Comparison of Threaded, Event-Loop and Hybrid API Server Designs"
short: "Tail latency of threaded, event-loop and hybrid servers"
author: "Pranjul Rathour"
affiliation: "Independent researcher, Kanpur, India · pranjulrathour41@gmail.com · https://pranjulrathour.scult.in"
date: "October 2026"
keywords: "tail latency, p99, concurrency models, event loop, asyncio, thread pool, process pool, global interpreter lock, closed-loop load testing, API servers"
---

## Abstract

Choosing a concurrency model is one of the first decisions in building an API server, and one of the least often measured. This paper measures it. Four minimal HTTP/1.1 servers were written in Python 3.13 that differ only in what they do while work is waiting: one operating-system thread per connection; a single event loop that runs CPU-bound work inline; an event loop that hands CPU-bound work to a thread pool; and an event loop that hands it to a process pool. Each was driven on the same machine, over loopback, by a closed-loop load generator at 1, 8, 32, 128 and 256 concurrent keep-alive clients, on three deterministic workloads (a 20 ms simulated I/O wait, about 3 ms of CPU work, and both), with three repeats per setting and the latency of every request recorded.

<!-- RESULTS SUMMARY: fill from results.json -->

The absolute numbers belong to one laptop. What transfers is how the four designs' latency distributions pull apart as load rises, and the specific mechanism behind each divergence: a blocked event loop, or the interpreter lock. The harness is a single file and runs in under an hour.

## 1. Introduction

Most API servers are built on one of three concurrency models: a thread (or process) per connection, an event loop that multiplexes many connections on one thread, or a hybrid that uses an event loop for I/O and a pool of workers for computation. Framework documentation recommends the hybrid. Folklore says event loops are for I/O-bound services and threads for CPU-bound ones. In practice, most teams choose whatever they already know, and few measure.

The quantity that should decide the choice is not throughput or mean latency but the tail: the latency of the slowest few per cent of requests. When a user request fans out to many services, the tail of each becomes the typical experience of the user (Dean and Barroso 2013). The tail is also where each design's structural weakness shows. A computation on an event loop delays every other connection on that loop; a thread pool busy with slow requests queues the fast ones behind them; and a process pool pays to copy every argument and result across a process boundary.

This paper measures the tail directly, with deliberately simple instruments, so that each mechanism is visible and a student can rerun the whole experiment in an afternoon.

## 2. Method

### 2.1 Servers

There are four servers, each a few dozen lines of standard-library Python. They are identical in protocol (HTTP/1.1 with keep-alive), routing and response, and differ only in concurrency model. Figure 1 shows how each one spends its time.

- **threaded**: `ThreadingHTTPServer`, one operating-system thread per connection.
- **async**: an `asyncio` server. I/O waits are awaited, and CPU work runs inline on the event loop, which is the pattern framework documentation warns against.
- **hybrid_thread**: the same `asyncio` server, with CPU work sent to a `ThreadPoolExecutor` of 12 workers (the machine's logical CPU count).
- **hybrid_proc**: the same again with a `ProcessPoolExecutor` of 12 workers, started and warmed before measurement begins.

![Figure 1. How each server design spends a request's time. Under the threaded and hybrid_thread designs, CPU work is serialised by the interpreter lock; under async it blocks the event loop; only hybrid_proc runs it in parallel. Schematic, not to scale.](figures/fig0_servers.png)

### 2.2 Workloads

Each request performs one of three deterministic workloads. **io** is a 20 ms sleep standing in for a downstream call to a database, a cache or a model API. **cpu** is a fixed loop of BLAKE2b hashes, calibrated to about 3 ms on the test machine; the duration is measured again at the start of every run and recorded with the results. **mixed** does the I/O wait and then the CPU work.

### 2.3 Load

A closed-loop load generator, written with `asyncio` and running in the harness process while the server runs in a process of its own, opens *C* keep-alive connections, with *C* ∈ {1, 8, 32, 128, 256}. Each client sends 40 requests in sequence, waiting for each response before sending the next, and the latency of every request is recorded on the client side. Every path is warmed up first. Each combination of server, workload and *C* is then run three times; the run with the median p99 is reported, and all three p99 values are kept to show the spread. Percentiles use the nearest-rank definition.

The closed loop is a deliberate choice with a known limitation (Schroeder, Wierman and Harchol-Balter 2006). Because each client waits for its response, the arrival rate falls as the server slows down. The generator therefore measures what each of *C* concurrent clients experiences, not what happens at a fixed arrival rate. That is the right question for how a server behaves as more users connect. The fixed-rate question needs an open-loop generator and is outside the scope of this paper.

### 2.4 Metrics and environment

For each setting the harness records the p50, p95, p99, maximum and mean latency in milliseconds, the throughput in requests per second, and the ratio of p99 to p50 as a one-number measure of how heavy the tail is. The results file also records the Python version, whether the interpreter's global lock was enabled, the platform, processor and core count, the measured duration of the CPU work, and the time of the run.

Timing benchmarks are sensitive to whatever else the machine is doing, so the harness waits before starting until other processes are using less than three-quarters of one core and at least 4 GB of memory is free, for up to two hours. It records the background load it saw at the start and again after each server, so a reader can judge how quiet the machine actually was.

### 2.5 Revision record

The design was written down before any measurement. Three things changed during the first attempts, all before any result was used.

The CPU loop was first calibrated at 8.5 ms per request, which made the CPU-bound workload dominate everything else. It was recalibrated to about 3 ms, so that CPU time and I/O wait are of comparable size.

The first full run failed at 256 clients against the threaded server, with the operating system refusing connections. Python's `socketserver` asks for a listen backlog of only five connections, and on Windows a full backlog causes outright refusal rather than a delay. The backlog was raised to 1,024 to match the `asyncio` servers, so that all four designs are compared on their concurrency model rather than on a socket default. The log of that failed run is kept in the repository as `run_first_attempt_backlog5.log`.

Server processes were first started as daemon processes, which are not allowed to start children, so the process-pool server could not create its workers. They now run as ordinary processes, and the harness terminates each server's whole process tree when it finishes, because Windows does not do this automatically.

### 2.6 Reproducibility

`python harness.py` runs the whole experiment and writes `results.json` and three figures, and `python harness.py --plots-only` redraws the figures from a saved `results.json`. Only the Python 3.13 standard library is needed for the measurements, plus psutil for the quiet-machine check and Matplotlib for the figures.

## 3. Results

<!-- RESULTS: fill from results.json
  Table 1: machine and run metadata (incl. background load, cpu_work_measured_ms, gil_enabled)
  Table 2: p50 / p99 / rps per server at C=1, 32, 256 for each workload
  Figure 2: p99 vs concurrency (3 panels); Figure 3: throughput vs concurrency; Figure 4: p99/p50 at C=256
  Text: io workload (all near floor at low C; where they diverge); cpu workload (async inline collapses; threaded and
        hybrid_thread GIL-bound; hybrid_proc scales to cores); mixed (the realistic case); p99/p50 signatures; repeat spread
-->

## 4. Discussion

<!-- fill after results -->

## 5. Limitations

*One machine, over loopback.* There is no real network, no network card and no other tenants. Absolute latencies don't transfer to other machines; the comparisons between designs are the result.

*The load generator shares the machine.* The generator is itself a single Python `asyncio` process on the same laptop. At high concurrency its own scheduling adds latency and it competes with the server for CPU. That affects every design, though not necessarily equally.

*Python only.* The interpreter lock makes the thread-pool hybrid behave differently from how it would in a runtime without one. The paper measures CPython 3.13 as most teams deploy it, and records the lock's state.

*Synthetic workloads.* A sleep and a hash loop have none of the variability of real dependencies or real request mixes, so real tails are heavier.

*Closed loop.* See Section 2.3: capacity at a fixed arrival rate is a different experiment.

*Minimal servers.* There is no framework, middleware, TLS, logging or serialisation. Real servers add overhead to every design, and whether they add it evenly isn't tested here.

*Small samples at low concurrency.* At *C* = 1 a run is only 40 requests, so the percentile estimates there are coarse. That is why the figures and the discussion concentrate on the higher concurrencies.

## 6. Conclusion

<!-- fill after results -->

## References

- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly, chapter 21.
- Dean, J. & Barroso, L. A. (2013). The tail at scale. *Communications of the ACM*, 56(2), 74–80.
- Pariag, D., Brecht, T., Harji, A., Buhr, P., Shukla, A. & Cheriton, D. R. (2007). Comparing the performance of web server architectures. *EuroSys 2007*, 231–243.
- Python Software Foundation (2023). PEP 703: Making the Global Interpreter Lock Optional in CPython.
- Schroeder, B., Wierman, A. & Harchol-Balter, M. (2006). Open versus closed: A cautionary tale. *NSDI 2006*.
- Tene, G. (2015). How NOT to measure latency. Talk at Strange Loop; HdrHistogram documentation.
- von Behren, R., Condit, J. & Brewer, E. (2003). Why events are a bad idea (for high-concurrency servers). *HotOS IX*.
- Welsh, M., Culler, D. & Brewer, E. (2001). SEDA: An architecture for well-conditioned, scalable internet services. *SOSP 2001*, 230–243.

## Data and code availability

The harness, `results.json` and the figures are at https://github.com/Pranjulrathour/research under `papers/p3-tail-latency/`, together with the log of the failed first run. The code is MIT-licensed. No external data are used.

## Declarations

*Competing interests and funding.* The author has no competing interests and received no funding for this work.

*Use of AI tools.* Generative AI tools were used to help draft parts of the text and code. All results were produced by the published harness, and the author reviewed the analysis and takes full responsibility for the content.
