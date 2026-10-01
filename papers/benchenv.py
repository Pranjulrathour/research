"""Benchmark hygiene shared by P3 and P4: wait for a quiet machine, and record the background load a run was taken under.

A laptop is not a lab. Latency and throughput numbers taken while another program is using two cores, or while the machine
is short of memory, are not comparable with numbers taken on an idle machine; on the author's laptop an Android emulator
running in the background cut multi-threaded FAISS throughput by an order of magnitude in one aborted run (2026-10-01).
So every benchmark run (1) waits until other processes are using less than MAX_OTHER_CORES and at least MIN_FREE_GB of RAM
is available, and (2) records, in results.json, what else was running when it started and at each checkpoint.
"""
from __future__ import annotations
import os, time

import psutil

MAX_OTHER_CORES = 0.75
MIN_FREE_GB = 4.0


def sample_load(seconds: float = 5.0, top: int = 6) -> dict:
    """CPU use of every other process over `seconds`, in cores, plus memory headroom."""
    me = psutil.Process(os.getpid())
    mine = {me.pid} | {c.pid for c in me.children(recursive=True)}
    procs = {}
    for p in psutil.process_iter(["pid", "name"]):
        try:
            p.cpu_percent(None); procs[p.pid] = p
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    time.sleep(seconds)
    usage = []
    for pid, p in procs.items():
        if pid in mine or pid == 0:
            continue
        try:
            c = p.cpu_percent(None) / 100.0
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if c > 0.02:
            usage.append((p.info["name"], round(c, 2)))
    usage.sort(key=lambda x: -x[1])
    vm = psutil.virtual_memory()
    return {"other_cores_used": round(sum(c for _, c in usage), 2), "top_other_processes": usage[:top],
            "ram_available_gb": round(vm.available / 2**30, 1), "ram_total_gb": round(vm.total / 2**30, 1),
            "sampled_utc": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())}


def wait_for_quiet(max_wait_min: float = 120, poll_s: float = 60, log=print) -> dict:
    """Block until the machine is quiet enough, or until max_wait_min passes; return the last sample with a verdict."""
    t0 = time.time()
    while True:
        s = sample_load()
        quiet = s["other_cores_used"] <= MAX_OTHER_CORES and s["ram_available_gb"] >= MIN_FREE_GB
        s["quiet"] = quiet
        if quiet or time.time() - t0 > max_wait_min * 60:
            s["waited_min"] = round((time.time() - t0) / 60, 1)
            log(f"[benchenv] start sample: other cores {s['other_cores_used']}, RAM free {s['ram_available_gb']} GB, "
                f"quiet={quiet}, waited {s['waited_min']} min, top: {s['top_other_processes'][:3]}")
            return s
        log(f"[benchenv] waiting for a quiet machine: other cores {s['other_cores_used']} (max {MAX_OTHER_CORES}), "
            f"RAM free {s['ram_available_gb']} GB (min {MIN_FREE_GB}); top: {s['top_other_processes'][:3]}")
        time.sleep(poll_s)
