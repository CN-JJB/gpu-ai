# Research Note 0025 — Storage / Model Loading / Page Cache

日期：2026-08-27

## Research question

Why can the same GGUF take much longer to start the first time than the second time?

And why does:

```
slow model startup
```

not automatically imply:

```
slow steady-state TG
```

after weights are resident?

The path is roughly:

```
model artifact
→ filesystem/storage
→ OS page cache
→ mmap/read
→ host-side metadata/buffers
→ device upload/allocation
→ model ready
→ first inference
```

Different stages dominate on different machines.

---

# Part I — File size is capacity, not load time

A model artifact has a byte size:

```
B_model
```

A crude full-read lower-order estimate is:

```
T_read
≈
B_model / effective_storage_bandwidth
```

But real startup also includes:
- metadata parsing;
- page faults/read-ahead;
- tensor validation/repacking;
- memory allocation;
- GPU/device upload;
- backend initialization.

Therefore:

```
file_size / advertised_SSD_GBps
```

is not a complete startup-time prediction.

---

# Part II — Sequential storage bandwidth

For a large model, storage reads are often mostly large/sequential.

A slow HDD can take much longer than an NVMe SSD to provide the same bytes.

But effective read rate depends on:
- device;
- filesystem;
- file fragmentation;
- encryption/compression layers;
- other I/O;
- queue depth/read-ahead;
- OS cache state.

Do not equate manufacturer peak bandwidth with model-load bandwidth.

---

# Part III — Linux page cache

Linux kernel documentation describes the page cache as the normal path through which file reads and file-backed mmaps interact with memory.

Normal reads, writes and mmaps go through page cache; direct I/O is an explicit bypass path.

A subsequent access can therefore be served from RAM rather than the backing disk if relevant pages remain resident.

Official:
- https://www.kernel.org/doc/html/v6.9/mm/page_cache.html
- https://www.kernel.org/doc/html/v5.17/admin-guide/mm/concepts.html

---

# Part IV — mmap intuition

`mmap()` creates a file-backed mapping in a process virtual address space.

The mapping itself does not mean:

```
all mapped bytes were synchronously read from disk
```

before `mmap()` returns.

Mapped pages can be faulted/read as they are accessed.

Linux `mmap(2)` also documents mechanisms such as `MAP_POPULATE` that can prefault/read-ahead pages, illustrating that fault timing is a distinct concern.

Official:
- https://man7.org/linux/man-pages/man2/mmap.2.html

For the course, stable mental model:

```
mmap
=
address-space mapping
+
pages become resident according to access/runtime/OS behavior
```

not:

```
mmap = copy entire file into RAM immediately
```

---

# Part V — Warm page cache

Suppose a 20 GiB model is read once.

If many model pages remain in RAM, a second process/start may read/fault those bytes from page cache.

Then the apparent source bandwidth can look like memory speed rather than disk speed.

Therefore:

> second run is faster

does not prove:
- storage became faster;
- runtime optimization occurred;
- GPU got faster.

Cache state changed.

---

# Part VI — First run is not automatically cold

A common benchmark mistake:

```
run #1 = cold
run #2 = warm
```

Run #1 may already be warm because:
- model was used earlier;
- backup/indexer scanned it;
- another process mapped/read it;
- OS has spare RAM and retained pages.

Correct wording without residency evidence:

```
first measured run
second run after same-file access
```

not:

```
cold
warm
```

---

# Part VII — File-specific cache evidence

On modern Linux, util-linux `fincore` can count pages of file contents resident in memory.

Current manual:
- reports resident file pages;
- uses `cachestat(2)` where available;
- can fall back to `mincore(2)`;
- warns scripts to request explicit output rather than rely on the changing default format.

Official:
- https://man7.org/linux/man-pages/man1/fincore.1.html

This is useful evidence, but:
- availability/version varies;
- permissions/kernel behavior can affect results;
- it reports page-cache residency, not SSD controller cache;
- residency alone does not prove which startup stage dominates.

---

# Part VIII — Why the course does not drop caches by default

Linux systems can deliberately drop page cache through privileged kernel controls.

That operation:
- affects the whole host;
- perturbs unrelated workloads;
- requires privilege;
- is easy to misuse on a learner's daily machine.

This course therefore does **not** make global cache dropping part of the default lab.

Instead:
- inspect cache state if possible;
- record first-run state as UNKNOWN when it is unknown;
- use repeated read/start as an explicitly warmer-state comparison.

---

# Part IX — Current llama.cpp loading behavior snapshot

Current pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

The current server help documents `--load-mode`.

Dynamic details belong in:

```
intelligence/llm/llama-load-mode-2026-08-27.md
```

Stable lesson:

```
runtime loading strategy
changes
when/how file pages and buffers are materialized
```

so exact flags must be rechecked.

---

# Part X — GPU upload is a separate stage

When model tensors are offloaded to a discrete GPU, startup may include host→device transfer and device allocation.

A rough serial teaching model:

```
T_ready
≈
T_storage/page_faults
+
T_host_overhead
+
T_device_upload
+
T_backend_init
```

Actual stages can overlap or behave lazily.

The formula is conceptual, not a profiler.

---

# Part XI — Upload bandwidth != VRAM bandwidth

If a model is copied to a discrete GPU, transfer may traverse:
- PCIe;
- platform/interconnect;
- driver staging.

Once resident, steady inference reads weights mostly from:
- VRAM / device memory;

not repeatedly from the SSD.

Therefore:

```
SSD bandwidth
!=
GPU VRAM bandwidth
```

This reconnects Slice 04 and Slice 11.

---

# Part XII — Startup vs steady TG

Synthetic thought experiment:

All four systems end with the same:
- model;
- GPU;
- execution config.

Storage differs.

Then:

```
cold-ish startup time
```

can differ dramatically while:

```
steady TG
```

is identical after weights are resident.

So:

> My HDD machine takes 100 seconds to start

does not imply:

> decode must be 10× slower forever.

---

# Part XIII — Synthetic 20 GiB example

Teaching model:

```
model = 20 GiB
host/backend overhead = 1 s
device upload = 20 GiB at 12 GiB/s
steady TG = 50 tok/s
```

Full-read source cases:

## HDD-like

```
0.2 GiB/s
read = 100 s
ready model ≈ 102.667 s
```

## SATA-SSD-like

```
0.5 GiB/s
read = 40 s
ready ≈ 42.667 s
```

## NVMe-like

```
3 GiB/s
read ≈ 6.667 s
ready ≈ 9.333 s
```

## Page-cache-like source

```
20 GiB/s
read = 1 s
ready ≈ 3.667 s
```

All:

```
steady TG = 50 tok/s
```

Synthetic only.

---

# Part XIV — Page cache competes for RAM

Cache residency is not guaranteed forever.

The kernel can reclaim clean file-backed cache under memory pressure.

Therefore:
- large RAM may make repeated starts look very fast;
- competing workloads can evict pages;
- a warm result is not a permanent property of the SSD.

---

# Part XV — mlock

Locking model pages in RAM is a different policy from mapping them.

It can reduce swapping/compression/reclaim for locked pages, but:
- consumes resident-memory budget;
- may require OS limits/privilege;
- can hurt overall system flexibility.

Do not teach:

```
mlock always faster
```

Measure the workload and host memory pressure.

---

# Part XVI — Direct I/O

Direct I/O aims to bypass normal page-cache behavior where supported.

It can be useful for specific loading designs/measurements.

It is not automatically faster.

Requirements/alignment and runtime support differ.

Do not use DirectIO merely to force a benchmark narrative.

---

# Part XVII — Hashing changes cache state

Computing a SHA256 of a multi-GiB model requires reading the model bytes.

That can populate page cache.

Therefore if the experiment question is startup from an initially unknown/cold state:

```
hash before timing
```

can alter the very state you intended to observe.

Capture an existing trusted artifact hash where possible, or be explicit that hashing warmed the file.

---

# Part XVIII — File read benchmark changes the state too

A sequential read benchmark:

```
read model prefix/full file
```

will itself populate/cache data through the normal buffered read path.

So Experiment 81 labels passes:

```
pass 1: initial state unknown
pass 2: after same-file read
```

It never calls pass 1 "cold" unless independent evidence supports that claim.

---

# Part XIX — Steady inference can still touch host/storage in some designs

The simple "SSD irrelevant after load" statement has boundaries.

Storage/host I/O can still matter when:
- model is larger than memory and pages continuously;
- CPU/mmap execution faults/reclaims weights;
- expert/tensor offload strategy uses host memory;
- model/router dynamically loads artifacts;
- adapters or multimodal assets are loaded on demand.

So the safe statement is:

```
when required weights are resident in the execution memory hierarchy,
steady TG need not be storage-bound
```

not a universal guarantee.

---

# Part XX — Real evidence workflow

1. Record exact model path and bytes.
2. Record current load mode/launch args.
3. If Linux `fincore` exists, snapshot file residency.
4. Run bounded sequential read probe if desired.
5. Snapshot residency again.
6. Run Experiment 73 startup/restart measurement.
7. Label initial cache state as known/unknown.
8. Compare readiness/first-inference, not only file-read MB/s.
9. Benchmark steady TG separately.
10. Keep storage and inference claims separate.

---

# Claims to avoid

- "second run proves SSD speed";
- "first run is automatically cold";
- "mmap reads the whole model immediately";
- "page-cache bandwidth is disk bandwidth";
- "SSD bandwidth equals VRAM bandwidth";
- "slow model load means slow steady TG";
- "hashing is measurement-neutral";
- "dropping global caches is required for a useful lab";
- "mlock always improves performance";
- "direct I/O is always faster";
- "all model weights are guaranteed resident forever after health 200".
