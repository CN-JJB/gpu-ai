# Expected — Experiment 18

本实验没有统一“正确速度”。

正确的是 Evidence 结构：

1. 拓扑先于 benchmark。
2. P2P capability 与实际 peer bandwidth 分开记录。
3. 性能 scaling 用“单卡本来就能运行”的同一模型做 A/B。
4. 单卡装不下、双卡装得下，只证明 capacity aggregation 成功，不产生 speedup 数字。
5. PP 与 TG 分开比较。
6. 任何 `row` / `tensor` 的当前行为都绑定 exact llama.cpp build。
7. 如果双卡 TG 更慢，这也是有效结果，不应删掉或解释成“实验失败”。

可能出现的真实模式包括：

- layer split 解决容量，但 TG 接近单卡或略慢；
- tensor/row 在强互联上降低延迟，在弱 PCIe/P2P 上收益有限；
- PP scaling 好于 TG；
- 异构卡被慢卡/慢链路拖住；
- 两个独立 replica 的总吞吐优于单模型跨卡。

课程不预填任何真实硬件数值。