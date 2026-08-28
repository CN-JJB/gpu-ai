# Spec 0043 — Intelligence unified verified tradeoff routing gate

Status: implemented in I42.

## Problem

After I41 there are two strong but distinct verified tradeoff paths:

~~~text
model artifact:
I33 → I36 → I37 → I38

execution variable:
I35 → I39 → I40 → I41
~~~

A caller still has to choose the correct verifier manually.

Choosing the wrong path can create semantic confusion even when each verifier is individually strict.

## Automatic routing

I42 reads the validated Experiment 61 manifest pair and selects the verifier from the declared intentional variable.

~~~text
variant.model
variant.model.*
→ MODEL_ARTIFACT_I38

variant.execution.*
→ EXECUTION_VARIABLE_I41

variant.runtime.*
variant.hardware.*
multi-variable/system/other unsupported variables
→ BLOCKED
~~~

There is no user-supplied `--route`.

The evidence itself determines the route.

## Variable-contract handling

Execution-variable route:
- requires `--variable-contract`;
- delegates full verification to I41.

Model route:
- rejects `--variable-contract`;
- delegates full verification to I38.

This prevents irrelevant or mismatched route metadata from being silently ignored.

## Verified envelope

On success I42 writes a small envelope:

~~~text
verified_tradeoff_schema_version = 1
comparison_id
intentional_variable
route
verifier
verification = PASS
joint_tradeoff schema/contract/SHA
source SHA roots
scope = DESCRIPTIVE_ONLY
~~~

The envelope deliberately does not duplicate PP/TG/PPL values and does not score them.

## Fail-closed cases

The dedicated self-test proves:
- model evidence routes to I38;
- execution evidence routes to I41;
- execution route without variable contract is blocked;
- model route with an irrelevant variable contract is blocked;
- runtime-variable attribution is unsupported and blocked;
- tampered joint evidence remains blocked by the selected underlying verifier.

## Trust boundary

I42 proves that a supported tradeoff artifact was sent through the correct verified evidence lane.

It does not add:
- statistical significance;
- SLO fitness;
- a weighted score;
- ACCEPT/REJECT;
- a purchase recommendation.
