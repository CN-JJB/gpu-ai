# Learning / Build Record — 2026-08-27 PSU / Power Delivery / Platform Integration

## Slice

47 — PSU capacity/headroom, GPU power paths, modular-cable compatibility and safe platform integration.

## Production output

Research:
- `research/hardware/0003-psu-power-delivery-platform.md`

Dynamic intelligence:
- `intelligence/hardware/psu-connectors-atx-2026-08-27.md`

Reference:
- `reference/hardware/psu-power-delivery.md`

Lesson:
- `lessons/47-psu-power-delivery/01-watts-headroom-connectors.html`

Labs:
- `labs/experiments/88-psu-power-budget-model/`
- `labs/experiments/89-real-psu-platform-dossier/`

Evidence:
- `examples/evidence/experiment-47-psu-power-delivery.md`

## Verified L0

```text
850W / 550W / compatible paths
→ ACCEPT

850W / 820W / synthetic 15% policy
→ REVIEW

1000W / 600W / wrong modular cable
→ REJECT
```

## Real dossier

Blank/incomplete template is blocked rather than interpreted as real evidence.

## Stable skill

Learner can separate:

```text
rated capacity
continuous estimate
headroom policy
transient unknowns
connector/cable compatibility
board-vs-wall measurement
```

and understands that total watts cannot override a failed cable/connector gate.

## Safety

No PSU opening, exposed-mains probing, protection bypass, intentional overload or improvised high-voltage fixtures.

## Next

Whole-machine System Integration Dossier:
- workload/model requirements;
- GPU/VRAM/software gates;
- PCIe/topology;
- host RAM;
- storage;
- PSU/cables;
- cooling;
- serving/network/privacy;
- TCO;
- blocking unknowns.
