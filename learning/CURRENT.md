# Current State

## Source of truth

- Repo: `CN-JJB/gpu-ai`
- Branch: `main`
- Course is independent; do not return to old fork history.

## Historical archive

The previous long-form CURRENT state through Slice 45 is preserved byte-for-byte at:

```text
learning/archive/CURRENT-through-slice45-2026-08-27.md
```

Detailed per-slice history also remains in:

```text
learning/records/
examples/evidence/
```

This file now stays intentionally short and tracks the active frontier.

## Completed frontier

```text
Slices 01–48 implemented
Experiments 01–91 exist
```

The course now spans:
- GPU architecture / execution / memory / Roofline;
- four major GPU ecosystems;
- quantization, KV, local inference and serving;
- multi-GPU / interconnect;
- secondhand market / purchase / acceptance;
- model architecture dossier and quality gates;
- benchmark/workload manifests;
- serving SLO/capacity/admission/fairness;
- service privacy/reliability/rollback/observability;
- energy, storage, host RAM/OOM and thermals;
- advanced used-GPU validation;
- PSU / power-delivery integration;
- whole-machine system feasibility.

## Recent frontier

### Slice 43 — Storage / Model Loading

Model bytes → page cache / mmap / page faults → readiness / first inference, kept separate from steady TG.

Real path avoids destructive global cache dropping by default.

### Slice 44 — Host Memory Pressure / Swap / OOM

`MemFree != MemAvailable`; file-backed reclaim differs from anonymous memory; host RAM OOM differs from discrete VRAM OOM; Apple unified memory remains a special architecture.

### Slice 45 — Thermal / Cooling / Sustained Performance

Short cold benchmark != sustained performance.

Evidence combines:

```text
temperature
+ clocks / limiter evidence
+ repeated TG
```

Default real path changes no OC/UV/power/fan settings.

### Slice 46 — Used-GPU Validation / Purchase Acceptance

Slice 20 remains transaction/arrival acceptance.

Slice 46 adds the deeper hardware-evidence layer:

```text
identity
→ VRAM
→ runtime recognition
→ PCIe capability/current state
→ ECC/RAS/XID/error evidence
→ sustained LLM
→ ACCEPT / REVIEW / REJECT
```

Verified L0:

```text
healthy → ACCEPT
idle PCIe x1 current / x16 max → REVIEW
24 GiB claimed / 12 GiB observed → REJECT
```

Default real lab is read-only plus ordinary inference; no firmware flash or destructive VRAM stress.

### Slice 47 — PSU / Power Delivery / Platform Integration

Independent gates:

```text
capacity/headroom
+
connector/cable compatibility
+
transient/documentation uncertainty
```

Verified L0:

```text
850W / 550W / compatible paths → ACCEPT
850W / 820W / synthetic headroom policy → REVIEW
1000W / 600W / incompatible modular cable → REJECT
```

No PSU opening, exposed-mains probing, protection bypass or intentional overload.

### Slice 48 — Whole-Machine System Integration Dossier

The course now combines prior Evidence as:

```text
HARD GATE
PURCHASE-CRITICAL UNKNOWN
PREFERENCE / OPTIMIZATION
```

Decision semantics:

```text
known hard fail → REVISE
critical unknown → BLOCKED
all required gates pass → ACCEPT
```

Verified L0:

```text
balanced design → ACCEPT
known VRAM shortfall → REVISE
unknown PSU cable compatibility → BLOCKED
```

There is deliberately no universal weighted hardware score.

## Stable design rule

Always evaluate in this order:

```text
workload/model identity
→ feasibility hard gates
→ blocking unknowns
→ measured performance/quality/SLO
→ preferences/TCO
→ decision
```

Do not let speed, price or a weighted score average away:
- insufficient VRAM;
- unsupported runtime;
- invalid power path;
- unresolved purchase/safety evidence.

## Next actions

1. Build the graduation Machine Design Capstone.
2. Turn Experiment 91 dossier into a human-readable final design report workflow.
3. Require an Evidence Packet index for every material hardware/model/performance claim.
4. Add revision scenarios: smaller model/quant, different GPU, multi-GPU, PSU/platform upgrade, or tighter serving target.
5. Produce a final `ACCEPT / REVISE / BLOCKED` machine design plus an upgrade roadmap, without auto-purchasing anything.
