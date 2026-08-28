# Spec 0032 — Intelligence fail-closed quality metric extraction

Status: implemented in I31.

## Problem

I28–I30 seal and authenticate a quality execution, but the course still has no machine-readable quality metric derived from the raw output.

Copying a PPL value by hand would reopen a provenance gap.

## Narrow parser contract

I31 supports exactly one raw-output contract:

~~~text
Final estimate: PPL = VALUE +/- UNCERTAINTY
~~~

The parser:
- searches both sealed stdout and stderr;
- requires exactly one matching line total;
- requires finite PPL > 0;
- requires finite reported uncertainty >= 0;
- does not parse chunk progress values as a fallback.

Parser contract ID:

~~~text
llama-perplexity-final-estimate-v1
~~~

## Why fail closed

Current llama.cpp documentation/source shows the standard final-estimate line for the ordinary perplexity path.

Current upstream reports also show a stride path that can finish with chunk values but no final-estimate line.

Therefore I31 refuses to infer the final metric from the last chunk.

No supported final line means BLOCKED, not a guessed PPL.

## Machine-readable artifact

`extract_quality_metric.py` first requires the full I28/I30 execution verifier to pass.

It then writes:

~~~text
quality_metric_schema_version
parser_contract
metric = PPL
value
reported_uncertainty
source.stream
source.line_number
source.line_sha256
evidence hashes/bytes for:
  quality-command.json
  quality-identity.json
  stdout.txt
  stderr.txt
~~~

## Independent verification

`verify_quality_metric.py`:
1. reruns I28/I30 execution verification;
2. reparses the raw streams independently;
3. reconstructs the expected metric artifact;
4. requires exact object equality.

Changing the copied metric value is therefore blocked even if the JSON itself is well formed.

## Trust boundary

I31 proves machine-readable extraction from one supported raw-output contract.

It does not prove:
- that unsupported output formats are invalid runs;
- that the reported uncertainty is statistically sufficient;
- cross-corpus/model comparability;
- task/chat quality;
- purchase suitability.

Integration into mandatory real intake remains a later gate.
