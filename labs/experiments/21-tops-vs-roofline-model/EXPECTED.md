# Expected — Experiment 21

默认是 synthetic model。

## Prefill-like

```text
AI = 200 ops/byte
memory roof = 200 TOPS-equivalent
```

近似：

| path | compute roof | effective |
|---|---:|---:|
| fp32 | 42.5 | 42.5 |
| fp16_matrix | 180 | 180 |
| int8_matrix | 320 | ~190.5 |
| int4_native | 520 | ~185.2 |
| q4_weight_only | 170 | ~154.5 |

解释：
- 高 precision matrix peaks 开始有价值；
- 但 memory roof=200 把更高 peak 截住；
- overhead 让低-bit path 低于理想 roof。

## Decode-like

```text
AI = 4 ops/byte
memory roof = 4 TOPS-equivalent
```

所有 path 都首先撞到 4 TOPS-equivalent memory roof，再扣 overhead。

因此：
- 50 TOPS 与 800 TOPS 的广告差距几乎消失；
- memory bandwidth / weight bytes 更关键；
- low-bit storage 需要通过提高实际 arithmetic intensity 才会显著抬高 decode roof。

## 重要边界

这个脚本没有真实建模“Q4 让 bytes 减 4× 后 AI 提升多少”，只把 precision peak 与 memory roof 的关系分开。

下一步真实 benchmark 才能回答某个 backend 的 low-bit kernel 到底如何实现。
