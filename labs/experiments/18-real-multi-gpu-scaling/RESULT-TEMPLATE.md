# Result — Experiment 18

## Identity

- Date:
- Host:
- Motherboard/platform:
- OS/kernel:
- Driver:
- GPU0:
- GPU1:
- VRAM:
- llama.cpp commit/build:
- Model:
- Model SHA256:
- Quant:
- Context/test:
- Cooling/power notes:

## Topology

Paste/summarize:

- `nvidia-smi topo -m` or AMD equivalent:
- P2P capability:
- NUMA/root-complex notes:
- negotiated PCIe notes:
- measured GPU↔GPU bandwidth tool:
- uni bandwidth:
- bi bandwidth:

Attach raw `topology.txt`.

## Performance-scaling A/B

| mode | devices | split | PP t/s | TG t/s | PP speedup | TG speedup |
|---|---|---|---:|---:|---:|---:|
| single | | none | | | 1.00 | 1.00 |
| layer | | | | | | |
| row | optional | | | | | |
| tensor | optional | | | | | |

Raw files:
- single.json:
- layer.json:
- row.json:
- tensor.json:

## Capacity-only result

- Model fits one GPU?:
- Model fits two GPUs?:
- Split used:
- Per-device VRAM:
- Was CPU offload involved?:
- This section is/not comparable for speedup because:

## Interpretation

### Capacity
What did the second GPU enable?

### PP
What changed and why might communication be amortized differently?

### TG
What changed in per-token generation?

### Interconnect
Does the result match topology / P2P / measured bandwidth?

### Buying decision
For this exact workload, would you prefer:
- one larger GPU
- two split GPUs
- two replicas
- CPU offload
- no upgrade

Why?

## Integrity

- [ ] No advertised PCIe number was reported as measured P2P.
- [ ] Model/config identical in comparable A/B runs.
- [ ] PP and TG kept separate.
- [ ] Capacity-only success was not misreported as speedup.
- [ ] Raw outputs preserved.
