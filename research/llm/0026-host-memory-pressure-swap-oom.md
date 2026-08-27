# Research Note 0026 — Host Memory Pressure / Swap / OOM

日期：2026-08-27

## Research question

A local LLM machine shows:

```
MemFree = 1.5 GiB
```

Does that mean RAM is almost exhausted?

Not necessarily.

For a useful diagnosis, separate:

```
free RAM
available RAM
file-backed cache
anonymous/process memory
swap/compression
host OOM
GPU VRAM OOM
```

---

# Part I — Free != available

Linux `/proc/meminfo` defines:

```
MemFree
```

as currently unused physical pages.

It also defines:

```
MemAvailable
```

as an estimate of memory available for starting new applications without swapping.

Official:
- https://man7.org/linux/man-pages/man5/proc_meminfo.5.html

Therefore:

```
low MemFree
```

alone is weak evidence of memory pressure.

The kernel intentionally uses otherwise-idle RAM for useful caches.

---

# Part II — File cache can be reclaimable

Slice 43 established:

```
file reads / mmap
→ page cache
```

Clean file-backed pages can often be reclaimed and re-read from storage later.

So a machine may look like:

```
32 GiB RAM
2 GiB free
18 GiB page cache
```

without being close to OOM.

The exact reclaimable amount is an OS decision.

Do not compute Linux `MemAvailable` with a simple homemade formula.

---

# Part III — Anonymous/process memory is different

Anonymous memory commonly includes:
- heap;
- stacks;
- runtime allocations;
- non-file-backed buffers.

Unlike clean file cache, it cannot simply be discarded and reconstructed from a backing file.

Under pressure, depending on OS/policy, it may:
- be swapped;
- compressed;
- trigger reclaim elsewhere;
- fail allocation / lead toward OOM.

---

# Part IV — mmap model pages under pressure

A file-backed mmap can allow clean model pages to be reclaimed.

If those pages are needed again:

```
reclaim
→ later page fault
→ storage/page-cache refill
```

This can cause latency spikes even before a process dies.

Thus:

```
model fits in address space
```

does not mean:

```
all model pages remain resident forever
```

---

# Part V — mlock boundary

Locked pages are deliberately kept resident and are less reclaimable.

That may reduce refault/pageout behavior for the locked region but increases pressure on the rest of the machine.

Therefore:

```
mlock
```

is a memory-residency policy, not a free speed boost.

---

# Part VI — Swap used != active swapping

Linux `SwapTotal - SwapFree` tells you how much swap is occupied.

But pages can remain in swap even after pressure subsides.

Current pressure needs activity evidence.

Useful cumulative counters in `/proc/vmstat` include:

```
pswpin
pswpout
pgmajfault
```

Official:
- https://man7.org/linux/man-pages/man5/proc_vmstat.5.html

Because they are cumulative since boot, use:

```
delta over observation window
```

not the raw absolute value.

---

# Part VII — Major faults

A major page fault generally means the needed page was not immediately resident and required I/O.

A rising:

```
pgmajfault
```

during the same workload can support a paging/refault hypothesis.

But:
- not every major fault is the model;
- storage/file activity from other processes also contributes.

Per-process evidence is stronger where available.

---

# Part VIII — Host OOM

If memory reclaim cannot satisfy important allocations, Linux may invoke OOM handling depending on policy.

Official kernel docs:
- https://www.kernel.org/doc/html/v6.0/mm/oom.html
- https://cdn.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html

An OOM event is different from:
- high RAM utilization;
- swap activity;
- slow paging.

Do not call ordinary high utilization "OOM".

---

# Part IX — Process memory

On Linux, useful read-only process evidence includes:

```
/proc/PID/status
/proc/PID/smaps_rollup
```

Potential fields:
- VmRSS;
- VmSize;
- RssAnon;
- RssFile;
- RssShmem;
- VmSwap;
- Pss.

These help separate file-backed vs anonymous/process memory.

Availability/permissions vary.

---

# Part X — RSS != total system pressure

A process RSS is not:

```
all RAM caused by this process
```

because:
- shared pages exist;
- page cache can be shared;
- GPU allocations live in a separate device domain on discrete GPUs;
- kernel/driver allocations may not appear as process RSS.

Use RSS/PSS as one layer of evidence.

---

# Part XI — GPU VRAM OOM is a different domain

For a discrete NVIDIA/AMD GPU:

```
host RAM
```

and:

```
GPU VRAM
```

are distinct allocation pools.

Possible:

```
host MemAvailable healthy
GPU VRAM allocation fails
```

or:

```
VRAM has headroom
host process is killed/host allocation fails
```

Do not diagnose one from the other.

---

# Part XII — Apple unified memory boundary

Apple silicon uses a unified memory architecture.

The simple discrete model:

```
system RAM pool
+
separate VRAM pool
```

does not map directly.

For Apple:
- CPU/GPU share the unified physical-memory system;
- OS memory pressure/compression is central;
- application/runtime allocation reporting should be interpreted in that architecture.

This course keeps Apple as a special case rather than forcing NVIDIA terminology onto it.

---

# Part XIII — Synthetic reclaim model

The L0 experiment uses a **teaching proxy**, not Linux's real MemAvailable algorithm.

Example:

```
RAM = 32 GiB
anonymous = 10
file cache = 18
kernel/other = 2
free = 2
```

Assume, only for the toy:

```
80% of file cache reclaimable
```

Then a crude proxy:

```
available_proxy
=
free + 0.8 × file_cache
=
16.4 GiB
```

An 8 GiB new request can fit after reclaim in the toy despite only 2 GiB being literally free.

---

# Part XIV — Anonymous-heavy synthetic case

```
RAM = 32
anonymous = 25
file cache = 3
kernel/other = 2
free = 2
```

At the same synthetic 80% file-cache reclaim fraction:

```
available_proxy
=
2 + 2.4
=
4.4 GiB
```

An 8 GiB request has:

```
3.6 GiB shortfall
```

This is much more pressure-prone than the cache-heavy case.

Again, this is a teaching proxy, not the kernel's formula.

---

# Part XV — Symptoms of host pressure

Evidence-compatible pattern:

```
MemAvailable ↓
pswpout delta ↑
pgmajfault delta ↑
request latency ↑
```

This supports a host-memory pressure/paging hypothesis.

Stronger if:
- process VmSwap rises;
- RssFile/page cache changes;
- server logs show allocation failures.

---

# Part XVI — Low MemFree but healthy pattern

Possible pattern:

```
MemFree low
MemAvailable healthy/stable
Cached high/stable
pswpout delta ≈ 0
pgmajfault delta low
SLO healthy
```

Interpretation:

```
cache-heavy healthy system is plausible
```

Do not "fix" it by killing cache blindly.

---

# Part XVII — Swap can save availability but hurt latency

Swap can let the system survive memory pressure.

But if actively used for hot pages:

```
page-in/page-out
→ storage latency
→ stalls
```

For interactive LLM serving, this can damage:
- TTFT;
- ITL;
- startup/refault behavior.

Survival and latency are different objectives.

---

# Part XVIII — Compression

Some operating systems use memory compression.

Compressed pages consume:
- less physical RAM;
- CPU work to compress/decompress.

This is another reason a simple:

```
RSS + free
```

story can be incomplete across platforms.

---

# Part XIX — Real lab is observation-only

Experiment 83 does not intentionally allocate a giant stress buffer.

It samples existing state while the learner runs a normal controlled workload.

This avoids turning a memory lesson into:
- host instability;
- OOM-killer exercise;
- accidental desktop crash.

If the learner already has a reproducible pressure workload, it may be observed, but the course does not create one by default.

---

# Part XX — Real Linux timeline

Useful fields:

```
MemTotal
MemFree
MemAvailable
Cached
SReclaimable
Shmem
SwapTotal
SwapFree
```

and deltas of:

```
pswpin
pswpout
pgmajfault
pgfault
oom_kill
```

If a PID is supplied, add:
- VmRSS;
- RssAnon;
- RssFile;
- VmSwap;
- smaps_rollup PSS where allowed.

---

# Part XXI — Correlate with GPU

Also record GPU:
- VRAM used/total;
- utilization;
- errors/logs.

Then you can distinguish:

```
host pressure compatible
```

from:

```
GPU VRAM pressure compatible
```

rather than using one vague word "memory".

---

# Claims to avoid

- "low MemFree means OOM";
- "Cached memory is wasted";
- "Linux MemAvailable = MemFree + Cached";
- "SwapUsed > 0 means active thrashing now";
- "raw pswpout counter proves current swapping";
- "RSS equals all process memory cost";
- "host OOM and GPU VRAM OOM are the same";
- "mmap guarantees model pages stay resident";
- "mlock is always beneficial";
- "Apple unified memory should be analyzed exactly like discrete NVIDIA VRAM".
