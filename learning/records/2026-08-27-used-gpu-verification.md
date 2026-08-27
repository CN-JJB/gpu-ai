# Learning / Build Record — 2026-08-27 Used GPU Verification

## Slice

20 — Used GPU transaction and acceptance verification.

## Production output

Research:
- `research/hardware/0002-used-gpu-transaction-verification.md`

Reference:
- `reference/hardware/used-gpu-acceptance-checklist.md`

Lesson:
- `lessons/20-used-gpu-verification/01-before-pay-after-arrival.html`

Labs:
- `labs/experiments/35-seller-evidence-quality/`
- `labs/experiments/36-real-used-gpu-acceptance/`

Evidence/intelligence:
- `examples/evidence/experiment-20-used-gpu-verification.md`
- `intelligence/hardware/used-gpu-acceptance-tools-2026-08-27.md`

## Stable acceptance chain

```
seller evidence
→ arrival chain-of-evidence
→ visual
→ identity
→ baseline errors
→ memory integrity
→ workload stability
→ thermals
→ after-test errors
→ ACCEPT / DISPUTE
```

## Safety design

Default collection is non-destructive and read-only.

No automatic:
- OC;
- power-limit modification;
- firmware/BIOS flash;
- extreme stress.

Stop conditions are explicit.

## Key teaching result

A GPU can pass:
- graphics stress;
but fail:
- memory integrity.

Or pass memory integrity but fail:
- sustained workload;
- thermal behavior;
- driver stability.

Acceptance therefore requires multiple independent evidence layers.

## Next work

Build price-threshold/watchlist workflow:

```
workload card
→ candidate dossier
→ max buy price
→ current market sample
→ evidence gaps
→ watch / buy / skip
```

Then continue into practical deployment projects using actually selected hardware.
