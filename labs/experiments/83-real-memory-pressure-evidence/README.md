# Experiment 83 — Real Read-Only Memory Pressure Evidence

硬件等级：L1/L2。

<figure>
  <img src="../../../assets/diagrams/host-memory-pressure.svg" alt="真实 memory-pressure Evidence 要把 RSS/cache/swap/reclaim 与请求延迟时间线对齐，才能判断 host memory 是否在拖慢推理。">
  <figcaption>真实 memory-pressure Evidence 要把 RSS/cache/swap/reclaim 与请求延迟时间线对齐，才能判断 host memory 是否在拖慢推理。</figcaption>
</figure>

## Goal

Observe host-memory state while running a normal local LLM workload.

Default lab does **not** create artificial memory pressure.

## Linux

```bash
python3 collect_memory.py \
  --pid LLAMA_SERVER_PID \
  --duration 60 \
  --interval 1 \
  --out-dir memory-evidence
```

Without PID:

```bash
python3 collect_memory.py --duration 30
```

## Captured host fields

From `/proc/meminfo`:
- MemTotal;
- MemFree;
- MemAvailable;
- Cached;
- SReclaimable;
- Shmem;
- SwapTotal/SwapFree.

From `/proc/vmstat`:
- pswpin;
- pswpout;
- pgmajfault;
- pgfault;
- oom_kill where present;
- selected workingset refault counters where present.

Counters are cumulative.

Use:

```
delta over the observation window
```

## Optional process evidence

With `--pid`:
- VmRSS;
- RssAnon;
- RssFile;
- RssShmem;
- VmSwap;
- smaps_rollup PSS where permitted.

## Optional NVIDIA evidence

If `nvidia-smi` is installed, raw:
- VRAM used/total;
- GPU utilization;

is saved per sample.

This helps keep:

```
host RAM
```

separate from:

```
discrete GPU VRAM
```

## Summarize

```bash
python3 summarize_linux.py memory-evidence/timeline.csv
```

The summarizer may emit hints such as:
- `LOW_FREE_BUT_AVAILABLE`;
- `HOST_PRESSURE_COMPATIBLE`;
- `OOM_EVENT_OBSERVED`.

They are not root-cause proof.

## Windows / macOS

See:
`PLATFORM-NOTES.md`.

A read-only PowerShell snapshot is included for Windows.

## Safety

The lab:
- performs no giant allocation;
- changes no swap settings;
- changes no kernel VM settings;
- does not clear page cache;
- does not trigger OOM intentionally.

## Pair with workload evidence

Correlate with:
- Experiment 63 client TTFT/E2E;
- Experiment 77 server/GPU telemetry;
- server logs.

## Complete

Use:
`RESULT-TEMPLATE.md`.


## Why this experiment

真实内存问题最容易被“free 很少”“VRAM 很满”这类单点截图误导。本实验只读采样 host memory、swap/page-fault counters 和可选 GPU VRAM，并把它们放到同一时间线上。

## Hypothesis

如果真实 host pressure 正在影响服务，MemAvailable、swap delta、major-fault/refault 等信号应与 latency/throughput 时间线出现可解释关系；单独低 MemFree 不足以判定压力。

## Fixed variables

采样期间保持同一正常 LLM workload，不故意制造压力、不清 page cache、不改 swap/kernel 参数。A/B 时一次只改一个 workload 或配置变量。

## What to observe

1. MemFree 与 MemAvailable 的差异。
2. pswpin/pswpout、pgmajfault 等累计 counter 的窗口 delta。
3. process RSS/anon/file/swap 的构成。
4. host RAM 与 discrete GPU VRAM 是否被正确分开。
5. memory signal 与 TTFT/E2E/server logs 是否同时间变化。

## Troubleshooting

- counter 是累计值，必须看 delta。
- LOW_FREE_BUT_AVAILABLE 只是提示，不是根因。
- OOM 要区分 OS OOM、cgroup limit、host allocation 与 GPU OOM。
- macOS/Windows 不要套 Linux /proc 语义，使用 PLATFORM-NOTES。

## Evidence to save

保存 memory-evidence 目录、timeline.csv、summarizer 输出、关联 workload/incident 时间窗和 RESULT-TEMPLATE。

## What this proves

你能生成真实、只读的 host-memory pressure 时间序列并与 workload 关联。

## What this does NOT prove

它不会自动给出根因，也不证明某次 high memory usage 是 leak。

## No-hardware fallback

没有可运行 LLM 环境时先完成 Experiment 82 的 reclaim 模型。

## Transfer question

MemFree 很低但 MemAvailable 稳定、swap delta 为 0、延迟也稳定，你应该先宣布“内存不足”吗？
