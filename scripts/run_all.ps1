# Run every empirical paper end to end, one at a time, each logging to papers/<id>/run.log.
# Order: the CPU-heavy model fits first (P5, P2), then the two latency-sensitive benchmarks (P4, P3), which also wait for a
# quiet machine themselves (see papers/benchenv.py).
$ErrorActionPreference = "Continue"
$papers = Join-Path $PSScriptRoot "..\papers"
$env:PYTHONIOENCODING = "utf-8"
$jobs = @(@("p5-fraud-imbalance", "analysis.py"), @("p2-ml-returns", "analysis.py"), @("p4-ann-frontiers", "benchmark.py"), @("p3-tail-latency", "harness.py"))
foreach ($j in $jobs) {
    $id = $j[0]; $script = $j[1]
    "=== $id start $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Tee-Object -FilePath (Join-Path $papers "run_all.log") -Append
    Push-Location (Join-Path $papers $id)
    $p = Start-Process -FilePath "python" -ArgumentList "-u", $script -NoNewWindow -PassThru -Wait -RedirectStandardOutput "run.log" -RedirectStandardError "run.err.log"
    Pop-Location
    "=== $id end   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') exit=$($p.ExitCode)" | Tee-Object -FilePath (Join-Path $papers "run_all.log") -Append
}
