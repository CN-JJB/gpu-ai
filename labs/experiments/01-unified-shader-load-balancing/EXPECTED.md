# Expected result

Verified with Python 3.

~~~text
Concept model: fixed 64/64 partition vs unified 128-unit pool
Unified scheduling/generalization overhead: 5%

scenario         fixed time   fixed util   unified time   unified util    speedup
----------------------------------------------------------------------------------
vertex-heavy         125.00       62.5%          82.03         95.2%      1.52x
balanced              78.12      100.0%          82.03         95.2%      0.95x
pixel-heavy          125.00       62.5%          82.03         95.2%      1.52x
~~~

## Interpretation

偏斜 workload 下，固定 50/50 分区的一半资源无法帮助另一半，因此出现闲置。统一池在本抽象中可以重新分配资源，所以利用率稳定。

balanced 场景是重要反例：固定分区恰好匹配 workload 时可以达到 100% 利用，而统一池被人为加入的 5% 开销使它略慢。

结论不是统一架构永远更快，而是统一可编程资源对 workload 变化更有适应性。
