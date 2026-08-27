# Evidence — Experiment 41: Observability / Incident Diagnosis

状态：stable incident-diagnosis lesson complete; three synthetic pattern cases verified; bounded loopback-only real collector ready.

## Claim

> Resource metrics are evidence, not root causes. A useful local-LLM incident diagnosis correlates client symptoms, traffic/errors, server saturation, GPU/resource telemetry and logs on one timeline.

## Monitoring framework

Google SRE's monitoring guidance emphasizes:

```
latency
traffic
errors
saturation
```

Official:
- https://sre.google/sre-book/monitoring-distributed-systems/
- https://sre.google/workbook/monitoring/

For this course:

```
latency
→ TTFT / ITL / E2E / tails

traffic
→ req/s / prompt tok/s / output tok/s / concurrency

errors
→ HTTP/runtime/OOM/SLO/quality failure

saturation
→ queue / slots / KV / VRAM / GPU / clocks / thermals
```

## Experiment 76 — queue case

Verified last/first:

```
TTFT = 6.0×
ITL = 1.06×
requests_deferred = +9
SM clock = 0.989×
```

Result:

```
QUEUE_PRESSURE_COMPATIBLE
```

Interpretation:
- waiting users pay large TTFT;
- active decode cadence remains nearly stable;
- clock does not collapse.

This supports a queue/admission hypothesis, not a GPU-failure claim.

## Thermal/clock case

Verified:

```
TTFT = 3.5×
ITL = 1.9×
temperature = +18 C
SM clock = 0.667×
```

Result:

```
THERMAL_CLOCK_HYPOTHESIS
```

This is still correlation-based evidence.

Vendor-specific throttle/power reasons or a controlled cooling follow-up may be required for confirmation.

## High stable VRAM case

Verified:

```
max VRAM fraction = 96.25%
VRAM range = 0.1 GiB
TTFT ratio ≈ 0.977×
ITL ratio ≈ 0.981×
```

Result:

```
HIGH_STABLE_VRAM
```

Therefore:

```
VRAM nearly full
```

alone is not evidence of a leak.

## Current pinned llama-server evidence

Pinned:

```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Server metrics provide internal context such as:
- prompt/predicted throughput;
- requests processing/deferred;
- busy slots/decode;
- context high watermark.

They remain complementary to client-observed TTFT/E2E.

## Experiment 77 safety

Collector:
- accepts only 127.0.0.1 / localhost / ::1;
- duration hard-capped at 300 seconds;
- interval must be >=0.5 s;
- generates no traffic itself;
- changes no clocks/power/driver/firewall.

It saves:
- raw /metrics snapshots;
- selected server-metric timeline;
- raw vendor telemetry when supported;
- collector manifest.

NVIDIA telemetry is captured read-only through installed `nvidia-smi`.

AMD output is stored raw from installed `amd-smi metric` or `rocm-smi` rather than forcing a fragile universal parser.

UNKNOWN is acceptable on unsupported/unavailable vendor tooling.

## Alerting boundary

Standalone:

```
GPU > 90%
```

is weak alert logic.

A high-utilization GPU can be healthy when:
- SLO passes;
- errors are low;
- clocks/thermals are healthy.

Stronger alerts combine:
- user-visible SLO/error symptoms;
- persistent saturation/resource evidence;
- actionable response.

## Learner should reject

- GPU 100% means overload;
- high stable VRAM means leak;
- low GPU utilization means buy a faster GPU;
- correlation proves causation;
- one screenshot is a timeline;
- server metrics replace client latency;
- every resource spike deserves an alert.
