# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–42 are implemented.
Experiments 01–79 exist.

## Slice 42 core

```
W = J/s
E = ∫Pdt
J/token = energy/tokens
tokens/J = reciprocal
```

Synthetic verified:

```
300W @ 60 tok/s → 5.0 J/token
220W @ 50 tok/s → 4.4 J/token
180W @ 42 tok/s → 4.285714 J/token
```

Therefore:
```
fastest
!= most energy-efficient
```

Integration sanity:

```
100,120,140W at 0,1,2s
→ 240J total
→ 120W average
```

Real NVIDIA lab:
- reuses read-only incident telemetry;
- filters participating GPU indices;
- sums board power;
- trapezoidal integration;
- refuses missing samples.

Boundary:

```
GPU board energy
!= whole-system wall energy
```

## Active next slice — Storage / Model Loading

Teach:

```
model file bytes
→ storage read/page faults
→ OS page cache
→ mmap/load mode
→ host memory
→ GPU upload/allocation
→ health ready
```

Questions:
- why first cold start can be slow;
- why second start can look much faster;
- why SSD speed may affect startup but not steady-state TG after weights are resident;
- why benchmarking "disk speed" from warm page cache is invalid.

Real lab should be read-only and avoid destructive cache-dropping commands by default.
