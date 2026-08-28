# Experiment 61 — Canonical Production IDs

These IDs already exist in the production Intelligence catalog.

They are identity references only.

They are not compatibility, performance, condition, price or purchase claims.

## Hardware

~~~text
NVIDIA GeForce RTX 3090 24GB
hw:nvidia:geforce-rtx-3090:24g

AMD Radeon RX 7900 XTX 24GB
hw:amd:radeon-rx-7900-xtx:24g

Apple Mac Studio M4 Max (40-core GPU, 64GB unified memory)
hw:apple:mac-studio-m4-max-40gpu:64g

Intel Arc A770 16GB
hw:intel:arc-a770:16g
~~~

## Model

~~~text
Qwen3-8B
model:qwen:qwen3-8b
~~~

## Runtime

~~~text
llama.cpp
runtime:ggml-org:llama.cpp
~~~

## First real acquisition skeleton

The current NVIDIA-first real acquisition skeleton uses:

~~~text
hardware_id = hw:nvidia:geforce-rtx-3090:24g
model_id    = model:qwen:qwen3-8b
runtime_id  = runtime:ggml-org:llama.cpp
~~~

File:

~~~text
real-evidence-session.rtx3090-qwen3-8b-llamacpp.skeleton.json
~~~

Only these canonical IDs are prefilled.

All local paths and build/execution details remain placeholders and must be established on the actual benchmark machine.

## Scope caution

A canonical ID only tells the tools which catalog entity you mean.

It does not prove:
- the current llama.cpp build supports that exact path;
- the selected GGUF fits;
- the benchmark will pass;
- the GPU is healthy;
- the current market price is acceptable.

Those remain separate evidence domains.
