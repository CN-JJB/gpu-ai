# Expected — Experiment 63

There is no universal real performance output.

A valid result should contain:
- exact server/model/runtime identity;
- exact request-trace identity;
- raw client request CSV;
- raw SSE logs;
- /metrics before/after or an explicit note that metrics were unavailable;
- client-observed TTFT/E2E;
- chunk-gap metric labeled as a proxy, not true ITL;
- request length distribution;
- SLO declared before interpreting the result.

Do not invent queue time from TTFT alone.
