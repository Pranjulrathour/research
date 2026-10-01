"""Download the public datasets the papers use, into each paper's data/ folder, and check them against the hashes recorded
in that folder's SNAPSHOT.json.

Usage:
    python fetch_data.py p1            # one paper (p1, p2, p4, p5; P3 needs no external data)
    python fetch_data.py all
    python fetch_data.py p1 --record   # (author only) write the SHA-256 of the current files into SNAPSHOT.json

The data are not redistributed in this repository. Index levels and prices are licensed by their providers (NSE Indices,
S&P Dow Jones Indices) and reach Yahoo Finance under those licences; the ANN and fraud datasets are large. Yahoo revises
history occasionally (and adjusted closes change after every dividend), so a fresh download can differ from the snapshot
the papers used. A hash mismatch is reported, not hidden: the numbers in each results.json belong to the hashed files.
"""
from __future__ import annotations
import hashlib, json, os, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
END = "2026-10-01"   # exclusive end date used for every Yahoo download: last row is 2026-09-30


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, out: Path) -> None:
    """Resumable download (the large files sometimes drop mid-transfer)."""
    have = out.stat().st_size if out.exists() else 0
    for attempt in range(8):
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={have}-"} if have else {})
            with urllib.request.urlopen(req, timeout=60) as r, open(out, "ab") as f:
                if have and r.status == 200:      # server ignored the range: start again
                    f.truncate(0); have = 0
                while chunk := r.read(1 << 20):
                    f.write(chunk); have += len(chunk)
            return
        except Exception as e:  # noqa: BLE001
            print(f"  retry {attempt + 1} after: {e}", flush=True); time.sleep(3)
    raise RuntimeError(f"download failed: {url}")


def yahoo_close(ticker: str, start: str, adjusted: bool):
    import yfinance as yf
    df = yf.download(ticker, start=start, end=END, auto_adjust=adjusted, progress=False, threads=False)
    s = df["Close"]
    return s.iloc[:, 0] if getattr(s, "ndim", 1) == 2 and s.shape[1] == 1 else s


def fetch_p1(d: Path) -> list[Path]:
    # both series start on 2007-09-17, the first NIFTY 50 date on Yahoo, so the two files cover the same span
    out = []
    for name, ticker in (("NIFTY50", "^NSEI"), ("SP500", "^GSPC")):
        p = d / f"{name}_daily_close.csv"
        s = yahoo_close(ticker, "2007-09-17", adjusted=False).dropna()
        s.rename("Close").to_frame().rename_axis("Date").to_csv(p)
        out.append(p)
    return out


DOW30 = ["AAPL", "AMGN", "AMZN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "GS", "HD", "HON", "IBM", "JNJ", "JPM",
         "KO", "MCD", "MMM", "MRK", "MSFT", "NKE", "NVDA", "PG", "SHW", "TRV", "UNH", "V", "VZ", "WMT"]


def fetch_p2(d: Path) -> list[Path]:
    import yfinance as yf
    px = yf.download(DOW30, start="2004-01-01", end=END, auto_adjust=True, progress=False, threads=False)["Close"]
    p1 = d / "dow30_adj_close.csv"; px[DOW30].rename_axis("Date").to_csv(p1)
    p2 = d / "sp500_close.csv"
    yahoo_close("^GSPC", "2004-01-01", adjusted=False).dropna().rename("Close").to_frame().rename_axis("Date").to_csv(p2)
    return [p1, p2]


def fetch_p4(d: Path) -> list[Path]:
    snap = json.loads((d / "SNAPSHOT.json").read_text(encoding="utf-8"))
    out = []
    for fname, info in snap["files"].items():
        p = d / fname
        if not p.exists() or p.stat().st_size != info["bytes"]:
            print(f"  downloading {fname} ({info['bytes'] / 2**20:.0f} MB)", flush=True); download(info["url"], p)
        out.append(p)
    return out


def fetch_p5(d: Path) -> list[Path]:
    import pandas as pd
    from scipy.io import arff
    snap = json.loads((d / "SNAPSHOT.json").read_text(encoding="utf-8"))
    raw = d / "creditcard.arff"
    if not raw.exists() or raw.stat().st_size != snap["bytes_arff"]:
        print("  downloading creditcard.arff (144 MB)", flush=True); download(snap["url_file"], raw)
    # read the ARFF's @data section as CSV text with pandas' default C float parser (how the snapshot CSV was built; it can
    # differ from an exact parse in the last digit, which is why the snapshot hash is checked); Class is quoted ('0'/'1')
    cols, skip = [], 0
    with open(raw, encoding="utf-8") as f:
        for skip, line in enumerate(f, 1):
            if line.lower().startswith("@attribute"):
                cols.append(line.split()[1])
            elif line.lower().startswith("@data"):
                break
    df = pd.read_csv(raw, skiprows=skip, header=None, names=cols, quotechar="'",
                     dtype={"Time": float, "Class": int})
    csv = d / "creditcard.csv"; df.to_csv(csv, index=False)
    return [raw, csv]


FETCH = {"p1": ("p1-fat-tails", fetch_p1), "p2": ("p2-ml-returns", fetch_p2), "p4": ("p4-ann-frontiers", fetch_p4),
         "p5": ("p5-fraud-imbalance", fetch_p5)}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    record = "--record" in sys.argv
    which = list(FETCH) if not args or args[0] == "all" else args
    status = 0
    for key in which:
        folder, fn = FETCH[key]
        d = HERE / folder / "data"; d.mkdir(parents=True, exist_ok=True)
        snap_p = d / "SNAPSHOT.json"
        snap = json.loads(snap_p.read_text(encoding="utf-8"))
        if record:
            files = sorted(p for p in d.iterdir() if p.name != "SNAPSHOT.json" and p.is_file())
        else:
            print(f"{key}: fetching into {d}", flush=True)
            files = fn(d)
        hashes = {p.name: {"sha256": sha256(p), "bytes": p.stat().st_size} for p in files}
        if record:
            snap["sha256"] = hashes
            snap_p.write_text(json.dumps(snap, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"{key}: recorded hashes for {', '.join(hashes)}")
            continue
        want = snap.get("sha256", {})
        for name, h in hashes.items():
            if name not in want:
                print(f"  {name}: no recorded hash")
            elif want[name]["sha256"] == h["sha256"]:
                print(f"  {name}: matches the snapshot the paper used")
            else:
                status = 1
                print(f"  {name}: DIFFERS from the snapshot the paper used ({h['bytes']:,} bytes vs {want[name]['bytes']:,});"
                      " results may differ slightly")
    sys.exit(status)


if __name__ == "__main__":
    main()
