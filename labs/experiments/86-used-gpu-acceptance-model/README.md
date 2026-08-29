# Experiment 86 — Used-GPU Acceptance Decision Model

硬件等级：L0

## Goal

Practice evidence classification without pretending one metric proves card health.

Run three synthetic cases:

```bash
python3 evaluate.py case-healthy.json
python3 evaluate.py case-idle-link-review.json
python3 evaluate.py case-vram-mismatch.json
```

## Expected

### Healthy

```text
ACCEPT
```

### Idle-link case

Current link is low but:
- max capability matches;
- observation is idle;
- runtime/workload otherwise pass.

Result:

```text
REVIEW
```

not REJECT.

### VRAM mismatch

Seller claims 24 GiB while observed is 12 GiB.

Result:

```text
REJECT
```

## Rules

Critical reject examples:
- major purchase-critical VRAM mismatch;
- target runtime not recognized;
- sustained workload repeatedly fails;
- observed uncorrectable hardware errors >0.

Review examples:
- PCIe current state lower than expected without a representative under-load check;
- telemetry unsupported;
- meaningful thermal/TG drift needing investigation;
- display outputs untested for a display-dependent purchase.

## Scope

All cases are synthetic.

The script is not a warranty or hardware-authenticity certificate.


## Why this experiment

二手 GPU 验收不能靠一个“通过/失败”指标。这个模型训练你把 identity、VRAM、PCIe、error、thermal、workload 等证据组合成 ACCEPT / REVIEW / REJECT。

## Hypothesis

Healthy case 应 ACCEPT；idle-link 因当前 PCIe state 可能只是省电状态，所以 REVIEW；VRAM mismatch 是购买关键 claim 冲突，应 REJECT。

## Fixed variables

使用三个 synthetic case 原样运行，不修改 evaluator 规则。

## What to observe

1. idle current link 与 max capability 的区别。
2. VRAM mismatch 为什么比单个低速 link 更严重。
3. unsupported telemetry 为什么通常是 UNKNOWN/REVIEW，不是“0 error”。
4. repeated workload failure 与单次异常的证据强度。

## Troubleshooting

- current PCIe Gen/width 在 idle 下可能动态降低。
- N/A 不是 0。
- 一次短测通过不能证明长期可靠。
- 真机 acceptance 要绑定 seller claim、exact device identity 和代表性 LLM workload。

## Evidence to save

保存三个 case、输出，并写出每个 decision 的关键证据链。

## What this proves

你会按证据严重性区分 ACCEPT / REVIEW / REJECT。

## What this does NOT prove

它不是保修、真伪鉴定或真实硬件健康证明。

## No-hardware path

完整 L0。

## Transfer question

为什么“当前 PCIe x1”通常值得 REVIEW，而“卖家声称 24GiB、runtime 只见 12GiB”通常应直接 REJECT？
