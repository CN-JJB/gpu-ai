# Research Note 0014 — Used GPU Transaction / Acceptance Verification

日期：2026-08-27

## Research question

二手 GPU 到底应该怎么“验”？

错误答案通常是：

> 跑一下 FurMark，没花屏就行。

或：

> 卖家说非矿、无修，所以风险低。

本课程把验卡拆成不同证据层：

```
identity
→ capacity
→ memory integrity
→ compute stability
→ thermals / throttling
→ driver/error state
→ workload-relevant benchmark
→ acceptance decision
```

任何一个层面都不能替代其他层面。

---

# Part I — Before payment: request evidence, not adjectives

Seller claims are useful context, not proof.

Ask for:

## Identity

- exact board photos;
- serial/label;
- exact GPU/VRAM screenshot;
- current timestamp or order-specific note in photo/video;
- BIOS/firmware version if card is unusual/modded.

## Current function proof

Ask for one current video showing:
- system boot;
- GPU recognized by OS/driver;
- exact VRAM;
- benchmark/stress start;
- temperatures after sustained load;
- no artifacts or driver reset.

## Modification/history

Ask directly:

```
是否维修过？
是否换过显存/核心？
是否刷过非原厂 BIOS？
是否改过显存容量？
是否服务器/矿场/工作室退役？
散热器/风扇/导热垫是否更换？
```

The goal is not to punish history.

The goal is to price the risk correctly.

---

# Part II — Evidence packet before payment

Save:

- listing page;
- seller description;
- seller chat commitments;
- serial/board photos;
- test video;
- price;
- shipping/inspection agreement;
- return/dispute terms.

Why save before payment?

Listings and chat context can change/disappear.

A dispute needs:
```
what was promised
vs
what arrived
```

---

# Part III — Arrival: preserve chain of evidence

Before installing:

1. record unopened parcel;
2. record shipping label;
3. record continuous unboxing if practical;
4. record serial label and board condition;
5. photograph connector/PCB/cooler exterior;
6. compare with seller evidence.

Do not disassemble before completing basic acceptance unless the transaction explicitly permits it.

Disassembly can:
- create new damage;
- complicate return disputes;
- destroy evidence about original condition.

---

# Part IV — Visual inspection without repair work

Look for:

- bent/bruised PCB;
- corrosion;
- missing screws;
- damaged PCIe fingers;
- damaged power connector;
- oil/residue;
- broken fan;
- obvious rework/reball signs visible externally;
- mismatched labels;
- aftermarket cooler on supposedly stock card;
- signs that serial labels were replaced.

This is screening, not electrical diagnosis.

If a connector/PCB looks unsafe, do not power the card simply to “see if it works”.

---

# Part V — Identity verification

Before stress:

## NVIDIA

Record:

```
nvidia-smi -L
nvidia-smi -q
nvidia-smi --query-gpu=name,uuid,serial,memory.total,vbios_version,pci.bus_id,driver_version --format=csv
```

Not every product exposes every field.

## AMD

Record current:

```
amd-smi version
amd-smi list
amd-smi static
rocminfo
```

## Intel

Record:

```
sycl-ls
clinfo -l
torch.xpu probe
llama-bench --list-devices
```

## Cross-vendor

```
lspci -nn
```

Identity failure examples:
- wrong GPU;
- wrong VRAM;
- unexpected device ID;
- missing GPU;
- BIOS mismatch on a supposedly stock card.

---

# Part VI — Baseline error state

Before load, record current error/health counters.

## NVIDIA

Useful fields can include:
- ECC state/counts on supported products;
- XID/error logs via system journal;
- retired pages / row remap on supported GPUs;
- PCIe link state;
- temperature/clocks.

## AMD

AMD SMI/RAS can expose ECC/RAS state and error counts on supported products.

## Datacenter card rule

For P40/P100/V100/A-series/Instinct-class used cards:

```
error counters
+ cooling compatibility
+ power compatibility
```

are first-class acceptance items.

A datacenter card can be computationally healthy while being impractical in a desktop chassis.

---

# Part VII — Memory integrity is its own test

A graphics benchmark cannot prove the whole framebuffer is healthy.

Options:

## NVIDIA DCGM on supported hardware

Current DCGM Diagnostics includes a `memory` plugin that:
- allocates a large portion of framebuffer;
- writes known patterns;
- reads them back;
- detects mismatches and ECC errors.

Current documentation also provides deeper `memtest` diagnostics on supported products.

Important:
- higher DCGM diagnostic levels are product/support dependent;
- on non-datacenter GPUs only documented supported levels should be used.

Do not assume every GeForce supports every DCGM plugin.

## Cross-vendor memtest_vulkan

Open-source `memtest_vulkan` provides a Vulkan compute memory test.

Current project guidance suggests a standard test period around five minutes and reports detected errors.

Use it as:
```
additional evidence
```

not:
```
official vendor certification
```

Known limitations include:
- some drivers limit tested allocation size;
- some integrated/AMD configurations can behave differently;
- Vulkan-driver path itself can affect the result.

## Acceptance signal

Any reproducible memory error is a serious failure signal for a normal working-card sale.

---

# Part VIII — Compute / workload stability

After identity and memory checks:

Run the workload you actually care about.

For this course:

```
llama-bench
```

is valuable because it can exercise:
- model loading;
- large memory allocation;
- matrix compute;
- prompt processing;
- generation;
- backend-specific kernels.

Use:
- exact model;
- repeat count;
- raw JSON;
- same config.

Then repeat enough times to reveal:
- driver resets;
- hangs;
- thermal throttling;
- unstable clocks.

Do not needlessly run hours of maximum power before the basic evidence is complete.

---

# Part IX — Thermals are not one temperature

Record what the vendor exposes:

- GPU/core temperature;
- hotspot;
- memory junction;
- fan speed;
- clocks;
- power;
- throttling/performance-state reasons.

A card can:
- avoid crashing;
- but throttle badly;
- or have excessive memory temperature.

That changes TCO and long-term confidence.

## Do not use one universal temperature limit

Different products expose different sensors and have different vendor limits.

Use:
- current vendor limits;
- exact product behavior;
- comparison with known-good examples.

The acceptance question is:

```
does it sustain expected workload
without abnormal thermal/power behavior?
```

---

# Part X — Driver and system errors

Watch for:

## NVIDIA
- XID errors;
- GPU fallen off bus;
- ECC uncorrectable errors;
- driver resets.

## AMD
- amdgpu reset/RAS errors;
- ECC/CPER on supported products.

## Intel
- device lost;
- Level Zero/XPU errors;
- driver resets.

A benchmark score without error-log review can miss intermittent faults.

---

# Part XI — Test order matters

Recommended order:

```
1 visual
2 identity
3 baseline errors
4 short memory test
5 short workload test
6 sustained workload
7 optional deeper diagnostics
8 final log review
```

Why?

If the card fails identity or basic memory integrity, there is no reason to keep stressing it.

---

# Part XII — Stop conditions

Abort the test if you observe:
- smoke/smell/arcing;
- obviously unsafe connector heating;
- repeated driver reset;
- artifacting;
- memory test errors;
- uncorrectable ECC;
- thermal shutdown;
- fan failure with rising temperature;
- card disappearing from PCIe;
- power-system instability.

The goal is acceptance testing, not destructive proof.

---

# Part XIII — Retail vs datacenter vs modified cards

## Retail gaming/workstation

Main concerns:
- VRAM;
- fans/thermals;
- board repair;
- driver stability;
- outputs;
- benchmark.

## Datacenter passive/no-display

Add:
- airflow solution already validated;
- correct power cable/interface;
- ECC/RAS;
- host compatibility;
- no-display workflow;
- server firmware/compute mode if relevant.

Do not improvise unsafe power adapters.

## VRAM-modified/repaired

Require stronger evidence:
- exact modified capacity;
- full-memory test;
- workload allocation near full VRAM;
- BIOS/driver compatibility;
- modder/seller provenance;
- larger risk discount.

---

# Part XIV — Acceptance decision

## ACCEPT

Use when:
- identity matches;
- capacity matches;
- no memory errors;
- no critical driver errors;
- workload stable;
- thermals reasonable;
- condition matches seller commitments.

## ACCEPT WITH DISCLOSED DEFECT

Only when:
- defect was known before payment;
- price reflected it;
- the defect does not violate the target workload.

## DISPUTE / RETURN

Strong triggers:
- identity mismatch;
- VRAM mismatch;
- undisclosed repair/modification;
- reproducible memory errors;
- repeated driver resets;
- severe thermal/fan defect;
- seller claims contradicted by evidence.

Preserve:
```
raw logs
+ photos
+ videos
+ exact timestamps
```

---

# Stable claims to avoid

- "FurMark pass = GPU healthy."
- "non-mining = healthy."
- "mining = broken."
- "third-party inspection = full memory test."
- "one memory test pass guarantees future reliability."
- "benchmark score alone proves stability."
- "ECC correctable count must always be zero on any old datacenter card."
- "repaired/modded cards are always bad."
- "a cheap broken card should be powered despite visible electrical damage."
