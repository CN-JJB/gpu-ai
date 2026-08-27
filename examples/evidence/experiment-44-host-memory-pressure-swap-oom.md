# Evidence — Experiment 44: Host Memory Pressure / Swap / OOM

状态：stable host-memory lesson complete; L0 reclaim model verified; read-only Linux memory timeline collector self-checked.

## Claim

> Low free RAM is not the same as low available RAM. Host memory pressure diagnosis must distinguish file-backed cache, anonymous/process memory, swap activity, host OOM and discrete GPU VRAM pressure.

## Linux memory semantics

Current Linux man-pages define:

```
MemFree
```

as currently free physical pages, while:

```
MemAvailable
```

estimates how much memory can be made available for starting new applications without swapping.

Official:
- https://man7.org/linux/man-pages/man5/proc_meminfo.5.html

Therefore:

```
low MemFree
```

alone is not sufficient evidence of memory pressure.

## Experiment 82 verification

Synthetic cache-heavy:

```
RAM = 32 GiB
anonymous = 10
file cache = 18
kernel/other = 2
free = 2

synthetic reclaimable cache = 14.4
available proxy = 16.4
new request = 8
→ FITS_AFTER_SYNTHETIC_CACHE_RECLAIM
```

Synthetic anonymous-heavy:

```
RAM = 32
anonymous = 25
file cache = 3
kernel/other = 2
free = 2

reclaimable cache = 2.4
available proxy = 4.4
request = 8
shortfall = 3.6
→ PRESSURE_BEYOND_SYNTHETIC_RECLAIM
```

Moderate-cache case also verifies:

```
free 4
available proxy 10
request 5
→ fits after synthetic reclaim
```

The course explicitly labels this:

```
available_proxy
!= Linux MemAvailable
```

It is a teaching model only.

## Swap/activity boundary

Linux `/proc/vmstat` exposes cumulative counters including:

```
pswpin
pswpout
pgmajfault
```

Official:
- https://man7.org/linux/man-pages/man5/proc_vmstat.5.html

The real lab uses:

```
delta(counter)
=
last - first
```

over the observation window.

Raw cumulative values are not interpreted as current activity.

## Real collector self-check

The bundled Linux collector was executed on a 1-second observation window with 0.5-second sampling.

Verified manifest:

```
platform = Linux
samples = 2
stress_allocation_performed = false
system_settings_changed = false
```

Observed self-check window:

```
Δpswpin = 0
Δpswpout = 0
Δpgmajfault = 0
Δoom_kill = 0
```

The result correctly returned:

```
NO_SIMPLE_PATTERN
```

rather than inventing pressure.

## Process evidence

When a PID is supplied, the collector attempts read-only:
- VmRSS;
- RssAnon;
- RssFile;
- RssShmem;
- VmSwap;
- PSS from smaps_rollup where permitted.

These remain partial memory-accounting views.

## Host vs GPU memory

For discrete NVIDIA/AMD:

```
host RAM
!=
GPU VRAM
```

The real packet optionally stores raw NVIDIA VRAM used/total evidence.

A GPU allocation OOM can occur while host MemAvailable is healthy.

A host OOM can occur while GPU VRAM still has headroom.

## Apple boundary

Apple silicon uses unified memory architecture.

The course does not invent a separate discrete VRAM pool for Apple.

Host/unified memory pressure must be interpreted using platform-appropriate evidence.

## No intentional OOM

Experiment 83:
- does not allocate a giant pressure buffer;
- does not change swap;
- does not clear page cache;
- does not change kernel VM settings;
- does not intentionally invoke the OOM killer.

## Learner should reject

- low MemFree means OOM;
- Cached memory is wasted;
- MemAvailable equals MemFree + Cached;
- SwapUsed > 0 proves active thrashing;
- raw pswpout count proves current paging;
- RSS is total system memory cost;
- host RAM OOM equals GPU VRAM OOM;
- mmap means pages stay resident forever;
- Apple unified memory is a discrete-VRAM system.
