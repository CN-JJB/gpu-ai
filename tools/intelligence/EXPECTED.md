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
- Experiment 61 importer reproduces PP/TG
- broken canonical hardware reference is rejected
~~~

The fixture PP/TG values are synthetic and prove only tool behavior.

They are not GPU performance claims.