#!/usr/bin/env bash
# Run every empirical paper end to end, one at a time, each logging to papers/<id>/run.log.
# Order: the two latency-sensitive benchmarks first (P3, P4) on a quiet machine, then the CPU-heavy model fits (P5, P2).
set -u
cd "$(dirname "$0")/../papers"
for id in p3-tail-latency p4-ann-frontiers p5-fraud-imbalance p2-ml-returns; do
  script=analysis.py; [ "$id" = p3-tail-latency ] && script=harness.py; [ "$id" = p4-ann-frontiers ] && script=benchmark.py
  echo "=== $id start $(date '+%F %T')" | tee -a run_all.log
  ( cd "$id" && PYTHONIOENCODING=utf-8 python -u "$script" > run.log 2>&1 ); rc=$?
  echo "=== $id end   $(date '+%F %T') exit=$rc" | tee -a run_all.log
done
