# Expected result

Verified against the L0 Python model.

~~~text
Concept model: one scheduler, one issue slot per cycle
Each group: 4 compute instructions + 1 memory instruction, then wait 20 cycles
Rounds per group: 20

resident groups     cycles     issued       idle   issue util
---------------------------------------------------------------
              1        480        100        380        20.8%
              2        561        200        361        35.7%
              4        723        400        323        55.3%
              8       1047        800        247        76.4%
             16       1695       1600         95        94.4%
             32       3200       3200          0       100.0%
~~~

## Interpretation

### 1 group

每一轮只发射 5 条指令，随后 memory dependency 让唯一 group 长时间不可运行。scheduler 没有替代工作，所以大量 cycles 空闲。

### 8 groups

不同 groups 的等待区间开始互相覆盖，scheduler 更经常能找到 ready group，idle cycles 明显减少。

### 16 groups

在本参数下已经接近完全覆盖等待。再增加 resident groups，边际收益很小。

### 32 groups

模型达到 100% issue utilization。但这不代表真实 GPU 的 100% occupancy，也不代表真实 kernel 会达到峰值性能；这里只有一个抽象 issue slot，没有模拟 bandwidth、cache、divergence、多个 pipelines、instruction dependencies 或架构限制。

## Resource-pressure thought experiment

如果某个优化使每个 block/group 使用更多 registers 或 shared memory/LDS，并把可驻留 groups 从 16 限制到 8，本模型的 issue utilization 从 94.4% 降到 76.4%。

但不能因此直接说这个优化更慢：真实 kernel 可能用这些资源换来更好的 data reuse、ILP 或更少 global-memory traffic。必须测真实 throughput。
