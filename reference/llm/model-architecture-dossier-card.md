# Model Architecture Dossier Card

<figure>
  <img src="../../assets/diagrams/model-dossier.svg" alt="Model Architecture Dossier Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Model Architecture Dossier Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## Identity

- repository:
- revision:
- config:
- architecture/model_type:
- exact GGUF/artifact:
- artifact bytes:
- SHA256:

## Core dimensions

- vocab:
- layers L:
- hidden d:
- Hq:
- Hkv:
- Dh:
- d_ff:
- context metadata:

## Attention

```
q_width = Hq × Dh
kv_width = Hkv × Dh
```

- MHA / GQA / MQA-like:
- attention projection baseline/layer:

## KV

```
2 × L × Hkv × Dh × bytes × context × sequences
```

- KV precision:
- context:
- sequences:
- homogeneous KV estimate:
- caveats:

## Dense FFN

```
3 × d × d_ff
```

- FFN weights/layer:
- FFN/attention ratio:

## MoE

- routed experts:
- top-k:
- shared:
- expert d_ff:
- expert/layer storage proxy:
- active expert proxy:
- layer-pattern caveat:

## Weight storage

Prefer:
```
actual artifact bytes
```

Otherwise:
```
params × effective bpw / 8
```

## Capacity

```
lower bound
=
weight/artifact
+ KV
+ explicit reserve
```

Verdict:
- FAIL-WITHOUT-OFFLOAD
- POSSIBLE-NOT-PROVEN
- UNKNOWN

## PP hypothesis

## TG hypothesis

## Must measure

- runtime VRAM
- backend/device
- PP
- TG
- thermal/power
- serving behavior if relevant
