# Expected — Experiment 71

No universal host result.

A valid audit:
- records actual listener evidence;
- does not modify firewall/router/NAT;
- does not expose a server publicly;
- does not record raw API keys;
- probes only localhost using the bundled status-only script;
- treats CORS/auth/TLS as different controls;
- checks metrics/slots/tools exposure;
- records model license separately from runtime license.

Unknown firewall/NAT state must remain UNKNOWN rather than guessed.
