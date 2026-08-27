# llama-server Concurrency / Batching / Latency 速查

## 一张图

~~~text
clients
  ↓
queue
  ↓
slots
  ↓
prompt processing
  ↓
active decode set
  ↓
continuous batching
  ↓
model/hardware
  ↓
stream
~~~

同时：

~~~text
active sequences × cached context
→ KV pressure
~~~

## Client concurrency ≠ server slots

Client concurrency：同一时刻客户端愿意发多少 request。

Server slots：server 可同时维护/处理多少 active request states。

例如：

~~~text
clients = 8
slots = 4

可能：
4 processing
4 deferred
~~~

current llama-server 可用 requests_processing 与 requests_deferred 验证。

## Continuous batching

静态 batch：

~~~text
[A short, B long]
A done
→ 空位不能立刻给 C
→ 等 B
~~~

continuous batch：

~~~text
A done
→ C 立即进入 active set
→ B + C 继续 batch
~~~

重点是 active set 动态变化，不死记某个 runtime 内部 scheduler。

## 5 个性能指标

| 指标 | 定义 | 用户感受 |
|---|---|---|
| TTFT | request start → first useful output | “多久开始说话” |
| ITL | 相邻 output token interval | “说话流不流畅” |
| E2E latency | request start → complete | “整题多久做完” |
| request throughput | completed requests / s | server 吞吐 |
| aggregate token throughput | output tokens / wall s | 总 token 产能 |

## Chunk gap 不是严格 ITL

SSE chunk 可以为空、包含多 token 对应文本，也会受网络/runtime buffering 影响。

普通 HTTP client 安全写法：

~~~text
stream chunk cadence proxy
~~~

不要直接写：

~~~text
exact token ITL
~~~

## TTFT 为什么会突然恶化

~~~text
TTFT
≈ queue
+ request/tokenization overhead
+ prompt processing
+ first decode step
~~~

slots 满以后：

~~~text
queue ↑
→ p95 TTFT ↑
~~~

不要求单-request decode t/s 先变差。

## Throughput ↔ latency

batch 更多 active sequences：

可能：
- aggregate tokens/s ↑
- hardware utilization ↑
- weight traffic 被更好摊薄

同时：
- decode step time ↑
- per-user cadence 变慢
- KV usage ↑

所以：

~~~text
best single-user latency
!= best multi-user throughput
~~~

## Current llama-server metrics

当前 upstream snapshot 可观察：

~~~text
prompt_tokens_total
prompt_seconds_total
prompt_tokens_seconds

tokens_predicted_total
tokens_predicted_seconds_total
predicted_tokens_seconds

requests_processing
requests_deferred
n_decode_total
n_busy_slots_per_decode
n_tokens_max
~~~

CLI/metric 名是动态接口；稳定概念不依赖 spelling。

## 两种 throughput

Server compute-time throughput：

~~~text
Δ predicted tokens / Δ predicted seconds
~~~

Wall aggregate throughput：

~~~text
Δ predicted tokens / experiment wall time
~~~

后者包含 queue/prompt/turnover/idle gap。

## KV connection

Slice 05：

~~~text
KV ∝ active sequences × tokens × kv_heads × layers × head_dim
~~~

所以 slots/concurrency 增加时，重新检查：

- memory headroom
- context
- KV dtype
- runtime cache policy

current llama-server 有 unified KV/prompt cache 等机制，不机械计算 real KV = slots × fixed ctx。

## 最小实验矩阵

固定 server：

~~~text
slots = 4
same model
same ctx
same KV type
same offload
continuous batching ON
~~~

客户端固定总请求数 8，扫：

~~~text
concurrency = 1, 2, 4, 8
~~~

观察：

- mean/p95 TTFT
- mean/p95 E2E
- stream-gap proxy
- wall output t/s
- server predicted t/s
- peak processing
- peak deferred
- busy slots/decode

## 结果怎么读

### concurrency ↑，aggregate ↑，TTFT 仍低

还有 batching headroom。

### concurrency > slots，deferred ↑，p95 TTFT 暴涨

queueing 已成为体验瓶颈。

### aggregate 不再涨，但 latency 继续涨

server 接近 saturation。

### busy slots/decode 很低

客户端虽然“并发”，但 server 没形成有效 active set，继续查 request timing / prompt mismatch / scheduler / config。

### 长 context 后吞吐掉

回查 KV traffic、cache、memory bandwidth、capacity headroom。

## Production 观念

单用户最快设置和多人服务最优设置不是一回事。

服务调参目标必须先写清：

~~~text
latency-first?
throughput-first?
balanced?
~~~
