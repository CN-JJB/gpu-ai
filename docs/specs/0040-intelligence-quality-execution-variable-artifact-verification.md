# Spec 0040 — Intelligence reproducible execution-variable quality comparison

Status: implemented in I39.

## Problem

I35 binds an execution-variable PPL A/B to an explicit manifest-value ↔ argv contract.

But its derived comparison JSON was not independently reproducible in the same way as I36's model-quality comparison.

## v2 artifact

I39 upgrades the execution-variable comparison to:

~~~text
quality_comparison_schema_version = 2
comparison_contract = ppl-declared-execution-variable-v2
~~~

and records:
- baseline/candidate metric SHA256;
- variable-contract SHA256;
- fixed quality identity;
- baseline/candidate executed evaluation argv;
- declared manifest variable path and values;
- quality executable SHA/bytes;
- model SHA/bytes;
- PPL delta/ratio/percent.

## Reusable builder

The producer now uses:

~~~text
build_execution_variable_quality_comparison(...)
~~~

which rechecks:
- Experiment 61 one-variable contract;
- I35 variable contract;
- both I31/I32 sealed metric bundles;
- same model artifact;
- same quality executable;
- fixed tokenizer/corpus/fixture identity;
- side-specific argv equality.

## Independent verifier

`verify_quality_execution_variable_comparison.py` rebuilds the entire v2 object from the same evidence roots and requires exact JSON-object equality.

## Tamper model

The dedicated test changes both PPL values and recomputes coherent delta/ratio/percent arithmetic.

It is still blocked because the edited numbers do not reproduce the sealed metric bundles.

## Trust boundary

I39 equalizes the provenance strength of the model-quality and execution-variable quality comparison paths.

It still does not prove the semantic meaning of declared upstream argv flags, significance, or purchase suitability.
