# Result — Experiment 43

## Model identity

- Repository/source:
- Revision:
- Config SHA/source:
- model_type:
- architecture class:

## Core dimensions

- vocab_size:
- hidden_size:
- intermediate_size:
- layers:
- Q heads:
- KV heads:
- head_dim:
- max position/context metadata:

## Block features

- norm:
- activation / gated MLP:
- RoPE:
- rope scaling:
- sliding/local attention:
- tied embedding/head:
- MoE/expert fields:

## Derived attention shape

For a prompt T:

```
X:
Q:
K:
V:
conceptual score:
```

For one-token decode at cache length S:

```
Q:
K/V new:
K/V cache:
conceptual score:
```

## KV baseline

- KV bits:
- sequences:
- bytes/token:
- chosen context:
- total baseline:
- architecture caveats:

## Local inference consequences

### Capacity

### PP

### TG

### Kernel/backend requirements

## What total parameter count failed to tell me

List at least three structural facts that mattered.
