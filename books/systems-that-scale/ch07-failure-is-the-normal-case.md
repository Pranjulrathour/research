# Chapter 7 — Failure is the normal case

On a large enough system, something is always broken. A disk is failing, a network link is flapping, a dependency is slow, a deployment is half-rolled, a certificate is about to expire. The engineering question is never whether the system has failures; it is whether the failures it has are the ones it was designed to survive. Systems that treat failure as exceptional fall over when it arrives. Systems that treat it as the normal case are built from parts that each assume the others will misbehave, and they bend rather than break.

This chapter is about the small set of mechanisms that make a system tolerant of the failures it will certainly have, the way those mechanisms themselves fail when misused, and the practice of finding out, on purpose, how a system breaks before it does so on its own.

## The principle

**Every dependency will fail, be slow, or return garbage. Decide in advance what your system does in each case, bound how long it waits, limit how hard it retries, and practise the failure before it happens.**

## The arithmetic of many parts

A service that depends on ten others, each available 99.9 per cent of the time, is available at most 99.9¹⁰ ≈ 99.0 per cent of the time if every dependency is required for every request: about 7 hours of downtime a month, from parts that each promised under an hour. Availability multiplies down. The only ways to beat the arithmetic are to depend on fewer things, to make dependencies optional (degrade when they fail rather than failing with them), or to make them redundant (two independent paths). All three are design decisions and none of them can be added by a configuration flag afterwards.

The same arithmetic in time rather than probability: if one dependency's latency goes from 20 ms to 2 s, every request that waits for it goes to 2 s, every thread or connection holding that request is tied up a hundred times longer, and the service's capacity falls by a hundred times. Chapter 2's blocking argument becomes an outage. The dependency did not fail; it slowed down, and the caller had not decided what to do about that.

## Timeouts: deciding how long to wait

A call without a timeout is a promise to wait forever, and forever is how long a hung connection can last. Every outbound call has a timeout, and the timeout is chosen, not defaulted.

Chosen how? From the latency budget (chapter 1). If the caller must respond in 200 ms and has 150 ms left when it calls a dependency whose p99 is 40 ms, a timeout of 100 ms is reasonable: well above the dependency's normal tail, well inside what the caller can afford. A timeout of 30 s, the default in many client libraries, is not a timeout; it is a way of discovering the problem from the users.

Two refinements. *Deadlines propagate*: pass the remaining budget downstream, so a dependency does not spend 100 ms on work the caller has already given up on. *Timeouts are not retries*: a timed-out request may have succeeded on the other side (chapter 6's first hard problem), and what happens next must be decided with that in mind.

## Retries: the mechanism that takes down healthy systems

Retrying a failed call is correct for transient failures (a dropped packet, a brief overload, a node mid-restart) and catastrophic for persistent ones. Here is the mechanism. A dependency slows under load. Callers time out and retry. The dependency now receives the original load plus the retries, slows further, and more callers time out and retry. Within seconds the dependency is receiving several times its capacity, almost all of it retries of work it is already struggling with, and it cannot recover because the load does not fall when it tries. This is a *retry storm*, and it has caused a large share of the famous outages of the past fifteen years, including several at the largest cloud providers.[^1]

The disciplines that prevent it are few and non-negotiable.

*Bounded retries.* A small fixed number (usually one to three), never unbounded.

*Exponential backoff with jitter.* Wait before retrying, wait longer each time, and randomise the wait so that a thousand callers who failed together do not retry together.[^2] Without jitter, backoff just synchronises the storm into waves.

*Retry budgets.* Cap retries as a fraction of total requests (say 10 per cent) across the whole client, so that when the failure rate is high, retries are shed rather than multiplied. This is the single most effective defence and the least commonly implemented.

*Retry only what is safe.* Idempotent operations (chapter 6), and only on errors that indicate the request did not get through. Never retry a request that returned "invalid"; it will be invalid again.

*Retry at one layer.* If the client retries, the proxy retries, and the service retries its own dependency, one failure becomes 3 × 3 × 3 = 27 attempts. Decide where retries live and make the other layers pass failures through.

## Circuit breakers and bulkheads

A *circuit breaker* wraps a dependency and counts failures. When failures exceed a threshold in a window, the breaker *opens*: calls fail immediately without being attempted, for a cooling period, after which a trial call tests whether the dependency has recovered. The point is twofold: the caller stops wasting its own capacity on calls that will fail, and the dependency gets the drop in load it needs to recover.[^3] A breaker is the automated version of a human noticing "that service is down, stop calling it" and it does so in milliseconds rather than minutes.

A *bulkhead* isolates resources per dependency, so that one slow dependency cannot consume every thread, connection or queue slot and starve the calls to healthy ones. The name is from ship design: compartments that contain flooding. In practice it means separate connection pools and concurrency limits per downstream, sized from each one's expected load, so that the failure of the recommendations service does not take down checkout because both were sharing one pool.

Together with timeouts and bounded retries, these four are the standard kit. Most mature service frameworks and service meshes provide all four; the engineering is in configuring them from the latency budget and the dependency map rather than accepting defaults.

## Graceful degradation: deciding what to drop

When a dependency is unavailable, the service has three options, and the one it takes should have been chosen in advance.

*Fail the request.* Correct when the dependency is essential (payment authorisation for a purchase).

*Degrade.* Serve without the dependency's contribution: a product page without recommendations, a feed from cache, search without personalisation. Correct when the dependency is an enhancement, and the user is better served by a slightly worse page than by an error. Degradation has to be designed: the code path that renders without recommendations has to exist and be tested, or the first time it runs will be during the outage.

*Fall back.* Use an alternative: a secondary provider, a stale cache, a default value. Correct when the alternative is genuinely acceptable and has been tested under realistic conditions; a fallback that has never run is a second outage waiting behind the first.

The design artefact is a table: every dependency, what happens when it fails, what happens when it is slow, and who decided. Most systems do not have this table, and their behaviour under failure is whatever the code happens to do, which is usually to wait and then fail.

## Load shedding: saying no on purpose

Chapter 2 made the case for bounded queues. The generalisation is *load shedding*: when the system is beyond capacity, reject some requests quickly rather than serving all of them slowly, because serving all of them slowly serves none of them within the budget and often leads to collapse. Shed by priority (health checks and payments before analytics), shed by cost (expensive queries first), shed early (at the edge, before work is done), and return an explicit "overloaded, retry after" so that well-behaved clients back off. A system that sheds load at 110 per cent of capacity stays up; one that accepts everything falls over at 120 and recovers slowly, because the backlog has to drain first.

## Finding out on purpose

Everything above is a hypothesis about how the system behaves under failure until it has been tested under failure. The practice of testing it, deliberately, in production or in a faithful copy, is *chaos engineering*, and it has moved in fifteen years from a provocative idea to standard practice at large operators.[^4]

The method is experimental. State a hypothesis ("if the recommendations service is unavailable, product pages render in under 300 ms without recommendations and error rate stays flat"). Inject the failure (kill the instances, add latency, drop the network) in a controlled scope. Measure. If the hypothesis holds, the system is as resilient as designed; if not, you have found the gap in a controlled setting rather than in an incident. Start small (one instance, in a test environment, during the day, with a hand on the abort switch) and expand as confidence grows.

A *game day* is the human-scale version: a planned exercise in which a team responds to a simulated failure, following its runbooks, with the goals of finding gaps in both the system and the response. The runbook that has never been run is as untested as the fallback that has never run.

## Learning from the ones you did not plan

Incidents happen anyway. The practice that turns them into resilience is the *blameless post-mortem*: a written account of what happened, in sequence, with times; what the impact was; what the contributing causes were; and what will change, with owners and dates.[^5] Blameless because the goal is the system's behaviour, not the person's, and because people who expect blame hide information.

Two habits make post-mortems useful. Ask "why" more than once: the outage was caused by a bad deployment, which happened because the canary did not catch it, because the canary measured only errors and not latency, because nobody had decided what the canary should measure. Each "why" is a different fix, and the deep ones prevent whole classes of incident. And track the actions to completion: a post-mortem whose action items are never done is a document, not a practice.

## The question you will be asked

*"Your dependency's latency doubled. What happens to your service in the next 60 seconds?"*

Walk it through. In the first second: requests in flight to that dependency take twice as long, the threads or connections they hold are tied up twice as long, and the pool for that dependency starts to fill. By ten seconds: if there is no bulkhead, the shared pool is full and *unrelated* requests begin to queue; if there is no timeout tighter than the new latency, nothing has failed yet, which is worse, because nothing has been shed. By twenty seconds: queues are growing, latency is rising for everything, and clients upstream of you have begun to time out and retry, so your incoming load is rising just as your capacity has fallen. By sixty seconds, without the kit, you are the outage. With it: the timeout fires at the budgeted point and the request degrades or fails fast; the bulkhead keeps the other dependencies' paths clear; the breaker opens after the threshold and stops the bleeding; retry budgets cap what upstream can send; and load shedding rejects the excess with a clear signal. Then say how you would see it: the dependency's p99, the pool saturation, the breaker state, the shed count, on a dashboard, with an alert on the first.

## The trade-off, stated

Resilience costs latency (timeouts shorter than the dependency's worst case mean some good requests fail), capacity (bulkheads reserve resources that are often idle), complexity (more configuration, more states, more things to get wrong) and engineering time (degradation paths, chaos experiments, post-mortems). It buys a system whose behaviour under failure is known and bounded. For a system that matters, the trade is not optional; the only choice is whether to pay before or after the incident.

## Run this yourself

Take the two-service setup from chapter 2's exercise, with a bounded concurrency on the upstream. Add a dependency call with a 30-second default timeout and no retry limit, and inject 2 seconds of latency into the dependency. Watch the upstream's p99 and throughput collapse within a minute. Then, one at a time, add a 200 ms timeout, three retries with exponential backoff and jitter, a retry budget of 10 per cent, a per-dependency concurrency limit, and a circuit breaker with a 50 per cent failure threshold over ten seconds. Measure after each. You will see each mechanism's contribution, and you will see the retry storm happen when you add retries before the budget: throughput to the dependency *rises* as it slows. That observation, made once with your own harness, is worth more than this chapter.

---

[^1]: Among the public post-mortems that describe retry amplification: Amazon Web Services, "Summary of the Amazon DynamoDB Service Disruption and Related Impacts in the US-East Region", September 2015; and the AWS Kinesis event of November 2020. Both are worth reading in full as examples of the genre.
[^2]: Brooker, M. (2015), "Exponential Backoff And Jitter", AWS Architecture Blog, March 2015 — the clearest demonstration that jitter, not backoff, is what prevents synchronised retries.
[^3]: Nygard, M. T. (2007; 2nd ed. 2018), *Release It! Design and Deploy Production-Ready Software*, Pragmatic Bookshelf — the book that named circuit breakers and bulkheads as software patterns.
[^4]: Basiri, A. et al. (2016), "Chaos Engineering", *IEEE Software* 33(3) — the Netflix team's statement of the discipline; principlesofchaos.org.
[^5]: Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016), *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly, chapter 15, "Postmortem Culture: Learning from Failure".

### Sources for this chapter
- Nygard (2007/2018), *Release It!* — stability patterns.
- Beyer et al. (2016), *Site Reliability Engineering*, chapters 21–22 (handling overload, addressing cascading failures) and 15 (post-mortems).
- Brooker (2015) — backoff and jitter; Brooker, M. (2022), "Fixing retries with token buckets and circuit breakers", marcbrooker.com — retry budgets.
- Basiri et al. (2016) — chaos engineering.
- AWS post-event summaries (2015, 2020) — retry amplification in the wild.
- Dean, J. & Barroso, L. A. (2013), "The Tail at Scale", *CACM* 56(2) — hedged requests and other tail-tolerance techniques.
