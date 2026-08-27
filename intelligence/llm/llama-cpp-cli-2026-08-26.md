---
snapshot_date: 2026-08-26
type: dynamic-intelligence
topic: llama-cpp-cli-build-benchmark
---

# llama.cpp CLI / Build / Benchmark Snapshot — 2026-08-26

## Purpose

llama.cpp CLI flags and build switches evolve. Stable Lessons teach the concepts; this file records current upstream spellings for Experiment 10.

Always re-check:

```bash
llama-cli --version
llama-cli --help
llama-bench --help
```

before a real deployment.

## Current build examples

Source:
https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md

### CPU

```bash
cmake -B build
cmake --build build --config Release
```

### NVIDIA CUDA

```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

### AMD HIP

Current upstream uses:

```bash
cmake -B build -DGGML_HIP=ON
cmake --build build --config Release
```

Architecture-specific `GPU_TARGETS` can be supplied when needed.

### Apple Metal

Current upstream build docs state Metal is enabled by default on macOS. Runtime use must still be verified from device/startup logs.

## Current llama-cli concepts / spellings

Source:
https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md

Current CLI exposes, among others:

- `--version`
- `--list-devices`
- `-t / --threads`
- `-c / --ctx-size`
- `-n / --n-predict`
- `-p / --prompt`
- `--perf`
- `-m / --model`
- `-hf / --hf-repo`
- `-ngl / --gpu-layers / --n-gpu-layers`
- `--fit`
- `--fit-target`

At this snapshot, `--n-gpu-layers` accepts exact/auto/all-style selection and auto-fit is available.

Do not make stable course logic depend on exact accepted strings. Experiment 10 records the current `--help`.

## Model loading

Source:
https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md

Current stable concepts:

- llama.cpp consumes GGUF for local model artifacts.
- local GGUF path can be passed directly.
- compatible Hugging Face repositories can be referenced through current HF-loading options.
- non-GGUF source checkpoints require conversion before native llama.cpp use.

For reproducible coursework, local artifact SHA256 is preferred after download.

## llama-bench

Source:
https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md

Current benchmark concepts:

- prompt processing: `pp`
- text generation: `tg`
- configurable prompt/gen token counts
- repetitions
- GPU-layer sweep
- CPU thread sweep
- context depth
- KV cache type
- JSON/CSV/JSONL/SQL output

Current examples/flags include:
- `-p / --n-prompt`
- `-n / --n-gen`
- `-r / --repetitions`
- `-t / --threads`
- `-ngl / --n-gpu-layers`
- `-d / --ctx-size` / context-depth-related test option as documented by current help
- `-ctk`, `-ctv`
- `-o json`

Exact CLI naming must be rechecked on the installed build.

## Benchmark metadata

Current JSON output includes rich reproducibility metadata such as:

- build commit
- CPU info
- GPU info / devices
- backend
- model size
- parameter count
- threads
- GPU layers
- KV cache types
- timing samples / mean / standard deviation

This is why the course stores raw JSON rather than transcribing only a single tokens/s number.

## Important limitation

Current llama-bench documentation states benchmark timing does not include tokenization or sampling.

Therefore:
- pp/tg are backend/runtime baselines;
- they are not complete TTFT / end-user latency measurements.

## Current upstream sample models

The llama.cpp README may show direct `-hf` examples such as small GGUF instruction models.

Course labs deliberately do not pin one forever:
- licenses change;
- repositories move;
- model architectures evolve.

A learner should pick a current compatible small model, record repository/revision/license, then hash the exact downloaded artifact.

## Freshness rule

This snapshot is historical evidence.

For a future deployment:
1. check current upstream docs/help;
2. update a new dated snapshot if interface behavior changed;
3. preserve old snapshots for reproducibility.
