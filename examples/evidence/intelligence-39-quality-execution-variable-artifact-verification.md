# Intelligence I39 — reproducible execution-variable quality comparison

Date: 2026-08-28

## Added

~~~text
tools/intelligence/verify_quality_execution_variable_comparison.py
tools/intelligence/quality_execution_variable_artifact_selftest.py
docs/specs/0040-intelligence-quality-execution-variable-artifact-verification.md
~~~

The I35 comparison is now a schema-v2 artifact with:
- variable-contract SHA;
- baseline/candidate metric SHA;
- explicit execution-variable path/values;
- actual per-side evaluation argv;
- model/executable identity.

## Negative case

A comparison with coherently edited PPL values and recomputed arithmetic is BLOCKED by full independent reconstruction.

## Synthetic-only boundary

No production quality or benchmark measurements are introduced.
