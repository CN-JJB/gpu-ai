# Learning / Build Record — 2026-08-27 Storage / Model Loading

## Slice

43 — Storage, page cache, mmap/page faults, model startup and steady-inference separation.

## Production output

Research:
- `research/llm/0025-storage-model-loading-page-cache.md`

Dynamic intelligence:
- `intelligence/llm/llama-load-mode-2026-08-27.md`

Reference:
- `reference/llm/storage-model-loading.md`

Lesson:
- `lessons/43-storage-loading/01-page-cache-mmap-startup.html`

Labs:
- `labs/experiments/80-storage-model-load-model/`
- `labs/experiments/81-real-storage-model-startup/`

Evidence:
- `examples/evidence/experiment-43-storage-model-loading.md`

## Verified L0

```
20 GiB model

0.2 GiB/s source
→ 102.666667 s simple ready

0.5 GiB/s
→ 42.666667 s

3 GiB/s
→ 9.333333 s

20 GiB/s page-cache-like
→ 3.666667 s

steady TG in all cases
= 50 tok/s
```

Synthetic only.

## Real-lab rule

Never auto-label first run as cold.

Use:
```
initial-state-unknown
after-same-file-read
```

unless stronger cache evidence exists.

## Stable skill

Learner can separate:
```
storage/file behavior
startup readiness
first inference
steady PP/TG
```

and understands that reading/hashing the model changes cache state.

## Next

Memory pressure / swap / OOM:
- RAM vs page cache vs anonymous memory;
- swap/compression;
- model mmap reclaim;
- GPU VRAM OOM vs host RAM OOM;
- why "free RAM" is not the same as available memory;
- safe read-only pressure diagnosis.
