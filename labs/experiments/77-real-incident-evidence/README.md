# Experiment 77 — Real Read-Only Incident Evidence Packet

硬件等级：L1/L2/L3。

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
