# Expected — Experiment 64

```
requests: 6
horizon: 5.000 s
throughput lambda: 1.200000 req/s

SYSTEM
mean W_system: 2.500000 s
lambda*W: 3.000000
trace-area L: 3.000000
peak: 5

ACTIVE
mean W_active: 2.250000 s
lambda*W: 2.700000
trace-area L: 2.700000
peak: 4

QUEUE
mean W_queue: 0.250000 s
lambda*W: 0.300000
trace-area L: 0.300000
peak: 1

L_system-(L_active+L_queue)
≈ 0

average active KV proxy:
4.050 GiB

peak active KV proxy:
6.000 GiB
```

All are synthetic trace arithmetic.
