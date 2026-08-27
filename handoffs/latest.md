# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–43 are implemented.
Experiments 01–81 exist.

## Slice 43 core

Loading path:

```
GGUF bytes
→ storage/filesystem
→ page cache
→ mmap/read/page faults
→ host buffers
→ device upload
→ health ready
→ first inference
```

Synthetic 20 GiB model:

```
0.2 GiB/s source
→ 102.667 s simple ready

0.5 GiB/s
→ 42.667 s

3 GiB/s
→ 9.333 s

20 GiB/s page-cache-like
→ 3.667 s
```

All keep:

```
steady TG = 50 tok/s
```

to teach:

```
startup bottleneck
!= steady decode bottleneck
```

Real lab:
- no global drop_caches;
- default bounded 512 MiB reads;
- optional raw Linux fincore evidence;
- first run labeled UNKNOWN unless residency evidence exists;
- reading/hashing is recognized as cache-changing.

Current pinned llama.cpp load-mode dynamic details are isolated in:
`intelligence/llm/llama-load-mode-2026-08-27.md`.

## Active next slice — Host Memory Pressure / Swap / OOM

Teach:

```
physical RAM
=
anonymous/process memory
+
file-backed page cache
+
kernel/other
```

with reclaimable-cache nuance.

Separate:
- free vs available memory;
- page-cache reclaim;
- swap/compression;
- host OOM;
- GPU VRAM OOM;
- mmap model behavior under pressure.

Real lab must be read-only by default:
- /proc/meminfo / vmstat on Linux;
- process RSS/maps where available;
- server/GPU telemetry;
- no memory stress allocation as a required course step.
