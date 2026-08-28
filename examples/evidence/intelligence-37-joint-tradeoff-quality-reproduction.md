# Intelligence I37 — mandatory comparison reproduction in joint tradeoff

Date: 2026-08-28

## Change

`bind_performance_quality_ab.py` now invokes I36 internally.

A joint PP/TG × PPL artifact cannot be emitted from `quality-comparison.json` alone.

It must also receive both sealed quality bundles, both exact model artifacts and the shared corpus.

## Output provenance

Joint schema v2 records:
- quality comparison SHA256;
- I33 comparison contract;
- baseline/candidate machine metric SHA256;
- `verification=INDEPENDENTLY-REPRODUCED-I36`.

## Negative case

The self-test edits both PPL values and recomputes a coherent 5% delta.

The joint tool still BLOCKS because the comparison cannot be reproduced from the sealed bundles.

## Synthetic-only boundary

All self-test PP/TG/PPL values remain synthetic fixtures.

Production benchmark data is unchanged and no recommendation is emitted.
