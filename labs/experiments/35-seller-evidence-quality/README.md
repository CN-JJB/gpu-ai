# Experiment 35 — Seller Evidence Quality

硬件等级：L0

## 目标

卖家说得很多，不等于 Evidence 很强。

本实验训练：

```
seller response
→ C0/C1/C2/C3/C4
```

## Condition evidence scale

### C0
没有可用状态证据。

### C1
卖家口述/旧截图。

### C2
当前功能证据：
- 当前识别；
- 当前负载；
- 基本温度/画面。

### C3
强售前证据：
- exact serial/board；
- current identity；
- VRAM；
- sustained load；
- memory test；
- thermals/error state。

### C4
第三方或买家本人独立验证。

## 运行

```bash
python3 check_evidence.py
```

## 思考

“验货宝通过”是否必然是 C4 的完整 GPU 健康证明？

不是。

它可以提高某些交易属性的独立证据强度，但是否覆盖显存/持续 LLM/温度，仍取决于具体查验范围。

所以 C4 在本课程里指：

```
target acceptance properties
were independently verified
```

而不是只看一个平台标签。