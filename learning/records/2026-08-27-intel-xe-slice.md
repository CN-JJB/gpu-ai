# Learning / Build Record — 2026-08-27 Intel Xe Slice

## Slice

17 — Intel lighter coverage: EU → Xe-Core/XMX → Arc Alchemist/Battlemage → oneAPI/SYCL/Level Zero.

## Production output

Research:
- `research/gpu/0011-intel-xe-arc-xmx-oneapi.md`

Reference:
- `reference/gpu/intel-xe-arc-xmx.md`

Lessons:
- `lessons/17-intel-xe/01-eu-xe-core-xmx.html`
- `lessons/17-intel-xe/02-arc-oneapi-llm.html`

Experiments:
- `labs/experiments/29-intel-xe-terminology-traps/`
- `labs/experiments/30-real-intel-xpu-sycl-inventory/`

Evidence/intelligence:
- `examples/evidence/experiment-17-intel-xe.md`
- `intelligence/gpu/intel-oneapi-xpu-2026-08-27.md`

## Stable model

```
EU-era Intel graphics
→ Xe-LP
→ Xe-HPG / Alchemist
→ Xe2 / Battlemage
```

Modern terms:
- Vector Engine；
- Xe-Core；
- XMX；
- SLM；
- subgroup。

Software:
```
framework
→ SYCL / torch.xpu / oneAPI libraries
→ Level Zero
→ driver
→ Xe hardware
```

## L0 result

Terminology checker:
```
10/10
```

## Key local-LLM lesson

```
XMX hardware
!=
quant storage
!=
backend kernel
!=
achieved LLM speed
```

Real device Evidence must prove each layer.

## Current software/product finding

As of 2026-08-27:
- oneAPI 2026.1；
- current PyTorch XPU validates Arc A/B；
- current llama.cpp SYCL is Intel-first；
- current Arc B consumer cards provide 10–12 GB；
- current Arc Pro B70/B65 provide 32 GB workstation options.

## Next slice

Converge all vendor architecture sections into one practical decision system:

```
model/workload
→ capacity
→ bandwidth
→ compute datatype
→ backend/kernel
→ interconnect
→ power/cooling
→ used-market risk
→ TCO
→ Evidence-based buy / keep / skip
```

This becomes the bridge from architecture study to garbage-hardware purchasing and deployment.
