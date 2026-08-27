# Expected — Experiment 34

The untouched template contains one deliberately excluded placeholder.

Running:

```bash
python3 summarize_market.py market-sample-template.csv
```

should report approximately:

```
raw rows=1 normalized rows=0 excluded=1
```

This is correct.

The experiment should never manufacture a price distribution when the raw sample is empty.

A publishable common-SKU snapshot should preferably have:
- 10+ normalized direct observations；
- exact date/window；
- price state；
- explicit exclusions；
- evidence grade。

If that is not available, publish a lower-confidence note rather than a fake median.