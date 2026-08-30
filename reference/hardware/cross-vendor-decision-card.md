# Cross-Vendor Used-Hardware Decision Card

<figure>
  <img src="../../assets/diagrams/hardware-decision-gates.svg" alt="Cross-Vendor Used-Hardware Decision Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Cross-Vendor Used-Hardware Decision Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## 0. Workload

Fill first:

```
model:
params:
quant:
weight bytes:
context:
KV:
concurrency:
runtime:
goal: interactive / service / learning
```

## 1. Fit gate

### dGPU
```
weights + KV + workspace + headroom
<= usable VRAM
```

### Apple/iGPU
```
runtime footprint
<= safe shared/unified working set
```

### multi-GPU
Need per-device fit + sharding + communication buffers.

Result:
- PASS
- PASS WITH OFFLOAD
- FAIL

## 2. Software gate

Rate:
- official-current
- official-pinned
- community-enabled
- runtime-visible-only
- unsupported

Record exact:
```
OS
driver
runtime
backend
GPU target
build
```

## 3. Expected bottleneck

Choose one or more:

- capacity
- memory bandwidth
- matrix compute
- interconnect
- software/kernel
- power/thermal

## 4. Performance Evidence

Same model/config:

| metric | value |
|---|---:|
| PP t/s | |
| TG t/s | |
| TTFT | |
| runtime memory | |
| power | |
| temperature | |

## 5. TCO

```
purchase
+ platform
+ PSU/cooling
+ expected energy
+ repair reserve
- resale
```

## 6. Risk

- board history
- BIOS
- repair
- VRAM errors
- corrosion
- fan/cooling
- power connectors
- seller testability
- software lifespan

Rate:
- low
- medium
- high

## 7. Evidence

Each important claim:

- E3 official/local raw
- E2 reproducible/reputable
- E1 weak anecdote/seller
- E0 unknown

## 8. Decision

Use:
- BUY
- BUY IF PRICE ≤ X
- KEEP
- SKIP
- NEEDS EVIDENCE

## No universal score

Only rank after:
```
FIT PASS
+
SOFTWARE PASS
```

and only under one explicit workload scenario.
