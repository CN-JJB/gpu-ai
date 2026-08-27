# Experiment 09 — 为什么 nominal 4-bit 不等于 4.000 bpw？

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3

## 问题

很多模型写“4-bit”，但真实 weight payload 往往明显大于 `params × 4 / 8`。最小原因之一就是 group quantization metadata。

## 模型

每个 group：
- G 个 weights
- 每 weight q-bit code
- one scale：s bits
- optional zero point：z bits

```text
quant-region bpw = q + (s + z) / G
```

若不是所有 parameters 都量化：

```text
whole-model bpw
= quant_fraction × quant_bpw
+ (1 - quant_fraction) × unquantized_bits
```

## 运行

```bash
python simulate.py --demo
```

demo 比较：
- 4-bit + FP16 scale
- group 32 / 64 / 128
- optional FP16 zero point
- 5% params 保持 FP16

## 自己试

```bash
python simulate.py \
  --params-b 7 \
  --qbits 4 \
  --group-size 64 \
  --scale-bits 16 \
  --zero-bits 0 \
  --quant-fraction 0.95 \
  --unquantized-bits 16
```

## 观察

4-bit + FP16 scale：
- G=32 → 4.5 bpw
- G=64 → 4.25
- G=128 → 4.125

若每 group 再存一个 FP16 zero：
- G=32 → 5.0
- G=64 → 4.5
- G=128 → 4.25

95% 用 4.25 bpw、5% 保持 16-bit：
```text
overall = 4.8375 bpw
```

## 限制

这不是任何具体 AWQ/GPTQ/GGUF/EXL2 文件格式模拟器。

没有建模 alignment、tensor padding、multiple scales、codebooks、importance data、mixed bit per layer、embedding/output rules、tokenizer/config metadata 或 backend repacking。

实验只证明：

```text
nominal code bits != whole-model effective bpw
```

## Evidence

回答：
1. group size 为什么改变 bpw？
2. zero point 为什么也是容量成本？
3. 只有 5% FP16 tensors，为什么 overall bpw 仍明显上升？
4. 为什么不能用这个公式声称“AWQ 一定比 GPTQ 小”？
5. 真实 artifact 应从哪些 metadata 得到真正 size/bpw？
