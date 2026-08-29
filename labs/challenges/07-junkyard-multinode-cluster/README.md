# Challenge 07 — 多机垃圾佬集群：先算网络，再谈“显存相加”

硬件等级：L0 主路径；L3 真机  
风险：medium（网络暴露）  
成本：L0 为 0；真机只使用已有机器

## Goal

理解：

~~~text
多机 capacity
!=
免费聚合 VRAM
!=
线性加速
~~~

先用 workload traffic 与网络 roof 判断什么值得分布。

## 1. 三种不同“多机”

### A. 独立请求分流

~~~text
client/router
→ server A
→ server B
~~~

模型各自完整驻留。

优点：
- 节点间不传每层 activation/KV；
- 容易隔离故障。

缺点：
- 单个超大模型仍必须在单节点/单节点组 fit。

### B. 模型/计算跨节点切分

每一步可能有网络通信。

要计算：

~~~text
bytes per synchronization
× synchronizations per token
÷ network effective bandwidth
~~~

### C. 分离 Prefill / Decode / KV 服务

更复杂，但说明“分布式”可以按 workload phase 切，不只是按 layer 切。

## 2. 先做 L0 network roof

假设每 token 必须跨节点传 X MiB，网络有效吞吐 Y GiB/s：

~~~text
network-limited tok/s <= Y / X
~~~

再加：
- RTT；
- serialization；
- copies；
- synchronization；
- load imbalance。

## 3. 异构垃圾佬问题

两台机器 GPU、memory、backend、PCIe 不同，“按显存比例切”只能是初始 heuristic。

最终看：
- per-stage time；
- transfer time；
- straggler；
- failure/retry。

## 4. llama.cpp RPC 只作为 current case study

当前 upstream RPC backend 可把远端 ggml device 暴露给主机，但上游明确标注它是 proof-of-concept、fragile/insecure。

因此课程真机路径：
- 只在可信、隔离、私有实验网络；
- 不把 RPC port 暴露公网；
- 不把它当生产安全架构；
- 运行前重新读当前 upstream README。

## 5. 先比较“多机”是否值得

至少与这些 baseline 比：
- 单机更小 quant；
- 单机降低 context/concurrency；
- 单机双 GPU；
- 两台独立 server 做 request-level load balancing。

分布式不是默认胜者。

## Retrieval Practice

1. 为什么 request-level scaling 不会帮单个过大的模型 fit？
2. layer split 的网络 bytes 为什么直接进入 TG roof？
3. RTT 小但 bandwidth 低与 bandwidth 高但 RTT 大，分别影响哪些通信模式？
4. 为什么当前 RPC POC 不应该暴露到不可信网络？

## 完成证据

提交 Network/Cluster Dossier：
- 节点配置；
- workload；
- partition strategy；
- bytes/sync；
- network roof；
- predicted bottleneck；
- security boundary；
- simpler alternative。

真机时再记录 actual link throughput 与 per-stage timing。

## Current Source

- llama.cpp RPC: https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md

当前命令/API 运行前重新确认。


## Expected outcome

先区分 request routing、model partition、prefill/decode/KV 分离三种“多机”，再用 network roof 与真实 workload 判断哪个方案有意义。

## Failure recovery

如果网络/软件栈证据不足，先停在 L0 roof；不要为了实验临时暴露不安全 RPC、关闭认证或跨不可信网络裸跑服务。

## What this does NOT prove

节点数量增加不等于单请求更快，也不等于总成本更低；跨节点模型切分尤其受网络与同步约束。

## No-hardware path

用 synthetic network bandwidth/latency 与模型 traffic 做 roof worksheet 即可完成核心推理。
