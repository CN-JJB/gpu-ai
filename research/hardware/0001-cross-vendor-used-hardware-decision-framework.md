# Research Note 0012 — Cross-Vendor Used-Hardware Decision Framework

日期：2026-08-27

## Problem

Architecture knowledge is useful only if it changes a real decision.

A garbage-hardware buyer often sees:

- one cheap 24 GB old NVIDIA card；
- one newer 12/16 GB NVIDIA card；
- one 16/24/32 GB AMD/Intel card；
- one 32/64/128 GB Apple-Silicon Mac；
- maybe two cheap GPUs instead of one large GPU。

The wrong question is:

> Which one is “best”?

The correct question is:

> For **this exact model, runtime, context, concurrency and service goal**, which candidate passes hard constraints, what roof limits it, and what is the total cost/risk?

This slice builds one stable cross-vendor decision system.

---

# Layer 1 — Workload identity comes before hardware

Minimum workload card:

```
model family
parameters
quant / representation
weight bytes
context
KV type
concurrency
backend candidate
prompt-processing goal
generation goal
service vs interactive
```

Without this, hardware comparison is mostly noise.

## Why PP and TG must remain separate

Prompt processing:
```
large matrix work
→ compute / matrix unit / kernel quality often important
```

Text generation:
```
stream weights + KV repeatedly
→ memory bandwidth / bytes/token often dominant
```

A GPU can win PP and lose TG.

---

# Layer 2 — Hard Gate A: Fit

Before ranking performance, ask whether the workload fits.

## Discrete one-GPU

```
usable VRAM
>= weights + KV + workspace + runtime headroom
```

## Multi-GPU

Not:
```
sum(VRAM) = one contiguous pool
```

Instead:
```
runtime sharding strategy
+ per-device allocations
+ communication buffers
+ per-device headroom
```

## Apple / integrated unified memory

```
safe working-set budget
>= runtime footprint
```

where safe budget is smaller than installed system memory.

## Gate result

Candidate status:
- **PASS** — full target workload fits；
- **PASS WITH OFFLOAD** — fits only with CPU/system-memory spill；
- **FAIL** — target cannot run with acceptable configuration。

A candidate that fails capacity should not receive a high “performance score” for that workload.

---

# Layer 3 — Hard Gate B: Software Support

Hardware features do not matter if the chosen runtime cannot use them.

Support chain:

```
OS / driver
→ runtime backend
→ exact GPU target
→ model representation
→ required kernels
→ correctness
```

Use states:

### Official-current
Exact device is currently supported by the vendor/runtime.

### Official-pinned
Works on an intentionally older supported stack.

### Community-enabled
Requires patches/custom builds/community packages.

### Runtime-visible only
Device enumerates but target kernels/libraries are not proven.

### Unsupported
No acceptable deployment path.

## Why this is a hard gate

A 24 GB card with unstable backend support can cost more engineering time than a 16 GB card with mature CUDA kernels.

Software maintenance is TCO.

---

# Layer 4 — Performance Roof A: Decode bandwidth

For memory-bound decode:

```
TG ideal roof
≈ usable memory bandwidth
 / bytes streamed per generated token
```

A practical first-order weight-only approximation:

```
bytes/token ≈ effective model weight bytes
```

Then add:
- KV traffic；
- dequant metadata/scales；
- cache miss；
- runtime overhead。

This is not a benchmark, but it catches absurd claims.

## Cross-vendor usefulness

The same equation works for:
- GDDR NVIDIA；
- GDDR Radeon；
- GDDR Arc；
- HBM accelerators；
- Apple unified memory。

The physical memory topology differs, but bytes and bandwidth still exist.

---

# Layer 5 — Performance Roof B: Prefill compute

For large GEMM-heavy prefill:

```
PP ceiling
≈ min(
  matrix compute roof × utilization,
  memory bandwidth × arithmetic intensity
)
```

Need:
- matrix datatype actually used；
- accumulator；
- shape；
- backend kernel；
- tile utilization。

Do not use:
```
marketing AI TOPS
```
unless the target kernel uses that exact datatype/mode.

---

# Layer 6 — Performance Roof C: Interconnect

If candidate needs:
- two GPUs；
- chiplets with exposed communication；
- CPU offload；
- host-memory fallback；

add:

```
communication bytes / effective link bandwidth
+ synchronization
+ imbalance
```

A larger aggregate memory setup can be slower per token.

---

# Layer 7 — System Cost

Purchase price is only one line.

## One-time cost

```
GPU / Mac / accelerator
+ motherboard/platform
+ PSU
+ cables/adapters
+ cooling
+ case/slot modifications
+ storage/RAM upgrade if required
```

## Operating cost

```
power draw × hours × electricity price
```

## Engineering cost

```
driver setup
+ kernel/backend troubleshooting
+ rebuild/pinning
+ maintenance
```

## Exit value

```
resale value
```

Total Cost of Ownership:

```
TCO
= acquisition
+ platform upgrades
+ expected energy
+ expected repair/maintenance
- expected resale
```

Time cost can be recorded separately rather than inventing a fake RMB/hour if the learner does not want to monetize time.

---

# Layer 8 — Used-Hardware Risk

Architecture does not reveal board condition.

Risk classes:

## Low
- normal retail/workstation card；
- verifiable serial/board；
- stock BIOS；
- no obvious repair；
- stable stress test。

## Medium
- unknown workload history；
- OEM board；
- old datacenter card；
- miner-used but testable；
- unusual cooling/power adapter。

## High
- engineering sample；
- modified BIOS；
- VRAM mod；
- repaired PCB；
- corrosion；
- intermittent memory errors；
- missing driver support；
- seller refuses testing。

Risk is not “bad by definition”.

It changes:
```
required discount
+ test burden
+ failure reserve
```

---

# Layer 9 — Evidence quality

Every candidate claim should carry a source class.

## E3 — Strong
- vendor official spec；
- current runtime docs；
- exact local benchmark raw output；
- exact board photos/serial/test logs。

## E2 — Useful
- reputable technical review；
- reproducible community benchmark；
- multiple consistent user reports。

## E1 — Weak
- single forum post；
- seller claim；
- screenshot without config；
- model-generated summary without source。

## E0 — Unknown
- no evidence。

Decision confidence should be constrained by the weakest important claim.

Example:

```
VRAM = E3
backend support = E3
TG performance = E1

→ do not treat TG as known
```

---

# Decision sequence

## Step 1 — Define target

```
model + quant + context + concurrency + PP/TG goal
```

## Step 2 — Pass capacity gate

Remove candidates that cannot fit the workload in an acceptable mode.

## Step 3 — Pass software gate

Remove candidates whose required support path is unacceptable.

## Step 4 — Identify expected roof

For each remaining candidate classify:

```
capacity-bound?
bandwidth-bound?
compute-bound?
interconnect-bound?
software-bound?
```

## Step 5 — Run comparable Evidence

Same model artifact and config where possible:

```
PP
TG
VRAM/working set
power
thermals
```

## Step 6 — Calculate TCO

Do not rank only by card sticker price.

## Step 7 — Apply risk

A high-risk card must offer enough economic advantage to justify the failure probability/testing burden.

## Step 8 — Final decision

Use one of:

- **BUY**
- **BUY IF PRICE ≤ X**
- **KEEP CURRENT**
- **SKIP**
- **NEEDS EVIDENCE**

This is more useful than a fake 87/100 universal score.

---

# Scenario-specific weighting

Only after hard gates pass may you use weighted ranking.

## Scenario A — Interactive single-user local LLM

Possible priorities:

```
fit        hard gate
support    hard gate
TG         high
PP         medium
noise/power medium
price      high
```

## Scenario B — Long-context / large model

```
fit        dominant
KV margin   high
support     hard gate
TG          medium
PP          medium
```

## Scenario C — Multi-user service

```
aggregate throughput
concurrency memory
power
stability
runtime maturity
```

## Scenario D — Learning / hacking

A less mature card may be rational because:

```
learning value
+ architecture diversity
+ source-code opportunities
```

are themselves goals.

But mark it as:
```
learning purchase
```
not:
```
best production purchase
```

---

# Cross-vendor comparison rules

## NVIDIA
Strength often:
- CUDA maturity；
- broad current kernel ecosystem。

Still check:
- old architecture support cutoff；
- exact VRAM/bandwidth；
- current quant kernel。

## AMD
Strength can be:
- VRAM/value；
- HBM/Instinct opportunities；
- modern Radeon AI hardware。

Still check:
- exact gfx target；
- ROCm current support；
- community workaround burden。

## Apple
Strength:
- large unified-memory capacity；
- no discrete host↔VRAM pool boundary；
- efficient integrated system。

Still check:
- safe working set；
- memory bandwidth；
- Metal/MLX backend；
- non-upgradability；
- purchase price。

## Intel
Strength:
- XMX；
- modern Arc pricing/VRAM options；
- oneAPI/PyTorch/SYCL path。

Still check:
- kernel maturity；
- driver/runtime；
- exact dGPU vs iGPU memory model。

---

# Claims to avoid

- "24 GB automatically beats 16 GB."
- "Newest architecture is best."
- "More AI TOPS = more llama.cpp tokens/s."
- "Unified memory means infinite effective VRAM."
- "Two GPUs equal one bigger GPU."
- "Official driver support means target LLM backend is optimized."
- "Seller says mining card is stable, so risk is low."
- "One benchmark from another model/quant proves performance."
- "One universal score can rank every workload."
