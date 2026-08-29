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


## Why this experiment

这一步把前面所有零散 Evidence 汇成一台真实机器的可行性结论。关键不是写配置单，而是让每个 hard gate 都能追到来源。

## Hypothesis

只有 required gates 全部 PASS 才能 ACCEPT；已知 FAIL 应 REVISE；purchase/safety/compatibility 关键 UNKNOWN 应 BLOCKED。

## Fixed variables

先冻结 target.md，再建立 dossier。不要看完候选硬件后反向放宽目标来制造 PASS。

## What to observe

- 每个 gate 的 status 与 source；
- UNKNOWN 是否有明确补证据动作；
- FAIL 是否有对应 revision；
- preference 是否只在 feasible candidate 之间比较；
- 最终 packet 是否能追到原始 evidence。

## Troubleshooting

- source 非空不等于证据内容正确，人工仍需复核。
- preference 不得覆盖 FAIL/UNKNOWN。
- 改模型/context/quant 后要重新检查受影响 gates。
- BLOCKED 是合法工程结论。

## Evidence to save

保存 target.md、dossier.json、validator 输出、DESIGN-REPORT-TEMPLATE 和最终 packet hash。

## What this proves

你能对一台真实 Local LLM 机器做可审计的 whole-system feasibility review。

## What this does NOT prove

它不会替你购买硬件，也不会把 UNKNOWN 自动变成 PASS。

## No-hardware fallback

可以用计划购买的候选与已有公开/卖家证据完成大部分 dossier；真实运行 gates 保留 UNKNOWN。

## Transfer question

如果换了量化后 VRAM gate 通过了，为什么还必须重新检查质量与性能相关 gate？
