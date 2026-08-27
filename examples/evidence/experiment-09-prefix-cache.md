---
experiment_id: example-prefix-cache-capacity
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

有限 Prefix Cache 的容量、命中与 eviction 如何影响重复前缀的 prefill work？为什么 decode work 不随 prefix-cache hit 改变？

## Hardware

无特殊硬件。

## Software

Python 3。

## Configuration

Request sequence：

~~~text
A, B, A, C, A, B
~~~

Per request：

- shared prefix = 1024 tokens
- unique suffix = 64 tokens
- new output = 128 tokens

Synthetic cache：

- capacity = 0 / 1 / 2 / 3 whole-prefix entries
- LRU-like eviction
- exact prefix ID match only

## Results

| capacity | hits | hit rate | evictions | prompt processed | reused | saved | decode total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0.0% | 0 | 6528 | 0 | 0 | 768 |
| 1 | 0 | 0.0% | 5 | 6528 | 0 | 0 | 768 |
| 2 | 2 | 33.3% | 2 | 4480 | 2048 | 2048 | 768 |
| 3 | 3 | 50.0% | 0 | 3456 | 3072 | 3072 | 768 |

Capacity 2 trace：

~~~text
A MISS → [A]
B MISS → [A,B]
A HIT  → [B,A]
C MISS, evict B → [A,C]
A HIT  → [C,A]
B MISS, evict C → [A,B]
~~~

## Observations

### Cache enabled does not imply cache useful

Capacity=1 is enabled but produces zero hits because the working set repeatedly displaces itself.

### Reused tokens matter more than hit count alone

Each exact hit saves 1024 prefix tokens of prompt processing in this simplified model.

### Decode work is invariant

All cases generate：

~~~text
6 × 128 = 768 new tokens
~~~

Prefix cache never removes those new-token decode steps.

## Conclusion

The useful accounting chain is：

~~~text
matching prefix
+ reusable state still resident
→ reused prompt tokens
→ less prefill work
→ lower TTFT opportunity
~~~

while：

~~~text
new generated tokens
→ still require decode
~~~

Finite cache capacity creates a second trade-off：

~~~text
retain more reusable KV
↔ leave less memory for active KV / other work
~~~

## Boundary

This L0 model uses whole-prefix entries, not real pages/blocks.

Real runtimes can have：

- partial prefix hits；
- block granularity；
- hashes/cache keys；
- adapters/model state in cache identity；
- active block references；
- eviction/offload；
- tenant isolation。

## Reproducibility

See：

- labs/experiments/13-prefix-cache-capacity-model/simulate.py
- labs/experiments/13-prefix-cache-capacity-model/EXPECTED.md

## Sources

- llama.cpp server prompt cache/timings
- vLLM Automatic Prefix Caching
- vLLM Prefix Caching design
- NVIDIA TensorRT-LLM KV cache reuse
