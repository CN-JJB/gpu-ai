# Expected — Experiment 27

默认近似输出：

```text
SYNTHETIC ONLY — no real Apple SKU claim

=== capacity ===
installed unified memory : 32.00 GiB
system/apps reserve      : 6.00 GiB
safety headroom          : 3.00 GiB
safe workload budget     : 23.00 GiB
weights                  : 18.00 GiB
KV                       : 2.00 GiB
workspace/runtime        : 1.00 GiB
runtime footprint        : 21.00 GiB
unified-memory fit       : YES
margin                   : 2.00 GiB

comparison dGPU VRAM     : 16.00 GiB
full-GPU-resident fit    : NO

=== decode bandwidth roof ===
total bandwidth          : 200.00 GiB/s
other traffic demand     : 40.00 GiB/s
model bandwidth budget   : 160.00 GiB/s
full-bandwidth TG roof   : 11.111 token/s
contended TG roof        : 8.889 token/s
```

## 应得出的结论

### Capacity
32 GiB installed unified memory 不等于 32 GiB safe model budget。

默认 reserve/headroom 后只有：

```
23 GiB
```

### Unified vs dGPU
同一 21 GiB runtime footprint：
- synthetic unified machine：可放；
- 16 GiB VRAM dGPU：不能 full-GPU-resident。

这证明的是 memory-pool/capacity 区别，不是性能结论。

### Bandwidth
即使容量够：
- 200 GiB/s full roof → 11.111 tok/s；
- 40 GiB/s 其他流量后 → 8.889 tok/s。

因此：
```
fit
!= fast
```

所有数字均为 synthetic teaching values。
