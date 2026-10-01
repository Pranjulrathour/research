# P5 — Defence notes
## Card-fraud detection under extreme class imbalance: a time-aware, cost-sensitive benchmark

*Private preparation notes for talking about this paper in an interview, a workshop or a review. Not part of the manuscript.*

## The three findings, in one breath each

1. **Pick models by PR-AUC, not accuracy or ROC-AUC.** Flagging nothing is 99.87% accurate. ROC-AUC put weighted logistic regression first (0.983) and the actual best model, the weighted random forest (PR-AUC 0.811), fifth of six. ROC averages over false-positive rates nobody operates at.

2. **Class weighting helps ranking and can wreck calibration.** PR-AUC up for every family (+0.036 logistic, +0.019 forest, +0.25 boosting), but the logistic model's Brier score got 25× worse and its validation threshold landed at 0.9999. Weighted scores aren't probabilities until you recalibrate them.

3. **The leak I set out to measure barely showed up, and that's the interesting part.** Random vs time-aware PR-AUC differences were small and went both ways. Two days of data have almost no drift, and a random split only leaks what changes over time. I still split by time, because you can't know the drift in advance.

Bonus finding to volunteer: **plain gradient boosting was a lottery (PR-AUC 0.50 ± 0.12) because of a library default.** scikit-learn turns on early stopping above 10,000 rows with a random 10% holdout, here about 38 frauds; it stopped after 11–19 rounds. Early stopping off: every seed gives the same 0.614. I checked this after the main run and labelled it post-hoc.

## The method in sixty seconds

ULB credit-card data (284,807 transactions, 492 frauds, two days in September 2013), rebuilt from the OpenML ARFF because `fetch_openml` silently drops the `Time` column. Sorted by time: 70% train, 10% validation, 20% test (the evening of day two). Seven models with defaults, five seeds for the stochastic ones. Threshold chosen on validation by maximising savings under a simple cost model (missed fraud costs its amount, an alert costs 2), then applied unchanged to test. The whole thing repeated on a stratified random split as the comparison.

## Questions I expect, and answers

**"Why didn't you use SMOTE or undersampling?"** Class weighting is the cheapest form of rebalancing and it's what most teams try first; the study shows its trade-off (ranking up, calibration down). SMOTE adds synthetic points in PCA space that don't correspond to real transactions, and Dal Pozzolo et al. (2015) show undersampling also distorts probabilities. It's a fair next experiment, alongside recalibration.

**"Your best model only recovers 68% of possible savings. Is that good?"** It's 5,168 of 7,579 with 81 alerts for 75 frauds, from PCA features with no account history. Real systems use velocity and merchant features this dataset doesn't have, so treat it as a floor. The more useful point is that the threshold is chosen on just 33 validation frauds, so savings are noisier than PR-AUC.

**"If the random split didn't inflate anything, why insist on a time split?"** Because the leak's size depends on drift, and drift is the thing you can't see until it bites. On two days there's almost none; on months of card data there's plenty (Dal Pozzolo et al. 2018). A time split costs nothing when there's no drift and protects you when there is. Reporting the near-zero result honestly matters more than confirming my hypothesis.

**"Isn't the early-stopping finding just a bug in your setup?"** It's the library default, used exactly as documented. The point is that defaults tuned for ordinary classification behave badly when positives are this rare. The post-hoc check is reproducible (`python analysis.py --post-hoc`) and stored separately in `results.json`, so it can't be mistaken for part of the pre-registered design.

**"Why is the amount rule's ROC below 0.5?"** In this data, frauds are on average smaller than legitimate transactions, so ranking by amount ranks them backwards. A useful reminder that "big transactions are risky" is an assumption, not a fact.

**"What would you do next?"** Recalibrate the weighted models (isotonic or Platt) and re-check savings; use a longer, drifting dataset to measure the leak properly; and try cost-sensitive thresholds with a larger validation window.

**"How does this connect to the job?"** Fraud, risk and anomaly work at Visa, the banks and Amazon is exactly this problem: rare positives, costly errors, decisions at a threshold. The habits are the transferable part: right metric, out-of-sample thresholds, check the defaults, and report the result you got, not the one you expected.

## Numbers to have memorised

- 284,807 transactions, 492 frauds (0.173%); time-aware test 56,962 rows with 75 frauds (0.132%); validation only 33 frauds.
- Dummy accuracy 99.868%; dummy PR-AUC 0.001.
- PR-AUC (time-aware): RF weighted 0.811 ± 0.003, RF 0.792, HGB weighted 0.752, LR weighted 0.748, LR 0.712, HGB 0.502 ± 0.124.
- ROC-AUC: LR weighted 0.983 (highest) vs RF weighted 0.947.
- Brier: LR 0.00062 → weighted 0.01571 (25×); RF 0.00044 vs 0.00045.
- Savings: RF weighted 5,168 of 7,579 possible (68%), 81 alerts.
- HGB early stopping: 11–19 rounds, PR-AUC 0.34–0.64 by seed; off: 0.614 for every seed.
- Leak: differences between protocols from −0.061 to +0.095, mixed in sign.

## Where everything is

`papers/p5-fraud-imbalance/analysis.py` (design and revision record in the docstring), `results.json` (all numbers; `post_hoc` holds the early-stopping check and test-set totals), `figures/fig0_split.png` (Figure 1), `fig1_pr_and_calibration.png` (Figure 2), `fig2_split_comparison.png` (Figure 3), `data/SNAPSHOT.json` (provenance and hashes), `run_first_attempt_threshold_bug.log` (the first run, kept), `paper.md`.
