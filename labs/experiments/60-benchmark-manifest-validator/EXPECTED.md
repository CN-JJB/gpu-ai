# Expected — Experiment 60

## Valid quant block

```
MANIFEST CONTRACT
- comparison_id: 'synthetic-quant-ab-001'
- intentional_variable: 'variant.model'
...
VALIDATION: PASS
```

Allowed differences:
- artifact SHA;
- artifact bytes;
- quant.

## Invalid prompt mutation

The second comparison must fail because:

```
variant.prompt.token_ids_sha256
```

changed outside the declared:

```
variant.model
```

block.

This is the central teaching result.
