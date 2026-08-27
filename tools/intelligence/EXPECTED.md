# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

Expected and verified on 2026-08-27:

~~~text
SELFTEST: PASS
- production catalog validates
- synthetic catalog validates only with explicit allowance
- Hardware ↔ Model ↔ Benchmark bridge returns the fixture observation
- same artifact/workload observations form one descriptive comparison group
- explicit same-cohort market rows enable descriptive price/performance
- evidence-linked TCO fixture reproduces the expected scenario arithmetic
- documented compatibility returns NEEDS-TEST, not measured PASS
- explicit UNKNOWN remains valid and returns BLOCKED
- Experiment 61 importer reproduces PP/TG
- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED
- a different artifact falls back to NEEDS-TEST
- broken canonical hardware reference is rejected
~~~

The final verification used a local tree whose checked Git blob SHAs matched the latest main-branch scripts and fixture/catalog files.

Detailed evidence:

~~~text
examples/evidence/intelligence-i01-i06-selftest-verification.md
~~~

Fixture PP/TG/price/TCO values are synthetic and prove only tool behavior.

They are not GPU performance or purchase claims.

## CI

The same checks are defined in:

~~~text
.github/workflows/intelligence-selftest.yml
~~~

The available GitHub connector did not surface a workflow run for this checkpoint, so do not claim CI success from the workflow file alone.
