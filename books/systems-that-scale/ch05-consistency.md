# Chapter 5 — Consistency, availability and what you actually get

A user changes their display name, the page reloads, and the old name is still there. They try again; now the new one shows. They open the app on their phone and see the old one. Nothing is broken, in the sense that every server is up and every request returned successfully. Something is wrong, in the sense that the system has told the same person three different things about one fact within ten seconds.

This chapter is about that gap: between a system that is available and a system that is telling the truth, and about the vocabulary engineers use to say precisely which truths a system promises. The vocabulary matters because the promises are expensive, the cheap ones are often good enough, and the worst outcome is not choosing a weak guarantee but failing to know which one you chose.

## The principle

**Consistency is a promise about what reads return relative to writes, and every promise has a price in latency, availability or both. Choose the weakest promise that keeps the user's experience coherent, and state it.**

## What CAP actually says

Almost everyone who has sat a system-design interview has heard of the CAP theorem, and almost everyone has heard a version that is wrong. The folk version is a menu: consistency, availability, partition tolerance, pick two. The theorem says something narrower and more useful.

A distributed system holds copies of data on more than one machine, and the network between those machines will sometimes fail: messages are delayed or lost, and for a period the machines cannot tell whether the others are down or merely unreachable. That is a *partition*. CAP, stated informally by Brewer in 2000 and proved by Gilbert and Lynch in 2002, says that *during a partition* a system must choose between answering every request (availability) and answering only with values that are guaranteed up to date (consistency).[^1] It cannot do both, because an isolated node cannot know whether the other side has accepted a newer write.

Three consequences follow that the menu version hides.

Partition tolerance is not a choice. Networks partition; a system that does not tolerate partitions is a system that corrupts data or stops when they happen. The real choice is only between C and A, and only while a partition is in progress.

Outside partitions, which is almost all of the time, CAP says nothing. A system can be both consistent and available when the network is healthy, and most are. The trade-off that applies in normal operation is a different one: between consistency and *latency*, because stronger guarantees require coordination between nodes, and coordination takes round trips. Abadi's PACELC formulation makes this explicit: if there is a Partition, trade Availability against Consistency; Else, trade Latency against Consistency.[^2] It is the more useful of the two acronyms and the less known.

"Consistency" in CAP means one specific, strong thing: linearizability, discussed below. Most of the consistency models engineers actually work with are weaker than that and are not what CAP is about.

## The models, in plain terms

Consistency models are promises about the order in which operations appear to happen. Here are the ones that matter, from strongest to weakest, each with the user-visible promise it keeps.

**Linearizability (strong consistency).** Every operation appears to take effect at a single instant between its start and its finish, and all clients agree on the order. If a write completes and then a read begins, anywhere, the read sees the write. This is what people mean by "the database just works". It is also the most expensive: every read or write that must be linearizable has to coordinate with a majority of replicas (or go through a single leader), which costs at least one network round trip and makes the operation unavailable when a majority cannot be reached. Promise kept: *you will never see stale data.* Systems that offer it for some or all operations include Spanner, etcd, ZooKeeper, and single-leader relational databases when reads go to the leader.

**Sequential consistency.** All clients see operations in the same order, and that order respects each client's own program order, but it need not match real time: a read may return a value that was overwritten a moment ago, as long as everyone sees the same history. Rarely offered explicitly; useful as a concept for understanding the next ones.

**Causal consistency.** If operation B could have been caused by operation A (B happened after A on the same client, or B read something A wrote), everyone sees A before B. Operations that are unrelated may be seen in different orders by different clients. Promise kept: *you will never see an effect before its cause*, such as a reply before the comment it replies to. This is the strongest model that can remain available during partitions, which makes it a natural target for systems that must keep working when the network does not.[^3]

**Session guarantees.** A family of promises scoped to one client's session, each cheap to provide and each solving a specific user-visible anomaly:[^4]

- *Read-your-writes*: after you write, your own reads see it. Solves the display-name problem that opened this chapter.
- *Monotonic reads*: once you have seen a value, you never see an older one. Solves "the comment appeared, then vanished, then came back".
- *Monotonic writes*: your writes are applied in the order you made them.
- *Writes-follow-reads*: a write you make after reading a value is ordered after that value everywhere.

Session guarantees are what most applications actually need, and they are often implemented not in the database but at the edge: by routing a user's requests to the same replica, by having the client carry a version token, or by reading from the leader for a few seconds after a user writes.

**Eventual consistency.** If writes stop, all replicas will converge to the same value, eventually. No promise about how long, and no promise about what you see in the meantime. Promise kept: *nothing is lost, and the copies will agree in the end.* It is the natural model for data that is replicated across regions, cached widely, or written in many places at once, and it is fine for data where a short disagreement does not matter: view counts, presence indicators, feeds, product catalogues. It is not fine for anything where two clients acting on different views can produce an irreversible conflict: balances, inventory, seat reservations, access control.

The important realisation is that these are not a ladder you climb as the budget allows. They are tools for different data. One system commonly offers linearizable operations on a few critical keys, causal or session consistency for user-facing state, and eventual consistency for the rest, and the engineering skill is in knowing which data is which.

## Where the big systems sit, and why

A handful of widely-used systems illustrate how the trade-offs are made in practice. Dates matter because these designs responded to specific needs at specific times.

**Dynamo (Amazon, 2007)** chose availability and eventual consistency for Amazon's shopping cart, on the reasoning that an unavailable cart cost more than a briefly inconsistent one, and introduced the mechanisms (vector clocks, sloppy quorums, hinted handoff, read repair) that a generation of "AP" stores copied.[^5] Its descendants, including Cassandra (2008) and Riak, let the client choose consistency per operation through tunable quorums: with *N* replicas, a write acknowledged by *W* of them and a read that consults *R*, the read is guaranteed to overlap a recent write when *W* + *R* > *N*. The arithmetic is simple and the behaviour under failure is not; the overlap guarantee says nothing about which of several concurrent writes you will see.

**Spanner (Google, 2012)** went the other way and showed that linearizable, globally distributed transactions were practical at scale, by using atomic clocks and GPS receivers to bound clock uncertainty (TrueTime) and waiting out the uncertainty before committing.[^6] The price is latency (commits wait for the clock bound and for cross-region consensus) and the hardware. Its lesson is that the trade-off can be moved by engineering, at a cost, when the application (financial transactions, in Google's case advertising billing) demands it.

**DynamoDB (Amazon, 2012)** descends from Dynamo's ideas but offers, since 2012, a choice per read between eventually consistent (cheaper, default) and strongly consistent, and later added transactions. The choice being explicit, per request, is itself the design lesson.

**Single-leader relational databases (PostgreSQL, MySQL and their managed forms)** are linearizable when every read goes to the leader and eventually consistent the moment reads are served from replicas, which is how most of them are run at scale. The replication lag is usually milliseconds and occasionally seconds, and the display-name anomaly that opened this chapter is almost always this: a write to the leader followed by a read from a lagging replica. The fix is a session guarantee (read-your-writes), implemented by routing the next few reads after a write to the leader.

## The question you will be asked

*"A user updates their profile and immediately sees the old value. Where did it come from?"*

The answer the interviewer wants is a diagnosis, not a guess. Walk the read path. Was the read served by a replica that had not yet applied the write (replication lag)? By a cache that still held the old value (cache invalidation, chapter 3)? By a CDN edge? By the client's own local state? Each is a different fix. Then name the guarantee that would have prevented it (read-your-writes), say how you would provide it (route the user's reads to the leader for *N* seconds after a write, or carry a version token and re-read until the replica catches up), and say what it costs (more load on the leader, or a small added latency for the user who just wrote). An answer that stops at "eventual consistency" without the diagnosis, the fix and the cost is an answer that has heard of the problem but not met it.

## The trade-off, stated

Stronger consistency buys correctness under concurrency and failure, and costs latency (coordination round trips), availability during partitions, and throughput (serialisation points). Weaker consistency buys speed and availability and costs the possibility of anomalies, which are either harmless for the data in question or must be prevented by application logic (idempotency, conflict resolution, compensation), which is harder than it sounds and the subject of chapter 6.

The failure mode to fear is not choosing weak consistency. It is choosing it implicitly: reading from replicas because it was the default, caching because it was easy, and discovering the guarantee you did not have when a customer is double-charged.

## Run this yourself

Set up a database with one leader and one replica (PostgreSQL streaming replication works; so does a managed service with a read replica). Write a script that updates a row on the leader and immediately reads it from the replica, a thousand times, and records how often the read is stale and by how much. Then add artificial load to the leader and repeat. You will see the lag distribution with your own eyes, which is worth more than any number this chapter could quote, because it depends on your hardware, your load and your configuration. Then implement read-your-writes (route to the leader for two seconds after a write) and confirm that the anomaly disappears. The whole exercise takes an afternoon and it is the single most common distributed-systems bug in production.

---

[^1]: Brewer, E. (2000), "Towards Robust Distributed Systems", keynote, *PODC 2000*; Gilbert, S. & Lynch, N. (2002), "Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services", *ACM SIGACT News* 33(2). Brewer revisited the misreadings in "CAP Twelve Years Later: How the 'Rules' Have Changed", *IEEE Computer*, February 2012.
[^2]: Abadi, D. (2012), "Consistency Tradeoffs in Modern Distributed Database System Design: CAP is Only Part of the Story", *IEEE Computer* 45(2).
[^3]: Mahajan, P., Alvisi, L. & Dahlin, M. (2011), "Consistency, Availability, and Convergence", UT Austin TR-11-22; Lloyd, W. et al. (2011), "Don't Settle for Eventual: Scalable Causal Consistency for Wide-Area Storage with COPS", *SOSP 2011*.
[^4]: Terry, D. B. et al. (1994), "Session Guarantees for Weakly Consistent Replicated Data", *PDIS 1994*.
[^5]: DeCandia, G. et al. (2007), "Dynamo: Amazon's Highly Available Key-value Store", *SOSP 2007*.
[^6]: Corbett, J. C. et al. (2012), "Spanner: Google's Globally-Distributed Database", *OSDI 2012*.

### Sources for this chapter
- Brewer (2000, 2012); Gilbert & Lynch (2002) — CAP and its misreadings.
- Abadi (2012) — PACELC.
- Terry et al. (1994) — session guarantees.
- Lloyd et al. (2011); Mahajan, Alvisi & Dahlin (2011) — causal consistency and availability.
- DeCandia et al. (2007) — Dynamo; Corbett et al. (2012) — Spanner.
- Kleppmann, M. (2017), *Designing Data-Intensive Applications*, chapters 5 and 9 — the best single treatment of replication and consistency for practitioners.
- Bailis, P. et al. (2013), "Highly Available Transactions: Virtues and Limitations", *VLDB 2014* — which guarantees can be offered without giving up availability.
