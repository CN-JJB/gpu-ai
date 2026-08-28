# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

## Current verified frontier

~~~text
I01–I41
~~~

Latest complete verification:

~~~text
workflow: Intelligence Self-Test
run #152
run id 33171494742
head 82b834197062216e33bde05c1ddc00f3fecd0027
job id 98849501909
conclusion success
Python 3.12
Ubuntu 24.04
~~~

The run explicitly passed:

~~~text
Compile intelligence tools
Run intelligence self-test
Run real benchmark capture self-test
Run model artifact gate self-test
Run command-model binding self-test
Run hardware profile gate self-test
Run prompt evidence gate self-test
Run quality corpus gate self-test
Run quality identity gate self-test
Run quality execution self-test
Run quality evaluation argv self-test
Run quality metric self-test
Run quality comparison self-test
Run quality comparison artifact self-test
Run reproducible performance-quality binding self-test
Run joint tradeoff artifact self-test
Run quality execution-variable self-test
Run quality execution-variable artifact self-test
Run execution performance-quality binding self-test
Run execution joint tradeoff artifact self-test
Run quality execution + metric intake self-test
Run market refresh self-test
~~~

## Provenance milestones

### I20–I32 — real intake chain

The suite proves fail-closed behavior for:
- raw benchmark ↔ manifest identity/config;
- local model artifact SHA/bytes;
- exact benchmark argv ↔ model binding;
- hardware profile;
- Experiment 57 prompt evidence;
- concrete quality corpus;
- quality identity schema v2;
- sealed quality execution;
- exact evaluation argv;
- narrow raw PPL extraction;
- mandatory independently reproducible quality metric.

### I33–I38 — model-artifact quality/tradeoff path

~~~text
I33 exact quality A/B
I36 independently reproduce comparison artifact
I37 require I36 reproduction in PP/TG × PPL binding
I38 independently reproduce full joint artifact
~~~

Tampering remains blocked even when edited PPL or PP/TG values have internally coherent delta/ratio/percent arithmetic.

### I35 / I39–I41 — execution-variable quality/tradeoff path

~~~text
I35 explicit manifest-value ↔ quality-argv contract
I39 schema-v2 reproducible execution-variable quality comparison
I40 bind reproduced PPL to matching Experiment 61 PP/TG
I41 independently reproduce full execution joint artifact
~~~

The current execution-variable path requires:
- `variant.execution.*`;
- same model artifact;
- same quality executable;
- fixed tokenizer/corpus/fixture identity;
- exact per-side evaluation argv from the declared variable contract.

The tooling authenticates the declared value ↔ argv relationship. It does not independently prove upstream flag semantics.

## Synthetic fixture boundary

All test PP/TG/PPL/price/TCO values are synthetic and prove tool behavior only.

They are not:
- GPU performance claims;
- model-quality claims;
- confirmed transaction data;
- causal conclusions;
- purchase recommendations.

Production benchmark rows remain zero until learner-owned real evidence is admitted.
