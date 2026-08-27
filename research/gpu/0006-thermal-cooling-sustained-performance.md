# Research Note 0027 — Thermal / Cooling / Sustained Performance

日期：2026-08-27

## Research question

Why can a GPU look excellent in a short benchmark and then become slower after several minutes?

Because the hardware state evolves:

```
workload duration
→ power
→ temperature
→ cooling response
→ clock / power-management state
→ sustained performance
```

A short cold run and a thermally soaked run are not the same experiment.

---

# Part I — Temperature is a state, not a benchmark score

Temperature depends on:
- workload;
- board power;
- ambient temperature;
- heatsink/cooler;
- fan/pump behavior;
- case airflow;
- neighboring GPUs;
- dust/age/paste/pads;
- laptop/desktop form factor.

Therefore:

```
GPU model name
```

does not uniquely determine operating temperature.

---

# Part II — One universal "bad temperature" does not exist

Different products expose different:
- target temperatures;
- max operating temperatures;
- edge/core temperature;
- hotspot/junction temperature;
- memory temperature.

Do not teach:

```
80 C = throttling
```

for every GPU.

A high reported temperature can coexist with stable clocks/performance.

A lower reported temperature can still coexist with a power cap or another limiter.

---

# Part III — Sensor names are not interchangeable

Common concepts:

```
edge / GPU temperature
hotspot / junction
memory temperature
VRM/sensor temperatures
```

A hotspot can be materially higher than edge temperature.

Vendor/device support differs.

Always label which sensor you recorded.

---

# Part IV — Clock behavior

A GPU dynamically changes clocks based on:
- workload;
- voltage/frequency policy;
- power limits;
- temperature;
- utilization;
- device-specific boost logic.

So:

```
clock lower
```

does not by itself prove:

```
thermal throttling
```

Need reason/context evidence.

---

# Part V — NVIDIA clock-event reasons

Current NVIDIA management docs expose clock-event/throttle reasons including concepts such as:
- software power cap;
- software thermal slowdown;
- hardware thermal slowdown;
- hardware power brake;
- other state/clock reasons.

Official:
- https://docs.nvidia.com/deploy/nvidia-smi/index.html
- https://docs.nvidia.com/deploy/nvml-api/group__nvmlClocksEventReasons.html

Therefore:

```
clock drop
+ thermal event reason
+ temperature rise
+ performance drift
```

is much stronger thermal-throttling evidence than temperature alone.

These fields are dynamic/vendor-specific and must be rechecked on the installed driver/tool.

---

# Part VI — NVIDIA power measurement boundary

Current `nvidia-smi` documentation describes power readings on supported GPUs.

Depending on device/tool generation, readings can be current/average board power.

Experiment 85 records the exact tool output rather than assuming one universal sensor implementation.

Reuse Slice 42:

```
board power
!=
whole-system wall power
```

---

# Part VII — AMD telemetry

Current AMD SMI documentation exposes GPU monitoring APIs/CLI around:
- edge/hotspot/memory temperature;
- GPU activity;
- power;
- GFX/memory clocks;
- VRAM use.

Official:
- https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html
- https://rocm.docs.amd.com/projects/amdsmi/en/latest/doxygen/docBin/html/group__tagGPUMonitor.html

AMD metrics availability differs by device/APU/partition.

Store raw output when parsing support is uncertain.

---

# Part VIII — Thermal soak

A cooler has thermal mass.

At workload start:

```
heatsink / case / coolant
```

may still be relatively cool.

Over minutes:

```
stored heat rises
→ equilibrium approaches
```

This is thermal soak.

A 15-second benchmark may measure a transient boost state rather than sustainable long-duration performance.

---

# Part IX — Sustained performance drift

Define:

```
drift
=
(last-window throughput / first-window throughput - 1)
```

Example:

```
first TG = 55 tok/s
last TG = 42 tok/s
```

Then:

```
drift
≈
-23.6%
```

If this occurs with:
- temperature rising strongly;
- clocks falling strongly;

thermal/power-management effects become plausible.

---

# Part X — Hot but stable

Synthetic example:

```
temperature ~82–84 C
clock ~1800 MHz
TG ~50 tok/s
```

If performance and clocks remain stable:

```
temperature alone
```

does not prove throttling.

Whether that temperature is desirable for longevity/noise is a separate hardware-policy question.

---

# Part XI — Clock drift without large thermal rise

Another pattern:

```
temperature modest/stable
clock ↓
TG ↓
power near configured envelope
```

Possible hypotheses:
- power cap;
- voltage/frequency policy;
- workload state;
- system/driver policy;
- measurement differences.

Do not force a thermal explanation.

---

# Part XII — Ambient temperature matters

A 20 C room and a 32 C room are not the same cooling test.

Record:
- approximate ambient;
- case state;
- fan/cooling configuration.

For used-GPU comparisons, ambient differences can overwhelm small cooler differences.

---

# Part XIII — Case airflow

Open-bench performance can differ from closed-case performance.

A hot exhaust path can recirculate into:
- the same GPU;
- a second GPU;
- CPU/VRM.

Multi-GPU garbage-hardware builds are especially sensitive to slot spacing and recirculation.

---

# Part XIV — Fan speed and noise

More cooling can cost:
- fan RPM;
- acoustic noise;
- dust accumulation.

A useful system objective can be:

```
sustained tok/s
subject to
temperature + noise constraints
```

not simply minimum temperature.

---

# Part XV — Noise measurement boundary

Fan percentage is not:
- RPM;
- dBA;
- perceived loudness.

If noise matters, record:
- measurement device;
- distance;
- room/background;
- case position.

The default course does not require a sound meter.

---

# Part XVI — Short benchmark vs long workload

For buying decisions:

```
peak 30-second TG
```

can overstate:
- a blower card in a hot case;
- laptop sustained performance;
- densely packed multi-GPU performance.

Use a sustained test representative of your actual session duration.

---

# Part XVII — llama-bench repeated samples

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current `llama-bench` supports:
- `-r/--repetitions`;
- JSON/JSONL output;
- `samples_ts` and `samples_ns` arrays in JSON output.

A TG test:

```
-p 0
-n N
```

can therefore preserve per-repetition throughput rather than only the final average.

Current details are dynamic; recheck `llama-bench --help`.

---

# Part XVIII — Warmup policy must be recorded

`llama-bench` currently has an optional `--no-warmup`.

For sustained thermal work:
- default warmup may remove some early transient;
- no-warmup can preserve more cold-to-hot behavior.

Neither is universally correct.

Record it in the workload manifest.

---

# Part XIX — Synthetic thermal-drift case

Synthetic:

```
t: 0 → 240 s
temp: 55 → 86 C
clock: 1900 → 1450 MHz
TG: 55 → 42 tok/s
```

Ratios:

```
clock last/first ≈ 0.763
TG last/first ≈ 0.764
temperature +31 C
```

This is compatible with thermal/clock/performance drift.

It still does not prove the exact limiter without reason telemetry.

---

# Part XX — Stable hot synthetic case

Synthetic:

```
temp: 80 → 84 C
clock: 1800 → 1790 MHz
TG: 50 → 49.8 tok/s
```

TG drift:

```
-0.4%
```

No meaningful performance collapse.

Therefore:

```
higher temperature
!= automatic throttling
```

---

# Part XXI — Real evidence workflow

1. Freeze model/runtime/execution manifest.
2. Choose sustained TG token count/repetitions.
3. Record warmup choice.
4. Start read-only telemetry.
5. Run one llama-bench process with many repetitions.
6. Preserve JSONL `samples_ts`.
7. Compare first/last windows.
8. Correlate with power/temp/clocks.
9. Check vendor limiter/event reasons if available.
10. Repeat under one controlled cooling/airflow change only if needed.

---

# Part XXII — Safe default

The course default real lab:
- does not overclock;
- does not undervolt;
- does not change power limit;
- does not change fan curve;
- does not disassemble hardware.

It measures first.

Any hardware tuning/maintenance is a separate explicit risk-level experiment.

---

# Claims to avoid

- "80 C always means throttling";
- "clock drop always means thermal throttling";
- "short benchmark equals sustained performance";
- "hotter card is automatically slower";
- "fan percentage is noise";
- "open-bench result equals closed-case result";
- "power-cap slowdown is thermal slowdown";
- "one temperature sensor represents every GPU component";
- "sustained TG drift proves the exact physical root cause without limiter evidence".
