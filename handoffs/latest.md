# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–47 are implemented.
Experiments 01–89 exist.

## Slice 47 core — PSU / Power Delivery / Platform Integration

Power-delivery decision is split into independent gates:

```text
continuous capacity/headroom
+
connector/cable compatibility
+
transient/documentation uncertainty
+
ordinary workload evidence
```

Synthetic verified:

```text
850W / 550W / compatible cables
→ ACCEPT

850W / 820W / 15% synthetic scenario policy
→ REVIEW

1000W / 600W / incompatible modular cable
→ REJECT
```

Important rules:

```text
total watts enough
!= power path valid

plug fits
!= modular cable compatible

board power
!= wall power

average power
!= transient proof
```

Real Experiment 89:
- exact external PSU identity/manual;
- cable map;
- ordinary GPU telemetry;
- optional consumer wall-meter evidence;
- no PSU opening/mains probing/protection bypass/intentional overload.

## Active next slice — Whole-Machine System Integration Dossier

Combine the course into one machine-design contract:

```text
workload + model dossier
→ GPU/VRAM fit
→ runtime/backend support
→ PCIe/topology
→ host RAM
→ storage/startup
→ PSU/cables
→ thermal/sustained performance
→ serving/network/privacy
→ budget/TCO
→ hard gates + unknown blockers
→ ACCEPT / REVISE / BLOCKED
```

Need teach:
- no single universal hardware score;
- hard gate vs optimization preference;
- UNKNOWN purchase-critical evidence blocks a final design;
- a system can fit the model but fail PSU/software/thermal constraints;
- multi-GPU capacity aggregation must include topology/power/cooling;
- graduation dossier should link raw Evidence rather than copy unverifiable numbers.

Recommended next labs:
- 90 synthetic whole-machine feasibility validator;
- 91 real machine design dossier / Evidence Packet.
