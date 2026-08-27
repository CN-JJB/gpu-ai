# Evidence — Experiment 20: Used GPU Transaction / Acceptance

状态：stable acceptance model complete; seller-evidence L0 verified; real read-only baseline packet ready.

## Claim

> Used-GPU acceptance requires separate evidence for identity, memory integrity, compute/workload stability, thermals and driver/error state. No single benchmark, seller adjective or inspection badge proves all of them.

## Seller evidence model

- C0: unknown;
- C1: seller claim/old evidence;
- C2: current functional evidence;
- C3: strong current pre-sale identity + memory/load/thermal evidence;
- C4: target acceptance properties independently verified.

## Experiment 35

Reference mapping:

```
A → C1
B → C2
C → C3
D → C4
```

Expected:

```
score: 4/4
```

The key lesson:
```
evidence grade describes verified properties
not seller reputation
```

## Real acceptance packet

Experiment 36 contains:
- seller evidence request;
- unboxing/identity checklist;
- read-only baseline collector;
- memory-test guidance;
- llama.cpp workload path;
- before/after error-state comparison;
- decision template.

The baseline script does not:
- overclock;
- change power limits;
- flash BIOS;
- modify firmware;
- start an automatic max-power stress test.

## Current memory-integrity evidence

NVIDIA DCGM official docs confirm current memory diagnostics can:
- allocate framebuffer;
- write known patterns;
- read/verify;
- detect mismatches/ECC errors on supported products.

Current DCGM also explicitly limits higher-suite availability by GPU class/product.

Therefore the course does not generalize datacenter diagnostics to every GeForce.

## Cross-vendor memory evidence

memtest_vulkan is kept as optional third-party evidence with explicit limitations and version recording.

## AMD RAS evidence

Current AMD SMI docs confirm supported devices can expose correctable/uncorrectable ECC/RAS information.

## Acceptance failure signals

Strong dispute/return evidence includes:
- wrong GPU/VRAM;
- undisclosed modification/repair;
- reproducible memory errors;
- uncorrectable ECC;
- repeated driver resets;
- artifacting;
- thermal/fan failure;
- device disappearing under ordinary supported workload.

## Learner should reject

- FurMark pass = healthy;
- non-mining = healthy;
- mining = broken;
- platform inspection = complete engineering diagnosis;
- memory-test pass = guaranteed future reliability;
- benchmark score alone = stability;
- modded/repaired = automatically unusable;
- visibly unsafe board should be powered just to test it.
