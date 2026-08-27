# Evidence — Experiment 43: Storage / Model Loading / Page Cache

状态：stable storage/loading lesson complete; L0 stage model verified; real read-only page-cache/startup evidence path ready.

## Claim

> Model startup and steady inference are different performance domains. Storage/page-cache behavior can dominate startup while steady TG remains unchanged once required weights are resident in the execution memory hierarchy.

## Stable path

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

## Linux page-cache evidence

Linux kernel documentation states that normal reads and file-backed mmaps interact with the page cache.

This means repeated access may be served from RAM rather than backing storage if pages remain resident.

Sources:
- https://www.kernel.org/doc/html/v6.9/mm/page_cache.html
- https://www.kernel.org/doc/html/v5.17/admin-guide/mm/concepts.html
- https://man7.org/linux/man-pages/man2/mmap.2.html

## mmap boundary

```
mmap
!=
copy entire file into RAM before mmap returns
```

The mapping establishes a file-backed virtual-memory mapping. Pages may become resident as they are accessed according to runtime/OS behavior.

## Experiment 80 verification

Synthetic assumptions:

```
model = 20 GiB
host/backend overhead = 1 s
device upload = 20 GiB @ 12 GiB/s
steady TG = 50 tok/s
```

Verified:

### HDD-like source

```
read = 100.000000 s
upload = 1.666667 s
simple ready = 102.666667 s
TG = 50 tok/s
```

### SATA-like source

```
read = 40.000000 s
upload = 1.666667 s
simple ready = 42.666667 s
TG = 50 tok/s
```

### NVMe-like source

```
read = 6.666667 s
upload = 1.666667 s
simple ready = 9.333333 s
TG = 50 tok/s
```

### Page-cache-like source

```
read = 1.000000 s
upload = 1.666667 s
simple ready = 3.666667 s
TG = 50 tok/s
```

All values are synthetic.

Central result:

```
startup differs dramatically
while
steady TG is identical in this model
```

## First-run naming rule

The course refuses to assume:

```
run 1 = cold
run 2 = warm
```

without independent cache-residency evidence.

Experiment 81 labels:

```
pass 1 = initial-state-unknown
pass 2+ = after-same-file-read
```

The read probe itself changes page-cache state.

## Real probe verification

The bundled probe was self-checked on a temporary regular file.

Verified behavior:
- bounded byte count;
- regular-file requirement;
- no cache-drop call;
- pass labels remain explicit;
- `cache_drop_performed=false`.

Default read boundary:

```
512 MiB / pass
2 passes
```

unless the learner intentionally chooses another bounded size or `--full`.

## fincore boundary

Current util-linux `fincore` can report resident file pages on Linux.

Experiment 81 stores raw output if available.

It does not claim that fincore measures:
- SSD controller cache;
- GPU residency;
- device-upload bandwidth.

Unavailable/failed residency evidence remains UNKNOWN.

## No default global cache dropping

The lab does not use privileged global page-cache dropping.

Reason:
- affects the whole host;
- perturbs unrelated workloads;
- can make a daily machine less stable/representative.

Unknown cache state is preferable to manufacturing a destructive-looking benchmark setup.

## Measurement interference

```
full SHA256
sequential read benchmark
```

both read the file and can alter cache state.

Therefore they are not measurement-neutral preparatory steps.

## Current pinned llama.cpp dynamic snapshot

Pinned:

```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current docs use:

```
-lm / --load-mode
```

with dated details stored in:

```
intelligence/llm/llama-load-mode-2026-08-27.md
```

Old mmap/mlock/direct-I/O switches are currently deprecated in favor of load-mode.

The installed build's `--help` remains authoritative.

## Learner should reject

- second-pass buffered throughput equals SSD bandwidth;
- first measured run is automatically cold;
- mmap synchronously reads the whole model;
- page-cache speed equals disk speed;
- SSD bandwidth equals VRAM bandwidth;
- slow startup proves slow TG;
- hashing is cache-neutral;
- drop_caches is required for every useful benchmark;
- health-ready proves all relevant pages remain resident forever.
