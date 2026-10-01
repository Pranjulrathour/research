# Chapter 6 — Replication, partitioning and the two hard problems

A single database on a single machine is the most consistent, simplest, best-understood system there is, and almost every system that matters outgrows it in one of two ways. It needs to survive the machine failing, which means more than one copy of the data: *replication*. Or it needs to hold or serve more than one machine can, which means splitting the data across machines: *partitioning* (or sharding). Both are old problems with known solutions, and both introduce the failure modes that fill incident reports, because both turn one fact into several that must be kept in agreement.

This chapter is about the shapes those solutions take, the problems each shape has, and the two specific hard problems (a payment that must happen exactly once, and a transaction that spans machines) that every engineer eventually meets.

## The principle

**Every copy of data is a place where the truth can diverge, and every boundary between machines is a place where an operation can half-complete. Design for both from the start: decide who may write, decide what happens when they disagree, and make every operation safe to repeat.**

## Replication: who may write

There are three shapes, and the whole design follows from which one you choose.

**Single leader.** One replica accepts writes; the others copy its log and serve reads. Simple to reason about (there is one order of writes, the leader's), and the model behind most relational databases, most managed database services and most systems that need strong consistency for some operations. The costs: writes are limited to one machine's capacity; the leader is a single point of failure that must be replaced when it fails; and reads from followers are stale by the replication lag (chapter 5's opening anomaly).

Replication may be *synchronous* (the leader waits for a follower to confirm before acknowledging the write; no data loss on leader failure, but a slow or dead follower slows or stops writes) or *asynchronous* (the leader acknowledges immediately; fast, but writes not yet copied are lost if the leader dies). Most production systems use a mix: one synchronous follower for durability, the rest asynchronous.

**Multi-leader.** Several replicas accept writes, usually one per region, and exchange changes. Writes are local and fast everywhere, and the system keeps accepting writes when regions cannot reach each other. The cost is the one that single-leader avoided: the same record can be written differently in two places at once, and the system must *resolve the conflict*. Last-writer-wins (by timestamp) is the common default and it silently discards one of the writes; application-specific merging is correct and expensive to write; conflict-free replicated data types (CRDTs) make certain structures (counters, sets, some text) mergeable by construction.[^1] Use multi-leader when write availability across regions matters more than simplicity, and only for data whose conflicts you have decided how to resolve.

**Leaderless.** Any replica accepts writes; clients write to and read from several, and a quorum (chapter 5: *W* + *R* > *N*) ensures reads overlap writes. The Dynamo family. No failover, no leader election, graceful behaviour under partial failure, and the same conflict problem as multi-leader, plus weaker guarantees about ordering. Use for high-availability data where eventual consistency is acceptable and the operational simplicity of "no leader" is worth the semantic complexity.

### Failover and the split brain

In a single-leader system the dangerous moment is when the leader fails, or appears to. A follower must be promoted, clients must be redirected, and the old leader, if it was only partitioned rather than dead, must be prevented from accepting writes when it comes back. If it is not, there are two leaders, both accepting writes, each unaware of the other: a *split brain*, and the writes to one will be lost or will conflict when the partition heals.

The defences are well established. Leader election through a consensus protocol (Raft, Paxos, or a coordination service such as ZooKeeper or etcd that implements one) ensures only one node believes itself leader at a time. *Fencing* ensures the old leader cannot act: a monotonically increasing epoch or fencing token accompanies every write, and storage rejects writes from an older epoch. And a *lease* ensures a leader that cannot renew its claim within a time bound stops acting on its own, before another is elected.[^2] A system that promotes followers automatically without fencing is a system that will, one day, have two leaders.

## Partitioning: where the data lives

When the data or the load exceeds one machine, it is split by a *partition key*. The choices are few and the consequences large.

**By key range.** Records with keys A–F on one machine, G–M on another. Range scans are efficient (adjacent keys are together); the danger is *hot spots*: if keys are timestamps, all writes go to the newest partition, and one machine does all the work while the others idle.

**By hash of key.** A hash function spreads keys evenly, so load is balanced. Range queries become scatter-gather across all partitions. Hot spots still occur when a single key is hot (one celebrity's record, one tenant's data), and the only fixes are application-level: split the key (append a random suffix and read from all variants) or cache it.

**Choosing the key.** The partition key should be the thing most queries filter by, so that most queries hit one partition, and it should spread load evenly over time. These goals conflict more often than not, and the choice of partition key is the single most consequential decision in a large data store because it is the hardest to change later.

**Rebalancing.** Adding machines means moving partitions. Naive hashing (key mod *N*) moves almost everything when *N* changes; *consistent hashing* and fixed-partition-count schemes (many more partitions than machines, assigned to machines and moved whole) keep the movement proportional to the change.[^3] Automatic rebalancing is convenient and it is also a way for a system to move large amounts of data at the worst possible moment, so good systems let an operator confirm.

**Secondary indexes.** Finding records by something other than the partition key. Either each partition indexes its own data (writes are local; reads must query every partition: scatter-gather) or the index is itself partitioned by the indexed value (reads go to one partition; writes must update an index somewhere else, asynchronously, and the index lags). Neither is free, and most systems offer one and let you feel its cost.

## The first hard problem: exactly once

Consider a payment service. A client sends "charge card X 500 rupees". The service charges the card and, before it can reply, the connection drops. The client does not know whether the charge happened. If it retries, the customer may be charged twice. If it does not, the customer may not be charged at all. There is no third option in the protocol itself: a message either arrives or it does not, and the sender cannot distinguish "lost before processing" from "lost after".

This is why *exactly-once delivery* is, strictly, impossible across an unreliable network, and why the claims of exactly-once in various systems are claims about *effective* exactly-once: at-least-once delivery combined with processing that is safe to repeat.[^4] The combination is a discipline, and it has a name.

**Idempotency.** An operation is idempotent if doing it twice has the same effect as doing it once. Reads are idempotent; "set balance to 1,000" is idempotent; "add 500 to balance" is not. Non-idempotent operations are made idempotent by attaching an *idempotency key*, a unique identifier chosen by the client for this logical operation, which the server records with the result. A retry with the same key returns the recorded result instead of re-executing. The payment APIs of every serious provider work this way, and a payment system without idempotency keys is a double-charge waiting for a flaky network.

The discipline has details. The key and the result must be stored atomically with the operation's effect, or a crash between them re-creates the problem. Keys must be retained long enough to cover any plausible retry. And the check must be at the point of effect, not at an edge that can be bypassed.

**Design a payment system that never double-charges** is a standard interview question and the answer is this: client-generated idempotency keys; a record of key → outcome written in the same transaction as the charge; retries that return the recorded outcome; a reconciliation job that compares the service's records with the card network's, because the network can fail in ways that leave the two disagreeing; and clear semantics for the client about how long a key is valid. Everything else (queues, retries with backoff, timeouts) is plumbing around that core.

## The second hard problem: transactions across machines

A transaction moves money from account A on partition 1 to account B on partition 2. Both must change or neither. On one machine, the database's transaction does this. Across machines, something has to coordinate.

**Two-phase commit (2PC).** A coordinator asks each participant to prepare (make the change durable but not visible, and promise to commit if asked), then, if all agree, tells each to commit. The guarantee is atomicity across machines. The costs are latency (two round trips to every participant) and the coordinator being a single point of failure *during the protocol*: if it dies after participants have prepared, they hold locks and cannot proceed until it returns. 2PC is correct and it is a blocking protocol, and that is why most large systems avoid it across service boundaries and use it only within a single database system that has a highly available coordinator.[^5]

**Sagas.** Break the transaction into a sequence of local transactions, each with a *compensating* action that undoes it. Debit A; then credit B; if crediting B fails, run the compensation: re-credit A.[^6] No locks held across machines, no blocking coordinator, and a different guarantee: the system passes through intermediate states that are visible (A has been debited and B not yet credited), and the compensations must themselves be reliable, idempotent and semantically sensible (you cannot un-send an email; you send a correction). Sagas are the pragmatic choice across services, and they move the hard work from the database into the application, where it must be designed, tested and monitored. A saga without a way to see which step each in-flight instance is on is a saga nobody can debug.

**Designing around the problem.** The best cross-partition transaction is the one you do not need. Choose partition keys so that the records that must change together live together (the customer and their orders; the account and its ledger entries). Where that is impossible, prefer sagas with idempotent steps, and accept, explicitly, the intermediate states.

## The question you will be asked

*"Design a payment system that never double-charges."*

The answer above. Then the follow-ups the question is really testing. *What if the card network times out?* Treat the charge as unknown, do not retry blindly, reconcile against the network's record. *What if two requests with the same key arrive at the same time?* The key insert must be atomic and unique-constrained so the second waits or fails. *What if the service crashes after charging but before recording?* Record and charge in one transaction where possible; where the charge is external, record "charge attempted with network reference R" before calling, and reconcile. *How do you know it works?* A metric for duplicate-key hits, a daily reconciliation report, and a chaos test that kills the service mid-charge. The interviewer is listening for the understanding that the network makes "exactly once" a property you build, not one you receive.

## The trade-off, stated

Replication buys durability and read capacity and costs consistency (lag, conflicts) and operational complexity (failover, fencing). Partitioning buys write capacity and storage and costs query flexibility (scatter-gather, lagging indexes) and the end of cheap transactions. Both are unavoidable at scale, and both are manageable with a small set of disciplines: one writer or a conflict rule; fencing on failover; a partition key chosen for the queries; idempotency everywhere; sagas with visible state where transactions must span machines. The systems that fail are not the ones that chose weak guarantees. They are the ones that did not notice they had.

## Run this yourself

Write a tiny payment service with an endpoint that "charges" by appending to a ledger file. Write a client that sends charges and retries on timeout. Run them with a proxy between them that drops 10 per cent of responses (not requests) and count the ledger entries against the client's intent. You will see double charges within a minute. Add an idempotency key to the request and a key → result table to the service, written atomically with the ledger entry, and run again. The duplicates vanish. Then kill the service with a signal at random moments under load and check the ledger and the key table agree. This is an afternoon's work and it is the whole of the first hard problem made visible.

---

[^1]: Shapiro, M., Preguiça, N., Baquero, C. & Zawirski, M. (2011), "Conflict-free Replicated Data Types", *SSS 2011*.
[^2]: Ongaro, D. & Ousterhout, J. (2014), "In Search of an Understandable Consensus Algorithm" (Raft), *USENIX ATC 2014*; Gray, C. & Cheriton, D. (1989), "Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency", *SOSP 1989*; Kleppmann, M. (2016), "How to do distributed locking", on fencing tokens.
[^3]: Karger, D. et al. (1997), "Consistent Hashing and Random Trees", *STOC 1997*; the fixed-partition scheme is described in the Dynamo and Riak literature.
[^4]: The impossibility is the Two Generals problem (Akkoyunlu, Ekanadham & Huber, 1975) in another guise; for the practical treatment see Kleppmann (2017), chapter 11, and the Kafka "exactly-once semantics" design notes (2017), which are explicit that the guarantee is idempotent production plus transactional consumption.
[^5]: Gray, J. (1978), "Notes on Data Base Operating Systems", in *Operating Systems: An Advanced Course*, Springer — the original description; Gray, J. & Reuter, A. (1993), *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann.
[^6]: Garcia-Molina, H. & Salem, K. (1987), "Sagas", *SIGMOD 1987*.

### Sources for this chapter
- Kleppmann (2017), *Designing Data-Intensive Applications*, chapters 5–9 — replication, partitioning, transactions and consistency for practitioners.
- Ongaro & Ousterhout (2014) — Raft; Lamport, L. (1998), "The Part-Time Parliament", *ACM TOCS* 16(2) — Paxos.
- Shapiro et al. (2011) — CRDTs.
- Karger et al. (1997) — consistent hashing.
- Gray (1978); Gray & Reuter (1993) — two-phase commit and transaction processing.
- Garcia-Molina & Salem (1987) — sagas.
- Stripe and Razorpay API documentation on idempotency keys — the production pattern, as deployed.
- Helland, P. (2012), "Idempotence Is Not a Medical Condition", *ACM Queue* 10(4) — the clearest essay on the first hard problem.
