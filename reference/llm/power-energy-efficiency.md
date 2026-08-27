# Power / Energy Efficiency Card

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
