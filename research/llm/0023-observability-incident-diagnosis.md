# Research Note 0023 — Observability / Incident Diagnosis

日期：2026-08-27

## Research question

When a local LLM feels slow or unstable, how do you avoid jumping from:

```
symptom
```

straight to:

```
root cause
```

without evidence?

A useful incident workflow correlates:

```
client experience
+ server state
+ GPU/resource telemetry
+ logs
```

on one timeline.

---

# Monitoring model

Google SRE's classic monitoring framework emphasizes four user/service signals:

```
latency
traffic
errors
saturation
```

Official references:
- https://sre.google/sre-book/monitoring-distributed-systems/
- https://sre.google/workbook/monitoring/

For local LLM serving, a practical mapping is:

## Latency
- TTFT;
- ITL/chunk-gap proxy;
- E2E;
- p95/p99.

## Traffic
- requests/s;
- prompt tokens/s;
- generated tokens/s;
- active sequences.

## Errors
- HTTP/runtime errors;
- timeouts;
- SLO misses;
- quality/correctness failures.

## Saturation
- requests deferred/queue;
- slot occupancy;
- KV/VRAM pressure;
- GPU utilization;
- memory bandwidth/compute limits;
- thermals/power/clocks.

---

# Part I — Symptom != cause

Example symptom:

```
TTFT p95 increased
```

Possible causes include:
- queue growth;
- longer prompts;
- prefix-cache miss;
- slower prefill;
- thermal/power throttling;
- CPU/tokenization delay;
- network/client effects.

Therefore:

```
high TTFT
→ investigation
```

not:

```
high TTFT
→ GPU is bad
```

---

# Part II — Timeline first

Record a shared time axis.

Example:

```
12:00:00
TTFT 200 ms
deferred 0
GPU util 70%
clock 1800 MHz
temp 65 C

12:00:30
TTFT 1200 ms
deferred 9
GPU util 98%
clock 1780 MHz
temp 72 C
```

This supports a much stronger queue/saturation hypothesis than isolated screenshots.

---

# Part III — Queue-pressure pattern

Synthetic pattern:

```
TTFT ↑ strongly
requests_deferred ↑
GPU util ↑
clock roughly stable
ITL roughly stable
```

Interpretation:

```
queue/admission pressure is compatible with evidence
```

Why ITL can remain stable:
- admitted active requests still decode normally;
- waiting requests pay the queue delay mainly in TTFT.

This reconnects Slice 34/36.

---

# Part IV — Thermal/clock pattern

Synthetic pattern:

```
temperature ↑
SM/core clock ↓
ITL ↑
TTFT ↑
GPU utilization stays high
```

Interpretation:

```
thermal/power/clock throttling becomes a plausible hypothesis
```

Do not claim exact throttle cause from correlation alone.

Additional vendor-specific throttle/power-limit evidence may be needed.

---

# Part V — High VRAM is not automatically a leak

A runtime may reserve:
- model weights;
- KV;
- compute buffers;
- allocator pools.

Synthetic pattern:

```
VRAM 95–96%
stable over time
latency stable
no OOM
no monotonic growth
```

does not prove a memory leak.

Leak-like evidence would need:
- unexplained growth across comparable workload states;
- failure to release expected allocations;
- OOM/fragmentation evidence;
- runtime-specific allocation investigation.

---

# Part VI — GPU 100% is not automatically bad

High utilization can simply mean the GPU is doing useful work.

If:
- latency SLO passes;
- errors are low;
- clocks/temperature are healthy;

then:

```
GPU utilization ≈ 100%
```

may be desirable.

Alerting on utilization alone can create noise.

---

# Part VII — Low GPU utilization is not automatically "weak GPU"

Low utilization plus poor latency can come from:
- CPU prompt preprocessing;
- tokenizer/template work;
- storage/model paging;
- host-device synchronization;
- too-small batch;
- queue/scheduler behavior;
- network/client delay;
- measurement sampling artifacts.

Collect evidence before replacing hardware.

---

# Part VIII — Current pinned llama-server signals

Pinned:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current `/metrics` exposes aggregate signals including:
- prompt token counters/time/rate;
- predicted token counters/time/rate;
- requests processing;
- requests deferred;
- busy slots per decode;
- context high watermark;
- speculative-decode metrics.

Pinned tests also verify cached prompt-token accounting.

These signals are useful for internal context but do not replace client-observed latency.

---

# Part IX — Metrics vs logs vs request trace

## Metrics
Good for:
- trends;
- rates;
- saturation;
- alerting.

## Logs
Good for:
- startup errors;
- model/backend failures;
- exceptional events;
- detailed context.

## Request trace
Good for:
- exact client arrival;
- first visible output;
- completion;
- per-request tail analysis.

Use the appropriate evidence type.

---

# Part X — Correlation is not causation

If:

```
temperature rises
and
latency rises
```

at the same time, thermal throttling is plausible.

But another hidden variable may drive both.

A diagnosis should say:

```
evidence supports hypothesis X
```

until a controlled test isolates the cause.

---

# Part XI — One-variable confirmation

After incident stabilization, use a controlled test.

Example hypothesis:

```
thermal limit is reducing clocks
```

Safer confirmation can be:
- improve cooling/ambient condition;
- rerun same workload;
- compare clocks/latency.

Do not change overclock/power-limit settings as the first diagnostic action.

---

# Part XII — Alert on symptoms and actionable saturation

For a user-facing local service, stronger alert candidates are:
- TTFT/SLO violation;
- error rate;
- persistent queue/deferred requests;
- readiness failure;
- VRAM/OOM risk;
- sustained thermal/clock degradation tied to SLO.

Weaker standalone alert:

```
GPU util > 90%
```

because this can be healthy.

---

# Part XIII — Tail matters

Google SRE monitoring guidance emphasizes request-latency distributions rather than relying only on averages.

This matches Slice 34:

```
mean healthy
!=
p95 healthy
```

Incident dashboards should retain the tail.

---

# Part XIV — Alert fatigue

An alert should imply an action.

If every:
- short GPU spike;
- temporary 95% VRAM;
- one slow request;

pages someone, the signal becomes noisy.

For a personal local server, use:
- dashboard/logging for informational signals;
- alerts for persistent user-impacting conditions.

---

# Part XV — Incident evidence packet

Preserve:
- incident start/end;
- workload identity;
- client request trace;
- server metrics;
- GPU telemetry;
- server logs;
- release/model/runtime identity;
- hypothesis;
- action;
- before/after result.

Do not preserve raw secrets/private prompts unnecessarily.

---

# Part XVI — Read-only telemetry

Experiment 77:
- samples only localhost server metrics;
- bounds duration;
- does not generate traffic itself;
- does not change clocks/power/driver;
- records vendor telemetry only if a supported CLI is already installed.

NVIDIA path captures raw:
- temperature;
- utilization;
- memory used/total;
- power draw;
- SM/memory clocks.

AMD paths capture raw `amd-smi metric` or `rocm-smi` output if available.

Other vendors may require separate tools; UNKNOWN is allowed.

---

# Part XVII — Sampling caveat

A one-second GPU-util sample is not the complete execution trace.

Short kernels/bursts can be missed or averaged.

Therefore:
- record sampling interval;
- do not overinterpret one point;
- correlate over windows.

---

# Part XVIII — Incident lifecycle

```
detect symptom
→ preserve timeline
→ classify latency/traffic/error/saturation
→ form hypothesis
→ seek confirming/refuting evidence
→ mitigate
→ controlled follow-up
→ document
```

A good postmortem records uncertainty, not only a confident story.

---

# Claims to avoid

- "GPU 100% means overload";
- "VRAM nearly full means memory leak";
- "low GPU utilization means buy a faster GPU";
- "correlation proves cause";
- "one screenshot is a timeline";
- "server metrics replace client latency";
- "average latency is enough";
- "every resource spike should alert";
- "first diagnostic step should be changing power/clock settings".
