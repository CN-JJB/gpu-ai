# Experiment 72 — Lifecycle / Readiness State Model

硬件等级：L0

## Goal

Show that startup/recovery has multiple states.

Synthetic trace:

```
spawn
→ first HTTP
→ health-ready
→ first inference complete
→ later warm request
```

## Run

```bash
python3 analyze.py trace-synthetic.json
```

## Key result

Cold start:

```
first HTTP: 400 ms
ready: 5000 ms
first inference complete: 5800 ms
warm request: 150 ms
```

Restart:

```
first HTTP: 450 ms
ready: 5100 ms
first inference complete: 6300 ms
warm request: 160 ms
```

All numbers are synthetic.

## Lesson

```
listener
!= readiness
!= first usable inference
!= warm steady state
```
