# Experiment 14 — 真实 llama-server Cold / Warm Prefix Cache Probe

Hardware level: L1 CPU-only / L2 GPU accelerator  
Risk: safe  
Cost: 0（已有 GGUF 与机器）  
需要：Python 3 + llama-server

## 问题

对一个较长 prompt：

~~~text
第一次 cold
→ prefix KV 尚未复用

第二次 exact repeat
→ warm prefix cache
~~~

current llama-server 的：

- cache_n
- prompt_n
- prompt_ms
- predicted_ms
- TTFT proxy

会怎么变化？

## 0. 复用 Experiment 10/12 身份记录

必须保存：

- llama.cpp version / commit
- model SHA256
- CPU/GPU/backend
- offload
- context
- KV type
- server command

## 1. 启动一个单-slot dedicated server

先看：

~~~bash
llama-server --version
llama-server --help
~~~

本实验优先单 slot，减少“请求落到不同 slot/context”带来的变量。

current snapshot 可以类似：

~~~bash
export MODEL=/path/to/model.gguf
export LLAMA_SERVER=./build/bin/llama-server
export GPU_LAYERS=0

"$LLAMA_SERVER"   -m "$MODEL"   -c 8192   -np 1   -cb   --cache-prompt   --metrics   -ngl "$GPU_LAYERS"   --port 8080
~~~

有 CUDA/HIP/Metal 时使用你已经验证过的固定 offload。

### 不要把 8192 当标准答案

选择能安全容纳：

- generated chat template
- test prefix
- output tokens
- runtime headroom

的 context。

## 2. 为什么不使用 Experiment 12 的 --no-cache-prompt？

Experiment 12 为了隔离 batching，故意关闭 prompt cache。

Experiment 14 则反过来：

~~~text
prefix cache is the independent variable
~~~

## 3. 运行 probe

~~~bash
python prefix_probe.py   --url http://127.0.0.1:8080   --prefix-repeat 64   --max-tokens 16   --output prefix-cache.json
~~~

如果 endpoint 需要 model alias：

~~~bash
--model <alias>
~~~

## 4. 脚本做两组独立 pair

### Pair A — server timings

生成一个本次运行唯一 prompt A：

~~~text
cold A  → non-streaming
warm A  → exact repeat
near A' → early marker differs
~~~

记录：

- timings.cache_n
- timings.prompt_n
- timings.prompt_ms
- timings.prompt_per_second
- timings.predicted_n
- timings.predicted_ms
- client E2E latency

near-miss 用来观察：

~~~text
visible content mostly similar
but exact prefix diverges early
~~~

### Pair B — TTFT

再生成另一个唯一 prompt B：

~~~text
cold B → streaming
warm B → exact repeat streaming
~~~

记录：

~~~text
request start
→ first non-empty streamed delta
= TTFT proxy
~~~

以及 stream-gap proxy / E2E。

Pair B 使用独立 prompt key，避免 Pair A 已经把它预热。

## 5. 预期形状

warm exact repeat 通常应出现：

~~~text
cache_n ↑
prompt_n ↓
prompt_ms ↓
~~~

如果 prefix 足够长，TTFT 也通常有下降机会。

但是：

~~~text
predicted_n
predicted_ms
~~~

不应该因为“新 output tokens 不需要 decode”而消失。

## 6. near-miss 怎么读？

如果 marker 很靠前：

~~~text
cold A exact prompt
near A' differs early
~~~

可复用 prefix 应明显短于 exact warm repeat。

实际 cache_n 取决于：

- chat template
- tokenizer
- cache granularity
- llama.cpp current cache policy

不要预设必须为 0。

## 7. Optional control — cache disabled

停止 server，保持其他参数完全相同，仅改：

~~~text
--no-cache-prompt
~~~

再次运行 probe。

如果 current version behavior 支持对照，你应该看到 warm exact repeat 的 reuse evidence 明显减少/消失。

## 8. Optional capacity / eviction

current llama-server 有 cache RAM / checkpoint / reuse 相关参数。

不要直接把这些当前 flags 当永久 API。

如果要做 eviction：

1. 保存 current --help；
2. 明确设置一个小但安全的 cache capacity；
3. 依次 warm 多个不同长 prefix；
4. 再回访最早 prefix；
5. 看 cache_n 是否下降。

本实验主路径不强制这个操作，因为 backend cache policy 比 L0 模型复杂。

## 9. 结果表

至少填：

| case | cache_n | prompt_n | prompt_ms | predicted_n | predicted_ms | E2E / TTFT |
|---|---:|---:|---:|---:|---:|---:|
| cold A | | | | | | |
| warm A | | | | | | |
| near A' | | | | | | |
| cold B stream | n/a | n/a | n/a | n/a | n/a | TTFT |
| warm B stream | n/a | n/a | n/a | n/a | n/a | TTFT |

若 current streaming response 也返回 timings，可以额外记录，但 lab 不依赖它。

## 10. Evidence questions

1. warm A 的 cache_n 增加了多少？
2. prompt_n / prompt_ms 减少了多少？
3. predicted_ms 为什么不应该按相同倍率下降？
4. warm TTFT 是否下降？如果没有，下一步查 network/client overhead、prefix 长度、prompt cache policy。
5. near-miss 为什么可能仍有小量 cache_n？
6. 这次 cache 的容量成本在哪里？
7. 如果 server 是多租户，哪些 prefix cache reuse 不应该跨用户共享？
