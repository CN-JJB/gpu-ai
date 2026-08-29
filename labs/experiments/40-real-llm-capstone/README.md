# Experiment 40 — Real Local-LLM Capstone A/B

硬件等级：L1/L2/L3，取决于硬件。

风险：默认采集和 benchmark 均为普通用户态运行；不修改 BIOS/功耗/超频。

## Goal

Complete the full course loop on one real machine:

```
hardware profile
→ runtime identity
→ model SHA
→ baseline
→ bottleneck hypothesis
→ ONE intentional variable
→ candidate
→ validate experiment discipline
→ compare
→ explain result
```

## Files

- `collect-profile.sh`
- `run-benchmark.sh`
- `baseline-manifest.template.json`
- `candidate-manifest.template.json`
- `validate_ab.py`
- `compare_bench.py`
- `CAPSTONE-CARD.md`

## 1. Hardware/runtime profile

```bash
export MODEL=/path/to/model.gguf
export LLAMA_BENCH=llama-bench
./collect-profile.sh | tee profile.txt
```

The collector is best-effort and records vendor-specific identity when tools are available:

- NVIDIA: `nvidia-smi`
- AMD: `amd-smi` / `rocminfo`
- Apple: `system_profiler` / Metal-capable system identity
- Intel: `sycl-ls`
- llama.cpp: version + device list
- model: bytes + SHA256

For deeper vendor-specific inventory, reuse Experiments 24, 26, 28 or 30.

## 2. Choose the baseline

Start from a stable configuration you can explain.

Example only:

```bash
export OUT=baseline.json
export PP=512
export TG=128
export REPEATS=5
export EXTRA_ARGS='-ngl 99 -fa 0'
./run-benchmark.sh
```

Before running, confirm current:

```bash
llama-bench --help
```

because flags can change across upstream versions.

## 3. Fill baseline manifest

Copy:

```bash
cp baseline-manifest.template.json baseline-manifest.json
```

Fill exact:
- model SHA256;
- runtime version/commit;
- device identity;
- PP/TG/repeats;
- semantic config fields;
- exact full command in `command_record`;
- raw result path.

`command_record` is audit evidence. It is deliberately **not** counted as an independent configuration variable by `validate_ab.py`, because changing one semantic option naturally changes the command string too.

## 4. Diagnose

Use:
`reference/system/capstone-bottleneck-decision-tree.md`

Write one hypothesis before the candidate run.

Example:

```
PP is weak while TG is healthy.
Hypothesis: attention/prefill kernel is the current bottleneck.
```

## 5. Choose exactly one variable

Example:

```
intentional_variable = config.flash_attention
```

Baseline:
```
false
```

Candidate:
```
true
```

Everything else in `config` should stay equal.

## 6. Run candidate

Example only:

```bash
export OUT=candidate.json
export EXTRA_ARGS='-ngl 99 -fa 1'
./run-benchmark.sh
```

Then fill:

```bash
cp candidate-manifest.template.json candidate-manifest.json
```

Record the exact candidate command in `command_record`.

## 7. Validate the A/B

```bash
python3 validate_ab.py baseline-manifest.json candidate-manifest.json
```

Expected for a valid experiment:

```
IDENTITY CHECK: PASS
ONE-VARIABLE CHECK: PASS
PLACEHOLDER CHECK: PASS
```

The validator checks:
- same model SHA;
- same runtime identity;
- same device identity;
- same PP/TG/repetitions;
- exactly one declared semantic `config.*` field differs.

It does **not** prove that hidden environment/thermal state is identical. You still record those manually.

## 8. Compare throughput

```bash
python3 compare_bench.py baseline.json candidate.json
```

Outputs PP/TG and speedup where current llama-bench JSON contains the expected fields.

## 9. Telemetry

Capture vendor telemetry before/after or during the run when available.

Examples:
- NVIDIA: `nvidia-smi`
- AMD: `amd-smi`
- Apple: system/Metal working-set evidence
- Intel: SYCL/XPU device state

Do not force one vendor's command onto another.

## 10. Complete CAPSTONE-CARD

A valid conclusion can be:

```
optimization helped
```

or:

```
optimization did not help
```

Both pass if the experiment is controlled and explained.

## Minimum graduation evidence

- `profile.txt`
- exact model hash
- baseline manifest + raw JSON
- candidate manifest + raw JSON
- A/B validator output
- comparison output
- CAPSTONE-CARD


## Stricter manifest upgrade

This Experiment 40 manifest remains a compact beginner A/B path.

For later course work, prefer Experiment 61:

```
labs/experiments/61-real-benchmark-evidence-packet/
```

It extends this lab with:
- prompt token identity;
- quality-evaluation identity;
- semantic variable blocks;
- quantization-friendly model-artifact changes;
- Evidence Packet hashes.

Do not maintain two conflicting truths: Experiment 61 is the stricter reproducibility contract, while Experiment 40 remains the simpler controlled-A/B introduction.


## Hypothesis

只要 baseline/candidate identity 固定且只改变一个声明的 semantic variable，就可以把 PP/TG 差异作为该受控 A/B 的描述性证据；优化无收益也是有效结果。

## Fixed variables

exact model/runtime/device/PP/TG/repeats 与除 intentional variable 外的 config 固定；thermal/background state 记录但 validator 无法自动证明一致。

## What to observe

- profile/artifact identity；
- ONE-VARIABLE validator；
- baseline/candidate raw PP/TG；
- candidate 是否符合原先 bottleneck hypothesis；
- negative/neutral result 是否被完整保留。

## Troubleshooting

- CLI flags 以当前 --help 为准。
- command string 变化不等于第二个 semantic variable。
- hidden thermal/background change 需要人工检查。
- 多块 semantic config 改变时改叫 system comparison。

## Evidence to save

保存 profile、两份 manifest/raw JSON、validator、comparison 和 CAPSTONE-CARD。

## What this proves

你能在一台真实机器上完成“诊断 → 单变量修改 → 复测 → 解释”的基础工程闭环。

## What this does NOT prove

它不替代 Experiment 61 的更严格 prompt/quality/packet contract。

## No-hardware fallback

完成 Experiment 39；真实 A/B 等上课时执行。

## Transfer question

候选 TG 提升 8%，但运行时 GPU 温度/clock 明显不同。为什么还不能立刻把 8% 全归因给 intentional variable？
