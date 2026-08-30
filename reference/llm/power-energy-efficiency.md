# Power / Energy Efficiency Card

<figure>
  <img src="../../assets/diagrams/power-energy-token.svg" alt="Power / Energy Efficiency Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Power / Energy Efficiency Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## Units

```
W = J/s
E = ∫P dt
1 kWh = 3.6e6 J
```

## Output generation

```
J/output-token
=
energy / output tokens
```

```
tokens/J
=
1 / (J/token)
```

Steady-state:

```
tok/s/W = tok/J
```

## Prompt processing

Report separately:
- J/prompt-token;
- PP tok/s;
- PP power boundary.

## Energy boundary

Choose and label:
- GPU board total;
- GPU board incremental above idle;
- whole-system wall.

Never mix them.

## Real record

- telemetry tool:
- sample interval:
- GPU indices:
- start/end:
- energy J:
- output tokens:
- J/token:
- tok/J:
- optional idle baseline:
- optional price/kWh:

## Thermal

- starting temperature:
- ending/steady temperature:
- clocks:
- performance drift:

## TCO

Energy is one input to:
```
purchase + platform + electricity + cooling + risk
```
