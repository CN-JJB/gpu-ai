# Foundation 03 — 数学、单位与估算：只学会用的

硬件等级：L0  
风险：safe  
成本：0

## 1. 这门课最常用的数学

主要是：
- 乘除；
- 比例；
- 百分比；
- powers of two；
- bytes / bits；
- 平均数/percentile 的基本含义；
- 少量指数与对数直觉（softmax/PPL）。

不要求先学线性代数证明。

## 2. bit 与 byte

~~~text
8 bit = 1 byte
~~~

例：

~~~text
7B parameters × 4 bit
≈ 28B bit
≈ 3.5 GB raw payload
~~~

但量化文件可能还有 scale/metadata/mixed tensors，所以真实 bytes 以 artifact 为准。

## 3. GB 与 GiB

~~~text
1 GB  = 10^9 bytes
1 GiB = 2^30 bytes
~~~

产品规格、工具输出可能使用不同口径。

比较前先统一单位。

## 4. 带宽

~~~text
bandwidth = bytes / second
~~~

如果每生成一个 token 近似要读 `W` bytes，粗略 bandwidth roof：

~~~text
tokens/s <= memory_bandwidth / W
~~~

只是上界模型，不是保证。

## 5. Arithmetic Intensity

~~~text
AI = FLOP / bytes moved
~~~

低 AI 更容易被 memory roof 限制；
高 AI 更容易接近 compute roof。

## 6. 百分比变化

Baseline 100，candidate 120：

~~~text
speedup = 120 / 100 = 1.2×
percent increase = (120-100)/100 = 20%
~~~

不要混：
- +20%
- 1.2×
- 快 20 tok/s

## 7. 平均值与 tail

一次请求很慢可以被平均值“稀释”。

Serving 后面常看：
- median/p50；
- p95；
- p99。

课程会说明具体 percentile 算法，不能假设所有工具实现完全一致。

## 8. PPL 的最小直觉

Cross-entropy 是平均负 log probability。

Perplexity：

~~~text
PPL = exp(cross_entropy)
~~~

你现在只要记住：
- 在**同 tokenizer / corpus / protocol**下，较低 PPL 通常表示模型给真实下一个 token 更高概率；
- PPL 不是所有任务质量的万能分数。

## 9. 矩阵 shape 比公式证明更重要

看到：

~~~text
[B, T, d]
~~~

先学会问：
- 每个维度是什么；
- 哪个维度在 prefill 很大；
- decode 时哪个变成 1；
- tensor 有多少 element；
- 每 element 几 bytes。

这已经足够解释大量本地推理瓶颈。

## 小练习

计算：
1. 8B 参数、4.5 bpw 的 raw weight bytes；
2. 24 GiB 转 bytes；
3. 600 GB/s 除以 5 GB/token 的理想 roof；
4. 50 tok/s → 60 tok/s 是多少倍、多少百分比。

## Retrieval Practice

1. 为什么 4-bit 模型文件不一定严格等于参数量×0.5 byte？
2. GB/GiB 混用会造成什么误差？
3. AI 高低分别更容易接近哪个 roof？
4. 1.25× 和 +25% 是什么关系？

## 完成证据

写一张单位表，后续所有预算都显式写单位，不只写裸数字。
