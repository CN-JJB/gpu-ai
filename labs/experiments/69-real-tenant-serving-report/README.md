# Experiment 69 — Real Per-Tenant Serving Report

硬件等级：L1/L2/L3，复用 Experiment 63。

## Goal

Break one real serving trace down by tenant without publishing private user identity/content.

## Workload metadata

Add pseudonymous:

```json
{
  "id":"r0",
  "tenant":"tenant-A",
  "prompt_tokens":512,
  "prompt_file":"...",
  "n_predict":128
}
```

Fields:
- `tenant`: pseudonymous ID;
- `prompt_tokens`: exact count from Experiment 57 / exact tokenizer;
- `n_predict`: requested output budget.

Experiment 63 collector ignores extra fields, so the same JSONL can be used for request generation.

## Run

After Experiment 63:

```bash
python3 tenant_report.py \
  workload.jsonl \
  evidence/requests.csv
```

## Output

Per tenant:
- request count;
- successful requests;
- prompt-token total;
- requested output budget;
- observed generated token IDs;
- TTFT p50/p95;
- E2E p95.

## Important

Request share is not resource share.

Compare:

```
request %
prompt token %
output token %
latency
```

## Privacy

Use pseudonymous tenant IDs.

The report does not require storing or publishing real identities.

## Quota experiment

If your application gateway supports tenant limits, compare one policy at a time:
- max concurrent;
- max output;
- max context;
- token budget.

Use Experiment 61 manifest discipline.

Do not claim llama-server itself implements a quota unless the exact runtime proves it.
