---
title: "Do Machine-Learning Return Predictors Beat Linear Baselines Out of Sample? A Small-Scale Walk-Forward Replication on Public Equity Data"
author: "Pranjul Rathour"
affiliation: "Independent researcher, Kanpur, India · pranjulrathour41@gmail.com · https://pranjulrathour.scult.in"
date: "October 2026"
keywords: "return predictability, machine learning, walk-forward validation, out-of-sample R-squared, look-ahead bias, Diebold-Mariano, long-short portfolio, Dow Jones Industrial Average"
jel: "C45, C53, G11, G17"
---

## Abstract

A widely cited result in empirical asset pricing is that tree ensembles and neural networks outperform linear models in predicting the cross-section of stock returns out of sample. The result was established on a universe of tens of thousands of US stocks with nearly a thousand predictors, data and compute beyond most independent researchers. This paper asks whether the ranking survives at the scale an individual can reproduce: 29 Dow Jones constituents with complete price history, ten standard price-based features, monthly horizon, 2005–2026. Six models (OLS, ridge, lasso, random forest, gradient boosting, a small neural network) are evaluated under a strict walk-forward protocol: train on all data to the end of year *Y*−1, select hyperparameters on the last 24 months of that window, test on year *Y*, for *Y* = 2012 to 2026. Metrics are pooled out-of-sample R² against a zero forecast, directional accuracy, a Diebold–Mariano test of each model against OLS, and a monthly long-short portfolio's Sharpe ratio with a block-bootstrap interval. The same models are then evaluated with shuffled five-fold cross-validation, the wrong way, to quantify the look-ahead inflation that random splitting manufactures in a time series.

<!-- RESULTS SUMMARY: fill from results.json -->

Code, data snapshots and every number are public and reproduce with one command.

## 1. Introduction

Gu, Kelly and Xiu (2020) compared linear and machine-learning methods for predicting monthly stock returns on the CRSP universe (about 30,000 stocks over sixty years) with 94 firm characteristics and their interactions with macroeconomic series, and found that trees and neural networks roughly doubled the out-of-sample R² of linear models and produced long-short portfolios with much higher Sharpe ratios. The paper has become the reference point for machine learning in asset pricing.

Two questions follow for anyone outside a well-resourced research group. First, *does the ranking depend on scale?* Nonlinear models need data to find nonlinearity; with a few thousand observations and ten features the comparison may invert. Second, *how much of the apparent skill in casual replications is an artefact of methodology?* Return data are a time series, and the most common error in student and practitioner replications is to split them randomly, which trains on the future.

This paper answers both on data anyone can download. Its ambition is deliberately limited: it is a small-scale replication, not a new method, and its value is in the protocol (fixed in advance, out of sample, with the wrong way measured alongside the right one) and in the candour of its reporting.

## 2. Data

Daily adjusted closing prices for the 30 current constituents of the Dow Jones Industrial Average and daily closes of the S&P 500 index were downloaded on 1 October 2026 via `yfinance` (version 1.7.0) for 2 January 2004 to 30 September 2026. One constituent lacked a full history over the window and was dropped by a 95 per cent completeness rule, leaving 29 stocks; the dropped ticker is recorded in `results.json`. Provenance is in `data/SNAPSHOT.json`.

**Survivorship.** The universe is the *current* Dow, so stocks that were removed (and the firms that failed) are absent, and the sample's average return is biased upward relative to an investable strategy. The paper's object is the *relative ranking of forecasting methods*, not the level of returns, and survivorship affects every model's target identically. It is nonetheless a limitation and is stated as one in Section 6; the long-short portfolio results in particular should be read as comparisons between models, not as achievable performance.

## 3. Method

### 3.1 Panel construction

One observation per stock-month. For each stock and month-end *t*, features are computed from daily log returns up to *t*; the target is the stock's log return over month *t*+1. Features, all standard in the cross-sectional literature:

| Feature | Definition |
|---|---|
| `ret_1m` | return over the last month (short-term reversal) |
| `mom_12_1` | return over months *t*−12 to *t*−1 (momentum) |
| `mom_6_1` | return over months *t*−6 to *t*−1 |
| `vol_1m`, `vol_12m` | standard deviation of daily returns over 1 and 12 months |
| `max_1m` | largest daily return in the last month |
| `beta_12m` | slope of daily returns on S&P 500 daily returns over 12 months |
| `mkt_1m`, `mkt_12m` | S&P 500 return over 1 and 12 months (identical across stocks in a month) |
| `month` | month of year, mapped to [−1, 1] |

Stock-level features are rank-normalised cross-sectionally within each month to [−1, 1], following Gu, Kelly and Xiu. Market features, being constant within a month, are instead scaled by their own expanding standard deviation using only past months. Two targets are examined: the raw next-month return and the same return demeaned by its month's cross-sectional average (the pure cross-sectional problem).

The panel has 7,537 stock-months over 260 month-ends from January 2005 to August 2026 (the last target month is September 2026).

### 3.2 Models

OLS; ridge (α ∈ {0.1, 1, 10, 100}); lasso (α ∈ {10⁻⁴, 10⁻³, 10⁻²}); random forest (300 trees, max depth ∈ {3, 6, none}, minimum leaf 20); histogram gradient boosting (300 iterations, learning rate 0.03, max depth ∈ {2, 3, 5}, L2 = 1); multilayer perceptron (two hidden layers of 32, early stopping, L2 α ∈ {10⁻³, 10⁻², 10⁻¹}, inputs standardised). Two benchmarks: a zero forecast and the expanding historical mean of the target.

### 3.3 Protocol

Walk-forward by calendar year. For test year *Y* (2012 to 2026), the training window is every stock-month with a target month before January of *Y*. Hyperparameters are chosen by mean squared error on the last 24 months of the training window (the validation block), with the model fitted on the earlier part; the chosen model is then refitted on the whole training window and applied to year *Y*. The window expands each year. Stochastic models are run with seeds 0–4.

### 3.4 Metrics

Pooled out-of-sample R² in the Gu–Kelly–Xiu form, 1 − Σ(*y* − *ŷ*)² / Σ *y*², against a zero forecast (and, additionally, against the historical mean); directional accuracy; a Diebold–Mariano test of each model's squared-error loss against OLS (HAC variance with lag 0, since forecasts are one step ahead), with positive statistics meaning the model beat OLS; and a monthly long-short portfolio that goes long the six stocks with the highest forecast and short the six lowest, equally weighted, reported as mean monthly return and annualised Sharpe ratio with a 90 per cent block-bootstrap interval (block length 6, 2,000 resamples).

### 3.5 The wrong way, measured

The same models with the middle hyperparameter of each grid are evaluated with shuffled five-fold cross-validation over all stock-months, pooling predictions and computing the same out-of-sample R². This protocol lets a model trained on 2020 predict 2015; it is the most common error in casual replications and its inflation is reported alongside the honest results.

### 3.6 Reproducibility

`python analysis.py` reproduces every number and figure from the committed data snapshots in about an hour on a 12-core laptop. Python 3.13, scikit-learn 1.9, pandas 2.2, SciPy 1.18.

## 4. Results

<!-- RESULTS: fill from results.json
  Table 1: panel and protocol summary
  Table 2: raw target — per model: R2 vs zero (mean±sd), R2 vs histmean, dir acc, DM vs OLS (stat, p), LS Sharpe (CI), leaky-CV R2
  Table 3: demeaned target — same
  Figure 1: honest vs leaky R2; Figure 2: long-short cumulative; Figure 3: yearly R2
  Text: ranking; whether any model beats OLS significantly; the size of the leak; year-to-year instability
-->

## 5. Discussion

<!-- fill after results -->

## 6. Limitations

*Scale.* 29 stocks and 10 features is two to three orders of magnitude smaller than the reference study in both dimensions. The paper tests whether the ranking holds at small scale; it cannot test the large-scale claim.

*Survivorship.* Discussed in Section 2. Affects return levels, not the relative evaluation of methods; but the long-short Sharpe ratios are not achievable numbers.

*Price-based features only.* No fundamentals, no analyst data, no macro series beyond the market return. The feature set is what is free; the reference study's advantage may lie precisely in the features the free data lack.

*Monthly horizon, one rebalance rule.* Results at daily or quarterly horizons, or with different portfolio construction, may differ.

*No transaction costs.* The long-short portfolio turns over substantially each month; realistic costs would reduce every model's Sharpe ratio, and would reduce the high-turnover (reversal-driven) strategies most.

*Hyperparameter grids are small.* Chosen to be defensible, not exhaustive. A larger search on the validation block might improve the nonlinear models; it might also overfit the validation block.

## 7. Conclusion

<!-- fill after results -->

## References

- Gu, S., Kelly, B. & Xiu, D. (2020). Empirical asset pricing via machine learning. *Review of Financial Studies*, 33(5), 2223–2273.
- Campbell, J. Y. & Thompson, S. B. (2008). Predicting excess stock returns out of sample: Can anything beat the historical average? *Review of Financial Studies*, 21(4), 1509–1531.
- Welch, I. & Goyal, A. (2008). A comprehensive look at the empirical performance of equity premium prediction. *Review of Financial Studies*, 21(4), 1455–1508.
- Diebold, F. X. & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263.
- Jegadeesh, N. & Titman, S. (1993). Returns to buying winners and selling losers: Implications for stock market efficiency. *Journal of Finance*, 48(1), 65–91.
- Bali, T. G., Cakici, N. & Whitelaw, R. F. (2011). Maxing out: Stocks as lotteries and the cross-section of expected returns. *Journal of Financial Economics*, 99(2), 427–446.
- Bailey, D. H., Borwein, J., López de Prado, M. & Zhu, Q. J. (2014). Pseudo-mathematics and financial charlatanism: The effects of backtest overfitting on out-of-sample performance. *Notices of the AMS*, 61(5), 458–471.
- López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. (Chapter 7, on cross-validation leakage in finance.)
- Politis, D. N. & Romano, J. P. (1994). The stationary bootstrap. *Journal of the American Statistical Association*, 89(428), 1303–1313.

## Data and code availability

Code, `results.json`, figures and `data/SNAPSHOT.json` are at https://github.com/Pranjulrathour/research under `papers/p2-ml-returns/`. Price data are from Yahoo Finance via `yfinance` and are redistributed only as dated snapshots for reproducibility.

## Declaration

The author has no competing interests and received no funding for this work.
