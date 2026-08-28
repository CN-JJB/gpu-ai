# Intelligence I38 — independently reproducible joint tradeoff artifact

Date: 2026-08-28

## Added

~~~text
tools/intelligence/verify_joint_tradeoff.py
tools/intelligence/joint_tradeoff_artifact_selftest.py
docs/specs/0039-intelligence-joint-tradeoff-artifact-verification.md
~~~

I37's builder is now reusable by both producer and verifier.

## Negative case

The self-test replaces PP, TG and PPL with new values while preserving coherent delta/ratio/percent arithmetic.

The artifact is still BLOCKED because the verifier rebuilds the expected object from:
- Experiment 61 manifests;
- benchmark records;
- I36-verified quality comparison;
- sealed quality bundles;
- exact model artifacts;
- corpus.

## Synthetic-only boundary

No self-test values are production measurements or recommendation evidence.
