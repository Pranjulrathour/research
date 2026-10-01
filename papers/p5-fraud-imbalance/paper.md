---
title: "Card-Fraud Detection Under Extreme Class Imbalance: A Time-Aware, Cost-Sensitive Benchmark on Public Data"
author: "Pranjul Rathour"
affiliation: "Independent researcher, Kanpur, India · pranjulrathour41@gmail.com · https://pranjulrathour.scult.in"
date: "October 2026"
keywords: "fraud detection, class imbalance, precision-recall, cost-sensitive thresholding, temporal validation, data leakage, gradient boosting, random forest, logistic regression"
---

## Abstract

Fraud detection is the canonical imbalanced-classification problem and the one most often taught with a methodology that would fail in production: random train/test splits that leak the future into the past, accuracy as the headline metric, and decision thresholds chosen on the test set. This paper benchmarks seven standard classifiers on the public ULB credit-card dataset (284,807 transactions over two days, 492 frauds, 0.173 per cent) under a protocol fixed before running: a strictly chronological 70/10/20 split, precision–recall area as the primary metric, a decision threshold chosen on the validation block by maximising expected savings under a simple cost model, and five seeds for every stochastic model. The same models are then evaluated under a stratified random split, labelled as the wrong way, to quantify how much apparent skill the leak manufactures.

<!-- RESULTS SUMMARY: fill from results.json -->

All code, the data snapshot's provenance and every number in the paper are public and reproduce with one command.

## 1. Introduction

Three habits make most published fraud-detection results unreliable as a guide to deployment.

The first is **random splitting**. Fraud evolves: patterns that appear late in a dataset were not available when early transactions were scored. A random split trains on the future and tests on the past, and the resulting metrics describe a model that could never have existed at deployment time. The leak is well known in forecasting and under-appreciated in classification, where the rows look exchangeable but are not.

The second is **the wrong metric**. With 0.17 per cent positives, a classifier that flags nothing is 99.83 per cent accurate. Accuracy, and to a lesser degree ROC-AUC (which is dominated by the ranking of the vast negative class), reward models that are useless for the task. The metric that tracks the operational question (*of the transactions I flag, how many are fraud, and how much fraud do I catch?*) is the precision–recall curve and its area.

The third is **threshold selection on the test set**. A probabilistic classifier is only a decision once a threshold is chosen, and the threshold should be chosen on data the test set has not seen, under the cost structure the business actually faces. Reporting "recall at the threshold that maximised F1 on the test set" is a form of tuning on the test set.

This paper does none of the three and measures what the first one costs. Its contribution is a clean, reproducible baseline on the most widely used public fraud dataset, with the methodology that practitioners need and students are rarely shown, and an explicit quantification of the leak.

## 2. Data

The dataset is the credit-card transaction set released by the Université Libre de Bruxelles Machine Learning Group (Dal Pozzolo et al., 2015), containing 284,807 transactions made by European cardholders over two days in September 2013, of which 492 (0.1727 per cent) are frauds. Features V1–V28 are principal components of the original confidential variables; `Time` is the number of seconds since the first transaction; `Amount` is the transaction value; `Class` is the label.

The copy used here is OpenML dataset 1597 (licence: Public). One detail matters for reproducibility: OpenML marks `Time` as the dataset's row-identifier attribute, so `scikit-learn`'s `fetch_openml` drops it silently. The analysis therefore reads the raw ARFF file (OpenML file id 1673544), which retains `Time`; `Time` is monotonically non-decreasing in row order, which the script verifies, so the chronological split is well-defined. Provenance, byte counts and the download time are recorded in `data/SNAPSHOT.json`.

## 3. Method

The design was fixed before the first run and is recorded in the script's docstring.

### 3.1 Split

Rows are sorted by `Time`. The first 70 per cent form the training set, the next 10 per cent the validation set, the final 20 per cent the test set. Nothing from validation or test is used to fit any model; the test set is touched once per model, at the end.

### 3.2 Models

Seven classifiers from `scikit-learn`, with default hyperparameters except where stated: a majority-class dummy (predicts the prior); logistic regression, plain and with balanced class weights; random forest (300 trees), plain and with `balanced_subsample` class weights; histogram gradient boosting (300 iterations, learning rate 0.05), plain and with balanced class weights. `Time` and `Amount` are standardised on the training set; V1–V28 are used as given. A rule-based baseline that flags the largest 0.2 per cent of amounts is included to show what no learning at all achieves.

### 3.3 Metrics

Primary: average precision (area under the precision–recall curve). Also reported: ROC-AUC (with the argument against relying on it), recall at precision 0.5 and 0.9, precision at recall 0.8, the Brier score and a reliability diagram for calibration, and, once, accuracy of the dummy classifier, to show why accuracy is meaningless here.

### 3.4 Threshold and cost model

A missed fraud costs its amount; a false alarm costs a fixed review cost of 2.0 currency units (the dataset's amounts are in an unstated European currency; the ratio is what matters). For each model, 400 candidate thresholds spanning the 90th to 99.99th percentile of validation scores are evaluated, and the one maximising validation savings (caught fraud amount minus review cost times alerts) is chosen. That threshold is applied unchanged to the test set, and test savings and alert count are reported. Savings are relative to doing nothing.

### 3.5 Seeds and the leak comparison

Stochastic models (the forests and the boosters) are run with seeds 0–4 and reported as mean ± standard deviation; deterministic models once. The entire protocol is then repeated on a stratified random split with the same 70/10/20 proportions (random state 0), labelled throughout as the wrong way, and the two sets of results are compared model by model.

### 3.6 Reproducibility

`python analysis.py` in the paper's directory reproduces every number and figure from `data/creditcard.csv` (rebuilt from the OpenML ARFF as described) in about an hour on a 12-core laptop, most of it in the random forests. Python 3.13, scikit-learn 1.9, pandas 2.2; exact versions in the repository's `requirements.txt`.

## 4. Results

<!-- RESULTS: fill from results.json
  Table 1: split sizes and fraud counts (time-aware vs random)
  Table 2: time-aware test metrics per model (AP mean±sd, ROC, R@P0.9, P@R0.8, Brier, savings, alerts)
  Table 3: random-split AP per model alongside time-aware AP, and the inflation
  Figure 1: PR curves + reliability
  Text: which model wins on AP; how much class weighting helps or hurts AP vs calibration; how far the leak inflates;
        the cost-model threshold's behaviour (alerts, savings) and the dummy accuracy
-->

## 5. Discussion

<!-- fill after results -->

## 6. Limitations

*One dataset, two days.* The ULB data is the standard public benchmark and it is small in time: two days cannot show seasonal or adversarial drift, and the chronological split tests only whether patterns from the first day and a half transfer to the last half-day. The direction of the leak's effect generalises; its size on this dataset is specific to it.

*PCA features.* The anonymised principal components prevent feature engineering of the kind real fraud systems depend on (velocity features, merchant history, device signals). Results are a floor for what the raw data would support.

*A toy cost model.* A fixed review cost and a loss equal to the amount ignore chargeback fees, customer friction from false declines, and the difference between card-present and card-not-present fraud. The point of the cost model is to make threshold selection explicit and out-of-sample, not to estimate real savings.

*No sequential or online learning.* Production systems retrain continuously and score transactions in sequence with features computed from the account's history. This paper evaluates a one-shot batch model, which is the setting most published results use and the one in which the leak is most often made.

*Default hyperparameters.* Nothing was tuned. Tuned models would score higher; the comparisons between models and between splits are the finding, not the absolute levels.

## 7. Conclusion

<!-- fill after results -->

## References

- Dal Pozzolo, A., Caelen, O., Johnson, R. A. & Bontempi, G. (2015). Calibrating probability with undersampling for unbalanced classification. *IEEE Symposium Series on Computational Intelligence (SSCI)*, 159–166.
- Dal Pozzolo, A., Boracchi, G., Caelen, O., Alippi, C. & Bontempi, G. (2018). Credit card fraud detection: A realistic modeling and a novel learning strategy. *IEEE Transactions on Neural Networks and Learning Systems*, 29(8), 3784–3797.
- Saito, T. & Rehmsmeier, M. (2015). The precision–recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE*, 10(3), e0118432.
- Davis, J. & Goadrich, M. (2006). The relationship between precision–recall and ROC curves. *ICML 2006*, 233–240.
- Elkan, C. (2001). The foundations of cost-sensitive learning. *IJCAI 2001*, 973–978.
- Kaufman, S., Rosset, S., Perlich, C. & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM TKDD*, 6(4), 15.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. *ICML 2005*, 625–632.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830.

## Data and code availability

Code, `results.json` (every number in this paper), figures and `data/SNAPSHOT.json` are at https://github.com/Pranjulrathour/research under `papers/p5-fraud-imbalance/`. The dataset is redistributed by OpenML (id 1597, Public) and is not committed here because of its size; the script documents how to rebuild the CSV with the `Time` column.

## Declaration

The author has no competing interests and received no funding for this work.
