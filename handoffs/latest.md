# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–45 are implemented.
Experiments 01–85 exist.

## Slice 45 core

Sustained timeline:

```
workload duration
→ power
→ temperature
→ clock/limiter
→ sustained TG
```

Synthetic verified:

```
thermal-like:
55→86C
1900→1450 MHz
55→42 tok/s
→ compatible thermal/clock/perf drift

hot-stable:
80→84C
clock stable
50→49.8 tok/s
→ sustained stable

clock/perf drift with only +6C:
→ investigate power/other limiter
```

Lesson:

```
high temperature
!= throttling
clock drop
!= automatically thermal cause
```

Real Experiment 85:
- pinned llama-bench repetitions / samples_ts;
- fixed local model;
- warmup recorded;
- read-only telemetry;
- no OC/UV/power/fan changes.

## Active next slice — Used-GPU Validation / Purchase Acceptance

Build for garbage-hardware buyers:

```
seller/model claim
→ PCI identity
→ VRAM identity
→ driver/runtime recognition
→ PCIe link
→ telemetry/error state
→ controlled sustained TG
→ thermal stability
→ acceptance decision
```

Need distinguish:
- cosmetic/model-name claim vs hardware IDs;
- idle PCIe link downshift vs under-load link capability;
- ECC-capable vs non-ECC consumer cards;
- error-free short test vs reliable card;
- display-port issue vs compute issue;
- BIOS/firmware flashing as OUT OF DEFAULT LAB.

Real lab should remain read-only plus ordinary inference workload; no firmware flash, overclock or destructive VRAM stress by default.
