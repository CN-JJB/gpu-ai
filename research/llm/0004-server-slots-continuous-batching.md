# Research Note 0004 — llama-server：Slots、Continuous Batching、Queueing 与服务指标

日期：2026-08-26

## Research question

为什么同一个本地 LLM：

- 单用户 llama-bench tg 很快；
- 一开多个并发请求，单个用户的首 token 与 token cadence 却变差；
- 同时 aggregate throughput 反而可能上升？

需要建立稳定的 server 心智模型：

~~~text
incoming requests
→ queue / admission
→ slots
→ prompt processing
→ continuous decode batch
→ KV state
→ streaming responses
~~~

并区分：

- TTFT
- output-token cadence / ITL
- end-to-end latency
- request throughput
- aggregate token throughput
- server-side prompt/decode throughput

## Scope

本笔记以 llama.cpp current llama-server 为现实实现，但稳定 Lesson 不把 current CLI flag spelling 或内部 scheduler 细节当永久规则。

动态接口快照单独保存到：

intelligence/llm/llama-server-concurrency-2026-08-26.md

研究时 upstream llama.cpp master：

d7a2074112d27649303fa107eb8c94db1ee435f3

## Primary sources

### 1. llama.cpp server README

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Current upstream explicitly lists：

- parallel decoding with multi-user support；
- continuous batching；
- OpenAI-compatible chat/completions API；
- streaming responses；
- monitoring endpoints。

Current server parameters include：

- --parallel N：number of server slots；
- --cont-batching：continuous/dynamic batching；
- --ctx-size；
- --cache-type-k/v；
- --kv-unified；
- --metrics；
- --slots。

### 2. llama-server /metrics

Same source：

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Current Prometheus metrics include：

- prompt_tokens_total
- prompt_seconds_total
- prompt_tokens_seconds
- tokens_predicted_total
- tokens_predicted_seconds_total
- predicted_tokens_seconds
- requests_processing
- requests_deferred
- n_tokens_max
- n_decode_total
- n_busy_slots_per_decode

这些指标足以观察：

~~~text
admitted work
queued/deferred work
batch occupancy
server prompt throughput
server generation throughput
~~~

### 3. llama-server /slots

Same source。

Current GET /slots is enabled by default unless disabled and returns per-slot state such as：

- slot id
- is_processing
- n_ctx
- task id
- sampling/config state
- decoded-token state

因此“server configured with N slots”与“此刻多少 slots 正忙”可以分开验证。

### 4. llama.cpp server benchmark

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/README.md

Official benchmark uses：

- OpenAI chat completions endpoint；
- configurable concurrent users；
- --parallel slots；
- continuous batching；
- metrics endpoint。

这证明 concurrency/slots 是 upstream 自己的 server benchmark dimension。

### 5. llama.cpp SPEED-Bench client

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/speed-bench/README.md

Current client reports：

- avg prompt t/s；
- avg predicted/decode t/s；
- average end-to-end latency；
- concurrency；
- raw JSON。

Its current source separately reads response usage/timings and client wall latency。

## Findings

### F1 — Slot 是 server admission/execution context，不是“一个 CUDA core”

Current --parallel N 定义 server slots。

稳定理解：

~~~text
slot
= server 同时维护一个 active request/sequence execution state 的容量单位
~~~

它不是一个 SM、一个 warp、一个 CPU thread，也不是一份完整模型副本。

多个 slots 共享同一个模型 runtime/hardware resources。

### F2 — Client concurrency 与 server slots 是两个不同数字

假设：

~~~text
client concurrency = 8
server slots = 4
~~~

最多只能有部分请求同时 processing，其余进入 deferred/queue state。

Current requests_processing 与 requests_deferred metrics 可以直接观察这件事。

因此：

~~~text
more clients
!= more simultaneous model execution
~~~

### F3 — Queueing 首先伤 TTFT

服务端 request 的首 token 等待可以拆成近似：

~~~text
TTFT
≈ queue wait
+ request/tokenization/server overhead
+ prompt processing
+ first decode step
~~~

active slots 已满后：

~~~text
queue wait ↑
→ TTFT ↑
~~~

即使单个 active request 的 decode speed 没变。

### F4 — TTFT、ITL 与 E2E latency 不是同一个指标

TTFT：

~~~text
request start → first useful streamed output
~~~

ITL：

~~~text
相邻 output tokens 的时间间隔
~~~

E2E latency：

~~~text
request start → response complete
~~~

一个系统可以 TTFT 很差但开始生成后很快，也可以 aggregate throughput 很高但单用户 latency 差。

### F5 — SSE chunk gap 不是严格 token-level ITL

OpenAI-compatible streaming 通过 SSE/chunks 返回。

客户端看到的一个 chunk 可能为空、可能包含多个 token 对应文本，还受 HTTP buffering/runtime batching 影响。

因此 real lab 记录：

~~~text
first non-empty stream delta → TTFT proxy
mean non-empty stream chunk gap → client-visible cadence proxy
~~~

不把 chunk gap 写成精确 ITL。

### F6 — Continuous batching 的核心是“活跃集合可以动态变化”

静态 batch 的低效情况：

~~~text
request A 很短
request B 很长
→ A 完成后 batch 出现空位
→ 若必须等 B 完成才能换下一批，资源浪费
~~~

continuous batching 的稳定概念：

~~~text
某 request 完成
→ 新排队 request 可以进入 active batch
→ 不必等整批结束
~~~

具体 llama.cpp scheduler 实现会演进，但这个 teaching model 是通用的。

### F7 — Batching 可以提高 aggregate throughput，同时恶化 active-user cadence

Decode 时多个 active sequences 可以共同进入模型执行批次。

抽象上：

~~~text
batch size ↑
→ 一次 step 产生更多 total output tokens
→ fixed/model-weight work 更容易摊薄
→ aggregate tokens/s 可上升
~~~

但单 step 通常也更重：

~~~text
batch size ↑
→ step time ↑
→ 单用户相邻 token 间隔可能变长
~~~

所以存在 throughput ↔ per-request latency trade-off。

### F8 — Continuous batching 与 Roofline 是同一问题的 server 版本

单用户 decode 常见低 arithmetic-intensity：

~~~text
大量 weight bytes
→ 少量当前-token work
~~~

多个 sequences batched：

~~~text
同一批模型执行
→ 服务多个 sequence
→ useful work / memory-traffic opportunity ↑
~~~

可能提高 aggregate throughput，但收益依赖 backend/model/quant/batch/memory bandwidth/KV traffic/hardware。

### F9 — 并发会把 KV capacity 压力推高

Slice 05：

~~~text
KV baseline ∝ active sequences × cached tokens
~~~

所以：

~~~text
more active sequences
→ more live KV state
→ memory pressure ↑
~~~

Current llama-server 还存在 unified KV、prompt cache、context checkpoints、cache types 等机制，因此 runtime memory 不应简单写成“slots × fixed n_ctx”。

稳定 Lesson 只保留：并发与 context 一起决定 KV pressure。

### F10 — n_busy_slots_per_decode 是 batching Evidence

Current metric n_busy_slots_per_decode 描述 average busy slots per llama_decode() call。

它可以回答：

> 客户端虽然并发，server 是否真的形成多-request decode active set？

这比单看 client concurrency 更接近实际 server execution。

### F11 — requests_deferred 是排队的直接 Evidence

当 client concurrency 超过可立即处理容量时：

~~~text
requests_deferred > 0
~~~

意味着 queue/admission 已进入 user latency。

real lab 同时保存：

- client TTFT；
- peak deferred；
- peak processing；
- busy slots/decode。

### F12 — Server-side throughput 与 client wall throughput 要分开

Server predicted throughput：

~~~text
Δ predicted tokens / Δ server predicted seconds
~~~

Aggregate wall throughput：

~~~text
Δ predicted tokens / experiment wall time
~~~

后者包含 queue、prompt phases、request turnover 与 client/server overhead。

两者差距本身就是系统 Evidence。

### F13 — Tail latency 比平均值更能暴露 queue

slots 饱和时，前几位 request 可能很快，后排 request 等待很久。

因此至少保存 mean、p50、p95/max。

小样本课程实验中的 p95 只是描述性统计，不是假装生产 SLA。

## Stable server mental model

~~~text
client concurrency
      ↓
request queue
      ↓ admission
server slots
      ↓
prompt processing
      ↓
dynamic active decode set
      ↓
continuous batching
      ↓
shared model + hardware
      ↓
streamed output
~~~

旁边同时存在：

~~~text
active sequences × context
→ KV pressure
~~~

## Investigation order

1. exact runtime/model/config identity
2. server slot count
3. client concurrency
4. queue/deferred evidence
5. actual busy slots/decode
6. TTFT distribution
7. stream cadence / decode timing
8. aggregate tokens/s
9. KV/context/headroom
10. only then tune batching/slots

## Claims to avoid

- “8 clients = batch size 8。”
- “8 slots = 8× throughput。”
- “continuous batching 一定让每个用户更快。”
- “单用户 tg 30 t/s，所以 4 用户就是 120 t/s。”
- “aggregate throughput 更高，所以体验更好。”
- “TTFT 变差说明 GPU decode 变慢。”
- “stream chunk gap 就是精确 ITL。”
- “slots × ctx 就一定等于真实 KV allocation。”
