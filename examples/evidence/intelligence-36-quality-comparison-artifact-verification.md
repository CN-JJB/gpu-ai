# Intelligence I36 — reproducible quality comparison artifact

Date: 2026-08-28

## Added

~~~text
tools/intelligence/verify_quality_comparison.py
tools/intelligence/quality_comparison_artifact_selftest.py
docs/specs/0037-intelligence-quality-comparison-artifact-verification.md
~~~

I33 is refactored so its exact comparison object can be independently rebuilt.

## Negative case

The dedicated self-test edits both PPL values and recomputes the corresponding delta, ratio and percent change.

The JSON remains arithmetically self-consistent but is still BLOCKED because it no longer equals the comparison independently reconstructed from sealed I31/I32 evidence.

## Synthetic-only boundary

All values are test fixtures only.

No real PPL, GPU performance, or recommendation data is introduced.
