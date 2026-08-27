# Expected — Experiment 52

## Dense synthetic config

Expected head relation:

```
GQA-like (4 Q/KV)
```

KV:

```
32 layers × 8 KV heads × Dh128 × FP16 × 32k
= 4 GiB
```

8B at 4.5 bpw weight proxy:

```
≈ 4.191 GiB
```

With 1 GiB reserve:

```
lower bound ≈ 9.191 GiB
```

On 12 GiB input:

```
POSSIBLE-NOT-PROVEN
```

not PASS.

## MoE synthetic config

The dossier must expose:
- 8 routed experts;
- top-2;
- common expert baseline;
- 4 GiB homogeneous KV baseline.

47B at 4.5 bpw alone is already around 24.622 GiB decimal-parameter proxy before KV/reserve, so with a 24 GiB memory input the verdict must be:

```
FAIL-WITHOUT-OFFLOAD
```

Exact displayed GiB depends on decimal parameter count converted to binary GiB.
