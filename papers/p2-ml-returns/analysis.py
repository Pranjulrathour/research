"""P2 -- Do machine-learning return predictors beat linear baselines out of sample?
       A small-scale replication on public equity data (Dow 30 constituents, 2004-2026).

Reproduce:  python analysis.py        (reads data/dow30_adj_close.csv, data/sp500_close.csv; writes results.json, figures/)

Design, fixed before running:
  * Universe: the 30 current Dow Jones Industrial Average constituents (survivorship-biased by construction; the paper
    says so and argues the bias affects return LEVELS, not the relative ranking of forecasting methods, which is the object).
  * Frequency: monthly. For each stock and month-end t, features use prices up to t; the target is the stock's log return
    over month t+1. One row per stock-month.
  * Features (standard, from the empirical asset-pricing literature; nothing invented):
      ret_1m (short-term reversal), mom_12_1 (12-1 month momentum), mom_6_1, vol_1m, vol_12m (realised volatility of
      daily returns), max_1m (largest daily return in the month), beta_12m (vs S&P 500), mkt_1m, mkt_12m (market returns,
      identical across stocks in a month), and the month-of-year as an integer.
    Features are rank-normalised cross-sectionally within each month to [-1, 1] (Gu, Kelly & Xiu 2020 practice).
  * Target: next-month log return, and a demeaned version (minus the month's cross-sectional mean) for the relative test.
  * Models: zero forecast, expanding historical mean, OLS, ridge, lasso, random forest, gradient boosting (HistGB), and a
    small MLP (two hidden layers of 32). Regularisation strength and tree depth are chosen on a VALIDATION block
    (the last 24 months of each training window), never on the test year.
  * Protocol: walk-forward by calendar year. Train on all months up to December of year Y-1 (first training window
    2004-2011, i.e. at least 8 years), test on year Y, for Y = 2012 .. 2026 (2026 through September). Expanding window.
  * Metrics: pooled out-of-sample R^2 against a zero forecast (GKX definition) and against the historical mean;
    directional accuracy; Diebold-Mariano test of each model's squared-error loss against OLS; a monthly long-short
    portfolio (top 6 minus bottom 6 predicted) with annualised Sharpe and a block-bootstrap 90% interval.
  * Leak demonstration: the same models evaluated with a shuffled 5-fold cross-validation over stock-months (the wrong
    way), to quantify how much apparent skill comes from look-ahead.
  * Seeds 0-4 for the stochastic models; results report mean and sd across seeds.
Nothing is tuned on the test years.
"""
from __future__ import annotations
import json, warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
SEEDS = (0, 1, 2, 3, 4)
FIRST_TEST_YEAR, LAST_TEST_YEAR = 2012, 2026
VALID_MONTHS = 24
FEATURES = ["ret_1m", "mom_12_1", "mom_6_1", "vol_1m", "vol_12m", "max_1m", "beta_12m", "mkt_1m", "mkt_12m", "month"]


# ----------------------------------------------------------------------------- data
def build_panel() -> pd.DataFrame:
    px = pd.read_csv(HERE / "data" / "dow30_adj_close.csv", parse_dates=["Date"], index_col="Date").sort_index()
    spx = pd.read_csv(HERE / "data" / "sp500_close.csv", parse_dates=["Date"], index_col="Date").sort_index().iloc[:, 0]
    dropped = [c for c in px.columns if px[c].notna().sum() < int(0.95 * len(px))]
    px = px.drop(columns=dropped)                                # tickers listed after 2004 lack a full history
    r = np.log(px).diff()
    rm = np.log(spx).diff().reindex(r.index)
    rows = []
    month_ends = r.resample("ME").last().index
    for i in range(12, len(month_ends) - 1):
        t = month_ends[i]
        past12 = r.loc[month_ends[i - 12] + pd.Timedelta(days=1): t]
        past1 = r.loc[month_ends[i - 1] + pd.Timedelta(days=1): t]
        past6 = r.loc[month_ends[i - 6] + pd.Timedelta(days=1): t]
        nxt = r.loc[t + pd.Timedelta(days=1): month_ends[i + 1]]
        m12, m1 = rm.loc[past12.index], rm.loc[past1.index]
        for s in r.columns:
            x12, x1, x6, y = past12[s].dropna(), past1[s].dropna(), past6[s].dropna(), nxt[s].dropna()
            if len(x12) < 200 or len(x1) < 15 or len(y) < 15:
                continue
            cov = np.cov(x12.values, m12.loc[x12.index].values)
            rows.append({"date": t, "ticker": s, "year": t.year, "month": t.month,
                         "ret_1m": x1.sum(), "mom_12_1": x12.sum() - x1.sum(), "mom_6_1": x6.sum() - x1.sum(),
                         "vol_1m": x1.std(ddof=1), "vol_12m": x12.std(ddof=1), "max_1m": x1.max(),
                         "beta_12m": cov[0, 1] / cov[1, 1] if cov[1, 1] > 0 else np.nan,
                         "mkt_1m": m1.sum(), "mkt_12m": m12.sum(),
                         "target": y.sum()})
    df = pd.DataFrame(rows).dropna()
    df.attrs["dropped_tickers"] = dropped
    df["target_dm"] = df["target"] - df.groupby("date")["target"].transform("mean")
    # cross-sectional rank normalisation to [-1, 1] within each month for stock-level features; market features are
    # identical across stocks in a month, so they are scaled by their own past (expanding) standard deviation instead,
    # using only data up to that month; month-of-year is mapped to [-1, 1]
    for f in FEATURES:
        if f == "month":
            df[f] = (df[f] - 6.5) / 5.5
        elif f.startswith("mkt_"):
            m = df.groupby("date")[f].first()
            scale = m.expanding(min_periods=12).std().bfill()
            df[f] = df["date"].map(m / scale)
        else:
            df[f] = df.groupby("date")[f].rank(pct=True) * 2 - 1
    return df.reset_index(drop=True)


# ----------------------------------------------------------------------------- models
def make_model(name: str, hp: dict, seed: int):
    if name == "ols": return LinearRegression()
    if name == "ridge": return Ridge(alpha=hp["alpha"])
    if name == "lasso": return Lasso(alpha=hp["alpha"], max_iter=5000)
    if name == "rf": return RandomForestRegressor(n_estimators=300, max_depth=hp["depth"], min_samples_leaf=20, n_jobs=-1, random_state=seed)
    if name == "hgb": return HistGradientBoostingRegressor(max_depth=hp["depth"], learning_rate=0.03, max_iter=300, l2_regularization=1.0, random_state=seed)
    if name == "mlp": return make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(32, 32), alpha=hp["alpha"], max_iter=400, early_stopping=True, random_state=seed))
    raise ValueError(name)


GRIDS = {"ols": [{}], "ridge": [{"alpha": a} for a in (0.1, 1, 10, 100)], "lasso": [{"alpha": a} for a in (1e-4, 1e-3, 1e-2)],
         "rf": [{"depth": d} for d in (3, 6, None)], "hgb": [{"depth": d} for d in (2, 3, 5)], "mlp": [{"alpha": a} for a in (1e-3, 1e-2, 1e-1)]}
STOCHASTIC = {"rf", "hgb", "mlp"}


def select_hp(name, Xtr, ytr, Xva, yva, seed):
    best, best_mse = None, np.inf
    for hp in GRIDS[name]:
        m = make_model(name, hp, seed).fit(Xtr, ytr)
        mse = float(np.mean((m.predict(Xva) - yva) ** 2))
        if mse < best_mse: best, best_mse = hp, mse
    return best


def r2_oos(y, yhat, bench):
    return float(1 - np.sum((y - yhat) ** 2) / np.sum((y - bench) ** 2))


def diebold_mariano(e1, e2, h=1):
    """DM test on squared-error loss differential d = e1^2 - e2^2 (positive => model 2 better). HAC variance, lag h-1."""
    d = e1 ** 2 - e2 ** 2
    n = len(d); dbar = d.mean()
    gamma0 = np.sum((d - dbar) ** 2) / n
    var = gamma0
    for k in range(1, h):
        gk = np.sum((d[k:] - dbar) * (d[:-k] - dbar)) / n
        var += 2 * gk
    dm = dbar / np.sqrt(var / n) if var > 0 else 0.0
    return float(dm), float(2 * stats.norm.sf(abs(dm)))


def long_short(df_pred: pd.DataFrame, col: str, k: int = 6) -> pd.Series:
    out = {}
    for d, g in df_pred.groupby("date"):
        g = g.sort_values(col)
        out[d] = g["target"].iloc[-k:].mean() - g["target"].iloc[:k].mean()
    return pd.Series(out).sort_index()


def sharpe(x: pd.Series) -> float:
    return float(x.mean() / x.std(ddof=1) * np.sqrt(12)) if x.std(ddof=1) > 0 else 0.0


def block_bootstrap_sharpe(x: pd.Series, n_boot=2000, block=6, seed=0):
    rng = np.random.default_rng(seed); v = x.values; n = len(v); out = []
    for _ in range(n_boot):
        idx = np.concatenate([np.arange(s, s + block) % n for s in rng.integers(0, n, size=n // block + 1)])[:n]
        out.append(sharpe(pd.Series(v[idx])))
    return [float(np.quantile(out, 0.05)), float(np.quantile(out, 0.95))]


# ----------------------------------------------------------------------------- protocol
def walk_forward(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, dict]:
    preds = df[["date", "ticker", "year", "target", "target_dm"]].copy()
    chosen = {}
    for name in GRIDS:
        for seed in (SEEDS if name in STOCHASTIC else (0,)):
            col = f"{name}_s{seed}"
            preds[col] = np.nan
            for Y in range(FIRST_TEST_YEAR, LAST_TEST_YEAR + 1):
                tr = df[df.year < Y]; te = df[df.year == Y]
                if te.empty: continue
                cut = tr["date"].sort_values().unique()[-VALID_MONTHS]
                tr_fit, tr_val = tr[tr.date < cut], tr[tr.date >= cut]
                hp = select_hp(name, tr_fit[FEATURES].values, tr_fit[target].values, tr_val[FEATURES].values, tr_val[target].values, seed)
                chosen.setdefault(name, {})[str(Y)] = hp
                m = make_model(name, hp, seed).fit(tr[FEATURES].values, tr[target].values)   # refit on full training window
                preds.loc[te.index, col] = m.predict(te[FEATURES].values)
            print(f"  walk-forward {target:9s} {col:10s} done", flush=True)
    # expanding historical mean benchmark (train-period mean of the target), by test year
    preds["histmean"] = np.nan
    for Y in range(FIRST_TEST_YEAR, LAST_TEST_YEAR + 1):
        preds.loc[preds.year == Y, "histmean"] = df.loc[df.year < Y, target].mean()
    return preds.dropna(subset=[c for c in preds.columns if c.endswith("_s0")]), chosen


def evaluate(preds: pd.DataFrame, target: str) -> dict:
    y = preds[target].values
    out = {"n_obs": int(len(preds)), "n_months": int(preds["date"].nunique()), "n_tickers": int(preds["ticker"].nunique()),
           "first_test": str(preds["date"].min().date()), "last_test": str(preds["date"].max().date()),
           "models": {}}
    e_ols = y - preds["ols_s0"].values
    hm = preds["histmean"].values
    out["benchmarks"] = {"zero": {"r2_vs_zero": 0.0, "mse": float(np.mean(y ** 2))},
                         "histmean": {"r2_vs_zero": r2_oos(y, hm, 0.0), "mse": float(np.mean((y - hm) ** 2))}}
    for name in GRIDS:
        cols = [c for c in preds.columns if c.startswith(name + "_s")]
        per_seed = []
        for c in cols:
            yhat = preds[c].values; e = y - yhat
            dm, dmp = diebold_mariano(e_ols, e)
            ls = long_short(preds, c)
            per_seed.append({"r2_vs_zero": r2_oos(y, yhat, 0.0), "r2_vs_histmean": r2_oos(y, yhat, hm),
                             "mse": float(np.mean(e ** 2)), "dir_acc": float(np.mean(np.sign(yhat) == np.sign(y))),
                             "dm_vs_ols": dm, "dm_p": dmp,
                             "ls_mean_monthly": float(ls.mean()), "ls_sharpe": sharpe(ls), "ls_sharpe_ci90": block_bootstrap_sharpe(ls),
                             "ls_by_year": {str(k): float(v) for k, v in ls.groupby(ls.index.year).sum().items()}})
        agg = {k: {"mean": float(np.mean([p[k] for p in per_seed])), "sd": float(np.std([p[k] for p in per_seed], ddof=1)) if len(per_seed) > 1 else 0.0}
               for k in ("r2_vs_zero", "r2_vs_histmean", "mse", "dir_acc", "dm_vs_ols", "dm_p", "ls_mean_monthly", "ls_sharpe")}
        agg["ls_sharpe_ci90_seed0"] = per_seed[0]["ls_sharpe_ci90"]
        agg["ls_by_year_seed0"] = per_seed[0]["ls_by_year"]
        agg["n_seeds"] = len(per_seed)
        out["models"][name] = agg
    return out


def leaky_cv(df: pd.DataFrame, target: str) -> dict:
    """The wrong way: shuffled K-fold over stock-months. Reported only to quantify look-ahead inflation."""
    X, y = df[FEATURES].values, df[target].values
    out = {}
    for name in GRIDS:
        r2s = []
        for seed in (SEEDS[:2] if name in STOCHASTIC else (0,)):
            yhat = np.zeros_like(y)
            for tr, te in KFold(5, shuffle=True, random_state=seed).split(X):
                hp = GRIDS[name][len(GRIDS[name]) // 2]
                yhat[te] = make_model(name, hp, seed).fit(X[tr], y[tr]).predict(X[te])
            r2s.append(r2_oos(y, yhat, 0.0))
        out[name] = {"r2_vs_zero_shuffled_cv": float(np.mean(r2s))}
        print(f"  leaky cv {name} done", flush=True)
    return out


def plots(res: dict, preds_raw: pd.DataFrame) -> None:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    names = list(GRIDS)
    # 1. OOS R^2 walk-forward vs leaky CV
    fig, ax = plt.subplots(figsize=(8, 3.8))
    wf = [res["walk_forward"]["raw"]["models"][n]["r2_vs_zero"]["mean"] * 100 for n in names]
    lk = [res["leaky_cv"]["raw"][n]["r2_vs_zero_shuffled_cv"] * 100 for n in names]
    xs = np.arange(len(names)); w = 0.38
    ax.bar(xs - w / 2, wf, w, color="#1c1b22", label="walk-forward (honest)")
    ax.bar(xs + w / 2, lk, w, color="#ff4d2e", label="shuffled 5-fold CV (look-ahead)")
    ax.axhline(0, color="grey", lw=0.8); ax.set_xticks(xs); ax.set_xticklabels([n.upper() for n in names])
    ax.set_ylabel("out-of-sample R² vs zero forecast (%)"); ax.legend(frameon=False)
    ax.set_title("Monthly return prediction, Dow 30, test years 2012–2026")
    fig.tight_layout(); fig.savefig(FIG / "fig1_r2_honest_vs_leaky.png", dpi=160); plt.close(fig)
    # 2. Long-short cumulative returns (seed 0) for OLS, HGB, RF, MLP
    fig, ax = plt.subplots(figsize=(9, 3.8))
    for n, c in (("ols", "#1c1b22"), ("ridge", "#5b5a66"), ("hgb", "#ff4d2e"), ("rf", "#b8321a"), ("mlp", "#8a8f9c")):
        ls = long_short(preds_raw, f"{n}_s0").cumsum()
        ax.plot(ls.index, ls.values, lw=1.0, color=c, label=n.upper())
    ax.axhline(0, color="grey", lw=0.8); ax.set_ylabel("cumulative log return, top-6 minus bottom-6"); ax.legend(frameon=False, ncol=5, fontsize=8)
    ax.set_title("Long-short portfolio from each model's monthly forecasts (out of sample)")
    fig.tight_layout(); fig.savefig(FIG / "fig2_long_short_cumulative.png", dpi=160); plt.close(fig)
    # 3. Yearly R^2 by model (raw target)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    for n, c in (("ols", "#1c1b22"), ("hgb", "#ff4d2e"), ("rf", "#b8321a"), ("mlp", "#8a8f9c")):
        yr = {}
        for Y, g in preds_raw.groupby("year"):
            yr[Y] = r2_oos(g["target"].values, g[f"{n}_s0"].values, 0.0) * 100
        ax.plot(list(yr), list(yr.values()), marker="o", ms=3, lw=1.0, color=c, label=n.upper())
    ax.axhline(0, color="grey", lw=0.8); ax.set_ylabel("yearly OOS R² (%)"); ax.legend(frameon=False, ncol=4, fontsize=8)
    ax.set_title("Skill is unstable year to year"); fig.tight_layout(); fig.savefig(FIG / "fig3_yearly_r2.png", dpi=160); plt.close(fig)


def main():
    df = build_panel()
    print(f"panel: {len(df)} stock-months, {df.ticker.nunique()} tickers, {df.date.min().date()} .. {df.date.max().date()}", flush=True)
    res = {"meta": json.load(open(HERE / "data" / "SNAPSHOT.json")), "features": FEATURES, "seeds": list(SEEDS),
           "protocol": {"first_test_year": FIRST_TEST_YEAR, "last_test_year": LAST_TEST_YEAR, "validation_months": VALID_MONTHS,
                        "panel_rows": int(len(df)), "tickers": sorted(df.ticker.unique().tolist()),
                        "dropped_tickers_incomplete_history": df.attrs.get("dropped_tickers", [])},
           "walk_forward": {}, "hyperparameters_chosen": {}, "leaky_cv": {}}
    preds_raw = None
    for key, target in (("raw", "target"), ("demeaned", "target_dm")):
        preds, chosen = walk_forward(df, target)
        res["walk_forward"][key] = evaluate(preds, target)
        res["hyperparameters_chosen"][key] = chosen
        res["leaky_cv"][key] = leaky_cv(df, target)
        if key == "raw": preds_raw = preds
    json.dump(res, open(HERE / "results.json", "w"), indent=1, default=str)
    plots(res, preds_raw)
    for key in ("raw", "demeaned"):
        print(f"\n== {key} target ==  histmean R2 vs zero: {res['walk_forward'][key]['benchmarks']['histmean']['r2_vs_zero']*100:.2f}%")
        for n, m in res["walk_forward"][key]["models"].items():
            print(f"  {n:6s} R2 {m['r2_vs_zero']['mean']*100:6.2f}% (sd {m['r2_vs_zero']['sd']*100:.2f})  dir {m['dir_acc']['mean']*100:5.1f}%  "
                  f"DM vs OLS {m['dm_vs_ols']['mean']:+.2f} (p {m['dm_p']['mean']:.2f})  LS Sharpe {m['ls_sharpe']['mean']:+.2f}  "
                  f"leaky-CV R2 {res['leaky_cv'][key][n]['r2_vs_zero_shuffled_cv']*100:6.2f}%")
    print("wrote results.json and", len(list(FIG.glob("*.png"))), "figures")


if __name__ == "__main__":
    main()
