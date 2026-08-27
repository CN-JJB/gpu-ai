# Expected result

Verified with Python 3.

~~~text
Abstract server model; units are synthetic and do not represent llama.cpp or any real GPU.

Part A — 8 equal requests, 32 output tokens each
 slots  active step   makespan  agg tok/u  avg first  max first
--------------------------------------------------------------------
     1         1.00     256.00      1.000     113.00     225.00
     2         1.22     156.16      1.639      59.78     118.34
     4         1.66     106.24      2.410      28.22      54.78
     8         2.54      81.28      3.150       2.54       2.54
    16         2.54      81.28      3.150       2.54       2.54

Part B — mixed lengths, slots=2
lengths: 8, 32, 8, 32, 8, 32
    strategy   makespan  agg tok/u  avg first  max first
----------------------------------------------------------
      static     101.28      1.185      34.98      68.74
  continuous      82.56      1.453      20.74      50.02
~~~

## Part A interpretation

slots 增加后：

### Queue wait decreases

8 requests 同时到达，slots 越多，越少 request 需要等上一批完全结束。

所以 first-token-wait proxy 从：

~~~text
113.00
→ 59.78
→ 28.22
→ 2.54
~~~

下降。

### Active step gets slower

抽象模型故意设置：

~~~text
batch=1 → 1.00 time-unit
batch=2 → 1.22
batch=4 → 1.66
batch=8 → 2.54
~~~

所以更多 batch 并不是每个 user 更快。

### Aggregate throughput increases sublinearly

~~~text
1.000
→ 1.639
→ 2.410
→ 3.150
~~~

不是 1×→2×→4×→8×。

### slots=16 has no extra benefit

只有 8 requests，因此 active batch 不可能超过 8。

## Part B interpretation

static groups：

短请求完成以后，下一 queued request 仍不能补位。

continuous admission：

短请求完成就补入新 request。

因此：

~~~text
makespan
101.28 → 82.56

aggregate
1.185 → 1.453
~~~

这个 improvement 来自 scheduling/admission，不是硬件峰值算力改变。

## Boundary

不要把这些 synthetic numbers 和真实 llama-server 对照成倍率。

真实 server 还有：

- prompt processing
- model/KV/cache traffic
- kernels
- CPU/GPU scheduling
- sampling
- request arrival distribution
- output-length distribution
- network/HTTP
- runtime cache policy
