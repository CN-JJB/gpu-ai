# Expected — Experiment 79

No universal real energy value.

A valid result:
- uses exact workload/token boundary;
- records sampling interval;
- selects only participating GPUs;
- fails rather than silently filling missing samples;
- labels board energy separately from whole-system energy;
- labels total vs incremental-above-idle energy separately.

Do not compare J/token from different PP/TG/request-shape workloads as if identical.
