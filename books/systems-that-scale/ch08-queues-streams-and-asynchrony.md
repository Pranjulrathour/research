# Chapter 8 — Queues, streams and asynchrony

The most common performance fix after caching is to make something asynchronous: take the slow part out of the request, put it on a queue, return to the user, and do the work later. It is often right, it is frequently done for the wrong reasons, and it changes the system's failure modes in ways that are easy to miss until the queue is a million messages deep and nobody knows whether the work is being done.

This chapter is about when asynchrony is the right tool, what a queue actually promises, how the two main families (message queues and logs) differ, and the one metric that tells you whether an asynchronous system is healthy.

## The principle

**Make work asynchronous when the user does not need its result to continue, never merely because it is slow. A queue decouples the producer's rate from the consumer's; it does not create capacity, and queue depth is the metric that tells you the truth.**

## When asynchrony is right, and when it is a mistake

The test is simple. Does the user, or the caller, need the result of this work to proceed? If a user uploads a photo and the system must generate three thumbnails, the user needs confirmation that the upload succeeded and does not need to wait for the thumbnails; asynchronous is right. If a user submits a payment, they need to know whether it succeeded before they leave the page; asynchronous is wrong, however slow the authorisation is, and the fix for slowness is to make it faster or to show honest progress, not to hide the wait and hope.

The mistake is making something asynchronous because it is slow. The work does not get faster. It gets *invisible*: the user no longer waits, which means the user no longer notices when it does not happen, which means neither does anyone else until the backlog is discovered. Asynchrony converts a latency problem, which is visible, into a reliability problem, which is not. That conversion is worth making only when the work can genuinely wait and when the system has the means (queue depth, dead-letter handling, monitoring) to know it is getting done.

Three cases where it is the right tool. *Fan-out*: one event triggers many pieces of work (notify, index, log, bill); doing them inline makes the request as slow as the slowest and as fragile as the least reliable. *Smoothing*: load arrives in bursts and the work can be spread; a queue absorbs the burst and the consumers run at a steady rate. *Decoupling*: producer and consumer are different teams, deploy on different schedules, and should not take each other down.

## What a queue promises, and what it does not

A queue promises *buffering* (the producer can continue while the consumer is busy) and *delivery* (a message put in will be given to a consumer, under the queue's delivery guarantee). It does not promise *capacity*. If producers add 1,000 messages a second and consumers process 800, the queue grows by 200 a second forever. A queue in that state is not healthy, it is a slow-motion failure, and the only fixes are more consumers, faster consumers, or fewer messages. The queue made the mismatch survivable for a while; it did not make it go away.

This is why **queue depth** (or its time equivalent, the age of the oldest unprocessed message) is the health metric for every asynchronous system. Latency and error rate tell you about the synchronous path; depth tells you whether the asynchronous work is keeping up. A depth that is growing is an alarm, regardless of how it looks on any other dashboard. A depth that is stable but large means the backlog is a permanent delay that every message pays. A depth near zero means consumers have headroom.

**Delivery guarantees.** Most queues offer *at-least-once*: a message is redelivered if the consumer does not acknowledge it, so a consumer that crashes mid-processing will see the message again. Chapter 6's lesson applies in full: consumers must be idempotent, because they will receive duplicates. *At-most-once* (no redelivery) is simpler and loses messages on failure; acceptable for metrics, not for orders. *Exactly-once* is, as chapter 6 argued, at-least-once plus idempotent consumption, sometimes packaged by the system (transactional consumption with deduplication) and always subject to the same limits at the boundary with the outside world.

**Ordering.** A single queue with a single consumer preserves order. Add consumers for throughput and order is lost across them; a message that failed and was redelivered arrives after its successors. Systems that need order within a key (all events for one account, in sequence) partition by that key and process each partition with one consumer at a time, which is exactly the log model below. Systems that need global order have one consumer and therefore one consumer's throughput. There is no third option.

**Dead letters.** A message that fails repeatedly (a bug, a malformed payload, a dependency that rejects it) will be redelivered until it blocks the queue, if nothing stops it. A *dead-letter queue* receives messages that exceed a retry count, so that the main queue keeps flowing and the failures are visible, inspectable and replayable. A system without a dead-letter queue has a poison-message outage waiting in it. A system with one that nobody monitors has a silent data-loss problem instead.

## Two families: message queues and logs

The two dominant designs differ in one idea: what happens to a message after it is consumed.

**Message queues** (RabbitMQ, Amazon SQS, ActiveMQ, Azure Service Bus and their relatives) hand each message to one consumer and delete it once acknowledged. The queue holds only unprocessed work. Natural for *task distribution*: a pool of workers, each taking the next job. Flexible routing (topics, fan-out exchanges, priorities), per-message acknowledgement, and simple semantics: a message is pending, in flight, done or dead. The limits: once a message is consumed it is gone, so a new consumer cannot see history, and throughput per queue is bounded by the broker's per-message bookkeeping.

**Logs** (Apache Kafka, Amazon Kinesis, Apache Pulsar, Redpanda) append every message to a partitioned, ordered, durable log and keep it for a retention period regardless of consumption. Consumers track their own position (offset) in each partition. The same message can be read by many independent consumer groups, each at its own pace; a new consumer can start from the beginning; a consumer that had a bug can rewind and reprocess.[^1] Order is guaranteed within a partition and partitions are assigned to consumers within a group, so parallelism equals the partition count. Throughput is very high because the broker does almost nothing per message. The limits: no per-message acknowledgement or deletion (a consumer group's progress is one offset per partition, so one slow message holds up everything behind it in that partition); routing is by topic and partition key only; and the operational model (partitions, offsets, consumer-group rebalancing, retention) is more to learn.

The choice follows from the question *who else needs this data?* If the answer is "only the worker that does the job", a message queue is simpler. If the answer is "several systems, now and later, some of which do not exist yet", the log is the right substrate, and it is why logs became the backbone of event-driven architectures and of the data pipelines that feed analytics and machine learning. The *event* (something happened: an order was placed) is written once; billing, fulfilment, search indexing, fraud scoring and the data warehouse each consume it independently.

A note on the log as a design idea beyond messaging. The same structure (an append-only, ordered, replayable record of changes) is the replication log in a database (chapter 6), the write-ahead log that gives a database durability, and the change-data-capture stream that keeps caches and search indexes in step with the source of truth (chapter 3). Learning the log once pays off across the whole stack.[^2]

## Jobs that must complete

"Fire and forget" is the right pattern for work whose failure is acceptable: an analytics event, a cache warm-up. It is the wrong pattern for a refund, a report a customer is waiting for, or a provisioning step that leaves the system half-configured if it does not run. For work that must complete, the asynchronous system needs the properties of a transaction spread over time.

*Durable enqueue.* The job is persisted before the request returns, ideally in the same transaction as the state change that triggered it (the *transactional outbox*: write the job to an outbox table in the same database transaction, and have a relay publish it), so that a crash between "state changed" and "job queued" cannot lose the job.[^3]

*Idempotent execution with a status record.* The job has an identity, a status (pending, running, done, failed) that is updated as it progresses, and steps that can be re-run safely. A job that ran halfway and was retried continues or restarts cleanly.

*Visibility.* Someone can answer "what is the state of job 4812?" from a table, not from grepping logs. Chapter 6's sagas are this pattern applied to multi-step business transactions, and a *workflow engine* (Temporal, AWS Step Functions, Cadence and their relatives) is this pattern productised: durable state per workflow, retries with policy, timers, and the ability to see and resume every in-flight instance.

*Deadlines and escalation.* A job that has not completed within its expected time is a job that needs attention, and the system should notice before the customer does.

## Backpressure, again

Chapter 2 introduced backpressure for synchronous systems. In asynchronous ones it is the question of what happens when the queue is full or growing beyond bound. Three options, chosen in advance: *block* the producer (correct when the producer can wait, such as a batch loader), *shed* (drop or reject the message with a signal, correct for low-value, high-volume data), or *spill* (persist to slower, larger storage, correct when nothing may be lost and delay is acceptable). An unbounded queue is a choice of "spill to memory until the broker dies", which is the worst of the three.

## The question you will be asked

*"A job queue is growing. Is the system healthy?"*

No, and the answer is to say why and what to look at. A growing depth means consumers are slower than producers. Is the growth new? Then something changed: consumer count (did a deployment fail?), consumer speed (is a dependency slow? chapter 7), or producer rate (is there a burst, a retry storm, a loop?). Look at the age of the oldest message to translate depth into delay the user feels. Look at the dead-letter queue to see whether failures are the cause. Look at the consumers' own latency and error rate. Then act: scale consumers if the work is parallel, fix the dependency if it is slow, shed or throttle producers if the burst is abnormal. And say what should have happened before you were asked: an alert on depth trend or oldest-message age, not on depth alone, because a large stable depth and a small growing one are different problems.

## The trade-off, stated

Asynchrony buys lower request latency, burst absorption, decoupling between teams and systems, and fan-out without fragility. It costs visibility (the work is no longer in the request path, so its failure is silent unless instrumented), complexity (at-least-once delivery, idempotency, ordering, dead letters, a new component to operate), and eventual consistency between the triggering action and its effects (chapter 5). The trade is right when the user does not need the result to continue and the team is willing to treat queue depth as a first-class metric. It is wrong when the asynchrony is hiding slowness rather than enabling independence.

## Run this yourself

Set up a queue (Redis lists suffice; so does a local Kafka or RabbitMQ) with a producer that sends 1,000 messages a second and a consumer that processes 800. Plot depth over five minutes; watch it grow linearly. Add a second consumer and watch it drain. Then make the consumer fail on every fiftieth message without a dead-letter queue and watch the whole queue stall behind the poison message (in a log) or the broker redeliver it forever (in a queue). Add the dead-letter queue and watch the main queue flow again. Finally, kill the consumer mid-message and confirm you see the duplicate on restart. That is the whole chapter in an hour, and the shape of the depth curve under each condition is the thing to remember.

---

[^1]: Kreps, J., Narkhede, N. & Rao, J. (2011), "Kafka: a Distributed Messaging System for Log Processing", *NetDB 2011*.
[^2]: Kreps, J. (2013), "The Log: What every software engineer should know about real-time data's unifying abstraction", LinkedIn Engineering blog, December 2013 — the essay that generalised the idea.
[^3]: Richardson, C. (2018), *Microservices Patterns*, Manning, chapter 3 — the transactional outbox and polling-publisher patterns.

### Sources for this chapter
- Kreps, Narkhede & Rao (2011) — Kafka; Kreps (2013) — the log as abstraction.
- Kleppmann (2017), *Designing Data-Intensive Applications*, chapter 11 (stream processing) — logs vs message brokers, delivery semantics.
- Richardson (2018) — the outbox pattern.
- Hohpe, G. & Woolf, B. (2003), *Enterprise Integration Patterns*, Addison-Wesley — the vocabulary of messaging (dead letter channel, competing consumers, idempotent receiver).
- Temporal and AWS Step Functions documentation — durable execution as a product category.
- Beyer et al. (2016), *Site Reliability Engineering*, chapter 24 (distributed periodic scheduling) and 25 (data processing pipelines) — operating asynchronous systems at scale.
