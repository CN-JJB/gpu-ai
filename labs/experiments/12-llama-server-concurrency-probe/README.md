# Experiment 12 — 真实 llama-server Concurrency Probe

Hardware level: L1 CPU-only / L2 discrete GPU or Apple accelerator  
Risk: safe  
Cost: 0（已有模型与机器）  
需要：Python 3 + current llama-server + GGUF

<figure>
  <img src="../../../assets/diagrams/experiment-continuous-batching-timeline.svg" alt="真实并发 probe 不是只数总 tok/s，而是观察 slot utilization、queue wait、TTFT、TG 与尾延迟如何一起变化。">
  <figcaption>真实并发 probe 不是只数总 tok/s，而是观察 slot utilization、queue wait、TTFT、TG 与尾延迟如何一起变化。</figcaption>
</figure>

## 问题

固定同一台 server：

- slots = 4
- same model
- same context
- same KV type
- same offload
- continuous batching enabled

然后固定总工作量为 8 requests，只改变 client concurrency：

~~~text
1 → 2 → 4 → 8
~~~

会发生什么？

我们同时测：

- client TTFT proxy
- E2E latency
- stream-chunk cadence proxy
- request throughput
- aggregate generated tokens / wall time
- server prompt/decode throughput
- peak requests_processing
- peak requests_deferred
- busy slots/decode evidence

## 0. 先锁身份

复用 Experiment 10 的：

- llama.cpp version / commit
- model SHA256
- CPU/GPU
- backend
- offload
- context
- KV type

不要重新用“模型名字”代替 artifact identity。

## 1. 启动 dedicated server

先看：

~~~bash
llama-server --version
llama-server --help
~~~

本实验写作时 current snapshot 可使用类似：

~~~bash
export MODEL=/path/to/model.gguf
export LLAMA_SERVER=./build/bin/llama-server
export GPU_LAYERS=0
~~~

CPU-only：

~~~bash
"$LLAMA_SERVER"   -m "$MODEL"   -c 4096   -np 4   -cb   --metrics   --no-cache-prompt   -ngl 0   --port 8080
~~~

有 CUDA/HIP/Metal 时，把 GPU layer/offload 设置为 Experiment 10 已验证的固定值。

### 为什么显式写 continuous batching？

current upstream 默认启用，但实验要把控制变量写进 Evidence，而不是依赖默认值。

### 为什么关闭 prompt cache？

这轮先隔离 concurrency/batching。

多个相同 prompt 若命中 prefix/prompt cache，会引入另一个优化变量。Prefix Cache 会在下一切片单独研究。

### 为什么 context 只给示例值？

4096 只是 smoke-test 例子。

你必须根据：
- model
- memory headroom
- intended prompt/output length

选择 context，并保存实际 /props 与 /slots。

不要假定：

~~~text
real KV allocation = slots × ctx
~~~

current llama-server 有 unified KV 等机制。

## 2. 健康检查

~~~bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8080/props > props.json
curl -s http://127.0.0.1:8080/slots > slots-before.json
curl -s http://127.0.0.1:8080/metrics > metrics-before.txt
~~~

如果 /metrics 不可用，确认 server 是用 --metrics 启动。

## 3. Warm-up

先发一条短请求，再开始正式 metrics baseline。

可以用本实验脚本：

~~~bash
python load_probe.py   --concurrency 1   --requests 1   --max-tokens 16
~~~

正式实验前建议重启 server，或者至少明确 warm-up 已完成后再采集 baseline。

## 4. Concurrency sweep

固定 total requests = 8：

~~~bash
for c in 1 2 4 8; do
  python load_probe.py     --url http://127.0.0.1:8080     --concurrency "$c"     --requests 8     --max-tokens 64     --output "concurrency-$c.json"
done
~~~

如果 OpenAI-compatible endpoint 需要 model 字段：

~~~bash
--model <server-model-alias>
~~~

## 5. 脚本测了什么？

### Client side

每个 request：

~~~text
request POST start
→ first non-empty streamed delta
= TTFT proxy
~~~

还记录：

- full response latency
- non-empty stream event count
- mean stream event gap

### 为什么叫 proxy？

SSE chunk != guaranteed one token。

所以脚本不会把 stream gap 命名成 exact ITL。

### Server side

脚本在 experiment 前后读取 /metrics。

计算：

~~~text
server prompt t/s
= Δ prompt tokens / Δ prompt seconds
~~~

~~~text
server predicted t/s
= Δ predicted tokens / Δ predicted seconds
~~~

~~~text
wall aggregate output t/s
= Δ predicted tokens / experiment wall time
~~~

并在运行期间轮询：

- requests_processing
- requests_deferred
- n_busy_slots_per_decode

## 6. 预期“形状”，不预期固定数字

### concurrency 1 → 2 → 4

如果硬件还有 batching headroom：

- aggregate output t/s 可能增加；
- busy slots/decode 增加；
- per-request stream cadence 可能变慢一些；
- TTFT 不一定恶化很多。

### concurrency 8 while slots=4

可能看到：

- peak requests_processing ≈ slot capacity；
- requests_deferred > 0；
- p95/max TTFT 明显上升；
- aggregate throughput 增幅开始变小。

这是 queue saturation 的典型形状。

但不要预设具体倍率。

## 7. 如果 concurrency 增加后 aggregate 完全没涨

检查：

1. GPU/CPU 已经 saturation？
2. server 实际 busy slots/decode 是否增加？
3. prompt 太短或 requests 没真正重叠？
4. model/backend 对 batch 的效率？
5. KV/cache/memory bandwidth 是否成为新瓶颈？
6. CPU-only 是否受 RAM bandwidth 限制？
7. thermal/power 是否变化？

## 8. Optional A/B — continuous batching on/off

重启 server，保持所有参数相同，仅改变：

~~~text
continuous batching ON
vs
continuous batching OFF
~~~

然后用混合长度/不同 max_tokens requests 测。

这比所有请求等长更容易暴露 dynamic admission 的价值。

current flag spelling 以 --help 为准。

## 9. Optional slot sweep

分别重启：

~~~text
slots = 1
slots = 2
slots = 4
slots = 8
~~~

客户端始终：

~~~text
concurrency = 8
requests = 8
~~~

每次都重新检查：
- memory headroom
- /slots
- context/KV configuration

不要为了“更多 slots”把机器推到 swap/OOM。

## 10. Result files

至少保存：

- props.json
- slots-before.json
- server startup log
- concurrency-1.json
- concurrency-2.json
- concurrency-4.json
- concurrency-8.json
- RESULT.md

## 11. Evidence questions

1. concurrency 超过 slots 后，requests_deferred 是否出现？
2. p95 TTFT 从哪里开始明显抬升？
3. aggregate output t/s 在哪里开始饱和？
4. server predicted t/s 与 wall aggregate t/s 为什么不同？
5. n_busy_slots_per_decode 是否真的随 concurrency 增加？
6. 如果 aggregate ↑ 但 stream-gap proxy 也 ↑，这是坏结果吗？取决于什么目标？
7. 增加 slots 前，为什么必须重新检查 KV/headroom？


## Hypothesis

固定 slots=4 时，client concurrency 从 1→4 可能提高 aggregate throughput；超过 slot capacity 后 deferred/queue 与 tail TTFT 更容易上升，而 throughput 增益趋于饱和。

## Fixed variables

same model/context/KV/offload/server/total 8 requests；主 sweep 只改 client concurrency。Prompt cache 关闭，continuous batching 显式固定。

## What to observe

- client TTFT proxy / E2E；
- stream-gap proxy；
- request throughput 与 wall aggregate output t/s；
- server prompt/predicted t/s；
- peak processing/deferred；
- busy slots/decode；
- concurrency 超 slots 后的 tail 变化。

## Troubleshooting

- SSE event gap 不是 exact ITL。
- server predicted t/s 与 wall aggregate t/s 系统边界不同。
- concurrency 没真正重叠时不能叫并发压力。
- 增 slots 前先重算 KV/headroom。
- optional batching on/off、slot sweep 都要单独重启并保持其他条件一致。

## Evidence to save

保存 server startup log、props/slots、四组 concurrency JSON、metrics 与 RESULT。

## What this proves

你能在真实 server 上观察 concurrency、slot saturation、queue 与用户 latency 的 tradeoff。

## What this does NOT prove

它不自动给出最佳 slots，也不代表所有 arrival/output-length 分布。

## No-hardware fallback

完成 Experiment 11。

## Transfer question

concurrency=8 时 aggregate t/s 只比 4 高一点，但 p95 TTFT 翻倍。这是不是“更快”？答案取决于什么 SLO？
