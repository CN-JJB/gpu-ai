# Expected — Experiment 31

## Interactive

Required safe memory：

```
18 GiB
```

Expected gates：
- A → FAIL capacity；
- B → PASS；
- C → PASS；
- D → FAIL software because scenario rejects community-enabled。

Only B/C participate in ranking.

Because interactive emphasizes TG and cost, B should beat C under the default synthetic values despite C having more memory margin/lower risk.

## Long context

Required safe memory：

```
22 GiB
```

Expected：
- A → FAIL capacity；
- B → PASS；
- C → PASS；
- D → FAIL software。

Long-context weighting gives more weight to memory margin/risk, so C becomes much more competitive and can overtake B.

## Lesson

Same candidates：

```
different workload
→ different decision
```

Hard-gate failures never get rescued by a high soft score.

All candidate values are synthetic.