# Expected structural outcomes

Experiment 12 has no fixed performance numbers.

Different model/hardware/backend combinations should produce different results.

## What must be observable

### Server identity

The server should expose:

- /health
- /props
- /slots
- /metrics when started with metrics enabled

Exact fields can evolve.

### Concurrency <= slots

For a dedicated server with slots=4 and short requests:

- concurrency 1/2/4 should be able to run without slot-limit queueing in the ideal case；
- peak processing should rise toward client concurrency；
- requests_deferred may stay near zero。

This is not guaranteed if another runtime limit intervenes.

### Concurrency > slots

At concurrency=8 with slots=4, it is reasonable to expect some admission/queue pressure if requests overlap long enough.

Evidence may include：

- requests_deferred > 0；
- TTFT tail increases；
- wall request latency tail increases。

If it does not happen, inspect whether：

- requests are too short to overlap；
- current server auto-configured more slots than expected；
- workload ended before monitor sampling；
- server semantics changed；
- requests failed or were cached。

### Throughput

Aggregate output throughput may rise with concurrency and then saturate.

No fixed “4 slots = N×” multiplier is expected.

### Stream gap

Client-visible stream-gap proxy may increase as more requests share active decode work.

Do not label it exact ITL.

## What counts as a valuable unexpected result

- concurrency 8 gives no deferred requests；
- aggregate throughput falls as concurrency rises；
- GPU server scales worse than CPU；
- p95 TTFT spikes before client concurrency reaches slot count；
- n_busy_slots_per_decode stays near 1；
- server predicted t/s rises but wall aggregate t/s falls；
- OOM or severe memory pressure after raising slots/context。

All are valid Evidence if runtime/model/config are fully recorded.
