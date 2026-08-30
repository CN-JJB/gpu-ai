# Experiment 09 — 为什么 nominal 4-bit 不等于 4.000 bpw？

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3

<figure>
  <img src="../../../assets/diagrams/experiment-effective-bpw.svg" alt="Effective bpw 把 exact file bytes 与参数量联系起来；标称量化 bit 之外还有 scale、metadata 与 mixed tensors。">
  <figcaption>Effective bpw 把 exact file bytes 与参数量联系起来；标称量化 bit 之外还有 scale、metadata 与 mixed tensors。</figcaption>
</figure>

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


## Hypothesis

nominal q-bit 只描述 code payload；只要每 group 还要保存 scale/zero-point，或者一部分 tensor 保留更高精度，whole-model effective bpw 就会高于 nominal qbits。

## Fixed variables

一次只改变 group size、zero-point 或 quantized fraction 中的一项；参数量和其他 metadata 位数保持不变。

## What to observe

1. group size 越小，metadata 被更多 group 重复，因此 bpw 越高。
2. zero-point 增加固定 per-group 成本。
3. 少量 FP16 tensor 为什么也会把 overall bpw 明显抬高。
4. effective bpw 与最终文件 bytes 之间还缺哪些格式/对齐开销。

## Troubleshooting

- 参数量单位 B 与实际整数参数数不要混。
- group metadata 不能只算一次，要按 group 数量分摊。
- 不要用这个 toy 直接比较 AWQ/GPTQ/GGUF/EXL2 哪个一定更小。
- 真 artifact 应优先用 exact file bytes 与 metadata 反推/验证。

## What this proves

你能解释 nominal bit-width 与 effective bpw 为什么不同，并能做最小 metadata accounting。

## What this does NOT prove

它不是任何具体量化格式的完整文件模型，也不预测质量或速度。

## No-hardware path

完整 L0。

## Transfer question

两个都叫“4-bit”的 artifact，文件大小差 12%。在怀疑下载损坏前，你至少应该检查哪些 metadata/格式因素？
