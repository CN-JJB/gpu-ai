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
- documented compatibility returns NEEDS-TEST, not measured PASS
- Experiment 61 importer reproduces PP/TG
- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED
- a different artifact falls back to NEEDS-TEST
- broken canonical hardware reference is rejected
~~~

The fixture PP/TG values are synthetic and prove only tool behavior.

They are not GPU performance claims.