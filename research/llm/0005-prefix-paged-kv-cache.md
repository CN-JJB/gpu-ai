# Research Note 0005 — Prefix/Prompt KV Cache、Paged Blocks、Hit/Miss 与 Eviction

日期：2026-08-26

## Research question

当多个本地 LLM 请求共享：

- 相同 system prompt；
- 同一份长文档/RAG context；
- 多轮对话历史；
- 相同工具说明/协议前缀；

为什么第二次请求可能显著减少 prompt processing？

需要分清：

~~~text
ordinary per-request KV cache
vs
cross-request prefix KV reuse
vs
paged/block KV memory management
vs
llama.cpp unified KV
~~~

并回答：

- cache hit 到底省了什么？
- 为什么主要影响 prefill/TTFT，而不是新 token decode？
- 为什么 cache 有容量与 eviction？
- 为什么“同样的可见文本”也可能 miss？
- 多租户共享 prefix cache 有什么安全边界？

## Scope

稳定 Lesson 教跨 backend 原理。

current interface snapshot 进入：

intelligence/llm/prefix-kv-cache-2026-08-26.md

llama.cpp upstream source pinned：

d7a2074112d27649303fa107eb8c94db1ee435f3

## Primary sources

### 1. llama.cpp server README

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Current server exposes：

- prompt caching enabled/disabled；
- cache reuse setting；
- RAM cache size；
- context checkpoints；
- unified KV；
- idle-slot cache；
- response timings。

Current OpenAI-compatible response timings example includes：

- cache_n：prompt tokens reused from cache；
- prompt_n：prompt tokens actually processed；
- prompt_ms；
- prompt_per_second；
- predicted_n / predicted_ms。

This gives direct Evidence that cached prompt tokens and newly computed prompt tokens can be separated.

### 2. vLLM — Automatic Prefix Caching

https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html

Official stable concept：

prefix caching stores/reuses KV for existing prompt prefixes so a new request sharing the prefix can skip redundant prompt computation.

vLLM explicitly states：

- strong use case：repeated long-document query；
- strong use case：multi-round conversation；
- it reduces query/prefill processing；
- it does not reduce the cost of generating new output tokens；
- if requests do not share a prefix, there is no reuse benefit.

### 3. vLLM — Prefix Caching design

https://docs.vllm.ai/en/latest/design/prefix_caching/

Current vLLM implementation uses a KV block pool and prefix hashes。

Stable lessons supported：

- cached KV is managed in blocks；
- only matching prefix regions can be reused；
- cached blocks occupy finite pool resources；
- reusable blocks can be evicted when blocks are needed；
- current design uses a free queue / LRU-style eviction path；
- cache key must include enough context to avoid incorrect sharing；
- current vLLM provides cache_salt for multi-tenant cache isolation.

### 4. TensorRT-LLM — KV cache reuse

https://nvidia.github.io/TensorRT-LLM/advanced/kv-cache-reuse.html

Official docs state：

- requests beginning with same prompt can share/reuse KV cache pages；
- this can significantly reduce first-token latency；
- useful for system prompts and multi-turn requests；
- reusable state is finite and can be evicted when memory is needed；
- current reuse policy uses LRU-like eviction；
- timing/order matters: some concurrently launched same-prefix requests may start before reusable state exists.

### 5. TensorRT-LLM — KV Cache System

https://nvidia.github.io/TensorRT-LLM/features/kvcache.html

Stable concepts：

- KV cache can be managed as a pool of blocks/pages；
- blocks are assigned to requests as needed；
- cache system supports reuse/offload/eviction and MHA/GQA/MQA differences。

## Findings

### F1 — Ordinary KV cache and prefix cache solve different redundancy

Ordinary autoregressive KV cache：

~~~text
same request
past tokens
→ do not recompute K/V every decode step
~~~

Cross-request prefix cache：

~~~text
new request
shares old prompt prefix
→ reuse already-computed prefix KV
→ skip part of prefill
~~~

所以：

~~~text
per-request KV
!= cross-request prefix reuse
~~~

### F2 — Prefix cache mainly removes prompt/prefill work

如果新 request prompt：

~~~text
[shared 4000-token prefix]
[new 100-token suffix]
~~~

并且 4000-token prefix 命中：

~~~text
cache_n ≈ 4000
prompt_n ≈ 100
~~~

conceptually。

被省掉的是：

~~~text
shared-prefix prefill compute
~~~

不是后续新生成 token 的 decode work。

### F3 — Prefix cache 对 TTFT 比对 long-output decode 更直接

TTFT contains prompt/prefill。

所以：

~~~text
reused prompt tokens ↑
→ prompt compute ↓
→ TTFT opportunity ↓
~~~

但如果 response 生成 2000 个新 tokens：

~~~text
those 2000 decode steps still happen
~~~

因此 vLLM official docs 明确说 prefix caching 不降低 generating-new-tokens 的成本。

### F4 — Cache hit 不等于“原始文本相同”

Runtime 通常基于 tokenized/model-context state 判断 prefix identity。

可能影响 reuse 的因素包括：

- tokenizer/chat template；
- token IDs；
- system/tool formatting；
- multimodal content identity；
- LoRA/adapters；
- model/runtime cache key；
- tenant isolation salt；
- prefix boundary/block granularity。

所以：

~~~text
visually similar prompt
!= guaranteed cache hit
~~~

### F5 — Prefix reuse 通常只能延伸到第一个 divergence

如果：

~~~text
A B C D E F
A B C X Y Z
~~~

第二个请求最多复用共同 prefix：

~~~text
A B C
~~~

从 divergence 开始，后续 state 依赖不同历史，不能继续当成同一 KV。

实际 reuse boundary 还受 block/match granularity 影响。

### F6 — Paged/block KV 解决 allocation/reuse/eviction，不等于 prefix caching 本身

Paged/block KV 的稳定心智模型：

~~~text
large monolithic per-request buffer
→ finite reusable blocks/pages
→ requests dynamically own/reference blocks
~~~

它有利于：

- 动态 allocation；
- 减少 fragmentation；
- prefix sharing；
- eviction；
- offload。

但：

~~~text
paged KV
!= cache hit automatically
~~~

没有相同 prefix 就没有 prefix reuse。

### F7 — llama.cpp unified KV 不等于 vLLM/TensorRT paged KV

Current llama.cpp：

~~~text
unified KV
= one KV buffer shared across sequences
~~~

vLLM/TensorRT-LLM：

~~~text
paged/block KV
= block pool/page allocation abstraction
~~~

两者都在解决 multi-sequence KV management，但不是同一个具体 data structure/algorithm。

课程必须避免把“unified”“paged”“prefix cached”三个词混成同义词。

### F8 — Cache capacity 是有限资源

cached prefix KV 继续占用 memory。

所以更多 cached prefixes：

~~~text
hit opportunity ↑
but memory occupancy ↑
~~~

当新 active request 需要空间时：

~~~text
cached reusable state may be evicted
~~~

TensorRT-LLM/vLLM current docs 都明确存在有限 pool 与 eviction。

### F9 — LRU 只是一类 current policy，不是永恒最优

当前 vLLM/TensorRT-LLM docs 都描述 LRU-like eviction behavior。

稳定 Lesson 只教：

~~~text
finite capacity
→ must choose what reusable state to retain
→ eviction policy matters
~~~

不把“所有 runtime 永远使用 LRU”写死。

### F10 — Cache hit rate 不是唯一指标

假设两个 cache：

**Cache A**
- 90% hits
- 每次只省 16 tokens

**Cache B**
- 40% hits
- 每次省 4000 tokens

Cache B 可能节省更多总 prefill work。

更有意义的量：

~~~text
reused prompt tokens
processed prompt tokens
prompt_ms
TTFT
capacity cost
~~~

而不只是 hit count。

### F11 — Concurrency 会影响 reuse timing

TensorRT-LLM docs 提醒：

多个同 prefix 请求若几乎同时启动，在第一个 request 的 KV 还没变成 reusable state 前，后续请求可能无法立即复用。

这连接上一 slice：

~~~text
high concurrency
→ more simultaneous first-time work
→ cache warm-up timing matters
~~~

所以 cache benchmark 要区分：

- cold；
- warm sequential；
- warm concurrent。

### F12 — Prefix caching and continuous batching solve different phases

Continuous batching：

~~~text
improve active multi-request execution / throughput
~~~

Prefix caching：

~~~text
skip redundant shared-prefix prefill
~~~

它们可以同时使用，但不能用一个替代另一个。

### F13 — Prefix cache 也是 security boundary

共享 cache 会产生：

- timing side channels；
- accidental cross-tenant reuse concerns；
- hash/key correctness requirements。

Current vLLM supports per-request cache_salt to isolate reuse domains.

稳定原则：

~~~text
multi-tenant shared cache
→ performance optimization + isolation policy
~~~

本地单用户机器风险较低，但长期 LAN/server 部署必须知道这条边界。

## Stable mental model

~~~text
request tokens
      ↓
find longest reusable prefix
      ↓
cache hit?
  yes        no
   ↓          ↓
reuse KV    compute prefill
             /
    new suffix prefill
          ↓
       decode new tokens
~~~

旁边：

~~~text
finite KV/cache capacity
→ retain / evict / offload
~~~

## Investigation order

1. exact prompt after chat template/tokenization
2. cold response cache_n / prompt_n
3. identical warm response
4. near-match / divergence response
5. prompt_ms / TTFT
6. predicted/decode timing
7. cache capacity
8. eviction behavior
9. concurrent warm-up behavior
10. tenant isolation if shared service

## Claims to avoid

- “Prefix Cache 会让 decode tok/s 直接变快。”
- “只要 prompt 看起来一样就一定 hit。”
- “Paged Attention = Prefix Cache。”
- “llama.cpp unified KV = vLLM PagedAttention。”
- “cache hit rate 越高一定收益越大。”
- “命中过一次就会永远保留。”
- “更多 prefix cache 永远没有 memory 成本。”
- “共享 cache 只有性能问题，没有隔离问题。”
