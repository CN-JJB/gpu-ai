---
experiment_id: example-effective-bpw-metadata
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

为什么 nominal 4-bit quantized model 的 whole-model effective bpw 会高于 4？

## Hardware

无特殊硬件。

## Software

Python 3。

## Configuration

Abstract 7B model。

1. 4-bit codes + one FP16 scale/group。
2. group sizes 32 / 64 / 128。
3. optional FP16 zero-point。
4. 95% quantized + 5% FP16 parameters。

## Results

### Scale only

| group | quant bpw | 7B payload |
|---:|---:|---:|
| 32 | 4.500 | 3.667 GiB |
| 64 | 4.250 | 3.463 GiB |
| 128 | 4.125 | 3.361 GiB |

### Scale + zero

| group | quant bpw |
|---:|---:|
| 32 | 5.000 |
| 64 | 4.500 |
| 128 | 4.250 |

### 95% group64 scale-only + 5% FP16

- quantized region = 4.25 bpw
- whole model = 4.8375 bpw
- payload ≈ 3.942 GiB
- pure 4-bit baseline ≈ 3.260 GiB

## Conclusion

Nominal code width is not whole-model storage width。

```text
code bits
+ per-group metadata
+ unquantized/mixed tensors
+ format overhead
→ effective bpw
```

实验不声称复现任何命名 quantization format。

## Transfer

真实模型仓库：
1. identify quantization method；
2. identify container/representation；
3. inspect quant metadata；
4. 从 artifact size + parameter count 检查 effective bpw；
5. separately verify target backend/hardware compatibility。

## Sources

- Hugging Face quantization overview
- Hugging Face Safetensors metadata
- llama.cpp GGUF + quantize implementation
- GPTQ paper
- AWQ paper
- ExLlamaV2 EXL2 documentation
