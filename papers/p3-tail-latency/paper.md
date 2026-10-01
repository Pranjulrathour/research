---
title: "Tail Latency Under Load: An Empirical Comparison of Threaded, Event-Loop and Hybrid API Server Designs"
author: "Pranjul Rathour"
affiliation: "Independent researcher, Kanpur, India · pranjulrathour41@gmail.com · https://pranjulrathour.scult.in"
date: "October 2026"
keywords: "tail latency, p99, concurrency models, event loop, asyncio, thread pool, process pool, global interpreter lock, closed-loop load testing, API servers"
---

## Abstract

Choosing a concurrency model is one of the first decisions in building an API server and one of the least often measured. This paper measures it. Four minimal HTTP/1.1 servers were written in Python 3.13 that differ only in how they handle work while waiting: one operating-system thread per connection; a single event loop with CPU-bound work executed inline; an event loop that offloads CPU-bound work to a thread pool; and an event loop that offloads it to a process pool. Each was driven, on the same machine over loopback, by a closed-loop load generator at 1, 8, 32, 128 and 256 concurrent keep-alive clients, on three deterministic workloads (a 20 ms simulated IO wait; about 3 ms of CPU work; both), with three repeats per cell and every request's latency recorded.

<!-- RESULTS SUMMARY: fill from results.json -->

The study's contribution is not the absolute numbers, which belong to one laptop, but a reproducible demonstration of how the four designs' latency *distributions* diverge as load rises, and of the specific mechanism (blocking the loop; the interpreter lock) behind each divergence. The harness is a single file and runs in under half an hour.

## 1. Introduction

Modern API servers are built on one of three concurrency models: a thread (or process) per connection, an event loop that multiplexes many connections on one thread, or a hybrid that uses an event loop for IO and a worker pool for computation. Framework documentation recommends the hybrid; folklore favours the event loop for "IO-bound" services and threads for "CPU-bound" ones; and most teams choose by familiarity. Few measure.

The quantity that should decide the choice is not throughput or mean latency but the *tail*: the latency experienced by the slowest few per cent of requests, which, when a user request fans out to many services, becomes the typical user experience (Dean and Barroso, 2013). The tail is also where the designs' structural weaknesses appear: an event loop blocked by a computation delays every other connection; a thread pool exhausted by slow requests queues the fast ones; a process pool pays serialisation on every hand-off.

This paper measures the tail directly, with the simplest possible instruments, so that the mechanism is visible and the experiment is reproducible by a student in an afternoon.

## 2. Method

### 2.1 Servers

Four servers, each about forty lines of Python using only the standard library, identical in protocol (HTTP/1.1 with keep-alive), routing and response, differing only in concurrency model:

- **threaded**: `ThreadingHTTPServer`, one OS thread per connection.
- **async**: an `asyncio` server; IO waits are awaited; CPU work runs inline on the event loop (the pattern framework documentation warns against).
- **hybrid_thread**: the `asyncio` server with CPU work dispatched to a `ThreadPoolExecutor` sized to the core count.
- **hybrid_proc**: the same with a `ProcessPoolExecutor`, workers pre-warmed before measurement.

### 2.2 Workloads

Each request performs one of three deterministic workloads: **io**, a 20 ms sleep standing in for a downstream call (a database, a cache, a model API); **cpu**, a fixed loop of BLAKE2b hashing calibrated to about 3 ms on the test machine (the measured value is recorded with the results); **mixed**, the IO wait followed by the CPU work.

### 2.3 Load

A closed-loop generator built on `asyncio` in a separate process opens *C* keep-alive connections, *C* ∈ {1, 8, 32, 128, 256}; each client sends 40 sequential requests, waiting for each response before sending the next. Every request's latency is recorded client-side. Each (server, workload, *C*) cell is run three times after a warm-up of every path; the repeat with the median p99 is reported and the three p99 values are retained to show the spread.

The closed-loop model is a deliberate choice with a known limitation (Schroeder, Wierman and Harchol-Balter, 2006): because each client waits for its response, the arrival rate falls as the server slows, so the generator measures *what each of C concurrent clients experiences* rather than *what happens at a fixed arrival rate*. The former is the right question for "how does this server behave as more users connect"; the latter needs an open-loop generator and is out of scope.

### 2.4 Metrics and environment

Per cell: p50, p95, p99, maximum and mean latency (ms), throughput (requests per second), and the ratio p99/p50 as a one-number measure of tail heaviness. The results file records the Python version, whether the interpreter's global lock was enabled, the platform, processor and core count, the measured CPU-work duration and the run time.

### 2.5 Reproducibility

`python harness.py` runs the whole experiment and writes `results.json` and three figures. It should be run on an otherwise idle machine; background load inflates tails unevenly across designs. Python 3.13 standard library plus Matplotlib for the figures.

## 3. Results

<!-- RESULTS: fill from results.json
  Table 1: machine and run metadata
  Table 2: p50 / p99 / rps per server at C=1, 32, 256 for each workload
  Figure 1: p99 vs concurrency (3 panels); Figure 2: throughput vs concurrency; Figure 3: p99/p50 at C=256
  Text: io workload (all near floor at low C; where they diverge); cpu workload (async inline collapses; threaded and
        hybrid_thread GIL-bound; hybrid_proc scales to cores); mixed (the realistic case); p99/p50 signatures; repeat spread
-->

## 4. Discussion

<!-- fill after results -->

## 5. Limitations

*One machine, loopback.* No real network, no NIC, no other tenants. Absolute latencies are not transferable; the comparisons are.

*Python only.* The interpreter lock makes the thread-pool hybrid behave differently from how it would in a runtime without one; the paper measures CPython 3.13 as deployed by most teams and records the lock state.

*Synthetic workloads.* A sleep and a hash loop have none of the variance of real dependencies and real request mixes. Real tails are heavier.

*Closed loop.* As discussed in Section 2.3; capacity at a fixed arrival rate is a different experiment.

*Minimal servers.* No framework, middleware, TLS, logging or serialisation. Real servers add overhead to every design; whether they add it evenly is not tested here.

*Small cells.* 40 requests per client at *C* = 1 is 40 samples; percentile estimates at low concurrency are correspondingly coarse, which is why the figures emphasise the higher concurrencies.

## 6. Conclusion

<!-- fill after results -->

## References

- Dean, J. & Barroso, L. A. (2013). The tail at scale. *Communications of the ACM*, 56(2), 74–80.
- Schroeder, B., Wierman, A. & Harchol-Balter, M. (2006). Open versus closed: A cautionary tale. *NSDI 2006*.
- Welsh, M., Culler, D. & Brewer, E. (2001). SEDA: An architecture for well-conditioned, scalable internet services. *SOSP 2001*.
- Pariag, D., Brecht, T., Harji, A., Buhr, P., Shukla, A. & Cheriton, D. R. (2007). Comparing the performance of web server architectures. *EuroSys 2007*.
- von Behren, R., Condit, J. & Brewer, E. (2003). Why events are a bad idea (for high-concurrency servers). *HotOS IX*.
- Tene, G. (2015). How NOT to measure latency. Strange Loop; HdrHistogram documentation.
- Python Software Foundation (2023). PEP 703: Making the Global Interpreter Lock Optional in CPython.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly, chapter 21.

## Data and code availability

The harness, `results.json` and figures are at https://github.com/Pranjulrathour/research under `papers/p3-tail-latency/`. No external data are used.

## Declaration

The author has no competing interests and received no funding for this work.
