# Expected result

```bash
python simulate.py --demo
```

```text
Concept model: code bits + per-group metadata; not a real format simulator.

A) 4-bit codes + one FP16 scale per group
  group    quant bpw   7B payload GiB
---------------------------------------
     32        4.500            3.667
     64        4.250            3.463
    128        4.125            3.361

B) 4-bit codes + FP16 scale + FP16 zero per group
  group    quant bpw   7B payload GiB
---------------------------------------
     32        5.000            4.075
     64        4.500            3.667
    128        4.250            3.463

C) 95% quantized at group64 scale-only; 5% remains FP16
quant region bpw: 4.2500
whole-model bpw: 4.8375
7B payload: 3.942 GiB
pure 4-bit baseline: 3.260 GiB
```

## Interpretation

group64 scale-only：

```text
4 + 16/64 = 4.25 bpw
```

mixed tensors：

```text
0.95 × 4.25 + 0.05 × 16 = 4.8375 bpw
```

对抽象 7B，5% FP16 region 将 payload 从纯 4-bit 的约 3.260 GiB 推到约 3.942 GiB。

不要把这些具体数值转移到命名格式。真实 GGUF/GPTQ/AWQ/EXL2 有各自 block/group、metadata、mixed tensor、alignment 与 packing 规则。
