# Result — Experiment 83

## Identity

- OS:
- RAM:
- swap/pagefile:
- runtime/model:
- server PID:
- workload manifest:
- GPU/device:

## Host memory start

- MemFree / equivalent:
- MemAvailable / equivalent:
- Cached/file cache:
- Swap used:
- process RSS:
- RssAnon:
- RssFile:
- process swap:

## Host memory end

Same fields.

## Activity deltas

Linux:
- Δpswpin:
- Δpswpout:
- Δpgmajfault:
- Δoom_kill:

Other OS:
- equivalent pressure/activity evidence:
- exact tool/counter:

## GPU memory

- VRAM used/total:
- allocation failure?:
- device OOM log?:

## Client/server symptoms

- TTFT:
- ITL:
- E2E:
- errors:
- requests_deferred:

## Diagnosis

### Host pressure
- evidence for:
- evidence against:

### GPU VRAM pressure
- evidence for:
- evidence against:

### Paging/refault
- evidence for:
- evidence against:

## Architecture note

- discrete GPU:
- Apple unified memory:
- other:

## Conclusion

Use:
- evidence supports;
- evidence does not support;
- UNKNOWN.

Do not use "memory OOM" without saying which memory domain.
