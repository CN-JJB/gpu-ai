# Experiment 73 — Real Local llama-server Restart / Readiness Probe

硬件等级：L1/L2。

## Safety

This lab:
- launches its own `llama-server` child;
- forces `127.0.0.1`;
- manages only that child PID;
- installs no system service;
- changes no boot configuration;
- rejects auth/TLS/tools/agent/network overrides.

Use a free local port.

## Goal

Measure twice:

```
spawn
→ first HTTP
→ /health 200
→ one-token smoke inference
→ idle terminate
```

Then verify:
- server binary SHA;
- model SHA before/after;
- readiness recovery;
- first smoke inference recovery.

## Run

Example:

```bash
python3 restart_probe.py \
  --server-bin /path/to/llama-server \
  --model /path/to/model.gguf \
  --port 18080 \
  --extra-arg=-ngl \
  --extra-arg=99
```

Confirm current server options with:
```
llama-server --help
```

## Output

```
restart-evidence/
  server-1.log
  server-2.log
  restart-result.json
```

## Health interpretation

Pinned current server:

```
503
→ Loading model

200
→ model successfully loaded / ready
```

The script records status transitions.

## Stop interpretation

The child is terminated only after its smoke request has completed.

This is **not** an in-flight drain test.

A process signal must not be described as an application-level graceful drain unless that behavior is independently verified.

## Cache interpretation

Treat restart as cold for process-local prompt/KV cache unless explicit restore evidence exists.

Do not compare first-after-restart latency with a warm cached request and call the difference "GPU regression".

## Complete

Fill:
`RESULT-TEMPLATE.md`.
