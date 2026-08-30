# Experiment 77 — Real Read-Only Incident Evidence Packet

硬件等级：L1/L2/L3。

<figure>
  <img src="../../../assets/diagrams/incident-timeline.svg" alt="真实 incident Evidence 要保留事件前后状态、原始日志、变更点和恢复时间，防止事后只剩记忆中的因果故事。">
  <figcaption>真实 incident Evidence 要保留事件前后状态、原始日志、变更点和恢复时间，防止事后只剩记忆中的因果故事。</figcaption>
</figure>

## Goal

Collect a bounded timeline while you reproduce a problem on your own local server.

The collector does **not** generate workload.

Pair it with:
- Experiment 63 request trace;
- your normal local request;
- a controlled benchmark you own.

## Safety

The collector:
- only accepts localhost/loopback server URLs;
- caps duration at 300 seconds;
- requires interval >= 0.5 s;
- changes no power/clocks/driver/firewall;
- records only raw telemetry from already-installed tools.

## Run

Example:

```bash
python3 collect_incident.py \
  --base http://127.0.0.1:8080 \
  --duration 60 \
  --interval 1 \
  --out-dir incident-evidence
```

## Server evidence

Each sample saves raw `/metrics`.

`timeline.csv` extracts:
- prompt tokens/s;
- predicted tokens/s;
- requests processing;
- requests deferred;
- busy slots/decode;
- context high watermark.

If metrics are disabled, that fact is evidence.

## Vendor telemetry

If installed:

### NVIDIA
Raw `nvidia-smi` samples include:
- temperature;
- GPU utilization;
- memory used/total;
- power draw;
- SM/memory clocks.

### AMD
The collector tries:
```
amd-smi metric
```

or falls back to:
```
rocm-smi
```

and stores raw output rather than assuming one stable parser.

### Apple / Intel
This generic collector does not invent a dynamic telemetry CLI if the required tool is unavailable.

Record UNKNOWN and use the vendor-specific course tools/docs available on your machine.

## Add client trace

Run Experiment 63 over the same wall-clock window where practical.

Then correlate:
- TTFT/E2E;
- queue/deferred;
- server throughput;
- GPU telemetry.

## Logs

Copy/redact relevant server logs separately.

Do not include:
- API keys;
- Authorization headers;
- private prompts unnecessarily.

## Finish

Use:
`INCIDENT-TEMPLATE.md`.

Then hash the packet with Experiment 61 `build_packet.py`.


## Why this experiment

真实故障诊断最需要的是一条时间对齐的原始证据链，而不是问题发生后回忆“当时好像温度很高”。这个实验只读采样 server metrics 与可用 vendor telemetry，配合你自己的受控 workload。

## Hypothesis

如果某个性能问题可稳定复现，TTFT/E2E、queue/deferred、server throughput、GPU temperature/clock/power 等信号在同一窗口里应能形成可检查的相关模式，为下一步 discriminating test 提供依据。

## Fixed variables

先固定 model/runtime/workload 与采样 interval/duration。collector 本身不生成 workload，也不修改 clocks/power/network。

## What to observe

1. 问题发生的 exact elapsed time。
2. request trace 与 metrics timeline 是否重叠。
3. deferred/busy slots/context high watermark。
4. vendor telemetry 中 temperature/clock/power/VRAM 的同步变化。
5. metrics/tool 缺失是否被明确记录为 UNKNOWN。

## Troubleshooting

- 不要采集私人 prompt 或 Authorization header。
- Apple/Intel 若缺统一 telemetry 工具，保留 UNKNOWN，不编造数值。
- 采样太频繁可能有观测开销；A/B 保持同样 interval。
- correlation 只能生成 hypothesis，不能直接声明 root cause。

## Evidence to save

保存完整 incident-evidence 目录、客户端 trace、必要的已脱敏日志、INCIDENT-TEMPLATE，并用 Experiment 61 packet 工具做 hash 固化。

## What this proves

你能捕获一个真实、本地、只读且可复核的 incident 时间线。

## What this does NOT prove

collector 不自动诊断根因，也不证明观察到的相关性具有因果关系。

## No-hardware fallback

没有真实故障环境时先完成 Experiment 76。

## Transfer question

TTFT 恶化与温度上升同时发生，但 deferred queue 也暴涨。下一步为什么需要 discriminating test，而不能直接判 thermal throttling？
