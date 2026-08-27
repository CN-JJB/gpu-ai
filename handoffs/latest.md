# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Frozen constraints

Core ability stack:
**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Never fabricate benchmark, market, transaction or health data.

## Completed frontier

Slices 01–21 are implemented.

The hardware-acquisition chain is now complete:

```
architecture
→ workload sizing
→ cross-vendor decision
→ China secondhand market methodology
→ transaction/acceptance verification
→ max-buy-price/watchlist
```

## Slice 21

Key files:
- `research/market/0002-max-buy-price-watchlist.md`
- `reference/market/max-buy-price-watchlist-card.md`
- `lessons/21-watchlist/01-max-buy-price.html`
- `labs/experiments/37-max-buy-price-model/`
- `labs/experiments/38-real-candidate-watchlist/`

Core rule:

```
ask <= ceiling
```

is not enough.

BUY-CANDIDATE also requires:
- hard gates pass;
- performance sufficiently known;
- market evidence sufficient;
- condition evidence sufficient.

No auto-purchase.

## Active next slice — capstone deployment/optimization loop

Build a reusable project:

```
hardware profile
→ runtime identity
→ model identity/SHA
→ baseline configuration
→ PP/TG/VRAM/power/thermal Evidence
→ bottleneck diagnosis
→ choose ONE optimization
→ rerun same workload
→ compare
→ explain transfer to other hardware
```

Possible optimization branches:
- quant/backend;
- context/KV;
- FlashAttention;
- server slots/batching;
- prefix cache;
- speculative decoding;
- multi-GPU split.

Do not change multiple independent variables in one A/B test.

## Vendor paths

Use the same capstone structure for:
- NVIDIA CUDA;
- AMD ROCm/HIP;
- Apple Metal/MLX;
- Intel SYCL/XPU.

Do not force identical commands across ecosystems.

## Matt Pocock skills

High-frequency:
- `teach`
- `research`

Use verifiable exercises and explicit provenance.
