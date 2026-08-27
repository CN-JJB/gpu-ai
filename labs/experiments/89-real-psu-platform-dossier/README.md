# Experiment 89 — Real PSU / Power-Delivery Dossier

硬件等级：L2/L3（整机外部检查；可选消费级插座功率计）。

## Safety boundary

This lab does **not**:
- open a PSU enclosure;
- expose/probe mains wiring;
- bypass OCP/OVP/OTP/SCP;
- intentionally overload the PSU or connector;
- modify GPU/PSU power limits;
- create improvised high-voltage measurement fixtures.

If a connector/cable shows melting, charring, arcing evidence or severe damage:

```text
STOP USE
```

and follow manufacturer/qualified repair guidance.

## 1. Power off before physical cable inventory

Shut the system down and disconnect AC power before externally inspecting GPU power connections.

Do not open the PSU chassis.

## 2. Record exact PSU identity

Fill:

```text
PSU-LABEL-TEMPLATE.md
```

Record from the external label/manual:
- exact brand/model;
- rated output;
- revision if identifiable;
- manufacturer manual;
- modular cable compatibility documentation.

Do not settle for:

```text
"850W Gold"
```

as an identity.

## 3. Build cable map

Copy/fill:

```text
CABLE-MAP.csv
```

For every GPU auxiliary connection record:

```text
PSU port
→ cable part/type
→ branch/pigtail
→ GPU connector
→ compatibility source
```

If modular cable compatibility is unknown:

```text
REVIEW
```

Do not infer compatibility from connector shape.

## 4. Record GPU requirements

Use exact GPU/OEM manual or vendor documentation.

Record:
- auxiliary connector type/count;
- PSU recommendation if supplied;
- any exact cabling/adaptor instruction.

Do not invent a generic connector wattage and substitute it for the manual.

## 5. Record ordinary workload power

Reuse:
- Experiment 79 — NVIDIA board-energy integration;
- Experiment 85 — sustained TG/thermal telemetry;
- equivalent vendor telemetry where supported.

For multi-GPU:
- include only participating GPUs;
- record aggregate board power;
- add platform estimate separately.

## 6. Optional wall measurement

A consumer plug-in wall power meter can be recorded if used normally according to its own instructions.

Do not open wiring or expose mains conductors.

Wall power and PSU DC rating are different boundaries.

A slow consumer meter may not capture short transients.

## 7. Fill planning dossier

Copy:

```text
dossier.template.json
```

to your evidence directory.

Then run:

```bash
python3 check_dossier.py dossier.json
```

The checker can detect:
- arithmetic load > capacity;
- policy headroom shortfall;
- missing/false cable compatibility;
- connector-path shortfall;
- visible heat damage;
- unknown PSU identity.

It does **not** certify transient/electrical safety.

## 8. Finish

Fill:

```text
RESULT-TEMPLATE.md
```

A valid result separates:
- arithmetic capacity;
- connector/cable compatibility;
- transient unknowns;
- observed sustained workload behavior.
