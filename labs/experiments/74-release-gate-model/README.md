# Experiment 74 — Synthetic Release Gate / Rollback

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/release-rollback.svg" alt="发布 gate 先验证 correctness、兼容、性能与恢复条件；任何关键 gate 失败都应阻止 rollout 或触发 rollback。">
  <figcaption>发布 gate 先验证 correctness、兼容、性能与恢复条件；任何关键 gate 失败都应阻止 rollout 或触发 rollback。</figcaption>
</figure>

## Goal

Prove that a faster candidate can still fail release gates.

## Policy

Bundled example:

```
ready <= 8000 ms
first inference <= 9000 ms
TG speedup >= 1.0x
PPL ratio <= 1.02
critical fixtures pass
TTFT p95 <= 500 ms
SLO compliance >= 99%
```

These are synthetic project thresholds, not universal recommendations.

## Good candidate

```bash
python3 evaluate.py \
  policy.json baseline.json candidate-good.json rollback.json
```

Expected:

```
DECISION: ACCEPT
```

## Fast-but-bad candidate

```bash
python3 evaluate.py \
  policy.json baseline.json candidate-fast-bad.json rollback.json
```

Expected:
- TG gate passes;
- PPL gate fails;
- TTFT gate fails;
- SLO gate fails;

then:

```
DECISION: ROLLBACK
ROLLBACK: VERIFIED
```

## Rollback identity

The rollback JSON exactly restores baseline:
- runtime SHA;
- model SHA;
- config SHA.

Readiness/smoke are checked again.

## Scope

All values/hashes are synthetic.


## Why this experiment

升级最危险的思维是“新版本更快，所以发布”。真正的 release gate 必须同时保护功能、质量、性能、SLO 和可回滚性。

## Hypothesis

candidate-good 应通过所有 gate；candidate-fast-bad 即使 TG 更高，也应因为 PPL/TTFT/SLO 失败而 ROLLBACK。回滚还必须恢复 exact identity 并重新通过 readiness/smoke。

## Fixed variables

policy.json 固定；baseline 与 rollback identity 固定。只比较不同 candidate evidence。

## What to observe

1. 每个 gate 是 hard requirement 还是 preference。
2. fast-bad 中哪些 gate PASS、哪些 FAIL。
3. 为什么任一关键 FAIL 都不能被 TG speedup 抵消。
4. rollback 的 runtime/model/config SHA 是否精确回到 baseline。
5. rollback 后为什么还要功能验证。

## Troubleshooting

- 不要把 synthetic threshold 当通用推荐。
- 只回退 binary、没回退 config/model 不算 exact rollback。
- “rollback command 成功”不等于服务恢复；要重新 ready + smoke。
- 同时改太多变量会降低回归定位能力。

## Evidence to save

保存两次 evaluate 输出、四个 JSON，并画出 candidate → gate matrix → decision → rollback verification。

## What this proves

你能用显式 gate 做安全升级/回滚决策。

## What this does NOT prove

所有 hashes/metrics 都是 synthetic，不代表任何真实 runtime 发布。

## No-hardware path

完整 L0。

## Transfer question

新版本 TG +12%，但 PPL ratio 超过质量阈值且 TTFT p95 超标，你应该发布吗？为什么？
