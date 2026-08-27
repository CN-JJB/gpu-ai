# Experiment 36 — Real Used GPU Acceptance Packet

硬件等级：L2（需要真实 GPU）

风险：默认脚本只读。主动显存/负载测试需要人工启动。

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