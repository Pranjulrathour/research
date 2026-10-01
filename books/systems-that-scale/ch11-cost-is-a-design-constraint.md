# Chapter 11 — Cost is a design constraint

Every design decision in this book has had a price, and so far the price has been paid in latency, consistency, complexity or risk. This chapter pays it in money, because money is the constraint that decides which of the technically correct designs actually gets built, and because the engineers who can reason about cost with the same rigour they bring to latency are rare enough to be valuable for that reason alone.

The chapter is written for the engineer, not the accountant: how to see where money goes in a system, which design choices move it, when the slower or simpler design is the right one because it is cheaper, and how to decide between building, buying and renting with numbers rather than preferences.

## The principle

**Cost is a first-class output of a design, like latency and availability. Model it before you build, measure it after, and treat the system's bill per unit of useful work as a metric with a target.**

## Where the money goes

The bill for a system on cloud infrastructure, which is where most new systems live, has a small number of large lines.

**Compute.** Virtual machines, containers, serverless invocations, managed service instances. Priced by time and size, with large discounts for commitment (reserved or savings-plan pricing, typically 30–60% below on-demand for one- to three-year terms) and for interruptible capacity (spot or preemptible instances, often 60–90% below on-demand, with the catch that they can be reclaimed at short notice). Compute is usually the largest line and the one most sensitive to the design choices in chapters 2, 3 and 10.

**Storage.** Block volumes, object storage, databases, backups, logs. Priced by volume stored per month, by tier (hot, warm, cold, archive, with retrieval costs rising as storage costs fall), and by operations. Storage is cheap per gigabyte and expensive in aggregate because it accumulates: nothing deletes itself, and a system that has run for three years is often paying for data nobody has read in two.

**Data transfer.** Moving bytes out of a cloud region to the internet (egress), between regions, and sometimes between availability zones. Egress is the line that surprises people: it is priced per gigabyte at rates that make serving large files or media directly from compute far more expensive than serving them through a content-delivery network, and it is the reason multi-region and multi-cloud designs cost more than their compute suggests.

**Managed services.** Databases, queues, caches, search, monitoring, AI model APIs. Priced by instance, by request, by capacity unit or by token, each with its own curve. Managed services trade money for engineering time and operational risk, and the trade is usually good at small scale and increasingly worth re-examining as scale grows.

**People.** The line that is not on the cloud bill and usually dwarfs it. An engineer's time is the most expensive resource in most systems, and a design that saves a hundred dollars a month of compute by costing a week of engineering has lost money for years. Any cost analysis that omits the people is incomplete, and most do.

## Where the money leaks

Across systems and organisations the same leaks recur, and finding them is more valuable than any optimisation.

**Idle capacity.** Instances running at 5% utilisation, development environments left on overnight and at weekends, databases sized for a peak that happened once. The fix is measurement (chapter 9's utilisation metrics, read for cost rather than latency) and then scheduling, right-sizing or autoscaling. This is almost always the largest leak and the easiest to close.

**Over-provisioning from fear.** Chapter 10 argued for headroom below the knee; the leak is headroom far beyond it, bought because nobody measured the knee and everybody feared the incident. The fix is the measurement.

**Chatty services.** Architectures that make many small network calls per user request pay for each in latency (chapter 1) and, across zones or regions, in transfer charges. A design that fetches a hundred rows in a hundred calls costs more than one that fetches them in one, in every currency.

**Logs and metrics nobody reads.** Chapter 9's warning. Debug logging left on in production, metrics with exploding cardinality, traces sampled at 100%. Telemetry is valuable in proportion to its use, and the unused part is a pure leak.

**Data that should have been deleted or tiered.** Backups of backups, logs retained for years by default, old object versions, orphaned volumes. A retention policy and a lifecycle rule (hot to cold to archive to deleted, on a schedule) usually cut storage cost by more than half.

**Egress by accident.** Serving static assets from compute instead of a CDN; replicating data across regions that did not need it; pulling large datasets out of the cloud for processing elsewhere.

**The model-API line.** New since 2023 and growing fast: calls to large language models priced per token. The leaks are the familiar ones in new clothes: long prompts repeated on every call (a caching problem, chapter 3), a large model used where a small one would do (a right-sizing problem), retries without budgets (chapter 7), and no measurement of cost per useful outcome. Teams that treat model calls as free in development are routinely surprised by the first production bill.

## Performance per rupee

The cost lens changes some of the earlier chapters' conclusions, and it is worth being explicit.

**The slower design can be the right one.** A batch job that runs nightly on cheap interruptible capacity may be better than a real-time pipeline running on reserved instances around the clock, if nobody needs the result in under a day. A single-region deployment with a tested backup-and-restore may be better than an active-active multi-region one, if the business can tolerate an hour of downtime a year and cannot tolerate tripling the bill. The engineering instinct is toward the faster, more available design; the cost lens asks what the latency and availability are *for*, and chapter 9's SLO is the place that question gets answered.

**The simpler design is usually cheaper in people.** Every component is a thing to operate, patch, monitor and understand at 3 a.m. A system with fewer moving parts costs less in the line that is not on the bill.

**Scale changes the answer.** Managed services and serverless pricing are excellent at low volume (you pay nothing when idle) and expensive at high steady volume (you pay a premium on every unit). The crossover, where running your own becomes cheaper, exists for almost every service and is worth computing rather than assuming. The reverse is also true: a self-managed system that was cheaper at scale may be more expensive than the managed one once the engineering time to run it is counted.

**Free tiers have cliffs.** Many services offer a free or near-free tier that covers development and small production use, with pricing that steps up sharply at a threshold. Designs that depend on staying under the threshold should know exactly where it is and what happens when a traffic spike crosses it, because the first bill after the cliff is a common and avoidable surprise.

## Build, buy or rent

The recurring decision is whether to build a capability, buy a product, or rent a managed service, and it should be made with a short model rather than a long debate.

Estimate, over a horizon (three years is common), the total cost of each option: engineering time to build and to operate (at a loaded cost per engineer-month), infrastructure, licence or subscription fees, and the cost of the capability being unavailable or wrong. Then weigh three non-monetary factors: how central the capability is to what makes the product different (build what differentiates, rent what does not), how much the requirements are likely to change (rent while they are unstable), and what the exit costs are (how hard is it to leave the vendor or to replace the home-grown system later).

The common error is to count only the first month's infrastructure and forget the engineer-months, in both directions: underestimating the cost of building and operating something home-grown, and underestimating the integration and workaround cost of a product that almost fits.

## Cost as a metric

The practice that makes cost tractable is to treat it like latency: measure it continuously, attribute it to the thing that causes it, and set a target.

*Attribute.* Tag every resource with the service, team and environment that owns it, so the bill can be broken down. Unattributed spend is spend nobody will reduce.

*Normalise.* The raw bill grows with the business and tells you little. Cost per unit of useful work (per thousand requests, per active user, per gigabyte processed, per model call that produced a used answer) separates growth from waste, and it is the number to put on the dashboard next to p99.

*Set a target and review it.* Like an SLO: a cost-per-unit target, a review when it is exceeded, and an explicit decision when a design change will move it. A design document that states the expected cost per unit, and is checked against the measured one after launch, is a document that produces engineers who can reason about cost.

## The question you will be asked

*"Cut this system's bill by 40% without changing its SLO."*

Start with the breakdown: which lines dominate (compute, storage, transfer, managed services, model calls)? Then the leaks, in order of likely size: idle and over-provisioned compute (right-size from utilisation data, schedule non-production environments, add autoscaling below the knee); commitment pricing for the steady baseline and interruptible capacity for batch and stateless work; storage lifecycle rules and deletion of what nobody reads; telemetry volume and cardinality; egress moved behind a CDN; the model-API line attacked with prompt caching, a smaller model for the easy cases and retry budgets. Say what you would measure before and after each change and how you would confirm the SLO held (chapter 9's burn rate, during and after). Then the honest part: 40% is usually available from idle capacity and storage alone in a system that has never been cost-reviewed, and it is not available at all in one that has, where the next 10% costs a redesign. Say which case you think this is and why.

## The trade-off, stated

Cost optimisation costs engineering time and sometimes latency, availability or flexibility; it buys money, which buys everything else, including the engineering time. The failure modes are symmetric: systems that were never cost-reviewed and leak half their bill, and systems optimised so aggressively that an engineer-week was spent to save a month of a small instance. The skill is in the model: know the lines, know the leaks, measure per unit, and spend the engineering time where the numbers say.

## Run this yourself

Take any system you have access to, including a personal project on a free tier, and produce a one-page cost model: every resource, its unit price from the provider's published rates, its measured or estimated utilisation, and its monthly cost, with the total broken down by line. Then compute cost per unit of useful work for one meaningful unit. Then list the three largest leaks you can see and estimate what closing each would save. If the system is on a free tier, find the cliff: the exact threshold at which the first bill arrives and what it would be at twice the current usage. The whole exercise takes an evening, and the ability to do it from a cold start, for a system you did not build, is a skill few engineers have and every employer values.

---

### Sources for this chapter
- Public pricing pages and pricing calculators of the major cloud providers (current versions) — the primary source for every unit price; rates change, so the method matters more than any figure quoted here.
- FinOps Foundation (2023–2025), *FinOps Framework* and the *State of FinOps* reports — the vocabulary of cloud cost management (attribution, unit economics, commitment management).
- Beyer et al. (2016), *Site Reliability Engineering*, chapter 18 — capacity and cost in planning.
- Gregg, B. (2020), *Systems Performance*, 2nd ed. — utilisation measurement, the input to right-sizing.
- a16z (Wang, S. & Casado, M., 2021), "The Cost of Cloud, a Trillion Dollar Paradox" — the argument that cloud costs can dominate at scale and the counter-arguments it provoked; read with its critics.
- Provider documentation on prompt caching and model pricing tiers (2024–2026) — the model-API cost line.
