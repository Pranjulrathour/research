"""P3 -- Tail latency under load: threaded, async and hybrid API server designs.

One file holds the servers, the workload and the load generator, so the whole experiment is `python harness.py`.

Servers (all Python 3.13, same machine, one at a time, loopback, port 8899):
  threaded      stdlib ThreadingHTTPServer (one OS thread per connection)
  async         asyncio HTTP/1.1 server; IO-bound work awaited, CPU-bound work runs INLINE on the event loop (the classic mistake)
  hybrid_thread asyncio server; CPU-bound work offloaded to a THREAD pool (the common pattern; still under the GIL)
  hybrid_proc   asyncio server; CPU-bound work offloaded to a PROCESS pool (the pattern that actually uses the cores)
Workloads (per request, deterministic):
  io      simulated upstream call: sleep 20 ms (what an LLM / DB / network wait looks like to the server)
  cpu     ~3 ms of pure Python work (hashing loop) -- CPU-bound; the iteration count is calibrated and the measured ms recorded
  mixed   io then cpu
Load: closed-loop generator with C concurrent clients (C in CONCURRENCY), each sends N sequential requests on a keep-alive
connection; every request's latency is recorded; p50 / p95 / p99 / max and throughput reported. Three repeats per cell; the
repeat with the median p99 is kept. Closed loop means the arrival rate adapts to the server (it measures "what does each of C
clients experience", not "what happens at a fixed arrival rate"); the paper says so.
Caveats recorded in the paper: one machine, loopback network, Python-only servers (the point is the *design* comparison, not
absolute numbers), GIL present (whether the interpreter had the GIL enabled is recorded in meta).
"""
from __future__ import annotations
import asyncio, hashlib, json, multiprocessing as mp, os, platform, statistics, sys, time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORT = 8899
IO_MS = 20
CPU_ITERS = 20_000          # calibrated to ~3 ms on the author's machine; measured and recorded at run time
CONCURRENCY = (1, 8, 32, 128, 256)
REQUESTS_PER_CLIENT = 40
REPEATS = 3
WORKLOADS = ("io", "cpu", "mixed")
SERVERS = ("threaded", "async", "hybrid_thread", "hybrid_proc")


def cpu_work() -> str:
    h = b"x"
    for _ in range(CPU_ITERS):
        h = hashlib.blake2b(h, digest_size=16).digest()
    return h.hex()


# ------------------------------------------------------------------ servers
class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a): pass
    def do_GET(self):
        w = self.path.strip("/")
        if w in ("io", "mixed"): time.sleep(IO_MS / 1000)
        body = cpu_work().encode() if w in ("cpu", "mixed") else b"ok"
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


def serve_threaded():
    ThreadingHTTPServer.daemon_threads = True
    ThreadingHTTPServer(("127.0.0.1", PORT), _Handler).serve_forever()


async def _asyncio_server(mode: str):
    workers = os.cpu_count() or 4
    pool = {"async": None, "hybrid_thread": ThreadPoolExecutor(max_workers=workers), "hybrid_proc": ProcessPoolExecutor(max_workers=workers)}[mode]
    loop = asyncio.get_running_loop()
    if mode == "hybrid_proc":  # spin the worker processes up before the first request so they are not measured as latency
        await asyncio.gather(*[loop.run_in_executor(pool, cpu_work) for _ in range(workers * 2)])

    async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            while True:
                line = await reader.readline()
                if not line: break
                parts = line.split()
                path = parts[1].decode() if len(parts) > 1 else "/"
                while (await reader.readline()) not in (b"\r\n", b""): pass
                w = path.strip("/")
                if w in ("io", "mixed"): await asyncio.sleep(IO_MS / 1000)
                if w in ("cpu", "mixed"):
                    body = (cpu_work() if pool is None else await loop.run_in_executor(pool, cpu_work)).encode()
                else:
                    body = b"ok"
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\nConnection: keep-alive\r\n\r\n" % len(body) + body)
                await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()

    srv = await asyncio.start_server(handle, "127.0.0.1", PORT, backlog=1024)
    async with srv: await srv.serve_forever()


def serve_async(): asyncio.run(_asyncio_server("async"))
def serve_hybrid_thread(): asyncio.run(_asyncio_server("hybrid_thread"))
def serve_hybrid_proc(): asyncio.run(_asyncio_server("hybrid_proc"))
TARGETS = {"threaded": serve_threaded, "async": serve_async, "hybrid_thread": serve_hybrid_thread, "hybrid_proc": serve_hybrid_proc}


# ------------------------------------------------------------------ load generator (closed loop, asyncio clients)
async def _client(path: str, n: int, lat: list):
    reader, writer = await asyncio.open_connection("127.0.0.1", PORT)
    req = f"GET /{path} HTTP/1.1\r\nHost: x\r\nConnection: keep-alive\r\n\r\n".encode()
    for _ in range(n):
        t0 = time.perf_counter()
        writer.write(req); await writer.drain()
        await reader.readline(); length = 0
        while True:
            h = await reader.readline()
            if h in (b"\r\n", b""): break
            if h.lower().startswith(b"content-length:"): length = int(h.split(b":")[1])
        await reader.readexactly(length)
        lat.append((time.perf_counter() - t0) * 1e3)
    writer.close()


async def _load(path: str, c: int, n: int) -> dict:
    lat: list = []
    t0 = time.perf_counter()
    await asyncio.gather(*[_client(path, n, lat) for _ in range(c)])
    wall = time.perf_counter() - t0
    lat.sort()
    q = lambda p: lat[min(len(lat) - 1, int(p * len(lat)))]
    return {"n": len(lat), "wall_s": wall, "throughput_rps": len(lat) / wall, "p50_ms": q(0.50), "p95_ms": q(0.95),
            "p99_ms": q(0.99), "max_ms": lat[-1], "mean_ms": statistics.fmean(lat)}


def _wait_up(timeout=30):
    import socket
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(("127.0.0.1", PORT), timeout=0.5): return True
        except OSError: time.sleep(0.1)
    return False


def main():
    t0 = time.perf_counter(); cpu_work(); cpu_ms = (time.perf_counter() - t0) * 1e3
    gil = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True
    meta = {"python": platform.python_version(), "gil_enabled": gil, "platform": platform.platform(), "machine": platform.machine(),
            "processor": platform.processor(), "cpu_count": os.cpu_count(), "io_ms": IO_MS, "cpu_iters": CPU_ITERS,
            "cpu_work_measured_ms": round(cpu_ms, 2), "requests_per_client": REQUESTS_PER_CLIENT, "repeats": REPEATS,
            "concurrency": list(CONCURRENCY), "load_model": "closed loop, keep-alive, asyncio clients in a separate process",
            "run_utc": time.strftime("%Y-%m-%dT%H:%M", time.gmtime()), "network": "loopback, same machine"}
    print("cpu_work ~", round(cpu_ms, 2), "ms; GIL enabled:", gil, flush=True)
    rows = []
    for server in SERVERS:
        proc = mp.Process(target=TARGETS[server], daemon=True)
        proc.start()
        assert _wait_up(), f"{server} did not start"
        for w in WORKLOADS: asyncio.run(_load(w, 8, 10))   # warm-up every path
        for w in WORKLOADS:
            for c in CONCURRENCY:
                reps = [asyncio.run(_load(w, c, REQUESTS_PER_CLIENT)) for _ in range(REPEATS)]
                med = sorted(reps, key=lambda r: r["p99_ms"])[len(reps) // 2]
                rows.append({"server": server, "workload": w, "concurrency": c, **med,
                             "p99_spread_ms": [round(r["p99_ms"], 2) for r in reps]})
                print(f"{server:13s} {w:5s} c={c:4d}  p50={med['p50_ms']:7.1f}  p95={med['p95_ms']:7.1f}  p99={med['p99_ms']:8.1f}  rps={med['throughput_rps']:7.0f}", flush=True)
        proc.terminate(); proc.join(5)
        json.dump({"meta": meta, "rows": rows}, open(HERE / "results.json", "w"), indent=1)
        time.sleep(1)
    plots(rows)


def plots(rows):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    colors = {"threaded": "#1c1b22", "async": "#ff4d2e", "hybrid_thread": "#8a8f9c", "hybrid_proc": "#1f6feb"}
    def series(s, w, key):
        return sorted([(r["concurrency"], r[key]) for r in rows if r["server"] == s and r["workload"] == w])
    # 1. p99 vs concurrency
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, w in zip(axes, WORKLOADS):
        for s in SERVERS:
            pts = series(s, w, "p99_ms"); ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", ms=4, color=colors[s], label=s)
        ax.set_xscale("log", base=2); ax.set_yscale("log"); ax.set_title(f"{w}: p99 latency vs concurrency"); ax.set_xlabel("concurrent clients"); ax.set_ylabel("p99 (ms, log)")
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(HERE / "figures" / "fig1_p99_vs_concurrency.png", dpi=160); plt.close(fig)
    # 2. throughput vs concurrency
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, w in zip(axes, WORKLOADS):
        for s in SERVERS:
            pts = series(s, w, "throughput_rps"); ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", ms=4, color=colors[s], label=s)
        ax.set_xscale("log", base=2); ax.set_title(f"{w}: throughput vs concurrency"); ax.set_xlabel("concurrent clients"); ax.set_ylabel("requests / s")
        ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(HERE / "figures" / "fig2_throughput_vs_concurrency.png", dpi=160); plt.close(fig)
    # 3. tail heaviness p99/p50 at the highest concurrency
    fig, ax = plt.subplots(figsize=(8, 3.6))
    cmax = max(CONCURRENCY); width = 0.2
    for i, s in enumerate(SERVERS):
        vals = [next(r["p99_ms"] / r["p50_ms"] for r in rows if r["server"] == s and r["workload"] == w and r["concurrency"] == cmax) for w in WORKLOADS]
        ax.bar([j + (i - 1.5) * width for j in range(len(WORKLOADS))], vals, width, color=colors[s], label=s)
    ax.set_xticks(range(len(WORKLOADS))); ax.set_xticklabels(WORKLOADS); ax.set_ylabel("p99 / p50"); ax.set_title(f"Tail heaviness at {cmax} concurrent clients"); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(HERE / "figures" / "fig3_tail_ratio.png", dpi=160); plt.close(fig)


if __name__ == "__main__":
    (HERE / "figures").mkdir(exist_ok=True)
    mp.set_start_method("spawn")
    main()
