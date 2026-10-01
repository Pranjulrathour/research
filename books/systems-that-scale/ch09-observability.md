# Chapter 9 — Observability: you cannot fix what you cannot see

Every chapter so far has ended by telling you to measure something, and the measurement has been a tool for the exercise. In production, measurement is the product: a system that cannot report what it is doing is a system that is debugged by guessing, and guessing is slow, expensive and usually wrong. The engineer who can look at an unfamiliar system under incident and say, within minutes, where the time is going and what changed is doing something that looks like intuition and is in fact a practised use of three kinds of data and one organising idea.

This chapter is about those three kinds of data (logs, metrics, traces), the idea that turns them into a decision rule (service-level objectives and error budgets), and the discipline of alerting on what users feel rather than on what machines do.

## The principle

**Instrument so that any question about the system's behaviour can be answered from data that already exists. Define reliability as a number users would recognise, set a target, and let the gap between target and reality decide what the team works on.**

## Three kinds of data

**Logs** are records of discrete events: a request arrived, a query ran, an error occurred. They are the oldest form of telemetry and the one every engineer reaches for first. Their strength is detail: a log line can carry anything. Their weaknesses are volume (a busy service emits millions of lines an hour, and storage and search cost money), and the difficulty of aggregating free text into a picture. Two practices fix most of the weakness. *Structured logging*: emit key–value records (JSON or similar), not sentences, so that every field can be filtered and counted. And *log with intent*: every line should answer a question somebody will ask; "entering function" answers none.

**Metrics** are numbers aggregated over time: requests per second, p99 latency, error rate, queue depth, CPU. They are cheap to store (a time series is a few bytes per interval regardless of traffic), fast to query, and the natural material for dashboards and alerts. Their weakness is that aggregation destroys detail: a metric tells you that p99 rose; it cannot tell you which requests, from which users, for what reason. The four metrics that describe almost any service are latency (as a distribution, chapter 1), traffic (rate), errors (rate, by type) and saturation (how full the constraining resource is); the SRE literature calls these the golden signals, and a dashboard that shows them for each service and each dependency is the one you want at 3 a.m.[^1]

A note on *cardinality*. Metrics are indexed by labels (service, endpoint, status code, region). Each distinct combination of label values is a separate time series, and the cost of a metrics system scales with the number of series. A label with unbounded values (user ID, request ID, full URL) multiplies the series count without bound and is the classic way to make a monitoring system fall over. Metrics carry low-cardinality dimensions; high-cardinality detail belongs in traces and logs.

**Traces** follow one request through every service it touches, recording the time spent in each. A trace is a tree of *spans*, each a timed operation with a name and attributes, linked by a *trace ID* that travels with the request in a header. Traces are the only one of the three that answers "where did the time go for *this* request?" across service boundaries, which makes them the primary tool for latency debugging in any system with more than one service.[^2] Their cost is volume (one trace per request is a great deal of data), which is managed by *sampling*: keep a fraction of all traces, plus every trace that was slow or failed (tail-based sampling), so the interesting ones are always there.

The organising idea that connects the three is the **request identifier**. Assign every incoming request an ID at the edge; propagate it in every call, every log line, every span. Then a slow request found in a trace can be matched to its log lines, a spike in a metric can be drilled into the traces that caused it, and an error in a log can be placed in the request that produced it. Systems without a propagated request ID can still be debugged, slowly; systems with one can be debugged by following a thread. The OpenTelemetry project, which unified the earlier competing standards from about 2019, provides the vocabulary and the libraries for all three signals and the propagation between them, and it is the default to reach for in 2026.[^3]

## From data to decisions: SLIs, SLOs and error budgets

Having the data does not tell you what to do with it. A service emits a hundred metrics; which ones matter, how good is good enough, and when should the team stop building features and fix reliability? The framework that answers these questions was articulated by Google's SRE organisation and has become standard.[^4]

A **service-level indicator (SLI)** is a measurement of one aspect of the service that users care about, expressed as a ratio: the fraction of requests that succeeded, the fraction that completed under 300 ms, the fraction of time the service was reachable. Good SLIs are measured as close to the user as possible, because the user's experience is the thing being promised; a server that reports success while the load balancer in front of it drops requests has a misleading SLI.

A **service-level objective (SLO)** is a target for an SLI over a window: 99.9% of requests succeed, measured over 30 days; 99% of requests complete under 300 ms. The target is a product decision as much as an engineering one: it should be what users need, not what the system happens to achieve, and it should be below 100%, because 100% is infinitely expensive and users cannot tell the difference between 99.99% and 99.999% through a network that is itself less reliable than either.

An **error budget** is the complement of the SLO: at 99.9% over 30 days, the service may fail 0.1% of requests, roughly 43 minutes of total unavailability, before it has broken its promise. The budget is a quantity that can be spent, and that is the point. While budget remains, the team ships features, runs experiments, takes risks. When the budget is exhausted, the team stops shipping and works on reliability until the window rolls the budget back. The rule converts an endless argument (reliability versus velocity) into arithmetic, and it gives both sides a number they agreed to in advance.

Three practices make the framework work rather than decorate a slide.

*Few SLOs, well chosen.* Two or three per service: availability, latency at one or two percentiles, perhaps correctness or freshness for data services. A service with twenty SLOs has none.

*Burn-rate alerting.* Alert not on the SLI's instantaneous value but on how fast the budget is being consumed. A burn rate of 1 consumes exactly the budget over the window; a burn rate of 10 exhausts it in a tenth of the window. Alert urgently on a high burn rate over a short period (something is badly wrong now) and gently on a moderate burn rate over a long period (we are slowly failing the month). This replaces threshold alerts that fire on every blip with alerts that fire when the promise is actually at risk.[^5]

*Review the SLO, not only the system.* If the budget is never spent, the SLO may be too loose or the team too cautious; if it is always spent, the target may be unrealistic for the architecture, and that is a design conversation, not a firefighting one.

## Alerting: symptoms, not causes

A page at 3 a.m. should mean a human must act now. Most pages do not meet that bar, and the result is *alert fatigue*: the on-call engineer learns that pages are usually noise, responds slowly, and misses the one that mattered.

The cure is to alert on **symptoms**, the things users experience (error rate, latency SLO burn, unavailability), and to treat **causes** (CPU high, disk filling, a dependency slow, a queue growing) as diagnostics to look at once a symptom has fired. A high CPU that is not affecting users is not an emergency; a user-facing error rate is, whatever the CPU says. Cause-based alerts have their place as *tickets* (fix this disk before it fills, next business day) rather than pages.

Three more rules from the on-call trenches. Every page must be actionable: if the right response is "wait and see", it is not a page. Every page must link to a runbook that says what to check and what to do. And every page should be reviewed afterwards: did it need a human, did the runbook work, and if the answer to either is no, change the alert.

## What this costs

Observability has a bill and the bill surprises people. Logs are the largest line, because volume is proportional to traffic and retention is measured in weeks; the fix is structure (so fewer lines carry more), sampling of high-volume debug logs, and tiered retention (hot for days, cold for months). Metrics are cheap until cardinality explodes; the fix is discipline about labels. Traces are expensive per request and cheap per insight; the fix is sampling that keeps the slow and failed ones. A reasonable budget for telemetry in a mature system is a noticeable fraction of the compute bill, and it is money well spent exactly in proportion to how often it shortens an incident. Chapter 11 returns to the cost side.

## The question you will be asked

*"Define an SLO for a search API and say what you would do when the budget is spent."*

Choose two SLIs: availability (fraction of requests returning a non-error response, measured at the load balancer) and latency (fraction of successful requests completing under, say, 500 ms, because search users abandon beyond about a second and the page has other work to do). Set targets: 99.9% availability and 99% under 500 ms, over 30 days, and say why those and not higher (the budget they imply, the cost of the next nine). Say how you measure (at the edge, not the server; excluding health checks; including timeouts as failures). Define burn-rate alerts: page on a burn that would exhaust the budget in two days, ticket on one that would exhaust it in two weeks. Then the budget is spent: the team freezes feature launches, the on-call lead opens an investigation (which requests, which queries, which dependency: traces first), the team fixes the dominant cause, and the SLO review asks whether the target was right. An answer that stops at "99.9%" without the measurement point, the burn-rate alerts and the policy for a spent budget is an answer that has read about SLOs but not run one.

## The trade-off, stated

Instrumentation costs engineering time, runtime overhead (small but not zero), storage and tooling. It buys the ability to answer questions about the system from existing data, which is the difference between an incident that lasts fifteen minutes and one that lasts four hours, and between a performance regression caught at the canary and one caught by a customer. SLOs cost a hard conversation about how reliable the service needs to be. They buy the end of the argument about whether to fix reliability or ship features, because the budget decides. Neither is optional for a system that matters; the only question is whether you build them before or after the incident that proves you needed them.

## Run this yourself

Take the service from chapter 1's harness and add three things: a request ID generated at the entry point and included in every log line; structured JSON logs with the request ID, endpoint, status and duration; and a histogram metric of request duration labelled by endpoint and status (and nothing of higher cardinality). Run the load generator. Then, without looking at the harness output, answer three questions from your telemetry alone: what is the p99 for each endpoint; which single request was the slowest in the last minute and what did it do; and how many requests failed and why. If you can answer all three in under five minutes, your instrumentation is adequate. If you cannot, you have found the gap before an incident did. Then define one SLO for the service and compute its error budget for the run; you will find that the number makes the latency conversation concrete in a way that the raw percentiles did not.

---

[^1]: Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016), *Site Reliability Engineering*, O'Reilly, chapter 6, "Monitoring Distributed Systems" — the four golden signals.
[^2]: Sigelman, B. H. et al. (2010), "Dapper, a Large-Scale Distributed Systems Tracing Infrastructure", Google Technical Report — the design most tracing systems descend from.
[^3]: OpenTelemetry specification and documentation, opentelemetry.io; the project merged OpenTracing and OpenCensus in 2019.
[^4]: Beyer et al. (2016), chapter 4, "Service Level Objectives"; Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K. & Thorne, S. (eds.) (2018), *The Site Reliability Workbook*, O'Reilly, chapter 2, "Implementing SLOs".
[^5]: Beyer et al. (2018), *The Site Reliability Workbook*, chapter 5, "Alerting on SLOs" — the multi-window, multi-burn-rate method.

### Sources for this chapter
- Beyer et al. (2016), *Site Reliability Engineering*, chapters 4, 6, 10 and 11.
- Beyer et al. (2018), *The Site Reliability Workbook*, chapters 2, 3 and 5.
- Sigelman et al. (2010) — Dapper.
- OpenTelemetry documentation — signals, context propagation, sampling.
- Majors, C., Fong-Jones, L. & Miranda, G. (2022), *Observability Engineering*, O'Reilly — the case for high-cardinality event data and tracing-first debugging.
- Dean & Barroso (2013), "The Tail at Scale", *CACM* 56(2) — why the tail is what you instrument for.
