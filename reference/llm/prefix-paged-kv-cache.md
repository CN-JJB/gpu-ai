# Prefix KV Cache / Paged KV / Cache Hit 速查

<figure>
  <img src="../../assets/diagrams/experiment-prefix-cache-lifecycle.svg" alt="Prefix KV Cache / Paged KV / Cache Hit 速查 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Prefix KV Cache / Paged KV / Cache Hit 速查 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## 四个不要混的概念

### 1. Ordinary KV cache

同一个 autoregressive request：

~~~text
past K/V
→ 后续 decode 不重新算过去全部 K/V
~~~

### 2. Prefix / Prompt KV cache

不同 request 共享前缀：

~~~text
old request prefix KV
→ new request reuse
→ skip shared-prefix prefill
~~~

### 3. Paged / Block KV

KV memory 被切成 blocks/pages：

~~~text
pool
→ allocate/reference/free/evict
~~~

这是 memory-management abstraction。

### 4. Unified KV

某 runtime 让多个 sequences 使用统一 KV buffer/manager。

它不是“PagedAttention”的通用同义词。

## Prefix cache 省什么？

~~~text
prompt = shared prefix + new suffix
~~~

hit 后：

~~~text
shared prefix → cached KV
new suffix    → compute
new output    → decode normally
~~~

所以主要收益：

- prompt processing ↓
- TTFT opportunity ↓
- repeated-prefix throughput ↑

不是：

- new-token decode steps 消失

## llama-server current timings

current response can expose：

~~~text
cache_n
prompt_n
prompt_ms
prompt_per_second
predicted_n
predicted_ms
predicted_per_second
~~~

最直接判断：

~~~text
warm cache_n ↑
warm prompt_n ↓
warm prompt_ms ↓
~~~

实际字段是动态接口，见 dated intelligence snapshot。

## Prefix match

只有共同 prefix 能 reuse。

~~~text
A B C D E
A B C X Y
~~~

理论共同部分：

~~~text
A B C
~~~

实际 boundary 还可能受：
- block size
- match granularity
- template/tokenization
- adapter/model state
- multimodal identity
- tenant salt

影响。

## Cache hit rate 不够

更重要：

~~~text
reused_tokens
saved_prompt_ms
TTFT change
cache memory cost
~~~

### Example

90% hit × 16 reused tokens
可能不如
40% hit × 4000 reused tokens

## Finite capacity

cache memory 有限：

~~~text
new active KV needs space
→ old reusable blocks may be evicted
~~~

所以：

~~~text
capacity
↔ hit opportunity
↔ active-request headroom
~~~

## LRU

current vLLM/TensorRT-LLM documentation describes LRU-like eviction。

稳定概念：

~~~text
finite cache needs eviction policy
~~~

不要把 LRU 写成所有 backend 永久标准。

## Paged KV 为什么有用

固定 blocks/pages 可帮助：

- dynamic allocation
- reduce fragmentation
- prefix sharing
- eviction
- offload

但 paged KV 本身不创造相同 prefix。

## Continuous batching vs Prefix cache

| 优化 | 主要阶段 | 核心问题 |
|---|---|---|
| continuous batching | active prompt/decode scheduling | 同时来的 requests 怎么一起跑 |
| prefix cache | repeated prefill | 以前算过的共同 prefix 能不能不重算 |

可以叠加。

## Cold / Warm / Concurrent

### Cold

prefix state 不在 cache。

### Warm sequential

相同 prefix 已经完成并可复用。

### Warm concurrent

多个相同 prefix request 同时来。

可能因为 cache 尚未 materialize / become reusable 而无法全部 hit。

所以 benchmark 要写清 workload arrival pattern。

## Security

共享 server：

~~~text
prefix cache
→ timing differences
→ possible cross-tenant inference risk
~~~

current vLLM supports cache salt/isolation。

稳定原则：

- 单租户可最大化 reuse；
- 多租户要定义 reuse domain；
- 不只追 hit rate。

## 最小决策流程

~~~text
long repeated prefix?
→ yes
cache can reuse exact tokenized prefix?
→ yes
enough cache capacity?
→ yes
measure cache_n/prompt_n/TTFT
→ verify decode timing is not falsely credited
~~~
