# Evidence — Experiment 48: Whole-Machine System Integration Dossier

状态：system-integration slice implemented; L0 feasibility states verified; real Evidence-linked machine dossier ready.

## Claim

> Whole-machine design should use hard gates and blocking unknowns before performance/price preferences. A universal weighted score must not average away a fatal compatibility failure.

## Decision model

```text
known required gate FAIL
→ REVISE

purchase/safety/compatibility-critical UNKNOWN
→ BLOCKED

all required gates PASS
→ ACCEPT
```

Preferences are evaluated only after feasibility.

## Integrated domains

The dossier connects prior course Evidence for:
- workload/model identity;
- runtime VRAM/capacity;
- backend/software support;
- multi-GPU topology;
- host RAM;
- storage/model loading;
- PSU/cables;
- sustained thermal performance;
- serving SLO;
- network/privacy;
- budget/TCO;
- reliability/rollback.

## Experiment 90 verification

### Balanced case

Synthetic design:
- runtime VRAM requirement 24 GiB;
- runtime-confirmed capacity 24 GiB;
- backend supported;
- host RAM 64 GiB vs 48 GiB requirement;
- storage sufficient;
- PSU capacity/cable gates pass;
- sustained target passes;
- serving SLO passes;
- loopback-only scope;
- cost 1050 <= budget 1200.

Verified:

```text
DECISION: ACCEPT
```

This means feasible for the declared target, not universally optimal.

### Known VRAM failure

```text
required runtime capacity = 30 GiB
available = 24 GiB
```

Verified:

```text
DECISION: REVISE
```

The validator does not auto-select whether to change model, quant, context, offload, GPU or multi-GPU topology.

### Unknown cable compatibility

All other synthetic gates pass, but:

```text
psu.cable_compatibility_confirmed = UNKNOWN
```

Verified:

```text
DECISION: BLOCKED
```

This prevents purchase/safety-critical unknowns from being guessed as PASS.

## No weighted score

The feasibility validator intentionally excludes preference weights.

Example rejected logic:

```text
speed 10/10
price 10/10
VRAM 0/10
→ average still high
```

Correct logic:

```text
VRAM hard gate failed
→ current design REVISE
```

## Experiment 91

The real dossier freezes the machine target first, then requires every required gate to have:

```text
status: PASS / FAIL / UNKNOWN
source: path/URL/hash
```

Recommended sources include prior course artifacts such as:
- Model Architecture Dossier;
- benchmark/workload manifest;
- vendor hardware inventory;
- multi-GPU topology;
- host-memory/storage packets;
- Used-GPU and PSU dossiers;
- thermal evidence;
- serving trace;
- release/rollback evidence.

Missing source or UNKNOWN required evidence prevents final ACCEPT.

## Evidence principle

A real machine report should link raw Evidence rather than retyping folklore or seller claims as measured facts.

A valid final result may be:

```text
BLOCKED — do not buy yet
```

when a critical fact is unresolved.

That is a successful engineering conclusion.

## Learner should reject

- one hardware score can replace compatibility gates;
- aggregate VRAM alone proves fit;
- unknown software/cable/topology evidence can be assumed likely PASS;
- faster hardware rescues an invalid PSU or software stack;
- single-user TG proves serving SLO;
- individually healthy GPUs automatically make a good multi-GPU topology;
- ACCEPT means universally optimal.
