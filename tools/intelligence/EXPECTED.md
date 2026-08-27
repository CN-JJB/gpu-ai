# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python3 tools/intelligence/selftest.py
~~~

Expected:

~~~text
SELFTEST: PASS
- production catalog validates
- synthetic catalog validates only with explicit allowance
- Hardware ↔ Model ↔ Benchmark bridge returns the fixture observation
- same artifact/workload observations form one descriptive comparison group
- explicit same-cohort market rows enable descriptive price/performance
- evidence-linked TCO fixture reproduces the expected scenario arithmetic
- documented compatibility returns NEEDS-TEST, not measured PASS
- Experiment 61 importer reproduces PP/TG
- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED
- a different artifact falls back to NEEDS-TEST
- broken canonical hardware reference is rejected
~~~

The fixture PP/TG values are synthetic and prove only tool behavior.

They are not GPU performance claims.
## CI

The same checks run in:

~~~text
.github/workflows/intelligence-selftest.yml
~~~

CI executes Python compilation before the full self-test.
