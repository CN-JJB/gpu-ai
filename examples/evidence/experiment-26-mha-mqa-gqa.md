# Evidence — Experiment 26: MHA / MQA / GQA and KV Cost

状态：stable attention-head lesson complete; L0 KV/projection arithmetic verified; real config-comparison path ready.

## Claim

> KV cache scales with the number of key/value heads, not directly with the number of query heads. MQA/GQA are trained architecture choices that can reduce KV storage and decode memory traffic.

## Primary evidence

### MQA
https://arxiv.org/abs/1911.02150

The paper motivates shared K/V heads specifically to reduce incremental-decoding KV memory-bandwidth cost.

### GQA
https://arxiv.org/abs/2305.13245

GQA uses an intermediate number of KV heads:
```
1 < Hkv < Hq
```
to balance quality and inference efficiency.

### Llama 2
https://arxiv.org/abs/2307.09288

Llama 2 documents GQA as an inference-scalability choice in relevant larger variants.

## Stable formulas

```
q_width = Hq × Dh
kv_width = Hkv × Dh
```

```
KV bytes/token
=
2 × layers × Hkv × Dh × bytes/element
```

Common evenly grouped GQA:

```
group size = Hq / Hkv
```

when divisible.

## Experiment 46 verification

Default:

```
L=32
d=4096
Hq=32
Dh=128
KV=FP16
context=32768
```

Verified:

| type | Hkv | group | KV/token | KV total | attention Q/K/V/O weights/layer |
|---|---:|---:|---:|---:|---:|
| MHA | 32 | 1 | 512 KiB | 16 GiB | 67,108,864 |
| GQA-8 | 8 | 4 | 128 KiB | 4 GiB | 41,943,040 |
| MQA | 1 | 32 | 16 KiB | 0.5 GiB | 34,603,008 |

All values are synthetic formula outputs.

## Why the full model does not shrink 32×

In MQA:
- K/V projections become narrow;
- Q and O remain large;
- the MLP remains unchanged.

Therefore:
```
32× smaller KV-head count
!=
32× smaller model
```

## Decode consequence

Historical K/V traffic is proportional to:
```
Hkv × Dh × sequence length
```

so lower Hkv can directly reduce:
- long-context KV capacity;
- concurrency KV pressure;
- K/V reads in incremental decoding.

## Experiment 47

The real config comparison tool accepts multiple model `config.json` files and normalizes:
- context;
- KV precision;
- sequence count.

It reports:
- layers;
- Hq;
- Hkv;
- group size;
- head_dim;
- KV GiB;
- architecture caveats.

It does not compare quality.

## Architecture vs runtime

```
GQA/MQA
=
trained architecture

KV quant
=
runtime representation
```

They can combine but are not the same mechanism.

## Learner should reject

- Hq determines KV cost;
- MQA means one query head;
- MQA/GQA are llama.cpp flags;
- backend must physically duplicate GQA KV to every Q head;
- 4× smaller KV implies 4× faster TG;
- same parameter count implies same context memory;
- GQA and KV quant are interchangeable.
