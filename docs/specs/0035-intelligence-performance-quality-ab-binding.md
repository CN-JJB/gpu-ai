# Spec 0035 — Intelligence performance × quality A/B binding

Status: implemented in I34.

## Problem

I33 can produce an exact-contract PPL A/B, while Experiment 61 can produce a one-variable performance A/B.

Those two comparisons still need proof that they refer to the same baseline/candidate model pair and the same frozen experiment contract before anyone discusses a speed-vs-quality tradeoff.

## Inputs

I34 consumes:
- baseline Experiment 61 manifest;
- candidate Experiment 61 manifest;
- baseline ingested benchmark record;
- candidate ingested benchmark record;
- I33 `quality-comparison.json`.

## Shared one-variable contract

A reusable Experiment 61 manifest validator requires:
- same schema and comparison_id;
- same declared `intentional_variable`;
- no undeclared semantic differences;
- the declared variable actually changes;
- required protocol, quality, hardware, runtime, model, execution, prompt and sampler identity fields exist;
- no REPLACE/TBD/TODO placeholders.

Audit and label differences remain non-semantic.

## Benchmark ↔ manifest binding

Each benchmark record must exactly match its manifest for:
- model artifact SHA/bytes/quant/source revision;
- runtime identity/backend/build;
- hardware device/profile identity;
- PP/TG protocol and repetition settings;
- context/sequences/GPU layers/FA/KV/split/thread execution settings;
- prompt token identity.

PP and TG metrics must be finite and positive.

## Quality ↔ manifest binding

The I33 comparison must:
- use the expected I33 comparison contract and PPL metric;
- carry fixed quality identity exactly equal to both Experiment 61 manifests;
- bind baseline/candidate model SHA and bytes to the respective manifest model artifacts;
- reproduce its own PPL delta/ratio/percent arithmetic.

## Current scope

I33 intentionally requires identical quality executable bytes and identical evaluation argv across the two quality runs.

Therefore I34 currently allows joint attribution only when:

~~~text
intentional_variable == variant.model
or
intentional_variable is under variant.model.*
~~~

Execution/backend/KV-variable performance A/B is BLOCKED from receiving an I33 PPL attribution until a variable-aware quality comparator exists.

This is intentional fail-closed behavior.

## Output

Only a valid model-artifact A/B emits:
- comparison_id and intentional variable;
- exact semantic manifest differences;
- PP candidate/base delta, ratio and percent;
- TG candidate/base delta, ratio and percent;
- PPL candidate/base delta, ratio and percent;
- baseline/candidate model hashes.

No score, weighting, ACCEPT/REJECT, or recommendation is emitted.

## Trust boundary

I34 proves that performance and PPL evidence belong to the same exact model A/B contract.

It does not prove:
- statistical significance;
- target-task quality;
- causal superiority beyond the one-variable manifest discipline;
- deployment SLO fitness;
- purchase suitability.
