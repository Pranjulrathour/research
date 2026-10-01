# Chapter 2 — Concurrency models and the price of blocking

Every server has to answer one question before it answers any request: what happens while it is waiting? A request arrives, the server asks a database for something, and for twenty milliseconds there is nothing to do but wait. What the server does with those twenty milliseconds (hold a thread idle, switch to another request, hand the wait to the operating system) is its concurrency model, and the choice determines how the latency distribution of chapter 1 behaves when the load goes up.

This chapter is about the three models in common use, the one mistake that each tempts you into, the measurements that show the mistake happening, and the mechanism (backpressure) that keeps any of them alive when demand exceeds what they can do.

## The principle

**Concurrency is about what a server does while it waits. Choose the model that matches what your requests wait for, never let CPU-bound work block the thing that is supposed to be waiting, and bound every queue so that the system says no before it falls over.**

## Three models

**Thread per request.** The operating system gives each connection its own thread; when the thread waits (on a socket, a disk, a lock), the kernel runs another. This is the oldest model and the one most frameworks default to. Its strengths are simplicity (code reads top to bottom; a wait is just a line that takes a while) and isolation (one slow request does not stall another, because the kernel preempts). Its costs are memory (each thread has a stack, typically hundreds of kilobytes to a few megabytes, so ten thousand connections is gigabytes of stacks), context-switch overhead as thread counts grow, and, in languages with a global interpreter lock, the fact that threads give concurrency for waiting but not parallelism for computing.

**Event loop (asynchronous).** One thread runs a loop that picks up whichever connection has something ready, does a little work until that connection needs to wait again, and moves on. Waits are expressed as points where the code yields back to the loop. Its strength is efficiency for IO-bound work: a single thread can hold tens of thousands of idle connections at almost no cost, because an idle connection is a few bytes of state rather than a stack. Its cost is the one this chapter is about: the loop is cooperative. Nothing preempts it. If any piece of code does not yield (because it is computing rather than waiting), every other connection on that loop waits for it to finish.

**Hybrid.** An event loop for the waiting, with CPU-bound work handed to a pool of workers (threads or processes) so the loop stays free. This is the recommended pattern in every asynchronous framework's documentation and the one most often skipped, because it requires knowing which work is CPU-bound, and the answer changes as the code evolves. There are two sub-variants and they behave very differently in languages with a global interpreter lock: a *thread* pool keeps the loop responsive but still runs one computation at a time; a *process* pool actually uses the cores, at the cost of serialising arguments and results across process boundaries.

Other models exist (green threads and virtual threads, which make the thread model cheap enough to behave like the event loop; actor systems; structured concurrency) and each is a point between these three. Understanding the three is enough to reason about all of them.

## What blocks what

The word "blocking" does a lot of work in concurrency discussions, and it helps to be precise. An operation blocks a *thread* if the thread cannot do anything else until it completes: a synchronous socket read, a sleep, a lock acquisition, a long computation. An operation blocks an *event loop* if it runs on the loop's thread without yielding: any synchronous call, and any computation, however the code is written.

The first kind of blocking is fine in a thread-per-request server, because the kernel runs other threads. It is fatal in an event loop, because there is nothing else to run the other connections. This is the classic mistake, and it is classic because it is invisible in testing: a single request that computes for 3 ms returns in 3 ms whether or not it blocked the loop. The damage appears only under concurrent load, when a hundred connections each wait for the one that is computing, and it appears in the tail first.

The **global interpreter lock** (the GIL in CPython and, in different forms, in some other runtimes) adds a second layer. Even in the thread model, only one thread executes interpreter bytecode at a time; threads waiting on IO release the lock, so IO-bound work scales across threads, but CPU-bound work does not, however many threads or cores there are. The hybrid-with-thread-pool pattern keeps the event loop responsive (the loop is not blocked, so IO-bound requests proceed) and does nothing for throughput of the CPU-bound requests themselves, which still execute one at a time. Only a process pool, or moving the computation into native code that releases the lock, buys parallelism. CPython 3.13 shipped an experimental build without the GIL; whether the interpreter used for a measurement has the lock enabled is recorded in the companion study's metadata, because it changes which of these statements hold.

## What the measurements show

The companion study (Appendix A; paper P3) built four minimal HTTP servers in Python that differ only in concurrency model (thread per request; event loop with CPU work inline; event loop with a thread pool; event loop with a process pool), ran three workloads against each (IO-bound: a 20 ms simulated downstream wait; CPU-bound: about 3 ms of computation; mixed: both), and drove them with a closed-loop load generator at 1, 8, 32, 128 and 256 concurrent clients, three repeats per cell, recording every request's latency.

<!-- P3 numbers: fill from papers/p3-tail-latency/results.json after the run -->

The design of the study is as important as its numbers. The servers are deliberately minimal (no framework, no middleware) so that the model is the only variable. The workloads are deliberately synthetic so that the CPU and IO components are known exactly. The load is deliberately closed-loop, which, as chapter 10 explains, measures what each of N concurrent clients experiences rather than what happens at a fixed arrival rate; it is the right model for "how does this server behave as more users connect" and the wrong one for "what is this server's capacity at 3,000 requests a second". And the machine, interpreter and GIL state are recorded, because the absolute numbers belong to that machine; the comparisons are the finding.

## Backpressure: the system that says no survives

Every model above has a point at which demand exceeds capacity: more connections than threads, more computation than the loop can interleave, more jobs than the pool can take. What happens at that point is a design decision, and the default in most systems is the wrong one.

The default is an **unbounded queue**. Connections queue in the kernel's accept backlog; requests queue in the framework; jobs queue in the pool. Nothing is refused; everything waits. Under sustained overload the queues grow without limit, every request's latency grows with the queue in front of it, and the system reaches a state where it is working at full capacity and serving nobody within their timeout, because by the time a request reaches the front of the queue its client has given up and retried (chapter 7), which adds another request to the queue. This is **congestion collapse**, and it is how systems that were merely slow become systems that are down.

**Backpressure** is the alternative: when a stage cannot keep up, it signals upstream to slow down or stop, and the signal propagates to the source, which either waits, sheds, or fails fast. The mechanisms are mundane. Bounded queues that reject when full. Concurrency limits per stage (a semaphore around the expensive section) so that excess requests fail immediately with a clear "overloaded" rather than waiting. Admission control at the edge that refuses connections beyond what the system has been measured to handle (chapter 10). TCP's own flow control is backpressure at the transport layer, and the reason the internet does not collapse; applications must do the same at their layer.

The counter-intuitive consequence is that a system that rejects 10 per cent of requests under overload is *more* available than one that accepts all of them: the 90 per cent it serves, it serves within budget, and the rejected 10 per cent get an answer they can act on (retry later, show a fallback) instead of a timeout. Chapter 7 develops this as load shedding; the point here is that it is a property of the concurrency design, decided when the queues are sized, and almost impossible to retrofit during an incident.

## Choosing

Match the model to what requests wait for.

If requests are *IO-bound* (they spend most of their time waiting on other systems: databases, caches, other services, model APIs), the event loop is efficient and the thread model works until thread counts become expensive. Most web services, gateways, proxies and AI-application backends are in this category, and the event loop with a strict rule against inline computation is the right default.

If requests are *CPU-bound* (they compute: image processing, cryptography, parsing, numerical work), the event loop is wrong without a process pool, the thread model is wrong under a global interpreter lock, and the right answer is parallelism across processes or a runtime without the lock.

If requests are *mixed*, which most real services eventually become, the hybrid with a process pool for the computation is the design that holds up, and the engineering discipline is keeping the boundary honest: every piece of computation that creeps onto the loop is a future tail-latency incident.

Whichever model, bound the queues and decide what happens when they are full before the first user arrives.

## The question you will be asked

*"When would you choose threads over async?"*

When the work is CPU-bound and the runtime's threads actually run in parallel (no global interpreter lock, or native code that releases it). When the codebase or its libraries are synchronous and the cost of making them asynchronous (rewriting every IO call, finding every blocking library) exceeds the benefit. When isolation matters more than efficiency: in a thread-per-request server a slow request cannot stall others, and that property is worth paying stacks for in systems where a single misbehaving request is worse than lower connection capacity. When connection counts are modest (hundreds, not tens of thousands) and the event loop's efficiency buys nothing. And, honestly, when the team knows threads and does not know event loops; a model the team can operate beats a model it cannot. Then say what you would do in either case: bound the queues, measure the tail, and keep computation off whatever is supposed to be waiting.

## The trade-off, stated

The thread model buys simplicity and isolation and costs memory and, under a global lock, parallelism. The event loop buys connection efficiency and costs the discipline of never blocking it. The hybrid buys both and costs the boundary maintenance and, with processes, serialisation overhead. Backpressure costs some requests their service and buys the rest of them theirs. None of these is a free lunch, and the choice that is wrong for your workload will not show up in tests; it will show up in the p99 under load, which is why chapter 1 came first.

## Run this yourself

Run the P3 harness and look at the CPU-bound workload across the four servers at 128 concurrent clients. Then open the harness and move the CPU work in the event-loop server off the loop (the file already has the pool variants to copy from), and watch the tail collapse. Then do the opposite: add a tiny synchronous sleep (1 ms, say) inside the asynchronous IO path, simulating a blocking library call that nobody noticed, and watch the IO-bound tail that was flat at 20 ms open up as concurrency rises. Finally, put a semaphore of 16 around the CPU section in the threaded server and drive it with 256 clients: requests beyond the limit should fail fast rather than queue, and the p99 of the ones that are served should fall. Those three edits are the whole chapter, and each takes ten minutes.

---

### Sources for this chapter
- Welsh, M., Culler, D. & Brewer, E. (2001), "SEDA: An Architecture for Well-Conditioned, Scalable Internet Services", *SOSP 2001* — staged event-driven design and explicit backpressure between stages.
- Pariag, D. et al. (2007), "Comparing the Performance of Web Server Architectures", *EuroSys 2007* — a careful empirical comparison of thread- and event-based servers.
- von Behren, R., Condit, J. & Brewer, E. (2003), "Why Events Are a Bad Idea (for high-concurrency servers)", *HotOS 2003*, and Ousterhout, J. (1996), "Why Threads Are a Bad Idea (for most purposes)" — the two sides of the classic argument.
- Python Software Foundation, *asyncio* documentation, "Running blocking code" and the `concurrent.futures` executors; PEP 703 (2023), "Making the Global Interpreter Lock Optional in CPython".
- Beyer et al. (2016), *Site Reliability Engineering*, chapter 21, "Handling Overload" — admission control and the case for rejecting work.
- Paper P3 in the companion repository (Appendix A) — the measurements referred to in this chapter.
