# Expected — Experiment 17

默认参数的近似输出：

```text
single GPU baseline: 10.000 ms/token
GPUs: 2
critical transfer: 64.000 MiB/token

   GiB/s    comm_ms   total_ms    speedup       eff
    8.00     7.8125    13.0125     0.7685    0.3842
   16.00     3.9062     9.1063     1.0981    0.5491
   32.00     1.9531     7.1531     1.3980    0.6990
   64.00     0.9766     6.1766     1.6190    0.8095
  128.00     0.4883     5.6883     1.7580    0.8790
```

## 应得出的结论

- 8 GiB/s 场景下，通信时间超过理想节省的计算时间，所以双卡反而慢。
- 带宽提高后 speedup 上升，但仍受同步和通信限制，不能达到理想 2×。
- 2 卡获得 1.4× speedup 时，scaling efficiency 约 70%。
- 模型越“计算便宜、通信不变”，interconnect 占比越高。

这些结果只验证公式与因果关系，不是硬件 benchmark。