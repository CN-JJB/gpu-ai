# Research Note 0016 — Capstone: Measure → Diagnose → Change One Variable → Re-measure

日期：2026-08-27

## Why a capstone?

Slices 01–21 teach individual mechanisms:

- execution / latency hiding;
- tiling and memory hierarchy;
- Roofline;
- VRAM capacity / KV;
- quantization and backend;
- reproducible local inference;
- serving/batching;
- prefix cache;
- speculative decoding;
- multi-GPU;
- attention I/O;
- matrix units / precision;
- vendor architecture;
- hardware buying / acceptance.

The capstone must prove the learner can connect them.

The target ability is:

```
real machine
→ reproducible baseline
→ evidence-backed bottleneck hypothesis
→ one controlled change
→ reproducible A/B
→ explanation
→ transfer to another machine
```

The capstone is **not**:

```
toggle five options
→ keep the fastest screenshot
```

---

# Part I — Freeze identity before optimizing

A valid baseline identifies four things.

## Hardware identity

Record:
- exact CPU/system memory;
- exact accelerator;
- VRAM / unified memory;
- PCIe/interconnect where relevant;
- power/thermal mode.

## Runtime identity

Record:
- llama.cpp version / commit;
- backend;
- driver;
- compiler/build source if relevant;
- device list.

## Model artifact identity

Record:
- repository/source;
- revision;
- exact filename;
- bytes;
- SHA256;
- GGUF/quant;
- parameter count if known.

## Workload identity

Record:
- PP tokens;
- TG tokens;
- repetitions;
- context / depth;
- KV type;
- FlashAttention state;
- offload/device split;
- thread settings;
- concurrency if serving.

If any of these change unintentionally, the A/B is no longer one experiment.

---

# Part II — Baseline must answer more than "tokens/s"

Minimum baseline evidence:

```
PP t/s
TG t/s
runtime memory footprint
device utilization / telemetry where available
power / temperature where available
startup/backend log
raw benchmark JSON
```

Optional depending on workload:
- TTFT;
- ITL;
- aggregate throughput;
- prefix-cache metrics;
- speculative acceptance;
- interconnect traffic/scaling;
- context sensitivity.

## Why PP and TG stay separate

PP:
```
large matrix work
→ compute / matrix kernel / arithmetic intensity
```

TG:
```
serial decode
→ weight/KV traffic often dominates
```

A single combined "LLM score" hides the mechanism.

---

# Part III — Diagnose the likely bottleneck

## A. Capacity-bound

Signals:
- model barely fits;
- OOM near target context/concurrency;
- large CPU offload/spill;
- KV growth consumes remaining headroom.

Candidate interventions:
- smaller quant / representation;
- smaller context;
- lower KV precision if supported;
- lower concurrency;
- more memory / different sharding.

Do not start with speculative decoding if the system cannot hold its extra proposer/KV resources.

## B. TG memory-bandwidth-bound

Signals:
- decode workload;
- model fully resident;
- TG scales with memory bandwidth across comparable devices/configs;
- rough `bandwidth / bytes-per-token` roof is near achieved throughput;
- additional compute resources do not move TG much.

Candidate interventions:
- lower effective weight bytes;
- backend/kernel with better memory behavior;
- reduce avoidable memory traffic;
- speculative decoding if workload/headroom make sense.

Do not expect higher matrix TOPS alone to fix it.

## C. PP compute/kernel-bound

Signals:
- PP much weaker than expected for matrix hardware;
- large GEMM shapes;
- changing matrix datatype/backend/FA changes PP strongly;
- TG may already be healthy.

Candidate interventions:
- optimized backend;
- FlashAttention for attention-heavy prefill;
- matrix-compatible precision/layout;
- kernel/library update.

## D. Context / KV pressure

Signals:
- short-context TG is healthy;
- long-context TG or capacity degrades;
- KV footprint grows as predicted;
- concurrency multiplies pressure.

Candidate interventions:
- context reduction;
- KV type;
- GQA-aware model choice;
- cache policy;
- more capacity.

## E. Serving / queueing-bound

Signals:
- single request is fine;
- concurrent TTFT rises sharply;
- slots/queue dominate;
- aggregate throughput and per-user cadence move differently.

Candidate interventions:
- slots;
- continuous batching;
- request scheduling;
- concurrency target.

Do not optimize one-user TG if the service problem is queueing.

## F. Prefix-reuse opportunity

Signals:
- repeated long prefix;
- prefill/TTFT dominates;
- current runtime exposes reusable prefix path;
- workload has real prefix identity.

Candidate intervention:
- prefix cache / APC-equivalent path.

Do not expect it to speed new-token decode.

## G. Speculative-decoding opportunity

Signals:
- low/medium QPS;
- decode-bound target;
- cheap proposer or strong n-gram repetition opportunity;
- sufficient memory headroom;
- measured acceptance can be high enough.

Candidate intervention:
- speculative decoding.

Do not assume acceptance rate alone guarantees speedup.

## H. Interconnect-bound

Signals:
- one GPU baseline strong;
- multi-GPU scaling poor;
- communication-heavy split;
- low P2P bandwidth / host staging / NUMA penalty;
- PP/TG scaling differs.

Candidate interventions:
- different split mode;
- avoid tensor split on weak links;
- layer split for capacity;
- topology-aware device choice;
- one larger GPU.

---

# Part IV — Change one variable

Examples of valid one-variable A/B:

```
baseline: FA off
candidate: FA on
```

or:

```
baseline: KV f16
candidate: KV q8_0
```

or:

```
baseline: split-mode layer
candidate: split-mode tensor
```

Invalid:

```
baseline:
Q4_K_M + FA off + context 4k + old build

candidate:
Q5_K_M + FA on + context 16k + new build
```

Too many independent variables changed.

## Build update can itself be the variable

A runtime update is a legitimate experiment if:
- model/workload/config stay frozen;
- old/new commits are recorded;
- the hypothesis is backend/kernel improvement.

---

# Part V — Define success before running

Examples:

### FlashAttention
Success:
- PP improves materially;
- memory does not regress beyond acceptable amount;
- output/correctness remains valid.

### KV quant
Success:
- target context now fits or memory drops;
- TG/quality tradeoff is acceptable.

### Speculative
Success:
- end-to-end/TG improves;
- acceptance/overhead explain result;
- memory remains safe.

### Multi-GPU
Success:
- required model fits;
- or target throughput/latency improvement justifies second GPU/TCO.

A result can be technically faster and still fail the project objective.

---

# Part VI — Compare normalized results

For each A/B, record:

```
PP speedup = PP_B / PP_A
TG speedup = TG_B / TG_A
memory delta
power delta
temperature delta
```

For serving:
- TTFT ratio;
- ITL ratio;
- aggregate throughput ratio.

## Do not over-interpret tiny changes

If repeated runs vary by several percent and the "optimization" is +1%, that may be noise.

Record:
- repetitions;
- mean;
- stddev where tool provides it;
- thermal state.

The course does not impose one universal significance threshold.

---

# Part VII — Explain the result mechanistically

A complete capstone conclusion should say:

1. What was the baseline bottleneck hypothesis?
2. What single variable changed?
3. What metric should move if the hypothesis is correct?
4. What actually moved?
5. What did not move?
6. Why?
7. What is the next experiment?

Example:

```
TG +2%
PP +31%
VRAM ~same

→ optimization primarily improved prefill attention/kernel path
→ decode remains bandwidth-bound
```

This is more valuable than:

> "FA makes my GPU 31% faster."

---

# Part VIII — Vendor paths are different, experimental logic is the same

## NVIDIA / CUDA

Possible evidence:
- nvidia-smi;
- CUDA device/compute capability;
- llama.cpp CUDA backend;
- power/temp/utilization;
- multi-GPU topology.

## AMD / ROCm

Possible evidence:
- amd-smi;
- rocminfo/gfx target;
- HIP backend;
- RAS/telemetry where supported.

## Apple / Metal

Possible evidence:
- Metal device;
- unified-memory working-set properties;
- llama.cpp Metal / MLX identity;
- system power/thermal evidence where available.

Do not call installed unified memory "VRAM".

## Intel / SYCL

Possible evidence:
- sycl-ls / Level Zero;
- torch.xpu;
- llama.cpp SYCL;
- exact Arc/iGPU memory model.

The command syntax differs, but the scientific loop does not.

---

# Part IX — Capstone completion criteria

Minimum completion:

- one real hardware profile;
- one exact model SHA;
- one runtime identity;
- one reproducible baseline;
- one bottleneck hypothesis;
- one controlled A/B;
- raw before/after data;
- one evidence-backed conclusion;
- one next experiment.

A "negative optimization" still passes the course if the experiment is valid.

Example:

```
FA on
→ PP -3%
→ no benefit on this build/shape
```

That is useful evidence, not failure.

---

# Stable claims to avoid

- "fastest config found = understood optimization";
- "PP and TG can be merged into one score";
- "changing several options is still A/B";
- "1% faster always means improvement";
- "same GPU model means same result across runtime builds";
- "FlashAttention always improves TG";
- "KV quant only changes capacity";
- "speculative acceptance alone predicts speedup";
- "multi-GPU capacity scaling implies latency scaling";
- "a negative result is useless".
