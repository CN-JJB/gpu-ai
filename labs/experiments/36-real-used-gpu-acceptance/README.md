# Experiment 36 — Real Used GPU Acceptance Packet

硬件等级：L2（需要真实 GPU）

风险：默认脚本只读。主动显存/负载测试需要人工启动。

<figure>
  <img src="../../../assets/diagrams/used-gpu-acceptance-flow.svg" alt="二手 GPU 验收按身份/外观 → 枚举 → 保守测试 → 持续负载逐步升级，并在退货窗口内优先保存 Evidence。">
  <figcaption>二手 GPU 验收按身份/外观 → 枚举 → 保守测试 → 持续负载逐步升级，并在退货窗口内优先保存 Evidence。</figcaption>
</figure>

## 目标

生成一个可用于：

```
ACCEPT
or
DISPUTE / RETURN
```

的原始 Evidence packet。

## 0. 付款前

先复制：

```
seller-request-template.md
```

把问题发给卖家，并保存回复/图片/视频。

## 1. 开箱

不要先拆散热器。

保存：
- 包裹；
- 运单；
- 开箱视频；
- 序列号；
- PCB/接口/散热外观。

## 2. Baseline

```bash
./collect-baseline.sh > baseline.txt 2>&1
```

脚本尽量自动识别：
- NVIDIA；
- AMD；
- Intel。

它只采集：
- identity；
- memory；
- BIOS/driver；
- PCIe；
- vendor health/error fields；
- kernel error snippets；
- llama.cpp device list if installed。

## 3. Memory integrity

### Option A — supported NVIDIA DCGM

Current official DCGM diagnostics include a framebuffer-memory test.

Check support first.

On an appropriate supported system, current canonical form is:

```bash
dcgmi diag --run memory
```

Exact permissions/parameters depend on product and current DCGM configuration.

For consumer GeForce, do **not** assume higher diagnostic suites are supported just because DCGM installs.

### Option B — memtest_vulkan

Optional cross-vendor tool:
https://github.com/GpuZelenograd/memtest_vulkan

Current project documentation suggests a standard test around five minutes.

Record:
- exact release/commit；
- selected device；
- amount actually tested；
- errors；
- runtime。

Its result is additional evidence, not vendor certification.

## 4. Workload test

Use the course's existing llama-bench experiment with:
- exact model SHA256；
- PP；
- TG；
- repeat count；
- raw JSON。

Repeat while monitoring temperature/error state.

## 5. Monitoring

Do not use one universal thermal cutoff.

Use exact vendor/product limits.

Abort on:
- memory errors；
- artifacting；
- repeated driver reset；
- uncorrectable ECC；
- device lost；
- thermal shutdown；
- fan failure with rising temperature；
- unsafe smell/smoke/connector heating。

## 6. Final collection

Run:

```bash
./collect-baseline.sh > after-test.txt 2>&1
```

Compare before/after:
- error counters；
- device identity；
- PCIe state；
- temperature;
- ECC/RAS.

## 7. Fill result

`RESULT-TEMPLATE.md`

Keep the raw packet together.

## Why this experiment

二手卡到手后的第一目标不是“跑一个高分”，而是把卖家 claim、设备身份、显存、错误状态、代表性 workload 和 before/after telemetry 固化成可用于 ACCEPT 或退货争议的证据包。

## Hypothesis

健康候选应在 baseline、可用的 memory test、代表性 LLM workload 和 after-test 状态之间保持一致；任何 purchase-critical identity/VRAM mismatch、重复 device loss、uncorrectable error 等都应阻止 ACCEPT。

## Fixed variables

验收期间不要刷 BIOS、超频、改电压/功耗墙或拆散热器。先在收到时的原始状态下完成 evidence capture。

## What to observe

- seller claim 与实际 identity/VRAM；
- before/after error counters；
- memory test 的 exact tool/device/runtime；
- representative PP/TG 是否可重复；
- temperature/clock/error 是否随持续 workload 异常漂移；
- 任何 unsupported telemetry 是否被写成 UNKNOWN。

## Troubleshooting

- consumer GeForce 不要假设所有 DCGM suite 都支持。
- memory test 通过不等于整卡永远健康。
- 温度判断必须用 exact product guidance，不背通用阈值。
- 出现烟味、接口异常发热、烧蚀等安全迹象立即停止使用。

## Evidence to save

保留卖家材料、开箱记录、baseline.txt、memory-test 原始输出、benchmark 原始结果、after-test.txt 与 RESULT-TEMPLATE。

## What this proves

你能对真实二手 GPU 形成一次购买相关的验收证据链。

## What this does NOT prove

它不是永久健康保证，也不能证明所有显示输出/未来软件版本都正常。

## No-hardware fallback

未购买前完成 Experiment 35/86；真实验收留到有卡时。

## Transfer question

memory test 0 error，但 seller 声称 24GiB、runtime 只识别 12GiB。你能 ACCEPT 吗？
