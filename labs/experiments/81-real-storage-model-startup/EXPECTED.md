# Expected — Experiment 81

No universal real throughput/startup value.

A valid result:
- never calls the first pass "cold" without independent evidence;
- records that the read probe itself changes cache state;
- does not treat second-pass buffered MiB/s as SSD bandwidth;
- separates file-read, health-ready, first-inference and steady PP/TG;
- does not use global page-cache dropping by default;
- treats unavailable `fincore` as UNKNOWN rather than inventing residency.

A faster second startup is compatible with page-cache effects but does not prove page cache was the only cause.
