# Research Note 0006 — Speculative Decoding：Draft、Verification、Acceptance 与 Overhead

日期：2026-08-26

## Research question

为什么 autoregressive target model 原本：

~~~text
1 forward step → 1 new token
~~~

可以通过 speculative decoding 变成：

~~~text
cheap proposer drafts multiple tokens
→ target verifies them together
→ accept several tokens
→ fewer serial target steps
~~~

同时仍保持 target-model semantics/distribution？

需要回答：

- draft model / n-gram / MTP proposer 分别在做什么？
- target verification 为什么仍然是最终 authority？
- acceptance rate 为什么是核心指标之一？
- draft length 为什么不是越大越好？
- draft overhead / target verification / memory cost 如何决定是否加速？
- 为什么 low-batch memory-bound decode 更适合 speculation？
- speculative decoding 与 batching / prefix cache 是什么关系？

## Scope

Stable Lesson 教 proposal → verify → accept/correct → advance 的通用模型。

Current llama.cpp implementations/flags 进入：

intelligence/llm/speculative-decoding-2026-08-26.md

llama.cpp source pinned：

d7a2074112d27649303fa107eb8c94db1ee435f3

## Primary sources

### 1. Leviathan, Kalman, Matias — Fast Inference from Transformers via Speculative Decoding

https://arxiv.org/abs/2211.17192

Original paper establishes：

- autoregressive decoding requires serial model calls；
- a faster approximation model can speculate several tokens；
- target computation verifies speculation in parallel；
- algorithm can preserve outputs/distribution while reducing serial target steps；
- speedup depends on approximation quality and relative cost。

### 2. Chen et al. — Accelerating Large Language Model Decoding with Speculative Sampling

https://arxiv.org/abs/2302.01318

Original speculative-sampling paper establishes：

- draft continuation can be scored by target in parallel；
- modified rejection sampling preserves target distribution within hardware numerics；
- target model remains authority；
- parallel verification is useful because scoring a short continuation can have latency comparable to a single target-token call on underutilized hardware。

### 3. llama.cpp speculative decoding docs

https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md

Current upstream states：

- target verifies multiple draft tokens in a single batch；
- speedups occur when draft predictions are frequently correct；
- supports draft-model and draftless/history-based implementations；
- current statistics include generated draft tokens, accepted draft tokens and acceptance rate；
- current SPEED-Bench path is recommended for end-to-end throughput/latency/acceptance comparison。

### 4. llama.cpp SPEED-Bench

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/speed-bench/README.md

Current benchmark reports：

- avg prompt t/s；
- avg predicted/decode t/s；
- avg end-to-end latency；
- acceptance rate；
- baseline vs speculative decode_speedup / latency_speedup。

This reinforces that acceptance must be connected to end-to-end performance rather than treated as a score by itself.

### 5. vLLM Speculative Decoding

https://docs.vllm.ai/en/latest/features/speculative_decoding/

Current official docs characterize speculative decoding as：

- inter-token-latency optimization for medium-to-low QPS；
- particularly relevant to memory-bound workloads；
- lossless under the intended speculative framework/rejection sampler；
- subject to floating-point/batching numerical variation in practical implementations；
- supporting multiple proposer methods。

### 6. vLLM Speculators algorithms

https://docs.vllm.ai/projects/speculators/en/latest/user_guide/algorithms/

Current docs show proposer families including：

- EAGLE-style learned draft；
- block/parallel draft methods；
- MTP heads。

Stable teaching point：

the proposer does not have to be a standalone tiny language model.

### 7. TensorRT-LLM Speculative Decoding

https://nvidia.github.io/TensorRT-LLM/1.3.0rc20/features/speculative-decoding.html

Current docs state：

- lightweight mechanism proposes candidate tokens；
- target verifies them in one forward pass；
- matching/accepted tokens reduce serial forward passes；
- speedups are particularly observable at low batch sizes；
- draft/target mismatch such as tokenizer mismatch can drive acceptance very low and regress performance。

## Findings

### F1 — Speculation attacks serial target-model steps, not model math correctness

Baseline decode：

~~~text
target(x) → token 1
target(x,1) → token 2
target(x,1,2) → token 3
...
~~~

The dependency chain forces serial target calls.

Speculative decode inserts a cheap proposer：

~~~text
draft: d1 d2 d3 d4
target: score/verify d1..d4 together
~~~

If several draft tokens are acceptable, the target sequence can advance by multiple positions per expensive verification round.

### F2 — The draft is not trusted

A common misconception：

> 小模型替大模型生成几个 token，所以质量会下降。

Correct model：

~~~text
draft = proposal
target = verifier / authority
~~~

Correct speculative sampling includes acceptance/correction logic so output distribution follows target semantics.

For greedy decoding, a simple teaching analogy is：

- accept matching prefix；
- at first mismatch, use target token。

For stochastic sampling, naive “token equality” is insufficient; algorithms use rejection/correction sampling.

### F3 — Accepted prefix stops at the first rejected draft token in the simple chain model

Suppose draft proposes：

~~~text
A B C D
~~~

Target verifies and agrees：

~~~text
A B
~~~

but rejects C。

Then later D was conditioned on draft C, not the corrected target history, so that chain cannot simply keep D.

Teaching model：

~~~text
accept A,B
take corrected target token at mismatch
discard remaining draft suffix
restart speculation from corrected history
~~~

Tree/block methods can be more sophisticated, but the causal-history rule remains.

### F4 — Acceptance rate is important but not sufficient

Current llama.cpp can report：

~~~text
accepted draft tokens / generated draft tokens
~~~

High acceptance means more draft work survives verification.

But performance also depends on：

- draft cost；
- target verification cost；
- proposal length；
- target batch efficiency；
- memory placement；
- extra KV/model memory；
- request batch/concurrency。

Thus：

~~~text
high acceptance
!= guaranteed speedup
~~~

### F5 — Expected progress per verification grows with acceptance

A simple independent per-position model：

- each proposed token survives with probability p until first rejection；
- propose D tokens。

Expected accepted prefix：

~~~text
E[accepted]
= p + p² + ... + p^D
~~~

After verification/correction, a simplified round advances roughly：

~~~text
E[progress]
= 1 + p + p² + ... + p^D
~~~

The +1 represents the target/corrected token that advances the sequence even when the draft chain stops.

This is a teaching approximation, not the exact accounting of every implementation.

### F6 — Draft length has diminishing value when acceptance is low

If p is high：

~~~text
longer draft
→ many accepted tokens
→ target verification amortized across more progress
~~~

If p is low：

~~~text
longer draft
→ most later proposals never survive
→ draft overhead ↑
→ verification batch overhead ↑
→ little extra progress
~~~

Therefore “max speculative tokens” is a tuning parameter, not a universal maximum-performance knob.

### F7 — Speedup condition is economic

Teaching cost model：

~~~text
baseline time for progress
= target_serial_cost × tokens advanced
~~~

Speculative round：

~~~text
draft/proposer cost
+ target batched verification cost
+ acceptance/correction overhead
~~~

Speculation helps only when：

~~~text
cost per accepted progress
<
baseline serial target cost per token
~~~

### F8 — A smaller draft model introduces extra memory/state

Two-model speculation can require：

- draft model weights；
- draft KV cache；
- draft runtime buffers；
- possibly separate device placement。

This can reduce target-model memory headroom.

On marginal local GPUs：

~~~text
speculative speed idea
→ extra draft memory
→ target offload changes / OOM
→ overall regression
~~~

So memory configuration must be part of Evidence.

### F9 — Draftless proposer avoids model memory but has workload dependence

History/n-gram proposer：

~~~text
look for repeated token patterns
→ propose known continuation
~~~

Advantages：

- no second full draft model；
- low memory/compute overhead。

Weakness：

- acceptance depends heavily on repeated structure。

Good cases：
- code rewrite；
- repetitive reasoning/final-answer structure；
- summarization with copied spans。

Bad cases：
- novel unpredictable continuation。

### F10 — MTP/EAGLE-style proposers show that “draft model” is a broader category

Modern systems can propose using：

- small standalone model；
- target hidden states + learned draft head/model；
- multi-token-prediction heads；
- block/diffusion proposer；
- n-gram/history lookup。

Stable concept：

~~~text
proposal mechanism must be much cheaper than serial target decoding
while predicting target-compatible continuations
~~~

### F11 — Speculative decoding is often most useful when baseline decode underutilizes hardware

Original papers exploit the fact that：

~~~text
target score several positions in a batch
~~~

can cost much less than running the target serially once per token.

Current vLLM/TensorRT-LLM docs likewise emphasize low/medium QPS or low batch-size scenarios.

Why：

- single/few sequence decode is often memory-bound and underutilizes compute；
- batched verification increases useful parallel work。

### F12 — High server batching can reduce speculative headroom

Slice 08 continuous batching already increases active batch/useful work.

At high concurrency：

~~~text
baseline target already better utilized
→ verification batch is less “free”
→ proposer overhead can become less attractive
~~~

Therefore：

~~~text
single-user spec speedup
!= production high-concurrency speedup
~~~

Real benchmark must specify concurrency.

### F13 — Prefix cache and speculative decoding optimize different redundant work

Prefix cache：

~~~text
skip repeated prompt prefill
~~~

Speculative decode：

~~~text
reduce serial target decode rounds for new tokens
~~~

Continuous batching：

~~~text
combine active requests for throughput
~~~

They can compose, but must be benchmarked separately before stacking.

### F14 — Output equivalence needs careful wording

Theoretical speculative decoding/sampling algorithms are designed to preserve the target distribution.

Practical implementation may still show different exact token strings across runs because：

- stochastic sampling already varies；
- floating-point numerics；
- batch-size changes；
- nondeterministic kernels；
- backend sampling differences。

So correctness claim should be：

~~~text
distribution/lossless algorithmic guarantee under the intended verifier/sampler
~~~

not：

~~~text
byte-identical text in every runtime run
~~~

## Stable mental model

~~~text
history
  ↓
cheap proposer
  ↓
draft d1..dD
  ↓
target batched verification
  ↓
accepted prefix + corrected/target token
  ↓
advance several positions
  ↓
repeat
~~~

Performance side：

~~~text
acceptance × progress
vs
draft + verification + memory overhead
~~~

## Investigation order

1. baseline target-only decode
2. proposer type
3. draft length
4. generated draft tokens
5. accepted draft tokens / acceptance
6. target predicted t/s / E2E
7. memory/VRAM delta
8. concurrency
9. prompt/workload category
10. only then claim speedup

## Claims to avoid

- “Draft model 的答案会直接混进 target，所以质量一定下降。”
- “acceptance 90% 就一定 1.9× faster。”
- “draft 越长越快。”
- “speculative decoding 只需要更小的模型，不需要 target verify。”
- “speculative decode 主要优化 prefill。”
- “prefix cache 和 speculative decoding 是一回事。”
- “单用户 speedup 能直接乘到 8-user server。”
- “开启 spec 后文本必须逐字与 baseline 相同，否则算法不 lossless。”
