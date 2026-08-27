# Expected result

Verified with Python 3.

~~~text
Synthetic prefix-cache model; capacity is whole-prefix entries, not real KV blocks.
requests=A,B,A,C,A,B, prefix=1024, suffix=64, decode/request=128

capacity   hits   hit rate   evict  prompt proc     reused      saved   decode
------------------------------------------------------------------------------------
       0      0       0.0%       0         6528          0          0      768
       1      0       0.0%       5         6528          0          0      768
       2      2      33.3%       2         4480       2048       2048      768
       3      3      50.0%       0         3456       3072       3072      768

capacity=2 trace
  req 1: prefix=A MISS evict=- cache=[A]
  req 2: prefix=B MISS evict=- cache=[A,B]
  req 3: prefix=A  HIT evict=- cache=[B,A]
  req 4: prefix=C MISS evict=B cache=[A,C]
  req 5: prefix=A  HIT evict=- cache=[C,A]
  req 6: prefix=B MISS evict=C cache=[A,B]
~~~

## Key observations

### Cache enabled can still mean zero hit

capacity=1：

~~~text
A gets replaced by B
B gets replaced by A
A gets replaced by C
...
~~~

working set > capacity。

### Hit saves prefix work

每次 hit：

~~~text
1024 prefix tokens reused
64 suffix tokens still processed
~~~

capacity=2 有 2 hits：

~~~text
2 × 1024 = 2048 saved prompt tokens
~~~

### Decode does not change

所有配置：

~~~text
decode total = 768
~~~

这不是 bug。

它正是 prefix cache 只减少 repeated prefill 的设计边界。

## Boundary

真实 runtime：

- cache unit is not whole logical prefix；
- blocks/pages may have fixed granularity；
- partial hits exist；
- active requests reference blocks；
- cache key includes more state；
- eviction/offload policies differ；
- memory cost depends on model/KV dtype。

本实验只训练 finite-capacity reuse mental model。
