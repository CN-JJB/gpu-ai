# Evidence — Experiment 35: Serving Capacity / Little's Law

状态：stable capacity-planning lesson complete; L0 system/active/queue trace arithmetic verified; real-trace analyzer ready.

## Claim

> Little's Law is an average flow/occupancy relation. Correct serving use requires a consistent system boundary. End-to-end in-flight requests, active requests and queued requests are different quantities.

## Primary source

John D. C. Little, 1961:
"A Proof for the Queuing Formula: L = λW"
Operations Research 9(3):383–387.
DOI:
https://doi.org/10.1287/opre.9.3.383

## Stable relations

For consistent boundaries:

```
L_system = λ W_system
L_active = λ W_active
L_queue  = λ W_queue
```

and:

```
W_system = W_active + W_queue
L_system = L_active + L_queue
```

## Experiment 64 verification

Synthetic trace:

```
6 requests
5.0 s observation horizon
```

Verified throughput:

```
λ = 1.2 req/s
```

System:

```
mean W_system = 2.5 s
λW = 3.0
trace-area L_system = 3.0
peak system = 5
```

Active:

```
mean W_active = 2.25 s
λW = 2.7
trace-area L_active = 2.7
peak active = 4
```

Queue:

```
mean W_queue = 0.25 s
λW = 0.3
trace-area L_queue = 0.3
peak queue = 1
```

Identity:

```
3.0 = 2.7 + 0.3
```

verified exactly for this synthetic trace.

## KV teaching proxy

With constant synthetic:

```
1.5 GiB / active sequence
```

verified:

```
average active KV proxy
= 2.7 × 1.5
= 4.05 GiB

peak active KV proxy
= 4 × 1.5
= 6.0 GiB
```

This is not a real runtime allocation model.

## Important boundary

```
L_system
```

includes queued requests when W is client E2E time.

Queued/deferred requests do not necessarily consume the same active KV state as admitted model sequences.

Therefore:

```
ceil(L_system)
```

is not a valid universal slot-sizing rule.

## Experiment 65

The real analyzer accepts Experiment 63 request CSV.

With the current client-only trace it can derive:
- completed throughput;
- mean client E2E;
- average client in-system count;
- peak client in-system count.

It refuses to derive:
- active occupancy;
- queue occupancy;
- active KV;

without trustworthy `service_start_ms`.

## Stability boundary

A finite batch can satisfy the trace-area identity algebraically.

That does not prove:
- workload stationarity;
- sustainable arrival rate;
- future tail behavior.

If backlog grows persistently:

```
arrival rate > completion rate
```

the system is overloaded/non-steady for that offered load.

## Learner should reject

- Little's Law predicts p95;
- average in-flight equals required slots;
- queued requests always consume active-sequence KV;
- the law only applies to Poisson traffic;
- finite-trace identity proves production stability;
- average active memory is enough to size peak VRAM;
- more slots always improve latency.
