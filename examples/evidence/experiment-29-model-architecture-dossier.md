# Evidence — Experiment 29: Model Architecture Dossier

状态：integration slice complete; synthetic dense/MoE capacity cases checked; real dossier path ready.

## Claim

> A model architecture dossier can turn config facts into transparent memory/structure estimates and benchmark hypotheses, but it must not upgrade those estimates into confirmed runtime fit or performance.

## Integrated inputs

From Slices 24–28:
- decoder dimensions;
- Hq/Hkv/Dh;
- KV formula;
- dense FFN;
- MoE routed/shared experts;
- context architecture caveats.

## Weight planning

Preferred:
```
exact artifact bytes + SHA256
```

Fallback:
```
parameter count × effective bpw / 8
```

The fallback is explicitly a proxy.

## Capacity rule

```
lower bound
=
weight/artifact planning value
+ homogeneous KV baseline
+ explicit reserve
```

Asymmetric verdict:

```
lower bound > memory
→ FAIL-WITHOUT-OFFLOAD

lower bound <= memory
→ POSSIBLE-NOT-PROVEN
```

The second case is never called PASS because runtime buffers/workspace/layout are not modeled.

## Experiment 52 verification

### Synthetic dense GQA

```
8B
4.5 bpw
32 layers
Hq=32
Hkv=8
Dh=128
32k context
FP16 KV
1 GiB reserve
12 GiB memory input
```

Derived:
- weight proxy ≈ 4.191 GiB;
- KV = 4 GiB;
- lower bound ≈ 9.191 GiB;
- verdict = `POSSIBLE-NOT-PROVEN`.

### Synthetic MoE

```
47B
4.5 bpw
same 4 GiB KV baseline
1 GiB reserve
24 GiB memory input
```

Weight proxy alone:

```
≈ 24.622 GiB
```

Therefore the full lower bound exceeds 24 GiB and verdict must be:

```
FAIL-WITHOUT-OFFLOAD
```

## Experiment 53

The real dossier supports:
- actual model artifact bytes/SHA256;
- config anatomy;
- KV/context/sequences;
- dense attention/FFN baselines;
- MoE fields/caveats;
- hardware memory input.

It outputs only hypotheses for PP/TG.

## Evidence separation

### Known
Config/artifact facts.

### Derived
Formula outputs.

### Must measure
- actual runtime VRAM;
- backend;
- PP;
- TG;
- power/thermal;
- serving behavior.

## Learner should reject

- formula fit = runtime fit;
- params×bpw = exact GGUF;
- config = tokens/s;
- homogeneous KV is exact for every modern architecture;
- MoE active params determine VRAM.
