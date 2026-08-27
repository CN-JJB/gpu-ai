# Expected — Experiment 73

No universal real timing.

A valid packet must show:
- forced loopback binding;
- server binary SHA;
- model SHA before/after;
- health transition history;
- readiness timestamp;
- first smoke inference timestamp;
- child-process exit status;
- raw server logs.

The model SHA should remain unchanged.

Do not report:
- one universal startup time;
- SIGTERM as proven application drain;
- health 200 as steady-state performance;
- restart as preserving in-memory prefix/KV cache.
