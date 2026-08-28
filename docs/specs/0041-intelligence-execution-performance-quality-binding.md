# Spec 0041 — Intelligence execution-variable performance × quality binding

Status: implemented in I40.

## Problem

I39 makes execution-variable quality comparison independently reproducible.

Performance and quality still need to be bound to the same Experiment 61 execution-variable A/B before discussing a tradeoff.

## Inputs

I40 consumes:
- baseline/candidate Experiment 61 manifests;
- baseline/candidate benchmark records;
- I39 execution-variable quality comparison;
- baseline/candidate sealed quality bundles;
- baseline/candidate exact model artifacts;
- shared corpus;
- quality-variable contract.

## Reproduction first

The binder first invokes I39 verification.

The supplied comparison is not trusted directly.

Only an exact reconstruction from sealed quality evidence and the declared variable contract may continue.

## Experiment 61 binding

The same one-variable manifest validator must pass.

The intentional variable must be under:

~~~text
variant.execution.*
~~~

Each benchmark record must bind exactly to its corresponding manifest for model, runtime, hardware, protocol, execution and prompt identity.

## Quality binding

The I39 comparison must match the manifests for:
- comparison_id;
- intentional variable;
- declared baseline/candidate semantic values;
- fixed tokenizer/corpus/fixture identity;
- model SHA/bytes;
- variable-contract SHA.

## Output

I40 writes:

~~~text
joint_tradeoff_schema_version = 1
tradeoff_contract = experiment61-execution-performance-quality-v1
~~~

with:
- PP delta/ratio/percent;
- TG delta/ratio/percent;
- PPL delta/ratio/percent;
- declared execution variable path/values;
- per-side quality evaluation argv;
- comparison/contract/metric SHA roots;
- verification = INDEPENDENTLY-REPRODUCED-I39.

## Fail-closed cases

The self-test blocks:
- coherently edited I39 comparison JSON;
- benchmark workload drift;
- undeclared manifest drift.

## Trust boundary

I40 proves the performance and PPL evidence belong to the same declared execution-variable A/B.

It still does not prove:
- that upstream argv semantics match the declared variable;
- statistical significance;
- task-quality sufficiency;
- SLO fitness;
- purchase suitability.
