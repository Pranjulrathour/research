# P1 — Defence notes
## Fat tails and the failure of Gaussian risk models: NIFTY 50 and S&P 500, 2010–2026

*Private preparation notes for talking about this paper in an interview, a workshop or a review. Not part of the manuscript.*

## The three findings, in one breath each

1. **Gaussian VaR is fine at 95% and fails at 99%.** 57 violations against 36 expected on NIFTY 50; 89 against 37 on S&P 500. The normal distribution matches the data out to about 2σ and departs sharply beyond 3σ; 95% VaR sits at 1.65σ, 99% at 2.33σ. Validating at 95% and using at 99% is validating where the model works and applying it where it does not.

2. **Fat tails and volatility clustering are different problems, and the backtests separate them.** The Kupiec coverage test at 99% diagnoses tails; the Christoffersen independence test diagnoses clustering. Unconditional Student-t fixes coverage but not clustering; EWMA-Gaussian fixes clustering but not coverage. You need both.

3. **Filtered historical simulation is the only model that passes conditional coverage at 95% on both indices (p = 0.50, 0.98) and at 99% on NIFTY 50 (p = 0.25).** Nothing passes independence at 99% on the S&P 500, because of five violations in a few weeks of March 2020.

Bonus finding to volunteer if there is time: **the unconditional degrees of freedom (2.8 for S&P 500) mostly measure volatility clustering, not tail thickness.** Standardise by EWMA volatility and the fitted df rises to 4.7 and stops hitting 2. Reusing the raw df inside a volatility model double-counts and fails badly (317 violations against 186 expected). I kept that failed variant in the results on purpose.

## The method in sixty seconds

Daily log returns, 2010–2026, from Yahoo Finance via yfinance, snapshot committed. Rolling 500-day window, re-estimated every day, forecast strictly for the next day. Six models, nothing tuned (textbook window, textbook λ = 0.94). Kupiec and Christoffersen tests. Everything runs with one command in about ten minutes; every number in the paper is in `results.json`.

## Questions I expect, and answers

**"Why not GARCH?"** Because the paper's point is the separation of two effects with the simplest possible instruments, and EWMA is GARCH(1,1) with the parameters fixed at the RiskMetrics defaults. GARCH would likely improve models 4–6 a little; it would also introduce estimation choices that a sceptic could call tuning. I say in the limitations that GARCH is the natural next step.

**"Why not Expected Shortfall? Basel moved to ES in 2016/2019."** Correct, and ES backtesting is genuinely harder (it is not elicitable on its own; the standard approaches backtest VaR at multiple levels or use the Acerbi–Székely tests). It was out of scope and pre-specified as such. The "mean excess loss on violation days" column is the descriptive stand-in and it already shows the EWMA-based models lose less when they are wrong.

**"Isn't this well known?"** Yes, since Mandelbrot 1963 and in the VaR-comparison literature since the late 1990s (Kuester, Mittnik & Paolella 2006 is the standard reference). The contribution is a clean, current, reproducible demonstration on an Indian index alongside a US one, including 2020, 2022 and 2025, with a design a student can check. I am not claiming novelty of the phenomenon; I am claiming a careful measurement of it.

**"Your independence test rejects everything at 99% on S&P. Doesn't that mean your best model fails?"** At 99% on the S&P 500, yes, FHS has correct coverage (46 vs 37) but its violations cluster in March 2020. The Christoffersen test is first-order Markov and one run of consecutive violations is enough to reject. Two honest readings: either no simple daily model handles a liquidity crash of that speed, or the test is too sensitive to a single episode. I report both and did not switch tests after the fact, because that would be tuning the test to the result.

**"Why did your fifth model fail? Doesn't that mean you made a mistake?"** I did make a specification error and I documented it rather than hiding it. The lesson is substantive: a Student-t fitted to raw returns has low df because it is absorbing volatility regimes; put that df inside a model that already removes volatility regimes and you double-count, and the unit-variance scaling collapses the quantile when df is near 2. The fix (fit the t to standardised returns) is what a GARCH-t does, and it works. The failed variant is in `results.json` under `discarded_variants`.

**"Survivorship or look-ahead bias?"** Index levels, no constituents, so no survivorship. Every forecast uses only the window ending the previous day; the EWMA recursion uses only past returns; the one in-sample element is the EWMA variance initialisation at day zero (set to the first window's variance), which affects one standardised observation in the first window only.

**"Why Yahoo Finance?"** Free, public, reproducible by anyone, and the standard for independent work. The official closes from NSE and S&P DJI would differ, if at all, in the fourth decimal of a daily return.

**"What would you do next?"** Three things: GARCH(1,1)-t volatility to see how much the filtered models improve; Expected Shortfall backtests; and a broader cross-section (individual large-cap stocks, a bond index, a currency) to see whether the 95%-fine/99%-fails pattern generalises.

**"How does this connect to the job?"** Risk measurement is a backtesting discipline: specify, forecast out of sample, test, report failures. That is the same discipline as evaluating any model in production (define the metric before looking, hold out properly, report where it breaks). The paper is a small demonstration that I do this by habit, including when the result embarrasses my own first specification.

## Numbers to have memorised

- Excess kurtosis ≈ 13.3 and 13.5; skew −0.88 and −0.61.
- >4σ days: 17 and 28 observed vs 0.26 and 0.27 expected (65× and 105×). >5σ: 10 and 12 vs 0.002.
- Full-sample t df: 4.06 (NIFTY), 2.78 (S&P). Standardised rolling median df: 6.5 and 4.7.
- 99% Gaussian: 57/36 and 89/37. 99% FHS: 46/36 (CC p = 0.25) and 46/37 (UC p = 0.16, IND p = 0.002).
- 95% FHS CC p = 0.50 and 0.98.
- Discarded variant at 95%: 273/181 and 317/186.
- Worst days: NIFTY −13.9% (23 Mar 2020); S&P −12.8% (16 Mar 2020). Best S&P day +9.1% (9 Apr 2025).
- 3,613 and 3,711 forecast days; forecasts begin Jan 2012 / Dec 2011.

## Where everything is

`papers/p1-fat-tails/analysis.py` (method, fixed design, revision record in the docstring), `results.json` (all numbers), `figures/fig1–fig5`, `data/SNAPSHOT.json` (provenance), `paper.md` (manuscript).
