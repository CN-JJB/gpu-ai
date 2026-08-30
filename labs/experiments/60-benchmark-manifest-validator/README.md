# Experiment 60 — Semantic Benchmark Manifest Validator

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/benchmark-manifest.svg" alt="Benchmark manifest 把模型、runtime、硬件、workload、参数与 Evidence identity 固定下来，防止条件漂移后仍把结果当可比。">
  <figcaption>Benchmark manifest 把模型、runtime、硬件、workload、参数与 Evidence identity 固定下来，防止条件漂移后仍把结果当可比。</figcaption>
</figure>

## Goal

Prove that "one variable" can be a semantic block.

Synthetic experiment:

```
Q8_0 artifact
→
Q4_K_M artifact
```

The model change necessarily changes:
- artifact SHA;
- bytes;
- quant label.

All belong to:

```
variant.model
```

## Valid run

```bash
python3 validate_manifest_ab.py \
  baseline.json \
  candidate-valid.json
```

Expected:

```
VALIDATION: PASS
```

Semantic differences should be only:

```
variant.model.artifact_bytes
variant.model.artifact_sha256
variant.model.quant
```

## Invalid run

```bash
python3 validate_manifest_ab.py \
  baseline.json \
  candidate-invalid-prompt.json
```

Expected non-zero exit and:

```
VALIDATION: FAIL
undeclared differences:
variant.prompt.token_ids_sha256
```

## Leaf-variable mode

For an execution-only A/B, declare for example:

```
intentional_variable
=
variant.execution.flash_attention
```

Then only that exact semantic leaf may change.

## Scope

The manifests use synthetic hashes and device names.

No performance or quality result is implied.


## Why this experiment

“我只改了量化”在文件层面会同时改变 SHA、bytes、quant label。实验纪律要求的是**只改变一个语义变量块**，而不是只允许一个 JSON leaf 变化。

## Hypothesis

合法的 model-artifact A/B 可以同时改变 artifact bytes、SHA 和 quant，因为它们都属于 variant.model；如果 prompt token identity 也变了，就属于未声明的第二个语义变量，应 FAIL。

## Fixed variables

baseline/candidate 其余字段全部固定；intentional_variable 必须显式声明。

## What to observe

1. valid case 为什么允许多个 leaf diff。
2. invalid case 的 prompt hash 为什么被抓出。
3. leaf-variable mode 与 semantic-block mode 的区别。
4. validator 为什么只检查 manifest consistency，不检查 benchmark 数值真实性。

## Troubleshooting

- 不要为了 PASS 把 intentional_variable 写得过宽。
- artifact 改变时相关 identity fields 应一起变化。
- prompt、runtime、device、execution semantics 一旦意外变化，应重新设计 A/B，而不是忽略。

## Evidence to save

保存两次 validator 输出和两组 manifest diff。

## What this proves

你能把“单变量实验”定义到语义层，而不是机械 JSON 字段层。

## What this does NOT prove

它不证明任何性能/质量结果有效，也不验证 synthetic hash 对应真实文件。

## No-hardware path

完整 L0。

## Transfer question

如果只想比较 FlashAttention on/off，却同时升级了 runtime SHA，这还是单变量 A/B 吗？
