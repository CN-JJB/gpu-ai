# Spec 0036 — Intelligence declared execution-variable quality contract

Status: implemented in I35.

## Problem

I33 intentionally requires identical evaluation argv, so I34 can safely bind PPL only to model-artifact A/B.

For execution variables such as KV representation, a valid quality A/B may need the same model/executable but different quality argv.

Simply allowing arbitrary argv differences would destroy comparability.

## Explicit variable contract

I35 introduces a small machine-readable declaration:

~~~json
{
  "quality_variable_contract_schema_version": 1,
  "comparison_id": "...",
  "intentional_variable": "variant.execution.kv_k",
  "baseline": {
    "manifest_value": "f16",
    "evaluation_args": ["--cache-type-k", "f16"]
  },
  "candidate": {
    "manifest_value": "q8_0",
    "evaluation_args": ["--cache-type-k", "q8_0"]
  }
}
~~~

The concrete argv tokens are examples only; real runs must use the pinned executable's actual current flags.

## Required bindings

I35:
1. validates the Experiment 61 one-variable manifest pair;
2. currently accepts only `variant.execution.*`;
3. requires the contract comparison_id and intentional variable to equal the manifests;
4. requires baseline/candidate `manifest_value` to exactly equal the manifest dotted-path values;
5. requires each declared evaluation-argv list to exactly equal that side's I30 quality identity;
6. requires the evaluation argv to actually differ;
7. independently verifies both I31/I32 quality metric bundles;
8. requires fixed tokenizer/corpus/fixture identity to match;
9. requires identical model artifact SHA in both manifests and both quality runs;
10. requires identical quality executable SHA256 + bytes.

Only then may it compute descriptive PPL delta/ratio.

## Why this is still declared evidence

The contract proves:

~~~text
manifest semantic value
↔
declared quality argv
↔
actually executed quality argv
↔
reproducible PPL
~~~

It does not prove that the upstream executable interprets those argv tokens as the intended semantic field.

That semantic mapping remains an auditable declared assumption unless a future tool can independently derive it from runtime metadata/help output.

## Current exclusions

I35 does not support:
- `variant.runtime.*` build/backend changes;
- executable changes;
- hardware-variable quality attribution;
- arbitrary multi-variable quality experiments.

Those remain BLOCKED.

## Trust boundary

I35 enables explicit execution-variable quality evidence without weakening the exact provenance chain.

It is not a significance test, quality verdict, causal guarantee, or purchase recommendation.
