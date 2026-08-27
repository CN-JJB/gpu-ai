# Experiment 85 — Real Sustained TG / Thermal Evidence

硬件等级：L2。

## Goal

Measure:

```
repeated TG samples
+
temperature
+
clocks
+
power
```

over a sustained local workload.

Default lab changes no clock/power/fan setting.

## 1. Freeze workload

Use one exact:
- llama-bench binary;
- model;
- device/offload config;
- TG token count;
- repetition count;
- warmup policy.

## 2. Start telemetry

In terminal A, reuse Experiment 77:

```bash
python3 ../77-real-incident-evidence/collect_incident.py \
  --base http://127.0.0.1:8080 \
  --duration 180 \
  --interval 1 \
  --out-dir thermal-telemetry
```

For pure llama-bench without a server, Experiment 77's server-metrics fetches may fail; vendor telemetry is still useful. Alternatively use your existing read-only vendor monitor.

Make the telemetry window longer than the benchmark.

## 3. Run sustained llama-bench

Terminal B:

```bash
python3 run_sustained_tg.py \
  --bench-bin /path/to/llama-bench \
  --model /path/to/model.gguf \
  --n-gen 512 \
  --repetitions 20 \
  --extra-arg=-ngl \
  --extra-arg=all
```

Current pinned llama-bench supports:
- `-r` repetitions;
- JSONL;
- `samples_ts`;
- `samples_ns`.

Confirm installed:

```
llama-bench --help
```

## 4. Warmup policy

Default wrapper keeps llama-bench default warmup.

To preserve more initial transient:

```bash
--no-warmup
```

Record the choice.

Do not compare runs with different warmup policy as if identical.

## 5. Analyze repetitions

```bash
python3 analyze_sustained.py sustained-tg/manifest.json
```

Reports:
- first quartile TG;
- last quartile TG;
- drift;
- min/max;
- approximate cumulative sample timeline.

## 6. Correlate

Use benchmark:
- start/end wall time;

with telemetry:
- temperature;
- power;
- SM/GFX clock;
- utilization;
- raw vendor output.

Strong thermal hypothesis needs more than a hot temperature.

Look for:

```
temperature rise
+
clock decline
+
TG decline
+
thermal limiter/event evidence
```

where supported.

## 7. NVIDIA

Experiment 77 raw `nvidia-smi` samples already capture:
- temperature;
- utilization;
- board power;
- SM/memory clocks.

For limiter reasons, capture current read-only:

```
nvidia-smi -q
```

before/after or during diagnosis and preserve raw output.

Do not hard-code field parsing across all drivers.

## 8. AMD

Use current AMD SMI monitoring/raw output.

Current docs expose:
- power;
- temperature;
- GFX/memory clocks;
- activity;
- VRAM.

Store raw output if field support differs.

## 9. Ambient/case

Record:
- approximate ambient;
- side panel/open bench;
- slot spacing;
- fan policy;
- neighboring GPUs.

Without this, cooler comparisons are weak.

## 10. Default safety

Do not change:
- overclock;
- voltage;
- power limit;
- fan curve;

as part of this baseline experiment.

## Complete

Use:
`RESULT-TEMPLATE.md`.
