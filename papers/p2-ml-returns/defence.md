# P2 — Defence notes
## Do machine-learning return predictors beat linear baselines out of sample?

*Private preparation notes for talking about this paper in an interview, a workshop or a review. Not part of the manuscript.*

## The three findings, in one breath each

1. **At small scale, nothing beats the historical mean.** On 29 Dow stocks, monthly, walk-forward 2012–2026, the expanding mean had R² 2.41% against zero and no model beat it. The "best" model, lasso (2.36%), had shrunk into the mean: its forecasts barely vary across stocks (0.03 pp) and its directional accuracy (58.3%) equals the share of up-months.

2. **The nonlinear models were significantly worse than OLS, and validation knew it.** RF −0.27%, gradient boosting −1.68%, the neural net −1.69%, all significantly worse than OLS in Diebold–Mariano tests. Validation picked the most regularised setting of almost every model in almost every year. On relative (demeaned) returns every R² was below zero, and no long-short Sharpe interval excluded zero.

3. **Shuffled cross-validation manufactures 14–18 points of R² for trees, and the source is cross-sectional, not "the future".** RF goes from −0.27% to 13.44%, boosting from −1.68% to 15.89%. On the demeaned target the inflation vanishes, so it lives in the common monthly component: month-constant market features let a tree identify the month and read off what its month-mates earned.

## The method in sixty seconds

Current Dow 30 (Visa dropped, listed 2008), daily prices to monthly stock-months, ten standard features (reversal, momentum, volatility, max return, beta, market returns, month), ranks within month. Walk-forward by calendar year: train on everything before year Y, tune on the last 24 months of that window, refit, test on Y, for Y = 2012…2026. Six models plus zero and historical-mean benchmarks; R² vs zero and vs the mean, directional accuracy, Diebold–Mariano vs OLS, top-6-minus-bottom-6 long-short with a block bootstrap. Then the same models under shuffled 5-fold CV, labelled the wrong way.

## Questions I expect, and answers

**"So you're saying Gu, Kelly and Xiu are wrong?"** No. They had about 30,000 stocks, sixty years and 94 characteristics; I had 29 stocks and 10 features. The result locates the boundary of their finding: nonlinearity needs data to find, and at this scale the variance of a flexible model costs more than it buys. Validation said the same thing independently.

**"Isn't R² of 1–2% meaningless?"** Monthly return R² is always small; GKX's best models are a fraction of a per cent. The meaningful comparisons are relative: against the historical mean, and between models with a Diebold–Mariano test. Those are clear here.

**"Why does the historical mean do so well?"** Survivorship plus a bull market. The current Dow members are firms that did well, so the expanding mean is persistently positive and a zero forecast is persistently too low. That's exactly why I report R² against the mean as well as against zero, as Campbell & Thompson and Welch & Goyal recommend.

**"Survivorship bias invalidates this."** It biases levels, not the model comparison: every model forecasts the same targets. It does make the long-short Sharpe ratios non-investable, and the paper says so.

**"How do you know the leak is cross-sectional?"** Because it disappears on the demeaned target, where the shared monthly component is removed. If the trees were exploiting genuine future information about stock-level differences, demeaning wouldn't remove it. The mechanism is specific: mkt_1m and mkt_12m are identical for every stock in a month, so a tree can isolate the month.

**"Why only 10 features and these grids?"** They're the standard free price-based features; fundamentals need paid data. The grids are small, and validation chose their most regularised end almost every time, so a wider search would push models further towards the mean, not away from it.

**"What would you do next?"** A broader universe including delisted stocks (survivorship-free) to find where the crossover happens, fundamentals if a free source allows, and purged/embargoed cross-validation as a third protocol between walk-forward and shuffled.

**"How does this connect to the job?"** Quant research lives or dies on evaluation: the right benchmark, time-respecting splits, significance tests, and noticing when a "model" is just the mean. The leak finding in particular is a mistake I'd catch in a code review on day one.

## Numbers to have memorised

- 5,104 forecasts per model: 29 stocks × 176 month-ends (Jan 2012 – Aug 2026); 58.3% of stock-months positive.
- Raw R² vs zero: hist. mean 2.41, lasso 2.36, ridge 1.17, OLS 1.09, RF −0.27, GB −1.68, NN −1.69.
- DM vs OLS: ridge +3.57, lasso +5.95 (better); RF −2.50 (p 0.014), GB −4.76, NN −5.47 (worse).
- Demeaned: best ridge −0.07%; direction 50.2–51.5%.
- LS Sharpe: OLS 0.35 [−0.03, 0.79], ridge 0.34, RF 0.34, GB 0.10, NN 0.00, lasso −0.21.
- Shuffled CV: RF 13.44%, GB 15.89% (demeaned: −0.18%, −1.52%).
- Chosen regularisation: ridge α=100 in 15/15 years, lasso α=0.01 in 13/15, RF depth 3 in 12/15, GB depth 2 in 14/15, NN α=0.1 in 15/15.
- OLS yearly R²: +12.8% (2017) to −7.5% (2018).

## Where everything is

`papers/p2-ml-returns/analysis.py` (design in the docstring), `results.json` (all numbers; `post_hoc` holds the forecast-spread and by-year figures), `figures/fig0_protocol.png` (Figure 1), `fig2_long_short_cumulative.png` (Figure 2), `fig3_yearly_r2.png` (Figure 3), `fig1_r2_honest_vs_leaky.png` (Figure 4), `data/SNAPSHOT.json`, `paper.md`.
