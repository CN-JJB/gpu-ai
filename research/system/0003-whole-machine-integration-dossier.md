# Research Note 0003 — Whole-Machine System Integration Dossier

日期：2026-08-27

## Research question

How do you decide whether a complete Local-LLM machine design is actually feasible after separately learning:
- model/VRAM requirements;
- runtime/backend support;
- PCIe/multi-GPU topology;
- host RAM;
- storage/startup behavior;
- PSU/cables;
- cooling;
- serving/SLO/privacy;
- budget/TCO?

The answer should not be one universal weighted score.

Use three classes:

```text
HARD GATE
PURCHASE-CRITICAL UNKNOWN
PREFERENCE / OPTIMIZATION
```

and end with:

```text
ACCEPT
REVISE
BLOCKED
```

---

# Part I — Start from workload, not parts

A machine is only meaningful relative to a target.

Freeze:
- model artifact / architecture dossier;
- quant/backend;
- context;
- concurrency;
- PP/TG or serving SLO;
- privacy/network scope;
- budget/time horizon.

A machine that is excellent for one workload can be wrong for another.

---

# Part II — Hard gate

A hard gate is a requirement that must hold for the design to meet its declared target.

Examples:
- enough runtime-confirmed VRAM/capacity for the target configuration;
- intended backend supports the exact GPU/runtime stack;
- host RAM sufficient for the chosen load/offload strategy;
- required model/storage artifact fits available storage;
- PSU power paths/cables valid;
- required network/privacy controls exist;
- purchase budget is not exceeded if budget is declared hard.

If a hard gate is known false:

```text
REVISE
```

The design may be fixable, but the current version is not feasible.

---

# Part III — Purchase-critical UNKNOWN

Unknown is different from false.

Examples:
- seller has not proved exact 24 GiB SKU;
- ROCm/CUDA support for exact GPU/runtime is not verified;
- modular PSU cable compatibility is unknown;
- motherboard slot lane topology is unknown for the planned two-GPU split;
- exact model license/redistribution requirement is unknown for the deployment plan.

Do not convert an unknown into a guessed PASS.

If the unknown can change a purchase or safety decision:

```text
BLOCKED
```

until evidence resolves it.

---

# Part IV — Preference / optimization

After hard gates pass, compare preferences such as:
- faster TG;
- lower TTFT;
- lower J/token;
- lower noise;
- smaller chassis;
- cheaper purchase;
- easier driver maintenance;
- more upgrade headroom.

A preference should not rescue a failed hard gate.

Example:

```text
GPU A is 20% faster
but cannot fit the model
→ not selected for that workload
```

---

# Part V — No universal score

A weighted score can hide fatal failures.

Bad:

```text
VRAM fail = 0 points
price = 10 points
speed = 10 points
average = 7/10
→ buy
```

Correct:

```text
VRAM hard gate failed
→ current design REVISE
```

Ranking begins only after feasibility.

---

# Part VI — Model/capacity gate

Reuse Slices 05, 26, 28–30.

Capacity planning should include:
- model artifact/runtime weight footprint;
- KV/cache structure;
- context;
- concurrency;
- runtime workspaces/headroom;
- multi-GPU split semantics if applicable.

Do not use:

```text
GGUF file size <= total VRAM
```

as the sole fit rule.

---

# Part VII — Software gate

Reuse Slices 06, 14–17 and 23.

Separate:
- hardware exists;
- driver recognizes hardware;
- backend builds/loads;
- exact operation/model path runs.

A cheap GPU with no reliable intended backend can fail the machine design even with enough VRAM.

---

# Part VIII — Multi-GPU/topology gate

Reuse Slice 11 and Slice 46.

For a split model, record:
- GPU count/identity;
- per-device VRAM;
- split mode;
- PCIe/NVLink/xGMI topology;
- P2P support;
- lane/platform constraints;
- sustained scaling evidence.

Two GPUs that individually pass do not automatically form a good multi-GPU system.

---

# Part IX — Host RAM gate

Reuse Slice 44.

Record:
- installed RAM;
- available-memory evidence under representative state;
- model-loading/offload demand;
- swap/page-fault behavior if relevant.

Do not use MemFree alone on Linux.

For Apple unified memory, do not force a discrete VRAM+RAM model onto UMA.

---

# Part X — Storage gate

Reuse Slice 43.

Storage asks at least:
- enough capacity for artifacts/cache/evidence;
- acceptable startup/load behavior;
- filesystem/path/permissions;
- expected model hash present.

Storage bandwidth can affect cold/model load while having little effect on steady TG after weights are resident.

---

# Part XI — PSU/cable gate

Reuse Slice 47.

Pass requires more than:

```text
PSU watts >= estimated watts
```

Also record:
- exact PSU identity;
- headroom policy;
- required GPU power paths;
- modular cable compatibility;
- connector condition;
- transient/documentation unknowns.

Known incompatible cable/path is a hard failure.

---

# Part XII — Thermal/sustained gate

Reuse Slice 45.

A machine can pass a 20-second benchmark and fail the intended sustained workload.

Record:
- repeated TG/serving throughput;
- temperature;
- clocks;
- limiter/error evidence;
- airflow/chassis state.

If the workload target requires sustained performance and the machine degrades below the target:

```text
REVISE
```

Cooling is part of compute capacity.

---

# Part XIII — Serving/SLO gate

Reuse Slices 34–37.

For a service machine, target can include:
- TTFT p95;
- ITL p95/proxy;
- request throughput;
- SLO compliance;
- concurrency/fairness;
- queue/admission behavior.

A machine can have excellent single-user TG but fail the multi-user SLO.

---

# Part XIV — Privacy/network gate

Reuse Slice 38.

If the design requires LAN service, specify:
- bind scope;
- authentication;
- TLS path where needed;
- admin/metrics exposure;
- prompt/log policy;
- tool/agent trust boundary.

A public/wider-network design with unresolved auth/network exposure is BLOCKED, not “probably fine”.

---

# Part XV — Reliability/upgrade gate

Reuse Slices 39–40.

A long-lived machine should have:
- readiness/restart evidence;
- exact model/runtime identity;
- known-good baseline;
- rollback path for updates.

This may be a preference for a hobby desktop, but can be a hard requirement for a 24/7 service target.

---

# Part XVI — Energy/TCO

Reuse Slices 18, 21 and 42.

Separate:
- purchase price;
- required platform upgrades;
- electricity/duty cycle;
- cooling/platform cost;
- risk reserve/repair uncertainty.

Do not rank used GPUs by sticker price alone.

---

# Part XVII — Synthetic balanced build

Target:
- one quantized model;
- 24 GiB runtime capacity requirement;
- 64 GiB host RAM target;
- single GPU;
- local/loopback service;
- 850 W PSU/cables confirmed;
- budget 1200 units.

Observed design:
- 24 GiB GPU;
- runtime supported;
- RAM 64 GiB;
- storage sufficient;
- PSU/cables pass;
- sustained workload pass;
- budget 1050.

Result:

```text
ACCEPT
```

This says the declared feasibility gates pass. It does not say this is the universally best machine.

---

# Part XVIII — Known capacity failure

Target requires:

```text
30 GiB runtime capacity
```

Design has:

```text
24 GiB
```

All other fields may be excellent.

Result:

```text
REVISE
```

Possible revisions:
- smaller quant/model;
- lower context/concurrency;
- offload strategy;
- multi-GPU;
- different GPU.

The validator should not choose the revision automatically.

---

# Part XIX — Unknown PSU cable case

GPU/model/software all appear good.

But:

```text
modular cable compatibility = UNKNOWN
```

for a secondhand modular PSU.

Result:

```text
BLOCKED
```

because the unknown is safety/purchase critical.

Do not downgrade it to a preference.

---

# Part XX — Evidence links, not copied folklore

A real machine dossier should point to:
- model dossier;
- benchmark manifest;
- hardware inventory;
- used-GPU acceptance;
- PSU dossier;
- thermal evidence;
- serving trace;
- Evidence Packet hashes.

If a number came from a seller listing or forum post, label its provenance rather than copying it as measured truth.

---

# Part XXI — Graduation-design structure

A final machine-design report should explain:

1. workload/goal;
2. model requirement;
3. hardware architecture;
4. every hard gate;
5. every unresolved unknown;
6. benchmark/SLO evidence;
7. cost/energy;
8. risks;
9. upgrade/rollback plan;
10. final decision.

A good report can conclude:

```text
DO NOT BUY YET
```

if the evidence is missing.

That is a successful engineering result.

---

# Claims to avoid

- “one score can replace hard compatibility gates”;
- “enough aggregate VRAM means the model definitely fits/runs”;
- “unknown support can be treated as likely PASS”;
- “faster GPU rescues an invalid PSU cable path”;
- “single-user TG proves serving SLO”;
- “all components individually pass means multi-GPU topology is good”;
- “cheapest sticker price means lowest TCO”;
- “ACCEPT means universally optimal”.
