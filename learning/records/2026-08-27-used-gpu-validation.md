# Learning / Build Record — 2026-08-27 Used-GPU Validation / Purchase Acceptance

## Slice

46 — Advanced used-GPU identity, PCIe, error-state and sustained Local-LLM acceptance.

## Relationship to earlier course

Slice 20 remains the transaction/arrival workflow.

Slice 46 upgrades the hardware-evidence depth rather than replacing it.

## Production output

Research:
- `research/gpu/0007-used-gpu-validation-purchase.md`

Dynamic intelligence:
- `intelligence/gpu/used-gpu-validation-2026-08-27.md`

Reference:
- `reference/gpu/used-gpu-purchase-acceptance.md`

Lesson:
- `lessons/46-used-gpu-validation/01-identity-link-errors-acceptance.html`

Labs:
- `labs/experiments/86-used-gpu-acceptance-model/`
- `labs/experiments/87-real-used-gpu-acceptance/`

Evidence:
- `examples/evidence/experiment-46-used-gpu-validation.md`

## Verified L0

```text
healthy
→ ACCEPT

idle x1 current / x16 max / no under-load link check
→ REVIEW

24 GiB claimed / 12 GiB observed
→ REJECT
```

## Stable skill

Learner can separate:

```text
marketing identity
hardware identity
PCIe capability
current negotiated state
unsupported telemetry
observed errors
sustained workload stability
```

and can end a used-card test with an auditable technical decision.

## Safety

No firmware flashing, OC/UV, power/fan tuning, error injection or destructive VRAM stress in the default real lab.

## Next

PSU / power delivery / platform integration:
- continuous board/system power;
- PSU headroom;
- PCIe slot vs auxiliary power;
- connector/cable topology;
- transient/connector heating risk;
- multi-GPU aggregate power;
- safe non-invasive inventory.
