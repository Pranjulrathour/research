# Research — Pranjul Rathour

Code, data provenance and manuscripts behind my papers and books. Every number in every paper is produced by a script in
this repository from a dated snapshot of public data. `SNAPSHOT.json` in each paper's `data/` folder records the source,
URL, licence, download date and the SHA-256 hash of every file used. The data files themselves are not committed: the
market data are licensed by their index providers, and the benchmark datasets are large. `python papers/fetch_data.py all`
downloads everything and reports, file by file, whether the download matches the hashed snapshot. On 1 October 2026 it
reproduced the P1 and P5 files and the P2 S&P 500 file byte for byte; the P2 Dow 30 adjusted closes differed from the
snapshot by at most 1.5 parts per million, which is Yahoo's own rounding.

## Papers

| ID | Title | Data | Reproduce |
|---|---|---|---|
| P1 | Fat tails and the failure of Gaussian risk models: out-of-sample Value-at-Risk evidence from NIFTY 50 and S&P 500, 2010–2026 | Daily index closes (Yahoo Finance via `yfinance`) | `cd papers/p1-fat-tails && python analysis.py` |
| P2 | Do machine-learning return predictors beat linear baselines out of sample? A small-scale replication on public equity data | Dow 30 adjusted closes + S&P 500 | `cd papers/p2-ml-returns && python analysis.py` |
| P3 | Tail latency under load: an empirical comparison of threaded, async and hybrid API server designs | Own benchmark harness (no external data) | `cd papers/p3-tail-latency && python harness.py` |
| P4 | Recall–latency frontiers of approximate nearest-neighbour indexes on public datasets | ann-benchmarks.com SIFT-128, GloVe-100 | `cd papers/p4-ann-frontiers && python benchmark.py` |
| P5 | Card-fraud detection under extreme class imbalance: a reproducible benchmark on public data | ULB credit-card dataset (OpenML 1597) | `cd papers/p5-fraud-imbalance && python analysis.py` |

Each paper folder contains the script, `results.json` (the exact numbers quoted in the paper), `figures/`, the manuscript
(`paper.md`), and `defence.md` (the three findings, the method, the limitations, and the questions I expect to be asked).
Every script accepts `--plots-only` to redraw its figures from a previous run's saved results without re-running the
experiment.

Shared tooling in `papers/`:

| File | What it does |
|---|---|
| `fetch_data.py` | Downloads each paper's public data and checks it against the hashes in `SNAPSHOT.json`. |
| `benchenv.py` | Quiet-machine gate for the timing benchmarks (P3, P4): waits until other processes use under 0.75 of a core and 4 GB of RAM is free, then records the background load in `results.json`. |
| `plotstyle.py` | One figure style for all papers (STIX Two, ink plus one accent, hairlines). |
| `schematics.py` | The method diagrams (`figures/fig0_*.png`, Figure 1 in each paper). |
| `build_paper.py` | Typesets `paper.md` as an A4 preprint PDF, or IEEE-style two-column with `--two-column`. |

Logs named `run_first_attempt_*.log` (and the later `run_*_attempt_*` files in P4) are kept on purpose: they are the
failed or discarded runs described in each paper's revision record. P4's `compare_attempts.py` and
`merge_glove_attempts.py` show how its GloVe timings were taken from three attempts, and `benchmark.py --resume` keeps
completed datasets when a run is interrupted.

## Books

| | Title | Folder |
|---|---|---|
| 1 | The AGI Transition: A Field Guide for the Next Decade | `books/agi-transition/` |
| 2 | Systems That Scale: The Engineering Judgment Behind Reliable, Low-Latency Software | `books/systems-that-scale/` |

Build a book: `cd books && python make_cover.py && python build_book.py <folder>` → `books/<folder>/build/*.{html,epub,pdf}`.
Lint a book: `python books/lint_book.py <folder>`.
Build a paper PDF: `cd papers && python build_paper.py <paper-folder> [--two-column]`.

## Publishing
Venue-by-venue field values, identity settings and the order of operations are in `docs/SUBMISSION_CHECKLISTS.md`.

## Environment
Python 3.13; `pip install -r requirements.txt`. Machine specs for the benchmark papers (P3, P4) are recorded in their
`results.json` under `meta`, because absolute latency numbers depend on them; the comparisons within a paper do not.
PDFs are produced with headless Chrome (Playwright's `chrome-headless-shell` if present). Fonts are in
`books/assets/fonts/`, all under the SIL Open Font License: Source Serif 4, Inter, JetBrains Mono, Bodoni Moda and Archivo
for the books and covers, and STIX Two Text for the papers.

## Licence
Code: MIT. Manuscripts: © Pranjul Rathour, all rights reserved. Data: as per each source's licence (recorded per paper).

## Contact
pranjulrathour41@gmail.com · https://pranjulrathour.com

GitHub [Pranjulrathour](https://github.com/Pranjulrathour) · LinkedIn [pranjul-rathour](https://www.linkedin.com/in/pranjul-rathour/) · X [@PranjulRathourx](https://x.com/PranjulRathourx) · Instagram [@pranjulrathour.in](https://www.instagram.com/pranjulrathour.in/) · Threads [@pranjulrathour.in](https://www.threads.com/@pranjulrathour.in) · Bluesky [@pranjulrathour.bsky.social](https://bsky.app/profile/pranjulrathour.bsky.social) · [Facebook](https://www.facebook.com/profile.php?id=1377591238763842) · Dev.to [pranjulrathour](https://dev.to/pranjulrathour) · [Hashnode](https://pranjulrathour.hashnode.dev) · [Blogger](https://pranjulrathourtechguru.blogspot.com)
