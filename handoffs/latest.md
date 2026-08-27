# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–40 are implemented.
Experiments 01–75 exist.

## Slice 40 core

Release policy is defined before candidate interpretation.

Synthetic policy result:

```
candidate-good:
TG 1.08×
PPL ratio 1.01
TTFT 450 ms
SLO 99.3%
→ ACCEPT

candidate-fast-bad:
TG 1.20×
PPL ratio 1.04
TTFT 900 ms
SLO 92%
→ ROLLBACK
```

Rollback only completes when exact baseline:

```
runtime SHA
model SHA
config SHA
manifest SHA
```

is restored and readiness/smoke pass.

Real Experiment 75 consumes prior Evidence; it does not install services or overwrite artifacts.

## Active next slice — Observability / Incident Diagnosis

Build:

```
user symptom
→ timeline
→ client latency/error
→ queue/server metrics
→ GPU memory/utilization/clocks/temperature
→ logs
→ hypothesis
→ evidence
→ action
```

Teach:
- symptom != cause;
- 100% GPU can be healthy;
- low GPU utilization can be queue/CPU/tokenization/I/O or measurement artifact;
- VRAM full can be expected reservation rather than leak;
- thermals/clocks matter over time;
- correlate clocks/queue/TTFT rather than alerting on one metric.

Real lab should be read-only and produce an incident packet without changing power limits/clocks/driver settings.
