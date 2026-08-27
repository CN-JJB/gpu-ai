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
