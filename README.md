# Research — Pranjul Rathour

Code, data snapshots and manuscripts behind my papers and books. Every number in every paper is produced by a script in this
repository from a dated snapshot of public data; `SNAPSHOT.json` in each paper's `data/` folder records the source, URL,
licence and download date. Raw data files are not committed (they are large and re-downloadable); the scripts fetch or
expect them as documented.

## Papers

| ID | Title | Data | Reproduce |
|---|---|---|---|
| P1 | Fat tails and the failure of Gaussian risk models: evidence from NIFTY 50 and S&P 500, 2010–2026 | Daily index closes (Yahoo Finance via `yfinance`) | `cd papers/p1-fat-tails && python analysis.py` |
| P2 | Do machine-learning return predictors beat linear baselines out of sample? A small-scale replication on public equity data | Dow 30 adjusted closes + S&P 500 | `cd papers/p2-ml-returns && python analysis.py` |
| P3 | Tail latency under load: an empirical comparison of threaded, async and hybrid API server designs | Own benchmark harness (no external data) | `cd papers/p3-tail-latency && python harness.py` |
| P4 | Recall–latency frontiers of approximate nearest-neighbour indexes on public datasets | ann-benchmarks.com SIFT-128, GloVe-100 | `cd papers/p4-ann-frontiers && python benchmark.py` |
| P5 | Card-fraud detection under extreme class imbalance: a reproducible benchmark on public data | ULB credit-card dataset (OpenML 1597) | `cd papers/p5-fraud-imbalance && python analysis.py` |

Each paper folder contains the script, `results.json` (the exact numbers quoted in the paper), `figures/`, the manuscript
(`paper.md`), and `defence.md` (the three findings, the method, the limitations, and the questions I expect to be asked).

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
PDFs are produced with headless Chrome or Edge; fonts (Inter, Source Serif 4, Instrument Serif, JetBrains Mono; all OFL)
are in `books/assets/fonts/`.

## Licence
Code: MIT. Manuscripts: © Pranjul Rathour, all rights reserved. Data: as per each source's licence (recorded per paper).

## Contact
pranjulrathour41@gmail.com · https://pranjulrathour.scult.in
