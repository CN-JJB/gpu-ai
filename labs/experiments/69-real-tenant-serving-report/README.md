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


## Why this experiment

真实多租户服务中，“每个用户请求数差不多”不代表资源使用公平。这个实验把同一真实 request trace 按 pseudonymous tenant 拆开，同时避免保存真实身份和 prompt 内容。

## Hypothesis

不同 tenant 的 request share、prompt-token share、output-token share 和 latency share 可能明显不同；因此公平性分析必须至少看多维资源代理。

## Fixed variables

先复用同一 Experiment 63 trace。第一次只做 report，不改 scheduler/quota。之后若做 quota A/B，一次只改一个 policy。

## What to observe

1. 每 tenant request count。
2. prompt token total。
3. requested/observed output work。
4. TTFT p50/p95 与 E2E p95。
5. request % 与 token % 是否给出不同故事。

## Troubleshooting

- tenant ID 必须 pseudonymous。
- prompt_tokens 要来自 exact tokenizer evidence。
- 不要因为字段叫 tenant 就存真实姓名/email。
- 不要声称 llama-server 原生支持某 quota，除非 exact runtime 有证据。

## Evidence to save

保存 workload metadata、requests.csv、tenant report；公开时只保留匿名 ID 和必要统计。

## What this proves

你能用真实 trace 做 tenant-level workload/fairness 分解。

## What this does NOT prove

它不自动证明 scheduler 公平，也不等价于 GPU 资源精确计费。

## No-hardware fallback

没有真实 server 时先完成 Experiment 68；本实验留到 Learner Verified。

## Transfer question

Tenant A 只有 20% 请求，却占 70% generated tokens。只按 request quota 会有什么问题？
