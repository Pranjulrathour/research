"""P1 -- Fat tails and the failure of Gaussian risk models: NIFTY 50 and S&P 500, 2010-2026.

Reproduce everything:  python analysis.py        (reads data/*.csv, writes results.json and figures/*.png)

Design (fixed before looking at results):
  * Daily log returns, analysis window 2010-01-01 .. 2026-09-30, each index on its own trading calendar.
  * Distribution tests: moments, Jarque-Bera, empirical vs Gaussian exceedance frequencies at 2,3,4,5 sigma.
  * One-day VaR at 95% and 99%, rolling estimation window W = 500 trading days (~2 years), re-estimated daily,
    strictly out of sample (the window ends the day before the forecast day). Four models:
      gaussian      : mu_W + sigma_W * z_alpha
      historical    : empirical alpha-quantile of the window
      student_t     : MLE Student-t fit on the window (location, scale, df), quantile from the fitted t
      ewma_gaussian : RiskMetrics EWMA volatility (lambda = 0.94, zero mean) with Gaussian quantile
  * Backtests: Kupiec (1995) unconditional coverage, Christoffersen (1998) independence and conditional coverage;
    all p-values from chi-square. Expected Shortfall is not backtested (out of scope).
Nothing here is tuned to the data; the window length and lambda are the textbook defaults.
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)
START, END = "2010-01-01", "2026-09-30"
WINDOW = 500
ALPHAS = (0.95, 0.99)
LAMBDA = 0.94
SIGMAS = (2, 3, 4, 5)


def load(name: str) -> pd.Series:
    df = pd.read_csv(HERE / "data" / f"{name}_daily_close.csv", parse_dates=["Date"], index_col="Date")
    r = np.log(df["Close"]).diff().dropna()
    return r.loc[START:END]


def describe(r: pd.Series) -> dict:
    jb_stat, jb_p = stats.jarque_bera(r.values)
    z = (r - r.mean()) / r.std(ddof=1)
    exceed = {}
    for k in SIGMAS:
        emp = float((np.abs(z) > k).mean())
        gauss = float(2 * stats.norm.sf(k))
        exceed[f"{k}sigma"] = {"empirical_freq": emp, "gaussian_freq": gauss,
                               "ratio": (emp / gauss) if gauss > 0 else None,
                               "empirical_count": int((np.abs(z) > k).sum()),
                               "gaussian_expected_count": gauss * len(z)}
    df_t, loc_t, scale_t = stats.t.fit(r.values)
    return {"n_days": int(len(r)), "first": str(r.index.min().date()), "last": str(r.index.max().date()),
            "mean_daily": float(r.mean()), "std_daily": float(r.std(ddof=1)), "ann_vol": float(r.std(ddof=1) * np.sqrt(252)),
            "skew": float(stats.skew(r)), "excess_kurtosis": float(stats.kurtosis(r, fisher=True)),
            "jarque_bera_stat": float(jb_stat), "jarque_bera_p": float(jb_p),
            "min_day": {"date": str(r.idxmin().date()), "ret": float(r.min())},
            "max_day": {"date": str(r.idxmax().date()), "ret": float(r.max())},
            "student_t_fit_full_sample": {"df": float(df_t), "loc": float(loc_t), "scale": float(scale_t)},
            "exceedances": exceed}


def var_forecasts(r: pd.Series, alpha: float) -> pd.DataFrame:
    """Out-of-sample one-day VaR (as a positive loss number) for day t using data up to t-1."""
    x = r.values
    n = len(x)
    out = {m: np.full(n, np.nan) for m in ("gaussian", "historical", "student_t", "ewma_gaussian")}
    z = stats.norm.ppf(1 - alpha)
    # EWMA variance recursion over the whole series (uses only past data at each step)
    ew_var = np.full(n, np.nan)
    ew_var[0] = x[:WINDOW].var()
    for t in range(1, n):
        ew_var[t] = LAMBDA * ew_var[t - 1] + (1 - LAMBDA) * x[t - 1] ** 2
    for t in range(WINDOW, n):
        w = x[t - WINDOW:t]
        mu, sd = w.mean(), w.std(ddof=1)
        out["gaussian"][t] = -(mu + sd * z)
        out["historical"][t] = -np.quantile(w, 1 - alpha)
        df_, loc_, sc_ = stats.t.fit(w)
        out["student_t"][t] = -(loc_ + sc_ * stats.t.ppf(1 - alpha, df_))
        out["ewma_gaussian"][t] = -(np.sqrt(ew_var[t]) * z)
    return pd.DataFrame(out, index=r.index)


def kupiec(n: int, x: int, p: float) -> tuple[float, float]:
    """Unconditional coverage LR test. n obs, x violations, p = 1 - alpha."""
    if x == 0:
        lr = -2 * n * np.log(1 - p)
    else:
        ph = x / n
        lr = -2 * ((n - x) * np.log(1 - p) + x * np.log(p) - (n - x) * np.log(1 - ph) - x * np.log(ph))
    return float(lr), float(stats.chi2.sf(lr, 1))


def christoffersen(viol: np.ndarray, p: float) -> dict:
    """Independence (LR_ind) and conditional coverage (LR_cc = LR_uc + LR_ind)."""
    v = viol.astype(int)
    n00 = n01 = n10 = n11 = 0
    for a, b in zip(v[:-1], v[1:]):
        if a == 0 and b == 0: n00 += 1
        elif a == 0 and b == 1: n01 += 1
        elif a == 1 and b == 0: n10 += 1
        else: n11 += 1
    pi0 = n01 / (n00 + n01) if (n00 + n01) else 0.0
    pi1 = n11 / (n10 + n11) if (n10 + n11) else 0.0
    pi = (n01 + n11) / max(1, n00 + n01 + n10 + n11)

    def ll(p_, a, b):  # a = count of non-violation transitions, b = violation transitions
        return (a * np.log(1 - p_) if a and p_ < 1 else 0.0) + (b * np.log(p_) if b and p_ > 0 else 0.0)

    lr_ind = -2 * (ll(pi, n00 + n10, n01 + n11) - (ll(pi0, n00, n01) + ll(pi1, n10, n11)))
    lr_uc, _ = kupiec(len(v), int(v.sum()), p)
    lr_cc = lr_uc + lr_ind
    return {"lr_ind": float(lr_ind), "p_ind": float(stats.chi2.sf(lr_ind, 1)),
            "lr_cc": float(lr_cc), "p_cc": float(stats.chi2.sf(lr_cc, 2)),
            "transitions": {"n00": n00, "n01": n01, "n10": n10, "n11": n11}}


def backtest(r: pd.Series, alpha: float) -> dict:
    var = var_forecasts(r, alpha).dropna()
    actual = r.loc[var.index].values
    p = 1 - alpha
    res = {}
    for m in var.columns:
        viol = actual < -var[m].values
        x = int(viol.sum()); n = len(viol)
        lr_uc, p_uc = kupiec(n, x, p)
        c = christoffersen(viol, p)
        # loss on violation days relative to VaR: how far beyond the limit, on average (tail severity)
        excess = (-actual[viol] - var[m].values[viol])
        res[m] = {"n_obs": n, "violations": x, "expected_violations": n * p, "violation_rate": x / n,
                  "kupiec_lr": lr_uc, "kupiec_p": p_uc, **c,
                  "mean_excess_loss_on_violation": float(excess.mean()) if x else None,
                  "mean_var": float(var[m].mean())}
    return {"window": WINDOW, "alpha": alpha, "first_forecast": str(var.index.min().date()),
            "last_forecast": str(var.index.max().date()), "models": res}


def plots(returns: dict[str, pd.Series], results: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    # 1. QQ plots
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, (name, r) in zip(axes, returns.items()):
        z = ((r - r.mean()) / r.std(ddof=1)).values
        stats.probplot(z, dist="norm", plot=ax)
        ax.get_lines()[0].set(marker=".", markersize=3, color="#1c1b22"); ax.get_lines()[1].set(color="#ff4d2e")
        ax.set_title(f"{name}: standardised daily log returns vs normal"); ax.set_xlabel("theoretical quantiles"); ax.set_ylabel("sample quantiles")
    fig.tight_layout(); fig.savefig(FIG / "fig1_qq.png", dpi=160); plt.close(fig)
    # 2. Tail exceedance ratio bars
    fig, ax = plt.subplots(figsize=(7, 3.6))
    width = 0.38
    for i, (name, d) in enumerate(results["distribution"].items()):
        ratios = [d["exceedances"][f"{k}sigma"]["ratio"] or 0 for k in SIGMAS]
        ax.bar(np.arange(len(SIGMAS)) + (i - 0.5) * width, ratios, width, label=name, color=["#1c1b22", "#ff4d2e"][i])
    ax.set_xticks(range(len(SIGMAS))); ax.set_xticklabels([f">{k}σ" for k in SIGMAS]); ax.set_yscale("log")
    ax.axhline(1, color="grey", lw=0.8, ls="--"); ax.set_ylabel("observed / Gaussian-expected frequency (log)")
    ax.set_title("How often large moves happen, relative to a normal distribution"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(FIG / "fig2_exceedance_ratio.png", dpi=160); plt.close(fig)
    # 3. 99% VaR violations by model
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
    for ax, name in zip(axes, returns):
        bt = results["backtests"][name]["0.99"]["models"]
        models = list(bt); viol = [bt[m]["violations"] for m in models]; exp = bt[models[0]]["expected_violations"]
        ax.bar(models, viol, color=["#1c1b22", "#5b5a66", "#ff4d2e", "#c9ccd4"]); ax.axhline(exp, color="grey", ls="--", lw=0.9)
        ax.text(len(models) - 0.5, exp, f" expected {exp:.0f}", va="bottom", ha="right", fontsize=8, color="grey")
        ax.set_title(f"{name}: 99% one-day VaR violations, {bt[models[0]]['n_obs']} days"); ax.tick_params(axis="x", rotation=20)
    axes[0].set_ylabel("violations"); fig.tight_layout(); fig.savefig(FIG / "fig3_var99_violations.png", dpi=160); plt.close(fig)
    # 4. Rolling 99% VaR vs returns for S&P 500 (illustrative)
    r = returns["SP500"]; var = var_forecasts(r, 0.99).dropna()
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(r.loc[var.index].index, r.loc[var.index].values, color="#c9ccd4", lw=0.5, label="daily log return")
    ax.plot(var.index, -var["gaussian"], color="#1c1b22", lw=0.9, label="Gaussian 99% VaR (500d)")
    ax.plot(var.index, -var["student_t"], color="#ff4d2e", lw=0.9, label="Student-t 99% VaR (500d)")
    ax.plot(var.index, -var["ewma_gaussian"], color="#5b5a66", lw=0.7, label="EWMA-Gaussian 99% VaR")
    ax.set_title("S&P 500: returns against one-day 99% VaR forecasts (out of sample)"); ax.legend(frameon=False, fontsize=8, ncol=2)
    fig.tight_layout(); fig.savefig(FIG / "fig4_sp500_var_paths.png", dpi=160); plt.close(fig)


def main() -> None:
    returns = {n: load(n) for n in ("NIFTY50", "SP500")}
    results = {"meta": json.load(open(HERE / "data" / "SNAPSHOT.json")), "window": WINDOW, "lambda": LAMBDA,
               "distribution": {n: describe(r) for n, r in returns.items()},
               "backtests": {n: {str(a): backtest(r, a) for a in ALPHAS} for n, r in returns.items()}}
    json.dump(results, open(HERE / "results.json", "w"), indent=1)
    plots(returns, results)
    for n, d in results["distribution"].items():
        print(f"{n}: n={d['n_days']} ann_vol={d['ann_vol']:.3f} skew={d['skew']:.2f} exkurt={d['excess_kurtosis']:.2f} "
              f"JB p={d['jarque_bera_p']:.2e} t-df={d['student_t_fit_full_sample']['df']:.2f} "
              f">4σ: {d['exceedances']['4sigma']['empirical_count']} obs vs {d['exceedances']['4sigma']['gaussian_expected_count']:.2f} expected")
        for a in ALPHAS:
            bt = results["backtests"][n][str(a)]["models"]
            print(f"  VaR {int(a*100)}%: " + " | ".join(f"{m}: {v['violations']}/{v['expected_violations']:.0f} exp, Kupiec p={v['kupiec_p']:.3f}, cc p={v['p_cc']:.3f}" for m, v in bt.items()))
    print("wrote results.json and", len(list(FIG.glob("*.png"))), "figures")


if __name__ == "__main__":
    main()
