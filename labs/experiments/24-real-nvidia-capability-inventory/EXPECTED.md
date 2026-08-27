# Expected — Experiment 24

本实验没有统一 GPU 型号。

正确输出结构：

```
exact name
+ compute capability
+ architecture mapping
+ driver
+ raw nvidia-smi
```

## Current mapping examples

- 7.5 → Turing
- 8.0 → Ampere
- 8.6 → Ampere
- 8.9 → Ada
- 9.0 → Hopper
- 10.x / 12.x → current Blackwell mapping

Older:
- 7.0 Volta
- 6.x Pascal
- 5.x Maxwell
- 3.x Kepler
- 2.x Fermi

## Important

Compute capability identifies a CUDA architecture target, but it still does not tell you:
- exact VRAM；
- memory bandwidth；
- exact Tensor throughput；
- NVLink；
- product power limit；
- backend kernel quality。

So the correct final answer is never just：

```
"8.6 = Ampere, done"
```

It should become a launch point for exact SKU Evidence.