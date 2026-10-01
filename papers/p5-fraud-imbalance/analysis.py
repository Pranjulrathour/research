"""P5 -- Card-fraud detection under extreme class imbalance: a reproducible benchmark on public data.

Reproduce:  python analysis.py        (reads data/creditcard.csv from OpenML id 1597, writes results.json + figures/)

Design, fixed before running:
  * Data: ULB credit-card transactions (284,807 rows, 492 frauds = 0.173%), two days, PCA features V1-V28 + Time + Amount.
  * Split is TIME-AWARE, never random: train = first 70% of transactions by Time, validation = next 10%, test = last 20%.
    Random splits leak future into past and overstate performance; the paper quantifies that leak by also reporting a
    stratified random split for comparison (clearly labelled as the wrong way).
  * Models: logistic regression (class-weighted), random forest, gradient boosting (HistGradientBoosting), each with and
    without class weighting / balanced subsampling; a majority-class dummy and an "amount-threshold" rule as baselines.
  * Metrics: PR-AUC (average precision) as primary; ROC-AUC reported but argued against; recall at fixed precision 0.5 and
    0.9; precision at recall 0.8; Brier score and a reliability curve for calibration; accuracy reported once to show why
    it is meaningless here (the dummy gets 99.83%).
  * Thresholding: the decision threshold is chosen on the VALIDATION split by maximising expected savings under a simple
    cost model (missed fraud costs the amount; a false alarm costs a fixed review cost of 2.0 currency units), then applied
    unchanged to the test split.
  * Seeds fixed (0); 5 seeds for the stochastic models to report mean +- sd.
Nothing is tuned on the test split.

Revision record: (1) the OpenML copy drops `Time` (it is the dataset's row-id attribute), so data/creditcard.csv is rebuilt
from the raw ARFF; (2) the first run's threshold search had no "flag nothing" candidate, which forced the constant-score
dummy to flag every transaction; the candidate set now includes an infinite threshold (savings 0). Both fixed before any
model result was examined beyond the first three log lines.
"""
from __future__ import annotations
import json, time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, brier_score_loss, precision_recall_curve, roc_auc_score, accuracy_score)
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
REVIEW_COST = 2.0
SEEDS = (0, 1, 2, 3, 4)


def load():
    df = pd.read_csv(HERE / "data" / "creditcard.csv").sort_values("Time").reset_index(drop=True)
    X = df.drop(columns=["Class"]); y = df["Class"].astype(int).values
    return df, X, y


def time_split(df, X, y):
    n = len(df); a, b = int(0.7 * n), int(0.8 * n)
    return (X.iloc[:a], y[:a]), (X.iloc[a:b], y[a:b]), (X.iloc[b:], y[b:])


def metrics(y, p, amounts) -> dict:
    prec, rec, thr = precision_recall_curve(y, p)
    def rec_at_prec(t):
        ok = prec[:-1] >= t
        return float(rec[:-1][ok].max()) if ok.any() else 0.0
    def prec_at_rec(t):
        ok = rec[:-1] >= t
        return float(prec[:-1][ok].max()) if ok.any() else 0.0
    return {"pr_auc": float(average_precision_score(y, p)), "roc_auc": float(roc_auc_score(y, p)),
            "recall_at_precision_0.5": rec_at_prec(0.5), "recall_at_precision_0.9": rec_at_prec(0.9),
            "precision_at_recall_0.8": prec_at_rec(0.8), "brier": float(brier_score_loss(y, p)),
            "positives": int(y.sum()), "n": int(len(y))}


def savings(y, p, amounts, thr) -> float:
    """Money saved vs doing nothing: caught fraud amounts minus review cost of every alert."""
    alert = p >= thr
    caught = float(amounts[(alert) & (y == 1)].sum())
    return caught - REVIEW_COST * float(alert.sum())


def best_threshold(y, p, amounts) -> float:
    # "flag nothing" (threshold above every score, savings 0) must always be an option; without it a model with constant
    # scores (the dummy) is forced to flag everything. Added 2026-10-01 after the first run exposed it; see docstring.
    cands = list(np.quantile(p, np.linspace(0.90, 0.9999, 400))) + [np.inf]
    return float(max(cands, key=lambda t: savings(y, p, amounts, t)))


def models(seed: int):
    return {
        "dummy_majority": DummyClassifier(strategy="prior"),
        "logreg": LogisticRegression(max_iter=2000, random_state=seed),
        "logreg_balanced": LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed),
        "random_forest": RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=seed),
        "random_forest_balanced": RandomForestClassifier(n_estimators=300, n_jobs=-1, class_weight="balanced_subsample", random_state=seed),
        "hist_gb": HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=seed),
        "hist_gb_balanced": HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, class_weight="balanced", random_state=seed),
    }


def run_split(name, tr, va, te, out, scaler_cols):
    (Xtr, ytr), (Xva, yva), (Xte, yte) = tr, va, te
    sc = StandardScaler().fit(Xtr[scaler_cols])
    def prep(X):
        Z = X.copy(); Z[scaler_cols] = sc.transform(X[scaler_cols]); return Z.values
    Ztr, Zva, Zte = prep(Xtr), prep(Xva), prep(Xte)
    amt_te = Xte["Amount"].values; amt_va = Xva["Amount"].values
    # amount-rule baseline: flag the top 0.2% amounts
    p_rule = Xte["Amount"].rank(pct=True).values
    out[name] = {"baseline_amount_rule": metrics(yte, p_rule, amt_te),
                 "accuracy_of_majority_dummy": float(accuracy_score(yte, np.zeros_like(yte))), "models": {}}
    for mname in models(0):
        per_seed = []
        for s in (SEEDS if mname.startswith(("random_forest", "hist_gb")) else SEEDS[:1]):
            m = models(s)[mname]; t0 = time.perf_counter(); m.fit(Ztr, ytr); fit_s = time.perf_counter() - t0
            pva = m.predict_proba(Zva)[:, 1]; pte = m.predict_proba(Zte)[:, 1]
            thr = best_threshold(yva, pva, amt_va)
            r = metrics(yte, pte, amt_te)
            r.update({"threshold_from_validation": thr, "test_savings_at_threshold": savings(yte, pte, amt_te, thr),
                      "test_alerts_at_threshold": int((pte >= thr).sum()), "fit_seconds": fit_s, "seed": s})
            per_seed.append(r)
        agg = {k: {"mean": float(np.mean([r[k] for r in per_seed])), "sd": float(np.std([r[k] for r in per_seed]))}
               for k in per_seed[0] if isinstance(per_seed[0][k], (int, float)) and k not in ("seed",)}
        out[name]["models"][mname] = {"runs": len(per_seed), "agg": agg}
        print(f"[{name}] {mname:24s} PR-AUC {agg['pr_auc']['mean']:.3f}+-{agg['pr_auc']['sd']:.3f}  ROC {agg['roc_auc']['mean']:.3f}  "
              f"R@P.9 {agg['recall_at_precision_0.9']['mean']:.2f}  savings {agg['test_savings_at_threshold']['mean']:.0f}  alerts {agg['test_alerts_at_threshold']['mean']:.0f}")


LABEL = {"dummy_majority": "Majority dummy", "logreg": "Logistic regression", "logreg_balanced": "Logistic regression, weighted",
         "random_forest": "Random forest", "random_forest_balanced": "Random forest, weighted",
         "hist_gb": "Gradient boosting", "hist_gb_balanced": "Gradient boosting, weighted"}


def reliability_plot(tr, te, scaler_cols):
    import sys
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from sklearn.calibration import calibration_curve
    sys.path.insert(0, str(HERE.parent))
    import plotstyle as ps
    ps.apply(9.0)
    (Xtr, ytr), (Xte, yte) = tr, te
    sc = StandardScaler().fit(Xtr[scaler_cols])
    def prep(X):
        Z = X.copy(); Z[scaler_cols] = sc.transform(X[scaler_cols]); return Z.values
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))
    for mname, color in (("logreg", ps.INK), ("hist_gb", ps.ACCENT), ("random_forest", ps.ACCENT2)):
        m = models(0)[mname].fit(prep(Xtr), ytr); p = m.predict_proba(prep(Xte))[:, 1]
        prec, rec, _ = precision_recall_curve(yte, p)
        axes[0].plot(rec, prec, color=color, lw=0.9, label=f"{LABEL[mname]} ({average_precision_score(yte, p):.2f})")
        fr, mp = calibration_curve(yte, p, n_bins=10, strategy="quantile")
        axes[1].plot(mp, fr, "o-", ms=2.6, lw=0.8, color=color, label=LABEL[mname])
    base = yte.mean()
    axes[0].axhline(base, color=ps.MID, lw=0.5, ls=(0, (3, 2)))
    axes[0].text(0.02, base + 0.02, f"fraud base rate {base * 100:.2f}%", fontsize=7, color=ps.MID, va="bottom")
    axes[0].set_xlabel("recall"); axes[0].set_ylabel("precision"); axes[0].set_xlim(0, 1); axes[0].set_ylim(0, 1.02)
    axes[0].set_title("Precision against recall", loc="left", fontsize=9.5, fontweight="bold", pad=6)
    axes[0].legend(loc="lower left", fontsize=7.2, handlelength=1.2, title="average precision", title_fontsize=7.2)
    axes[1].plot([0, 1], [0, 1], color=ps.MID, lw=0.5, ls=(0, (3, 2)))
    axes[1].set_xscale("symlog", linthresh=1e-3); axes[1].set_yscale("symlog", linthresh=1e-3)
    axes[1].set_xlim(0, 1); axes[1].set_ylim(0, 1)
    axes[1].set_xlabel("predicted probability"); axes[1].set_ylabel("observed fraud rate")
    axes[1].set_title("Calibration", loc="left", fontsize=9.5, fontweight="bold", pad=6)
    fig.tight_layout(w_pad=2.0); fig.savefig(FIG / "fig1_pr_and_calibration.png"); plt.close(fig)


def split_plot(out):
    """PR-AUC by model under the time-aware split and the (leaky) stratified random split, mean +- sd over seeds."""
    import sys
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    sys.path.insert(0, str(HERE.parent))
    import plotstyle as ps
    ps.apply(9.0)
    names = [m for m in out["time_aware"]["models"] if m != "dummy_majority"]
    fig, ax = plt.subplots(figsize=(6.3, 2.7))
    ys = np.arange(len(names))[::-1]
    for k, (split, color, lab) in enumerate((("time_aware", ps.INK, "time-aware split (train on the past)"),
                                             ("random_stratified", ps.ACCENT, "stratified random split (look-ahead)"))):
        mu = [out[split]["models"][n]["agg"]["pr_auc"]["mean"] for n in names]
        sd = [out[split]["models"][n]["agg"]["pr_auc"]["sd"] for n in names]
        off = 0.17 if k == 0 else -0.17
        ax.errorbar(mu, ys + off, xerr=sd, fmt="o", ms=3.6, color=color, ecolor=color, elinewidth=0.8, capsize=0, label=lab)
    ax.set_yticks(ys); ax.set_yticklabels([LABEL[n] for n in names], fontsize=7.8); ax.tick_params(axis="y", length=0)
    ax.set_xlim(0.3, 1.0); ax.set_xlabel("PR-AUC on the test split (mean ± sd over seeds)")
    ax.grid(axis="x", color=ps.RULE, lw=0.5); ax.set_axisbelow(True)
    ax.legend(loc="lower left", handlelength=1.0)
    fig.tight_layout(); fig.savefig(FIG / "fig2_split_comparison.png"); plt.close(fig)


def main():
    import sys
    df, X, y = load()
    scaler_cols = ["Time", "Amount"]
    tr, va, te = time_split(df, X, y)
    if "--plots-only" in sys.argv:
        reliability_plot(tr, te, scaler_cols); split_plot(json.load(open(HERE / "results.json")))
        print("redrew figures"); return
    out = {"meta": json.load(open(HERE / "data" / "SNAPSHOT.json")), "review_cost": REVIEW_COST, "seeds": SEEDS,
           "splits": {"time_aware": {"train": int(len(tr[1])), "val": int(len(va[1])), "test": int(len(te[1])),
                                     "train_frauds": int(tr[1].sum()), "val_frauds": int(va[1].sum()), "test_frauds": int(te[1].sum())}}}
    print("time-aware split:", out["splits"]["time_aware"])
    run_split("time_aware", tr, va, te, out, scaler_cols)
    # The wrong way, for comparison: stratified random split (leaks time)
    Xtv, Xte_r, ytv, yte_r = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
    Xtr_r, Xva_r, ytr_r, yva_r = train_test_split(Xtv, ytv, test_size=0.125, stratify=ytv, random_state=0)
    out["splits"]["random_stratified"] = {"train": int(len(ytr_r)), "val": int(len(yva_r)), "test": int(len(yte_r)), "test_frauds": int(yte_r.sum())}
    run_split("random_stratified", (Xtr_r, ytr_r), (Xva_r, yva_r), (Xte_r, yte_r), out, scaler_cols)
    json.dump(out, open(HERE / "results.json", "w"), indent=1)
    reliability_plot(tr, te, scaler_cols); split_plot(out)
    print("wrote results.json")


if __name__ == "__main__":
    main()
