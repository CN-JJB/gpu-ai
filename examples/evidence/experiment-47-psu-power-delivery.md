# Evidence — Experiment 47: PSU / Power Delivery / Platform Integration

状态：stable PSU/power-delivery lesson complete; L0 capacity-vs-cable cases verified; real non-invasive dossier ready.

## Claim

> PSU total wattage is a necessary but insufficient condition for a Local-LLM GPU system. Capacity/headroom and connector/cable compatibility are independent gates.

## Dynamic official evidence

### PCI-SIG 12V-2x6

PCI-SIG's published 2023 ECN states that 12V-2x6, defined in CEM 5.1, replaces 12VHPWR and updates connector encoding/measurement consistency.

Official:
https://pcisig.com/PCI%20Express/ECN/Base/12V-2x6ConnectorUpdatestoPCIeBase_6.0

### Intel public ATX guidance

Current public Intel ATX design guidance includes dedicated topics for:
- PCIe add-in-card power excursions;
- add-in-card and PSU power budgets;
- PSU power excursions;
- auxiliary GPU power connectors;
- 12V-2x6 sideband signals;
- PSU protections.

Official:
https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/

### Modular cable compatibility

Official Seasonic and Corsair guidance both warn that PSU-side modular pinouts/cables are not universally interchangeable and exact compatibility must be checked.

Official:
- https://knowledge.seasonic.com/article/68-cable-compatibility
- https://www.corsair.com/eu/en/explorer/diy-builder/power-supply-units/are-psu-cables-universal/
- https://www.corsair.com/ww/en/s/psu-cable-compatibility

Central rule:

```text
plug fits
!= electrically compatible
```

## Experiment 88 verification

### Single-GPU synthetic case

```text
PSU capacity = 850 W
estimated continuous load = 550 W
headroom = 300 W
headroom fraction = 35.294%
compatible GPU power paths confirmed
```

Verified:

```text
DECISION: ACCEPT
```

### Multi-GPU tight-headroom case

```text
PSU capacity = 850 W
estimated continuous load = 820 W
headroom = 30 W
headroom fraction = 3.529%
scenario policy minimum = 15%
```

Verified:

```text
DECISION: REVIEW
```

The 15% value is a synthetic case policy, not a universal PSU recommendation.

### Cable mismatch

```text
PSU capacity = 1000 W
estimated load = 600 W
headroom = 400 W / 40%
modular cable compatibility = false
```

Verified:

```text
DECISION: REJECT
```

This proves the course does not reduce power delivery to one wattage comparison.

## Real dossier hardening

Experiment 89 empty/default template was checked and returns:

```text
DOSSIER: BLOCKED_MISSING_EVIDENCE
```

when exact PSU identity, rated capacity, system load and cable-compatibility source are missing.

It does not compute a fake verdict from default zeros.

## Measurement boundaries

Reuse Slice 42:

```text
GPU board power
!= whole-system wall power
```

Wall power includes platform load and PSU conversion losses.

A slow consumer wall meter may also miss short excursions.

## Transient boundary

```text
average board power
!= transient/excursion compatibility proof
```

Exact PSU/GPU documentation wins over generic course heuristics.

## Connector/path boundary

GPU supply can include:
- motherboard PCIe slot path;
- auxiliary GPU connector path(s).

Do not assume the slot can compensate for missing auxiliary power.

For multi-GPU, record an auditable map:

```text
PSU port
→ cable part/type
→ branch
→ GPU connector
```

## Safety boundary

Experiment 89 does not:
- open the PSU chassis;
- expose/probe mains wiring;
- bypass OCP/OVP/OTP/SCP;
- intentionally overload a PSU/cable;
- modify power limits;
- create improvised high-voltage measurement fixtures.

Visible melting/charring/arcing evidence is a STOP USE / REJECT condition.

## Learner should reject

- PSU wattage label is the whole design;
- modular cables are interchangeable because plugs fit;
- one universal headroom percentage exists;
- the PCIe slot safely makes up missing aux power;
- 12V-2x6 means one universal safe wattage independent of exact card/cable/PSU;
- efficiency certification proves transient/cable suitability;
- opening a PSU is a routine beginner inspection step.
