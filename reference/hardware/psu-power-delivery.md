# PSU / Power Delivery Card

## Identity

- PSU brand:
- exact model:
- revision/serial if needed:
- rated output W:
- ATX/spec claim:
- manufacturer manual URL:
- cable compatibility URL:

## Continuous planning

```text
estimated DC load
=
Σ GPU load
+ CPU/platform
+ storage/fans/peripherals
```

- estimated load:
- PSU capacity:
- arithmetic headroom W:
- arithmetic headroom %:
- chosen policy minimum:

No universal headroom percentage is implied.

## Measurement boundary

- GPU board power:
- whole-system wall power:
- meter/tool:
- sampling interval:

```text
board power != wall power
```

## Connector/cable gate

For each GPU:

| GPU | required input | PSU port | cable part/type | branch | compatibility source | visual condition |
|---|---|---|---|---|---|---|
| | | | | | | |

Rules:
- plug shape alone does not prove modular-cable compatibility;
- exact PSU/GPU manufacturer guidance wins;
- do not assume slot power makes up missing auxiliary power.

## Transient/excursion

- exact PSU/GPU transient guidance:
- ATX/spec evidence:
- unknowns:

Average board power is not proof of transient headroom.

## Safety

Default course:
- do not open PSU;
- do not probe mains/high-voltage internals;
- do not intentionally overload PSU/cables;
- do not bypass protections;
- inspect visible connectors only when powered off/unplugged.

## Decision

- ACCEPT
- REVIEW
- REJECT / STOP

Tie decision to both:
- capacity policy;
- connector/cable compatibility.
