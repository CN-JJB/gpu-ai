# Non-Linux Notes — Experiment 83

## Windows

Use the bundled read-only PowerShell snapshot:

```powershell
./collect-memory.ps1 -TargetPid 1234
```

It records:
- total/free physical memory;
- virtual/commit-related OS totals exposed through CIM;
- page-file usage;
- optional process working set/private/virtual size.

Do not translate these fields 1:1 into Linux `MemAvailable` semantics.

## macOS / Apple silicon

Useful read-only local commands include:

```
vm_stat
sysctl -n hw.memsize
```

macOS memory-pressure/compression concepts differ from Linux and from discrete-GPU VRAM accounting.

On Apple silicon:

```
CPU + GPU
share unified memory architecture
```

so do not add a fictional separate VRAM pool.

Record:
- Activity Monitor / memory pressure evidence;
- process memory;
- runtime-reported model allocations;
- workload latency.

The course does not prescribe purge/cache-clearing or synthetic pressure as a default step.
