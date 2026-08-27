# Expected — Experiment 83

No universal real memory-pressure result.

A valid report:
- interprets MemAvailable separately from MemFree;
- uses vmstat deltas, not raw cumulative counts;
- distinguishes file cache from anonymous memory;
- distinguishes host RAM from discrete GPU VRAM;
- does not intentionally trigger host OOM;
- leaves unsupported fields UNKNOWN.

Swap usage alone must not be reported as proof of active swap thrashing.
