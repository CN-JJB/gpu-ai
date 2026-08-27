# Research Note 0017 — Serving Capacity Planning with Little's Law

日期：2026-08-27

## Research question

How can a serving operator connect:

```
requests / second
+
seconds / request
```

to:

```
average in-flight requests
```

without pretending that an average predicts:
- p95 latency;
- peak concurrency;
- exact slot count;
- exact KV memory?

The stable relation is Little's Law:

```
L = λ W
```

where:
- L = long-run average number of items in the chosen system;
- λ = long-run throughput/flow rate through that system;
- W = long-run average time each item spends in that system.

Primary source:
John D. C. Little, 1961,
"A Proof for the Queuing Formula: L = λW",
Operations Research 9(3):383–387.
DOI: https://doi.org/10.1287/opre.9.3.383

---

# Part I — Define the system boundary first

The equation is meaningless until you define:

```
what counts as "in the system"?
```

For an LLM request, possible boundaries include:

## End-to-end system

```
client send
→ queue
→ active service
→ completion
```

Then:

```
W_system
=
E2E time
```

and:

```
L_system
=
average queued + active requests
```

## Active service only

```
server service start
→ completion
```

Then:

```
W_active
=
active service time
```

and:

```
L_active
=
average requests actually occupying service capacity
```

## Queue only

```
arrival
→ service start
```

Then:

```
W_queue
=
queue wait
```

and:

```
L_queue
=
average queued/deferred requests
```

With consistent boundaries:

```
W_system
=
W_queue + W_active
```

and:

```
L_system
=
L_queue + L_active
```

---

# Part II — Basic intuition

Suppose stable throughput is:

```
λ = 2 requests/s
```

and average end-to-end time is:

```
W = 3 s/request
```

Then:

```
L = 2 × 3 = 6 requests
```

On average, six requests are somewhere in the system.

This does **not** mean:
- exactly six at every instant;
- six slots are sufficient;
- six requests actively own KV;
- p95 concurrency is six.

It is an average occupancy.

---

# Part III — Trace-area view

For a finite trace, draw each request as an interval.

Example:

```
request 0: [arrival, completion)
request 1: [arrival, completion)
...
```

At time t:

```
N_system(t)
=
number of request intervals covering t
```

Then time-average occupancy:

```
L_system
=
area under N_system(t)
/
observation duration
```

The area is also:

```
Σ request E2E times
```

So for a complete finite batch:

```
L_system
=
Σ W_i / T
```

while:

```
λ
=
N / T
```

and:

```
W
=
Σ W_i / N
```

therefore algebraically:

```
λ W
=
(N/T)(ΣW_i/N)
=
ΣW_i/T
=
L
```

This finite-trace identity is useful for validation.

But a representative capacity forecast still requires the trace to represent the workload you care about.

---

# Part IV — Synthetic example

Six requests over a 5-second observation horizon.

| id | arrival | service start | completion |
|---|---:|---:|---:|
| r0 | 0.0 | 0.0 | 3.0 |
| r1 | 0.5 | 0.5 | 2.5 |
| r2 | 1.0 | 1.0 | 5.0 |
| r3 | 1.5 | 2.0 | 3.0 |
| r4 | 2.0 | 2.5 | 4.5 |
| r5 | 2.5 | 3.0 | 4.5 |

Throughput:

```
λ = 6 / 5 = 1.2 req/s
```

Mean system time:

```
W_system = 2.5 s
```

So:

```
L_system = 1.2 × 2.5 = 3.0
```

Mean active time:

```
W_active = 2.25 s
```

So:

```
L_active = 1.2 × 2.25 = 2.7
```

Mean queue time:

```
W_queue = 0.25 s
```

So:

```
L_queue = 1.2 × 0.25 = 0.3
```

And:

```
3.0 = 2.7 + 0.3
```

---

# Part V — Average is not peak

For the same trace:

```
average in system = 3.0
peak in system = 5

average active = 2.7
peak active = 4

average queued = 0.3
peak queued = 1
```

This is the key capacity lesson:

```
average active demand
!=
peak active demand
```

Sizing exactly to the mean guarantees no headroom for bursts.

---

# Part VI — Slots

A simple server often has a configured maximum number of active sequences/slots.

It is tempting to do:

```
slots = ceil(L_system)
```

Wrong.

Why?

Because:

```
L_system
includes queued requests
```

while slots usually describe active service capacity.

If service-start timing is available, `L_active` is a more relevant average.

Even then:

```
slots = ceil(L_active)
```

is not a complete sizing rule because:
- peak/burst concurrency matters;
- service times are variable;
- long prompts/outputs create tails;
- continuous batching changes throughput as active set changes;
- admission policy can intentionally queue.

---

# Part VII — KV pressure

Only requests that have been admitted into model execution generally need active per-sequence KV.

A deferred HTTP request sitting in a scheduler queue usually does not yet consume the same active KV footprint.

Therefore:

```
L_system × KV_per_sequence
```

can overstate active KV when queueing is present.

A better first planning proxy is:

```
L_active × representative_active_KV
```

but even this is crude.

Why?

Because per-sequence KV varies with:
- current prompt/context length;
- generated length;
- sliding/hybrid architecture;
- KV quant type;
- prefix-cache implementation;
- unified KV;
- retained idle cache.

The most general memory accounting remains:

```
Σ active/retained sequence state
```

not one fixed sequence constant.

---

# Part VIII — Constant-KV teaching proxy

For a synthetic example only, suppose each active sequence is treated as if it occupies:

```
1.5 GiB
```

Then:

Average active proxy:

```
2.7 × 1.5
=
4.05 GiB
```

Peak active proxy:

```
4 × 1.5
=
6.0 GiB
```

The gap is exactly why mean-only sizing is unsafe.

This is not a real llama.cpp allocation model.

---

# Part IX — Throughput rate must match the boundary

For a stable system:

```
arrival rate
≈
completion throughput
```

over a sufficiently representative window.

If backlog is continuously growing:

```
arrival rate > completion rate
```

then taking the offered arrival rate as λ while using an old average W does not produce a valid capacity solution.

Operational symptom:

```
queue grows
TTFT tail grows
requests_deferred stays elevated
```

The system is overloaded or the window is non-stationary.

---

# Part X — Little's Law does not require Poisson traffic as a practical teaching rule

Do not teach:

> Little's Law only works for Poisson arrivals.

The original theorem and later generalizations are broader.

For this course, the safe practical statement is:

```
under stable, consistently defined long-run flow
L = λW
```

Do not turn this beginner lesson into a full stochastic-process proof.

---

# Part XI — It does not predict latency distribution

Knowing:

```
λ
and
average L
```

lets you derive:

```
average W = L/λ
```

under the law.

It does not give:
- p95 W;
- p99 TTFT;
- max queue;
- probability of an SLO miss.

Two traces can have identical:
- λ;
- mean W;

and wildly different tails.

Use Slice 34 for percentiles/SLO.

---

# Part XII — It does not tell you optimal concurrency

Increasing slots can:
- reduce queue wait;
- increase active batch size;
- improve aggregate utilization;
- worsen per-user ITL;
- increase KV memory.

The capacity decision is multi-objective:

```
slots
→ queue
→ TTFT
→ active concurrency
→ ITL
→ KV
→ throughput
```

Little's Law helps connect averages.

It does not optimize this chain.

---

# Part XIII — Practical planning workflow

1. Capture a representative workload trace.
2. Measure completed throughput λ.
3. Measure E2E W.
4. Compute/verify average L_system.
5. If service-start evidence exists:
   - compute W_queue;
   - compute W_active;
   - derive L_queue/L_active.
6. Record peak observed concurrency.
7. Convert active concurrency to KV pressure using architecture-specific per-request state.
8. Add headroom.
9. Run real serving SLO test.
10. Increase/decrease slots based on both throughput and latency.

---

# Part XIV — Production trace caution

A finite batch always gives an exact area identity if all request intervals are fully contained in the observation horizon.

That algebraic check does not prove:
- the trace is representative;
- the production process is stationary;
- the same λ can be sustained forever.

Capacity planning requires representative repeated windows, not one convenient batch.

---

# Part XV — Connection to garbage-hardware planning

Suppose two cheap GPUs offer enough total VRAM for:
- model weights;
- 8 active sequence KV states.

But the PCIe split makes decode slower, increasing:

```
W_active
```

At the same arrival throughput λ:

```
L_active = λW_active
```

rises.

So a slower system can need **more concurrent active state** to serve the same request rate.

This links:
- interconnect;
- TG;
- serving capacity;
- KV memory.

Hardware speed and memory capacity are not independent.

---

# Claims to avoid

- "Little's Law predicts p95 latency";
- "average in-flight requests equals required slots";
- "queued requests consume the same KV as active requests";
- "L = λW requires Poisson arrivals only";
- "if the finite-trace identity holds, the server is stable";
- "arrival rate should be used as λ even while backlog grows forever";
- "average KV pressure is enough to size VRAM";
- "more slots always reduce user latency".
