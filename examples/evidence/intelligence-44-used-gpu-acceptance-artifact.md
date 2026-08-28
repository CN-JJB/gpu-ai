# Intelligence I44 — packet-bound used-GPU acceptance

Date: 2026-08-28

## Added

~~~text
tools/intelligence/evaluate_used_gpu_acceptance.py
tools/intelligence/verify_used_gpu_acceptance.py
tools/intelligence/used_gpu_acceptance_selftest.py
labs/experiments/87-real-used-gpu-acceptance/acceptance-case.template.json
docs/specs/0045-intelligence-used-gpu-acceptance-artifact.md
~~~

## Provenance

The machine acceptance case must be PACKET-indexed.

The producer and verifier both re-evaluate Experiment 86-compatible ACCEPT / REVIEW / REJECT semantics.

## Negative cases

The self-test proves:
- a VRAM mismatch becomes REJECT;
- changing the derived REJECT artifact to ACCEPT is blocked;
- broken PACKET SHA is blocked.

## Important boundary

The output explicitly keeps:

~~~text
condition_grade_mapping = UNDEFINED
~~~

No C3/C4 mapping is invented.

All self-test evidence is synthetic.
