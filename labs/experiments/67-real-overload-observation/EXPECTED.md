# Expected — Experiment 67

No universal real result.

A valid packet:
- uses a server you own/control;
- uses a bounded finite burst;
- records exact workload identity;
- saves client trace and server metrics;
- reports actual errors/deferred behavior instead of assuming a queue policy;
- counts retry attempts separately from original requests;
- does not claim a client timeout cancelled GPU work without server evidence.
