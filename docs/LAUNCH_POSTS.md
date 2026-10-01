# Launch copy — one post per publication, spaced over October–November 2026

*Drafts for Pranjul Rathour's own accounts. Replace `<link>` with the store page or DOI once live. Post one at a time, a few days apart; the brand-engine's LinkedIn slot is 2/day with 45 s spacing, so one publication post per day at most, never a burst. Blogger gets the long version with figures. Tone: plain, specific, no hype; say "preprint" and "self-published" where true.*

## 1. Book — The AGI Transition: A Field Guide for the Next Decade

**LinkedIn (short)**
I have published a book.

*The AGI Transition: A Field Guide for the Next Decade* is not a book of predictions. It is twelve frameworks for reasoning about AI between now and 2036: how to read a capability claim, why automation has four economic effects and not one, what happens to the entry-level job, what replaces the essay as proof of learning, how the major jurisdictions are regulating, what agents change, which skills compound with the tools, and what the decade means for India.

Every chapter ends with "What would make this chapter wrong" and "What to do this year". Every number has a source and a year. Nothing depends on a product that could vanish.

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

Preprint: <DOI> · Code and data: github.com/Pranjulrathour/research/tree/main/papers/p1-fat-tails

**Blogger (long)**: abstract, Figures 2, 3 and 5 with captions, the Table 3 summary for 99%, the discarded-variant section, and the reproduction command.

## 4. Paper P2 — Machine-learning return predictors vs linear baselines

<!-- fill after results: lead with the honest-vs-leaky R² comparison and whether anything beat OLS -->

## 5. Paper P3 — Tail latency under load

<!-- fill after results: lead with the async-inline collapse on CPU work and the p99/p50 signatures -->

## 6. Paper P4 — Recall–latency frontiers of ANN indexes

<!-- fill after results: lead with the single-query vs batched gap and the recall knee -->

## 7. Paper P5 — Card-fraud detection under extreme imbalance

<!-- fill after results: lead with the leak inflation (random vs time-aware split) and the dummy's 99.83% accuracy -->

## Carousel material (Instagram / Threads / Facebook, via brand-engine)

- From Book 1, chapter 12: "Ten habits for the decade" — one habit per slide.
- From Book 1, Appendix A: "Ten questions to ask of any AI capability claim" — one per slide.
- From Book 2, chapter 12: "Twelve questions to ask of any system design" — one per slide.
- From P1: "Why your risk model is right at 95% and wrong at 99%" — Figure 2 and Figure 3 as slides.

## Wording rules (apply to every post)
- "preprint", "working paper", "self-published": yes. "Peer-reviewed", "published in": no.
- Name the venue (Preprints.org / SSRN / TechRxiv / Kindle / Leanpub / Google Play) rather than implying one.
- Link the code with every paper post; the reproducibility is the point.
- No AI-tool attribution in any post, matching the books and papers.
