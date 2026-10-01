# Run every empirical paper end to end, one at a time, each logging to papers/<id>/run.log.
# Order: the CPU-heavy model fits first (P5, P2), then the two latency-sensitive benchmarks (P4, P3), which also wait for a
# quiet machine themselves (see papers/benchenv.py).
#
#   & scripts\run_all.ps1                                   # everything
#   & scripts\run_all.ps1 -Only p4-ann-frontiers,p3-tail-latency -ScriptArgs @{ "p4-ann-frontiers" = "--resume" }
#
# Launch it detached (Start-Process powershell -ArgumentList "-File", ...) if the calling shell might be closed; a run takes
# hours and a killed parent shell takes its children with it.
param([string[]]$Only = @(), [hashtable]$ScriptArgs = @{})
$ErrorActionPreference = "Continue"
$papers = Join-Path $PSScriptRoot "..\papers"
$env:PYTHONIOENCODING = "utf-8"
$jobs = @(@("p5-fraud-imbalance", "analysis.py"), @("p2-ml-returns", "analysis.py"), @("p4-ann-frontiers", "benchmark.py"), @("p3-tail-latency", "harness.py"))
foreach ($j in $jobs) {
    $id = $j[0]; $script = $j[1]
    if ($Only.Count -gt 0 -and $Only -notcontains $id) { continue }
    $argList = @("-u", $script)
    if ($ScriptArgs.ContainsKey($id)) { $argList += $ScriptArgs[$id] }
    # Add-Content with an explicit encoding: Tee-Object -FilePath writes UTF-16 in Windows PowerShell 5.1
    $line = "=== $id start $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') args=$($argList -join ' ')"
    $line; Add-Content -Path (Join-Path $papers "run_all.log") -Value $line -Encoding UTF8
    Push-Location (Join-Path $papers $id)
    $p = Start-Process -FilePath "python" -ArgumentList $argList -NoNewWindow -PassThru -Wait -RedirectStandardOutput "run.log" -RedirectStandardError "run.err.log"
    Pop-Location
    $line = "=== $id end   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') exit=$($p.ExitCode)"
    $line; Add-Content -Path (Join-Path $papers "run_all.log") -Value $line -Encoding UTF8
}
