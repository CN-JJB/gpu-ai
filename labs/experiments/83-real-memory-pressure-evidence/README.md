# Experiment 83 — Real Read-Only Memory Pressure Evidence

硬件等级：L1/L2。

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
