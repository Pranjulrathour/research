# Launch copy — one post per publication, spaced over October–November 2026

*Drafts for Pranjul Rathour's own accounts. Replace `<link>` with the store page or DOI once live. Post one at a time, a few days apart; the brand-engine's LinkedIn slot is 2/day with 45 s spacing, so one publication post per day at most, never a burst. Blogger gets the long version with figures. Tone: plain, specific, no hype; say "preprint" and "self-published" where true.*

## 1. Book — The AGI Transition: A Field Guide for the Next Decade

**LinkedIn (short)**
I have published a book.

*The AGI Transition: A Field Guide for the Next Decade* is not a book of predictions. It is twelve frameworks for reasoning about AI between now and 2036: how to read a capability claim, why automation has four economic effects and not one, what happens to the entry-level job, what replaces the essay as proof of learning, how the major jurisdictions are regulating, what agents change, which skills compound with the tools, and what the decade means for India.

Every chapter ends with "What would make this chapter wrong" and "What to do this year". Every number has a source and a year. Nothing depends on a product that could vanish.

Running through it are nine stories from transitions we already know the end of: the telephone operators of the 1920s, the sixty-year pause in British wages, the horse, the scribes who argued against printing (in print), the dockworkers who negotiated for the container before it arrived, India's wheat and India's UPI, and seventy years of "twenty years away". Each with a chart drawn from the original numbers.

Written from Kanpur, for the students who kept asking me "what should I do now?"

Available on Kindle, Leanpub and Google Play: <link>

**Blogger (long)**: the preface, the contents, one full chapter (chapter 10, the skill portfolio) and the store links. Title: "I wrote a field guide for the next decade of AI. Here is chapter 10, free."

## 2. Book — Systems That Scale

**LinkedIn (short)**
My second book is out.

*Systems That Scale: The Engineering Judgment Behind Reliable, Low-Latency Software* teaches system design through measurement rather than opinion. Twelve principles: latency is a distribution; what blocks what; caching; data structures at scale; consistency; replication and the two hard problems; failure as the normal case; queues; observability; capacity; cost; and how to make and document a design decision.

Each chapter states the principle, shows it with a number you can reproduce (the benchmark code is public), names the trade-off, and ends with the question an interviewer or an incident review will ask you, plus an experiment you can run in an afternoon.

Companion code and measurements: github.com/Pranjulrathour/research
Available on Kindle, Leanpub and Google Play: <link>

**Blogger (long)**: the preface, the twelve closing questions from chapter 12, and the two benchmark figures from chapters 1 and 4.

## 3. Paper P1 — Fat tails and the failure of Gaussian risk models

**LinkedIn**
New preprint: *Fat Tails and the Failure of Gaussian Risk Models: Out-of-Sample Value-at-Risk Evidence from NIFTY 50 and S&P 500, 2010–2026*.

Three findings from 16.75 years of daily data, all out of sample, all reproducible with one command:

1. Gaussian one-day VaR is fine at 95% and fails at 99%: 57 violations against 36 expected on NIFTY 50, 89 against 37 on S&P 500. The normal distribution matches returns to about 2σ and departs sharply beyond 3σ; 95% VaR sits inside that range, 99% outside it.

2. Fat tails and volatility clustering are different problems, and standard backtests separate them. An unconditional Student-t fixes coverage but not clustering; EWMA volatility fixes clustering but not coverage. You need both.

3. Filtered historical simulation was the only model to pass conditional coverage at 95% on both indices. At 99% on the S&P 500, nothing passed independence, because of March 2020.

One more thing I kept in the paper on purpose: a model specification of mine that failed, and why. The raw-return Student-t degrees of freedom (2.8 for the S&P) mostly measure volatility clustering, not tail thickness; reuse them inside a volatility model and you double-count.

Preprint: <DOI> · Code: github.com/Pranjulrathour/research/tree/main/papers/p1-fat-tails

**Blogger (long)**: abstract, Figures 2, 3 and 5 with captions, the Table 3 summary for 99%, the discarded-variant section, and the reproduction command.

## 4. Paper P2 — Machine-learning return predictors vs linear baselines

**LinkedIn**
New preprint: *Do Machine-Learning Return Predictors Beat Linear Baselines Out of Sample? A Small-Scale Walk-Forward Replication on Public Equity Data*.

The famous result is that trees and neural networks beat linear models at predicting stock returns. It was found on about 30,000 stocks. I tested it on the 29 Dow stocks with complete histories, walk-forward from 2012 to 2026, tuning only on past data.

What I found:

1. Nothing beat the historical average. The best model, lasso, had quietly shrunk itself into that average: its forecasts barely differed from stock to stock.

2. Random forest, gradient boosting and a neural network were all significantly worse than plain OLS. Validation kept choosing the most constrained version of every model, year after year.

3. Then I evaluated the same models the wrong way, with shuffled cross-validation. The tree models jumped from below zero to 13–16% R². That gain comes entirely from the shared monthly part of returns: shuffle a panel and a tree can work out which month it is looking at, then read off what the other stocks did that month.

Small data, honest protocol, negative result, and a very clear picture of how a leak manufactures skill.

Preprint: <DOI> · Code: github.com/Pranjulrathour/research/tree/main/papers/p2-ml-returns

**Blogger (long)**: abstract, Figure 1 (the protocol), Table 2, Figure 4 (honest vs shuffled R²), the section "The leak, measured", and the reproduction command.

## 5. Paper P3 — Tail latency under load

**LinkedIn**
New preprint: *Tail Latency Under Load: An Empirical Comparison of Threaded, Event-Loop and Hybrid API Server Designs*.

I wrote four tiny Python servers that differ only in how they handle concurrency, hit each with the same load on three workloads, and recorded every request's latency.

The result I keep coming back to: at 256 clients on CPU-bound work, the thread-per-connection server and the single-threaded event loop did the same amount of work (116 vs 152 requests a second) with the same median. Their p99s were 8.2 seconds and 2.2 seconds, and the threaded server's worst request took 16.7 seconds. Same capacity, four times the tail. The event loop serves requests in order; 256 threads fighting for the interpreter lock are scheduled with no fairness at all.

Two more:

1. Moving CPU work to a thread pool, which every async framework recommends, kept the loop responsive and bought zero throughput under the lock.

2. The process pool paid about 4.7 ms per hand-off, more than the 2.8 ms of work it carried, then doubled throughput and quartered the tail, then plateaued at about one core's worth, because the dispatcher is serial.

One number to put on a dashboard: p99 divided by p50 at full load. Every event-loop design: 1.2 to 1.6. Threads: 3.1 to 5.4.

Preprint: <DOI> · Code: github.com/Pranjulrathour/research/tree/main/papers/p3-tail-latency

**Blogger (long)**: abstract, Figure 1 (how each design spends a request's time), Figure 2 (p99 vs concurrency), Table 3, the fairness discussion, the failed first run (a listen backlog of five), and the reproduction command.

## 6. Paper P4 — Recall–latency frontiers of ANN indexes

<!-- fill after results: lead with the single-query vs batched gap and the recall knee -->

## 7. Paper P5 — Card-fraud detection under extreme imbalance

**LinkedIn**
New preprint: *Card-Fraud Detection Under Extreme Class Imbalance: A Time-Aware, Cost-Sensitive Benchmark on Public Data*.

On the public ULB credit-card data (284,807 transactions, 492 frauds), a model that flags nothing is 99.87% accurate. So I ranked seven models by precision–recall area instead, trained on the past and tested on the future, and chose every decision threshold on held-out data under a cost model.

What I found:

1. A random forest with balanced class weights won (PR-AUC 0.811) and recovered 68% of the largest possible saving. ROC-AUC would have picked a different, weaker model.

2. Class weighting improved every model's ranking and wrecked the calibration of two of them. Weighted scores aren't probabilities until you recalibrate them.

3. Plain gradient boosting was a lottery across seeds (PR-AUC 0.50 ± 0.12). The cause was a library default: early stopping on a random holdout of about 38 frauds. With it off, every seed gives the same model.

4. The result I expected didn't happen. A random train/test split didn't inflate performance here, because two days of data barely drift. I reported that rather than hiding it, and I still split by time, because you can't know the drift in advance.

Preprint: <DOI> · Code: github.com/Pranjulrathour/research/tree/main/papers/p5-fraud-imbalance

**Blogger (long)**: abstract, Figure 1 (the split drawn on the real data), Table 2, Figure 2, the early-stopping table (Table 3), the section "The leak that didn't appear", and the reproduction command.

## Carousel material (Instagram / Threads / Facebook, via brand-engine)

- From Book 1, chapter 12: "Ten habits for the decade" — one habit per slide.
- From Book 1, Appendix A: "Ten questions to ask of any AI capability claim" — one per slide.
- From Book 2, chapter 12: "Twelve questions to ask of any system design" — one per slide.
- From P1: "Why your risk model is right at 95% and wrong at 99%" — Figures 3 and 4 (the exceedance ratios and the 99% violation counts) as slides.
- From P5: "99.87% accurate and useless" — the accuracy paradox, then Figure 2 and the early-stopping table.

## Wording rules (apply to every post)
- "preprint", "working paper", "self-published": yes. "Peer-reviewed", "published in": no.
- Name the venue (Preprints.org / SSRN / TechRxiv / Kindle / Leanpub / Google Play) rather than implying one.
- Link the code with every paper post; the reproducibility is the point.
- Don't name tools in posts. Each paper's Declarations carries the AI-use disclosure the venues require, so never claim in a post that the work was done without AI help.
