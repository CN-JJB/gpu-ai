# Spec 0034 — Intelligence exact quality A/B comparability

Status: implemented in I33.

## Problem

I31/I32 make each side's PPL machine-reproducible, but two individually valid PPL values are not automatically comparable.

A delta is meaningful only when the quality evaluation contract is held fixed.

## Exact comparison contract

Before computing a PPL delta or ratio, I33 independently verifies both quality bundles and requires exact equality of:

~~~text
tokenizer_identity
corpus_sha256
fixture_revision
evaluation_args
quality metric parser_contract
metric name
quality executable SHA256
quality executable bytes
~~~

The same concrete corpus artifact is supplied to both verifiers.

Different model artifacts are allowed because the model/quant/backend candidate may be the intended comparison variable.

## Bundle layout

Each side uses the I28–I32 quality bundle:

~~~text
quality-command.json
stdout.txt
stderr.txt
PACKET.json
quality-identity.json
quality-metric.json
~~~

The comparator also receives the exact local baseline/candidate model artifacts and shared corpus.

## Output

Only after exact comparability passes, the tool writes:

~~~text
baseline PPL
candidate PPL
candidate - baseline delta
candidate / baseline ratio
percent change
reported uncertainty for each side
fixed quality identity
quality executable hash
model artifact hashes
~~~

No uncertainty propagation or significance test is invented.

## Fail-closed cases

Comparison is blocked when:
- either side fails I31/I32 verification;
- tokenizer/corpus/fixture/evaluation args differ;
- parser/metric differs;
- quality executable bytes/hash differ.

## Trust boundary

I33 is a descriptive exact-contract quality A/B.

It does not prove:
- the model artifact is the only system variable;
- statistical significance;
- target-task quality;
- causal superiority;
- purchase suitability.
