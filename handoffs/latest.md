# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–41 are implemented.
Experiments 01–77 exist.

## Slice 41 core

Service views:

```
latency
traffic
errors
saturation
```

LLM mapping:

```
TTFT/ITL/E2E
req/s/tok/s
HTTP/OOM/SLO
queue/slots/KV/GPU/thermal
```

Synthetic verified:

```
queue:
TTFT 6×
deferred +9
ITL ~flat
clock ~flat

thermal:
temp +18C
clock 0.667×
ITL 1.9×

stable VRAM:
96.25% peak
only 0.1 GiB variation
latency stable
```

Diagnoses remain hypotheses until controlled confirmation.

Real collector:
- loopback only;
- max 300 s;
- read-only;
- server metrics + raw vendor telemetry;
- no clock/power/driver changes.

## Active next slice — Power / Energy Efficiency

Teach:

```
power W
=
joules / second

energy
=
integral of power over time

joules/token
=
energy / useful output
```

Separate:
- idle board/system power;
- model load;
- PP;
- TG;
- serving concurrency.

Metrics:
- tok/s/W;
- J/output-token;
- J/request;
- electricity cost per 1M tokens / per workload day.

Use synthetic integration first.

Real lab should read telemetry only and label GPU-board power vs whole-system wall power separately.
