---
experiment_id: example-speculative-acceptance-overhead
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

Acceptance、draft length 与 proposer/verification overhead 如何共同决定 speculative decoding 是否加速？

## Hardware

无特殊硬件。

## Software

Python 3。

## Configuration

Synthetic baseline：

~~~text
target serial step/token = 1.0
~~~

Spec cost：

~~~text
draft/token = 0.08
verify = 1.08 + 0.04 × D
~~~

Acceptance model：

- each draft position survives independently with probability p until first rejection
- p = 0.30 / 0.60 / 0.90
- D = 1 / 2 / 4 / 8

Expected progress：

~~~text
1 + p + p² + ... + p^D
~~~

## Results

| p | D | expected progress | round cost | speedup |
|---:|---:|---:|---:|---:|
| 0.30 | 1 | 1.3000 | 1.2000 | 1.083× |
| 0.30 | 2 | 1.3900 | 1.3200 | 1.053× |
| 0.30 | 4 | 1.4251 | 1.5600 | 0.914× |
| 0.30 | 8 | 1.4285 | 2.0400 | 0.700× |
| 0.60 | 1 | 1.6000 | 1.2000 | 1.333× |
| 0.60 | 2 | 1.9600 | 1.3200 | 1.485× |
| 0.60 | 4 | 2.3056 | 1.5600 | 1.478× |
| 0.60 | 8 | 2.4748 | 2.0400 | 1.213× |
| 0.90 | 1 | 1.9000 | 1.2000 | 1.583× |
| 0.90 | 2 | 2.7100 | 1.3200 | 2.053× |
| 0.90 | 4 | 4.0951 | 1.5600 | 2.625× |
| 0.90 | 8 | 6.1258 | 2.0400 | 3.003× |

## Observations

### Low acceptance makes long drafts wasteful

At p=0.30, expected progress saturates near 1.43 tokens/round while round cost keeps increasing.

### Medium acceptance has an interior optimum

At p=0.60, D=2 is slightly better than D=4 and clearly better than D=8 in this cost model.

### High acceptance can justify longer proposals

At p=0.90, accepted progress grows fast enough to amortize the longer proposal/verification cost.

## Conclusion

The useful performance equation is not：

~~~text
acceptance high → fast
~~~

but：

~~~text
accepted sequence progress
--------------------------
draft + verify overhead
~~~

Speculative decode helps only when the numerator grows faster than the cost.

## Boundary

Synthetic units do not predict llama.cpp/vLLM/TensorRT-LLM speed.

Real systems have correlated acceptance、dynamic drafting、tree/block methods、sampling correction、KV/memory and batching interactions.

## Reproducibility

See：

- labs/experiments/15-speculative-acceptance-overhead-model/simulate.py
- labs/experiments/15-speculative-acceptance-overhead-model/EXPECTED.md

## Sources

- Leviathan et al. speculative decoding
- Chen et al. speculative sampling
- llama.cpp speculative decoding
- vLLM speculative decoding
- TensorRT-LLM speculative decoding
