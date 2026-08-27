# Expected — Experiment 26

没有统一硬件答案。

正确的方法输出至少包含：

```
exact GPU
+ gfx target
+ ROCm/HIP version
+ current official support check
```

## Example mappings

- gfx908 → CDNA / MI100
- gfx90a → CDNA2 / MI200
- gfx942 → CDNA3 / MI300
- gfx950 → CDNA4 / MI350
- gfx1030 → RDNA2
- gfx1100 → RDNA3
- gfx1151 → RDNA3.5
- gfx1201 → RDNA4

## If rocminfo shows architecture but libraries fail

This is possible.

Interpretation:

```
HIP runtime can enumerate hardware
!=
every prebuilt ROCm library supports the exact GPU
```

## If AMD SMI works but rocminfo does not

Driver/system-management visibility is not the same as working ROCm compute stack.

## If exact card is not on official matrix

Record:

```
unsupported / community-enabled / TheRock path
```

rather than silently calling it “supported”.

## No performance expectations

Do not prefill tokens/s from another Radeon with the same architecture.
