# Experiment 89 — Real PSU / Power-Delivery Dossier

硬件等级：L2/L3（整机外部检查；可选消费级插座功率计）。

<figure>
  <img src="../../../assets/diagrams/psu-power-delivery-path.svg" alt="真实 PSU/platform dossier 要记录额定能力、接口/线材拓扑、GPU/主板要求与安全余量，而不是只写一个 W 数字。">
  <figcaption>真实 PSU/platform dossier 要记录额定能力、接口/线材拓扑、GPU/主板要求与安全余量，而不是只写一个 W 数字。</figcaption>
</figure>

## Safety boundary

This lab does **not**:
- open a PSU enclosure;
- expose/probe mains wiring;
- bypass OCP/OVP/OTP/SCP;
- intentionally overload the PSU or connector;
- modify GPU/PSU power limits;
- create improvised high-voltage measurement fixtures.

If a connector/cable shows melting, charring, arcing evidence or severe damage:

```text
STOP USE
```

and follow manufacturer/qualified repair guidance.

## 1. Power off before physical cable inventory

Shut the system down and disconnect AC power before externally inspecting GPU power connections.

Do not open the PSU chassis.

## 2. Record exact PSU identity

Fill:

```text
PSU-LABEL-TEMPLATE.md
```

Record from the external label/manual:
- exact brand/model;
- rated output;
- revision if identifiable;
- manufacturer manual;
- modular cable compatibility documentation.

Do not settle for:

```text
"850W Gold"
```

as an identity.

## 3. Build cable map

Copy/fill:

```text
CABLE-MAP.csv
```

For every GPU auxiliary connection record:

```text
PSU port
→ cable part/type
→ branch/pigtail
→ GPU connector
→ compatibility source
```

If modular cable compatibility is unknown:

```text
REVIEW
```

Do not infer compatibility from connector shape.

## 4. Record GPU requirements

Use exact GPU/OEM manual or vendor documentation.

Record:
- auxiliary connector type/count;
- PSU recommendation if supplied;
- any exact cabling/adaptor instruction.

Do not invent a generic connector wattage and substitute it for the manual.

## 5. Record ordinary workload power

Reuse:
- Experiment 79 — NVIDIA board-energy integration;
- Experiment 85 — sustained TG/thermal telemetry;
- equivalent vendor telemetry where supported.

For multi-GPU:
- include only participating GPUs;
- record aggregate board power;
- add platform estimate separately.

## 6. Optional wall measurement

A consumer plug-in wall power meter can be recorded if used normally according to its own instructions.

Do not open wiring or expose mains conductors.

Wall power and PSU DC rating are different boundaries.

A slow consumer meter may not capture short transients.

## 7. Fill planning dossier

Copy:

```text
dossier.template.json
```

to your evidence directory.

Then run:

```bash
python3 check_dossier.py dossier.json
```

The checker can detect:
- arithmetic load > capacity;
- policy headroom shortfall;
- missing/false cable compatibility;
- connector-path shortfall;
- visible heat damage;
- unknown PSU identity.

It does **not** certify transient/electrical safety.

## 8. Finish

Fill:

```text
RESULT-TEMPLATE.md
```

A valid result separates:
- arithmetic capacity;
- connector/cable compatibility;
- transient unknowns;
- observed sustained workload behavior.


## Why this experiment

整机供电安全不能用“总瓦数够”一句话覆盖。这个 dossier 把 PSU exact identity、模组线 provenance、每条 GPU 供电路径、普通 workload power 与未知 transient 分开。

## Hypothesis

只有 arithmetic capacity、connector/cable compatibility 与普通 workload 行为都有证据时，方案才有资格进入接受评审；未知模组线兼容性或可见热损伤必须阻止乐观 PASS。

## Fixed variables

不改 power limit、不超频、不换线测试“能不能撑”。物理清点前关机断开 AC，只做外部检查。

## What to observe

- exact PSU model/revision/manual；
- PSU-port→cable→branch→GPU cable map；
- exact GPU/OEM connector guidance；
- sustained board/wall power 的测量边界；
- cable provenance UNKNOWN/false；
- visible connector damage。

## Troubleshooting

- “850W Gold”不是足够的 PSU identity。
- 模组接口能插进去不等于 pinout 兼容。
- wall power 与 PSU DC rating 是不同边界。
- 消费级插座表不能证明短时 transient。

## Evidence to save

保存 PSU label/manual reference、CABLE-MAP.csv、GPU requirement sources、ordinary workload power、dossier.json、checker 输出与 RESULT-TEMPLATE。

## What this proves

你能对真实整机供电路径做非侵入、可审计的可行性检查。

## What this does NOT prove

它不认证 PSU 内部电气安全、transient response，也不允许拆 PSU/裸测市电。

## No-hardware fallback

完成 Experiment 88。

## Transfer question

PSU 额定余量 40%，但一根模组 GPU cable 来源未知。为什么 arithmetic PASS 不能覆盖 cable gate？
