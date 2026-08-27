# Research Note 0003 — PSU / Power Delivery / Platform Integration

日期：2026-08-27

## Research question

For a Local-LLM GPU or multi-GPU system, why is:

```text
PSU wattage >= GPU TGP
```

not a sufficient power-delivery design?

A safe engineering view separates:

```text
continuous system budget
+
headroom / excursions
+
connector and cable path
+
platform slot power
+
physical/thermal condition
```

The default course workflow is non-invasive. It does not open a PSU chassis, probe mains/high-voltage circuits, intentionally overload cables/connectors, or modify PSU protection circuitry.

---

# Part I — PSU nameplate wattage is capacity, not measured draw

A PSU labelled:

```text
850 W
```

means a rated output capability under its specified conditions.

It does not mean:
- the PC always draws 850 W;
- the GPU may consume the entire 850 W;
- every cable/connector can individually carry any fraction of 850 W;
- transient behavior is automatically solved.

Actual wall power is a workload-dependent measurement.

---

# Part II — GPU board power is not whole-system power

Reuse Slice 42:

```text
GPU board power
!=
whole-system wall power
```

Whole-system load also includes:
- CPU/platform;
- RAM;
- storage;
- fans/pumps;
- USB/peripherals;
- other GPUs;
- PSU conversion loss at the wall boundary.

For a simple planning estimate:

```text
estimated DC load
≈
Σ GPU board load
+ CPU/platform load
+ storage/fans/peripherals
```

This is planning arithmetic, not a substitute for measurement.

---

# Part III — Continuous estimate vs headroom

Suppose a synthetic system estimates:

```text
GPU 300 W
CPU/platform 180 W
other 70 W
=
550 W
```

on an:

```text
850 W PSU
```

Arithmetic headroom:

```text
850 - 550 = 300 W
```

headroom fraction relative to PSU capacity:

```text
300 / 850
≈ 35.3%
```

This does not prove transient compatibility.

It only describes the chosen continuous estimate against rated capacity.

---

# Part IV — No universal headroom percentage

The course does not teach:

> always buy exactly 20% more PSU.

Appropriate headroom depends on:
- PSU design/specification;
- GPU/CPU excursion behavior;
- number of GPUs;
- workload;
- ambient/cooling;
- aging;
- future upgrades;
- vendor recommendations.

Experiment 88 therefore makes the minimum headroom fraction an explicit **policy input**, not a universal constant.

---

# Part V — Power excursions / transients

Modern add-in cards can change load faster than a long averaging window suggests.

Current public Intel ATX design guidance includes dedicated sections for:
- PCIe add-in-card power excursions;
- add-in-card and PSU power budgets;
- PSU power excursion behavior.

Official:
https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/

The stable lesson is:

```text
average board power
!= guaranteed worst short-duration demand
```

Do not invent transient limits for a specific PSU/GPU without exact documentation.

---

# Part VI — Total watts and connector path are different gates

A system can pass total-watt arithmetic but fail connector/cable compatibility.

Example:

```text
1000 W PSU
estimated system load 600 W
```

looks comfortable.

But if the installed modular cable is incompatible with that exact PSU model:

```text
REJECT / STOP
```

regardless of unused wattage capacity.

This is why Experiment 88 has separate:
- capacity gate;
- connector/cable gate.

---

# Part VII — Modular PSU cables are not universally interchangeable

Official Seasonic guidance warns that modular DC cables are often incompatible across brands and can differ even within a brand/series; it recommends using compatible/original cables.

Official:
https://knowledge.seasonic.com/article/68-cable-compatibility

Corsair similarly documents that PSU-side modular pinouts are not universal and requires exact cable-family compatibility.

Official:
https://www.corsair.com/eu/en/explorer/diy-builder/power-supply-units/are-psu-cables-universal/

Therefore:

```text
connector physically fits
!= electrically compatible
```

Never infer pinout compatibility from shape alone.

---

# Part VIII — PCIe slot and auxiliary power are separate paths

A GPU add-in card can receive power through:
- the motherboard PCIe slot;
- one or more auxiliary GPU power connectors.

Exact allowed power/current depends on the applicable card/connector/platform specifications.

Do not design by assuming:

```text
all GPU power comes through auxiliary cables
```

or:

```text
slot can safely make up any cable shortfall
```

Use exact GPU and platform documentation.

---

# Part IX — 12V-2x6 is a specification, not a magic power number

PCI-SIG's published 2023 ECN states that the 12V-2x6 connector, defined in CEM 5.1, replaces 12VHPWR and updates connector encoding/measurement consistency.

Official:
https://pcisig.com/PCI%20Express/ECN/Base/12V-2x6ConnectorUpdatestoPCIeBase_6.0

Intel's public ATX guidance also treats the 12V-2x6 auxiliary connector and sideband signals as a distinct design topic.

Do not reduce this to:

> 16-pin connector = always X watts.

Actual allowed/requested card power depends on the card, PSU, cable and signaling/implementation.

---

# Part X — Connector seating and mechanical condition

A high-current connector path must also be physically sound.

Inspect while powered off/unplugged, without opening the PSU:
- connector fully seated per manufacturer guidance;
- no visible gap where the connector is expected to latch fully;
- no melted/discolored housing;
- no burnt smell/residue;
- no crushed/damaged terminals visible externally;
- cable is not under severe strain near the connector;
- cable/adaptor is the exact approved part for the PSU/GPU combination.

If there is heat damage/arcing evidence:

```text
STOP USE
```

and consult the manufacturer or a qualified repair professional.

---

# Part XI — Daisy-chain / pigtail cables

Do not teach a universal:

> one pigtail is always fine

or:

> pigtails are always forbidden.

Cable construction, PSU ports, connector requirements and GPU guidance differ.

Use the exact PSU/GPU manufacturer cabling instructions.

For a multi-GPU build, record a cable map:

```text
PSU port
→ physical cable
→ connector branch
→ GPU connector
```

so the design is auditable.

---

# Part XII — Multi-GPU aggregate budget

For two GPUs:

```text
GPU0 300 W
GPU1 300 W
platform 220 W
=
820 W estimated DC load
```

An 850 W PSU leaves only:

```text
30 W
≈ 3.5%
```

of nameplate arithmetic headroom.

That does not automatically mean the machine will fail, but under a policy requiring more margin it should be REVIEW rather than silently accepted.

Multi-GPU also creates:
- more auxiliary connectors/cables;
- more chassis heat;
- more fan/pump load;
- possible different simultaneous transient behavior.

---

# Part XIII — PSU rails / protections

PSUs may implement protections and rail/current-limit arrangements differently.

Do not assume:

```text
same total wattage
=
same behavior on every connector/rail
```

Exact PSU manual/specification is authoritative for:
- connector mapping;
- rail/current limits where applicable;
- supported modular cable type;
- protection behavior.

The default course does not bypass or modify OCP/OVP/OTP/SCP protections.

---

# Part XIV — Efficiency rating is not capacity quality proof

An efficiency certification primarily concerns conversion efficiency under defined conditions.

Do not infer from an efficiency badge alone:
- transient performance;
- cable quality;
- age/health;
- connector availability;
- suitability for your exact GPU topology.

PSU model/revision evidence matters.

---

# Part XV — Age and secondhand PSU risk

A secondhand PSU adds uncertainty:
- unknown thermal history;
- fan wear;
- missing/replaced modular cables;
- undocumented repairs;
- connector wear;
- model revision ambiguity.

For a used PSU, exact model/serial/revision and cable set are more important than a generic:

```text
"850W Gold"
```

label.

Do not open the PSU to inspect internal capacitors as part of this course.

---

# Part XVI — Wall measurement

A consumer wall power meter can provide whole-system AC input energy/power if used according to its own safety instructions.

This is a stronger electricity/TCO boundary than GPU board power alone.

But:
- wall measurements include PSU losses;
- meter update rate may miss fast transients;
- do not probe bare mains conductors;
- do not build improvised mains measurement fixtures.

The default real lab accepts wall power as optional evidence only.

---

# Part XVII — Real acceptance workflow

1. Identify exact PSU model/revision from external label/documentation.
2. Record rated capacity and manufacturer cabling documentation.
3. Inventory every GPU auxiliary connector requirement.
4. Map actual PSU modular ports/cables to each GPU.
5. Verify each modular cable is approved for that exact PSU model/family.
6. Inspect visible connectors powered off/unplugged.
7. Record ordinary sustained GPU board-power telemetry.
8. Optionally record whole-system wall power with a proper consumer meter.
9. Compare against the predeclared capacity/headroom policy.
10. Record unknown transient behavior as UNKNOWN unless documented/measured appropriately.

---

# Part XVIII — Decision model

## REJECT / STOP
Examples:
- estimated continuous load exceeds rated PSU capacity;
- required GPU connector path is unavailable;
- modular cable compatibility is known false;
- visible connector heat/arcing damage;
- PSU/GPU manufacturer explicitly disallows the configuration.

## REVIEW
Examples:
- very low arithmetic headroom relative to your chosen policy;
- exact PSU model/revision unknown;
- cable compatibility not proven;
- multi-GPU transient behavior unknown;
- wall/board measurements incomplete.

## ACCEPT
The defined policy gates pass, cable/connector compatibility is confirmed, and the ordinary sustained workload shows no material power/thermal instability in the test window.

This is an engineering status, not a lifetime guarantee.

---

# Claims to avoid

- “850W PSU means the PC draws 850W”;
- “total wattage is all that matters”;
- “modular PSU cables with the same plug are interchangeable”;
- “the PCIe slot can make up missing auxiliary power”;
- “12V-2x6 means one universal safe wattage for every setup”;
- “80 Plus/efficiency badge proves transient quality”;
- “one wall-meter value captures GPU transients”;
- “open the PSU to inspect it before buying a new one”;
- “bypass protections if the PSU trips under load”.
