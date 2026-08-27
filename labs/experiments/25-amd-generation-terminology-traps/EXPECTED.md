# Expected — Experiment 25

直接运行：

```bash
python3 check_lineage.py
```

参考答案应：

```
score: 12/12
```

## 最重要的 false claims

### "RDNA only Wave32"
False.

Correct:
```
Wave32 primary
+ Wave64 supported
```

### "Infinity Cache = extra VRAM"
False.

Cache changes traffic/locality, not model capacity.

### "RDNA → CDNA is one generation line"
False.

They are different product/architecture branches.

### "RDNA3 dual issue = 2×"
False.

VOPD is conditional.

### "RDNA4 FP8/INT4 = Q4 LLM native AI accelerator"
False.

Need:
```
model representation
→ backend
→ kernel
→ instruction datatype
```

### "ROCm support = architecture support"
False.

Need exact:
```
SKU
+ gfx target
+ OS
+ ROCm version
+ component/library
```
