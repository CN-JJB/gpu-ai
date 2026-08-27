# Experiment 16 — 真实 llama-server Baseline vs Speculative Decoding

Hardware level: L1 CPU-only / L2 accelerator  
Risk: safe  
Cost: 0（已有 GGUF 与 runtime）  
需要：current llama-server + Python 3

## 问题

固定：

- same target model
- same target artifact hash
- same prompt/workload
- same sampling
- same context
- same target offload
- same concurrency

只改变：

~~~text
speculative decoding OFF
vs
speculative decoding ON
~~~

真实：

- draft tokens
- accepted tokens
- acceptance rate
- target decode calls
- predicted t/s
- E2E latency

会怎么变？

## Path A — 最低门槛：n-gram proposer

不加载第二个 draft model。

适合先建立：

~~~text
proposal
→ verify
→ acceptance
→ speedup/slowdown
~~~

Evidence。

### Baseline server

先检查 current：

~~~bash
llama-server --version
llama-server --help
~~~

示例：

~~~bash
export MODEL=/path/to/target.gguf
export LLAMA_SERVER=./build/bin/llama-server
export GPU_LAYERS=0

"$LLAMA_SERVER"   -m "$MODEL"   -c 8192   -np 1   --no-cache-prompt   --metrics   -ngl "$GPU_LAYERS"   --spec-type none   --port 8080
~~~

### Baseline smoke probe

另一个 terminal：

~~~bash
python spec_probe.py   --prompt-file PROMPT-REPETITIVE.txt   --max-tokens 512   --output baseline-repetitive.json
~~~

然后换：

~~~bash
python spec_probe.py   --prompt-file PROMPT-NOVEL.txt   --max-tokens 512   --output baseline-novel.json
~~~

保存 server log 后停止 server。

### Speculative n-gram server

保持所有 target/server 参数相同，只加入 current speculative config。

本切片 snapshot 时，例如：

~~~bash
"$LLAMA_SERVER"   -m "$MODEL"   -c 8192   -np 1   --no-cache-prompt   --metrics   -ngl "$GPU_LAYERS"   --spec-type ngram-mod   --port 8080
~~~

current n-gram-mod draft-length/match knobs 以 docs/speculative.md 和 --help 为准。

再次运行相同两个 prompts：

~~~bash
python spec_probe.py   --prompt-file PROMPT-REPETITIVE.txt   --max-tokens 512   --output spec-repetitive.json

python spec_probe.py   --prompt-file PROMPT-NOVEL.txt   --max-tokens 512   --output spec-novel.json
~~~

### Compare

~~~bash
python compare_runs.py   baseline-repetitive.json   spec-repetitive.json

python compare_runs.py   baseline-novel.json   spec-novel.json
~~~

## 为什么关掉 prompt cache？

Slice 09 已经证明 Prefix Cache 会减少 prefill。

本实验要隔离：

~~~text
new-token speculative decode
~~~

所以 baseline/spec 都显式关闭 prompt cache。

## 为什么 concurrency=1？

current vLLM/TensorRT-LLM docs 都提示 speculation 的收益更偏 low-batch / low-to-medium QPS。

先在最有机会的低 batch 环境建立 Evidence。

之后再做：

~~~text
concurrency 1 → 2 → 4
~~~

作为高级 A/B。

## Path B — 可选 two-model draft

如果你有一个 **明确兼容 target** 的 draft artifact：

记录：

- target SHA256
- draft SHA256
- tokenizer compatibility
- target/draft quant
- target/draft device placement
- target/draft GPU layers
- memory before/after load

current llama.cpp snapshot 可使用类似：

~~~text
--spec-type draft-simple
--spec-draft-model <draft.gguf>
--spec-draft-n-max N
--n-gpu-layers-draft ...
--device-draft ...
~~~

不要从模型名猜兼容性；按 current upstream/support evidence 选择。

### Memory Evidence

two-model path 至少记录：

- target-only resident memory
- target+draft resident memory
- target offload 是否被迫改变
- OOM / auto-fit behavior

如果加载 draft 导致 target 从 GPU 移回 CPU：

~~~text
speculative algorithm improvement
~~~

和：

~~~text
worse model placement
~~~

会同时发生，不能只怪 acceptance。

## spec_probe.py 记录什么？

它读取 /metrics 前后差值：

~~~text
tokens_predicted_total
tokens_predicted_seconds_total
n_decode_total
spec_decode_num_draft_tokens_total
spec_decode_num_accepted_tokens_total
spec_decode_num_drafts_total
~~~

并记录：

- client E2E latency
- response timings
- wall predicted t/s
- server predicted t/s
- acceptance rate
- accepted tokens per verification round

如果 current metric names 改变，更新 dated intelligence/probe，不要伪造 0。

## PROMPT-REPETITIVE

它故意要求模型输出高度重复文本。

目标：

~~~text
history-based n-gram proposer
→ likely easier proposals
~~~

不是语言能力 benchmark。

## PROMPT-NOVEL

开放式解释任务。

目标：

~~~text
less predictable continuation
→ acceptance may differ
~~~

这个对照用于证明 proposer 的 workload dependence。

## 正式 benchmark：SPEED-Bench

当 smoke probe 跑通后，推荐直接使用 current upstream：

~~~text
tools/server/bench/speed-bench
~~~

它已经支持：

- baseline vs speculative
- raw JSON
- prompt/decode throughput
- latency
- accept_rate
- category splits
- compare script

做正式数据时保持：

- --bench
- --category
- --osl
- --limit
- --concurrency

完全一致。

## Expected shapes

### High acceptance + speedup

最理想。

### High acceptance + no speedup

检查：

- proposer overhead
- verification cost
- baseline already well utilized
- extra memory/offload changes

### Low acceptance + slowdown

完全可能。

这正是 L0 p=0.3 / long-draft case 的现实对应。

### Repetitive faster, novel not

说明 n-gram proposer workload-dependent。

## Evidence questions

1. repetitive vs novel acceptance 差多少？
2. acceptance 和 decode speedup 是否单调对应？
3. n_decode_total 是否因 speculation 减少？
4. accepted tokens per verification 是否足够高？
5. two-model path 增加多少 memory？
6. concurrency 增加后 spec speedup 是否下降？
7. 如果输出文本不逐字相同，你用什么标准判断“lossless algorithmic guarantee”而不是错误地比较随机采样结果？
