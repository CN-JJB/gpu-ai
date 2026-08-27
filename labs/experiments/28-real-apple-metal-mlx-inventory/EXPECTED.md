# Expected — Experiment 28

没有统一 Mac 数值。

正确实验必须得到机器自己的 Evidence。

## Expected Apple-Silicon pattern

```
device.hasUnifiedMemory = true
```

`recommendedMaxWorkingSetSize` should be a real runtime value, not simply copied from installed RAM.

`threadExecutionWidth` is queried from the compiled pipeline.

Do not replace it with:

```
32
```

just because another Apple GPU reports 32.

## MLX

If installed, current MLX should expose CPU/GPU device information.

Do not interpret:
```
mx.gpu
```
as Neural Engine.

## llama.cpp

If installed, Metal should appear as a device/backend on a compatible Apple-Silicon build.

Performance numbers are intentionally blank.

## Valid failure modes

- Xcode Command Line Tools not installed;
- Metal source compile unavailable;
- MLX not installed;
- llama-bench not installed;
- M5 tensor path disabled/under active upstream change.

All are valid Evidence if recorded precisely.

## Important comparison boundary

```
installed unified memory
!= recommendedMaxWorkingSetSize
!= currentAllocatedSize
!= model file size
!= runtime footprint
```

Keep all five separate.
