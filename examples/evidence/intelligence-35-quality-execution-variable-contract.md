# Intelligence I35 — declared execution-variable quality contract

Date: 2026-08-28

## Added

~~~text
tools/intelligence/compare_quality_execution_variable.py
tools/intelligence/quality_execution_variable_selftest.py
labs/experiments/59-real-quality-gate/quality-variable-contract.template.json
docs/specs/0036-intelligence-quality-execution-variable-contract.md
~~~

## Positive path

A `variant.execution.*` quality A/B may pass when:
- Experiment 61 manifests differ only at the declared variable;
- a small contract binds each manifest value to its exact evaluation argv;
- I30 proves those argv tokens were actually executed;
- I31/I32 independently reproduce each PPL;
- model artifact and quality executable remain identical.

## Negative cases

The self-test blocks:
- a contract value that disagrees with the candidate manifest;
- unchanged quality argv for a declared execution-variable change;
- undeclared manifest drift;
- changed quality executable bytes.

## Important boundary

The contract authenticates the declared manifest-value ↔ argv relationship.

It does not independently prove the upstream program's semantic interpretation of those argv flags.

All self-test values are synthetic only.
