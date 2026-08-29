# Experiment 87 — Real Used-GPU Purchase Acceptance Packet

硬件等级：L2。

## Goal

Collect read-only hardware identity/error evidence and combine it with the ordinary sustained Local-LLM workload from Experiment 85.

Default lab does **not**:
- flash VBIOS/firmware;
- overclock/undervolt;
- change power limit/fan curve;
- inject errors;
- run destructive VRAM stress.

## 1. Write seller claim first

Copy:

```bash
cp CLAIM-TEMPLATE.md claim.md
```

Record before interpreting the card:
- exact marketed model;
- promised VRAM;
- promised display/output condition;
- included accessories/adapters;
- any seller test claim.

## 2. Collect hardware identity

### Linux

```bash
./collect-linux.sh evidence-hardware
```

The script stores, when available:
- `lspci -nnk`;
- verbose PCI information;
- `nvidia-smi -L` and `nvidia-smi -q`;
- AMD SMI list/static/PCIe/ECC/bad-page raw output.

It is read-only.

### Windows

```powershell
./collect-windows.ps1 -OutDir evidence-hardware
```

It stores:
- PnP/display-controller identity;
- NVIDIA SMI raw output if installed;
- AMD SMI raw output if installed.

## 3. Check PCIe carefully

Record both:
- max/capability where available;
- current/negotiated state.

If current state is unexpectedly low while idle:

```text
REVIEW
```

then check:
- motherboard slot wiring;
- CPU lanes;
- riser;
- bifurcation;
- representative under-load state.

Do not call the card defective from idle downshift alone.

## 4. Error telemetry

Record exactly what the hardware supports.

If ECC/RAS is unavailable:

```text
N/A / NOT_SUPPORTED
```

not:

```text
0 errors
```

Look for raw evidence such as:
- NVIDIA query/error state and relevant OS/driver logs;
- AMD ECC/RAS/bad pages/PCIe replay/recovery where supported;
- runtime errors during the workload.

## 5. Run intended workload

Reuse Experiment 85 with the exact card/model you are evaluating.

Record:
- model SHA;
- runtime identity;
- repeated TG samples;
- telemetry;
- sustained drift;
- any runtime failure.

This is more purchase-relevant than a random graphics benchmark if your use case is Local LLM.

## 6. Display outputs

Software collection does not prove HDMI/DP works.

If display output matters to your purchase, test each required port separately with known-good:
- cable;
- monitor;
- mode/resolution.

Record results in `RESULT-TEMPLATE.md`.

## 7. Physical inspection

With power off and using ordinary electrical safety:
- inspect connectors;
- fan condition/noise;
- corrosion/liquid residue;
- damaged PCB/cooler/power connector.

Do not disassemble during a return-window test unless you accept warranty/return consequences.

## 8. Decision

Finish with one of:

```text
ACCEPT
REVIEW
REJECT
```

and list the exact evidence supporting the decision.

## 9. Evidence hygiene

Hash the packet using Experiment 61.

Do not publish serials/UUIDs if you consider them private inventory identifiers; redact in the public copy while retaining local originals if needed.


## 10. Machine-readable Intelligence bridge

Copy:

~~~bash
cp acceptance-case.template.json acceptance-case.json
~~~

Fill the summary from the retained raw evidence and include that case in a PACKET with the supporting files.

Build the Experiment 86-compatible machine decision:

~~~bash
python3 ../../../tools/intelligence/evaluate_used_gpu_acceptance.py \
  --case acceptance-case.json \
  --packet PACKET.json \
  --out acceptance.json
~~~

Verify it independently:

~~~bash
python3 ../../../tools/intelligence/verify_used_gpu_acceptance.py \
  --acceptance acceptance.json \
  --case acceptance-case.json \
  --packet PACKET.json
~~~

Then derive condition-evidence provenance:

~~~bash
python3 ../../../tools/intelligence/derive_condition_evidence_grade.py \
  --acceptance acceptance.json \
  --case acceptance-case.json \
  --packet PACKET.json \
  --out condition-evidence.json
~~~

For real non-synthetic evidence, this current path can produce C3 provenance.

Important:

~~~text
C3
!=
ACCEPT
~~~

C3 means the evidence is learner-owned, PACKET-bound and independently reproducible.

The separate technical decision may still be ACCEPT, REVIEW or REJECT.

C4 is reserved and is not emitted by the current tooling.


## Why this experiment

这是更完整的真实购买验收主路径：先冻结 seller claim，再收集硬件 identity/error/PCIe/physical evidence，最后用你真正关心的持续 LLM workload 验证。

## Hypothesis

真实 ACCEPT 必须同时满足 purchase-critical claim、可用软件路径和普通 sustained workload；C3 只表示 evidence provenance 强，不等于 technical decision 必须 ACCEPT。

## Fixed variables

验收期间不刷 firmware、不超频/降压、不改 power/fan，也不做破坏性压力注入。先观察收到时的状态。

## What to observe

- seller claim 与 observed model/VRAM；
- PCIe max/current 与 under-load context；
- supported error telemetry；
- repeated TG + thermal drift；
- physical/output requirements；
- ACCEPT/REVIEW/REJECT 与 C-grade provenance 的独立性。

## Troubleshooting

- idle PCIe downshift 先 REVIEW。
- N/A telemetry 不能写 0。
- display port 未测试就保持 UNKNOWN。
- serial/UUID 发布前按隐私需要脱敏。
- machine-readable summary 必须能回到 retained raw packet。

## Evidence to save

保存 claim.md、hardware raw、Experiment 85 evidence、physical/output notes、RESULT-TEMPLATE、PACKET、acceptance.json 和 condition-evidence.json。

## What this proves

你能用真实、PACKET-bound Evidence 做一次二手 GPU 技术验收。

## What this does NOT prove

C3 不是购买命令，也不是未来永久可靠性保证。

## No-hardware fallback

完成 Experiment 86；真实验收等有候选卡时执行。

## Transfer question

一张卡得到 C3 provenance，但 technical evaluator 输出 REVIEW。为什么这两者完全可以同时成立？
