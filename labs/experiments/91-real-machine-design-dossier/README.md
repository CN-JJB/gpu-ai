# Experiment 91 — Real Whole-Machine Design Dossier

硬件等级：L1–L3，取决于设计。

## Goal

Join prior course Evidence into one auditable machine feasibility decision.

This experiment does not buy hardware or change the machine.

## 1. Freeze target first

Copy:

```bash
cp TARGET-TEMPLATE.md target.md
```

Define:
- model/artifact;
- context/concurrency;
- local interactive vs serving workload;
- SLO if serving;
- privacy/network scope;
- maximum budget.

Do this before ranking hardware.

## 2. Build evidence matrix

Copy:

```bash
cp dossier.template.json dossier.json
```

Each hard gate contains:

```text
status: PASS / FAIL / UNKNOWN
source: path/URL/hash
```

Do not enter PASS without evidence.

## 3. Recommended evidence sources

### Model
- Slice 29 Model Dossier;
- Slice 05/30 capacity;
- Experiment 61 manifest.

### GPU / software
- vendor inventory Slices 14–17;
- Slice 46 used-GPU validation;
- Slice 23 vendor preflight.

### Multi-GPU
- Experiment 18 topology/scaling.

### Host RAM
- Experiment 83.

### Storage
- Experiment 81.

### PSU/cables
- Experiment 89.

### Thermal
- Experiment 85.

### Serving
- Experiment 63 plus SLO analysis.

### Power/TCO
- Experiment 79 plus market/watchlist evidence.

### Reliability
- Experiment 73/75.

## 4. Validate

```bash
python3 validate_dossier.py dossier.json
```

Decisions:

```text
ACCEPT
REVISE
BLOCKED
```

### ACCEPT
All declared hard gates PASS.

### REVISE
At least one required gate is known FAIL and no critical UNKNOWN remains.

### BLOCKED
At least one required purchase/safety/compatibility gate remains UNKNOWN.

## 5. Preferences

After feasibility, compare candidates separately using:
- performance;
- energy;
- noise;
- price/TCO;
- maintenance;
- upgrade room.

Do not let a preference override FAIL/UNKNOWN.

## 6. Hash the packet

Use Experiment 61 to build the final Evidence Packet index.

## 7. Finish

Fill:

```text
DESIGN-REPORT-TEMPLATE.md
```

A valid report may conclude:

```text
BLOCKED — do not buy yet
```

if evidence is missing.
