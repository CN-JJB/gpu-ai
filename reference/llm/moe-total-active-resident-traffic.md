# MoE Local-Inference Accounting Card

## Symbols

- d: hidden size
- d_e: expert FFN intermediate size
- N: routed experts
- k: selected routed experts/token
- S: shared experts
- L_moe: MoE layers
- b: effective bits/weight

## One SwiGLU-like expert

```
P_expert
≈
3 d d_e
```

## Total routed expert weights/layer

```
P_total_routed
≈
N × P_expert
```

## Active expert weights/token/layer

```
P_active_expert
≈
(k + S) × P_expert
```

only when shared experts have same size.

## Router

```
W_router [d,N]
```

Router is small relative to experts but controls downstream work.

## Four separate quantities

Never merge:

```
total parameters
active parameters/token
resident weight memory
actual weight bytes moved
```

## Single-token decode

Rough no-reuse expert-byte scale:

```
(k + S)
× expert weight bytes
× MoE layers
```

This is not a measured runtime bandwidth number.

## Prefill / batch

If multiple tokens select same expert:

```
group tokens by expert
→ reuse weight tiles
→ lower bytes/token
```

## Expert-parallel multi-GPU

```
route
→ dispatch token states
→ expert compute
→ return/combine
```

Watch:
- P2P/interconnect
- assignment balance
- slow-device tail

## Local fit

All experts resident on one GPU:

```
VRAM must hold total experts
```

not only top-k active experts.

## Quantization

Reduces:
- total expert storage
- selected expert traffic

but backend/kernel support still matters.
