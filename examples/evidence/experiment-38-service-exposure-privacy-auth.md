# Evidence — Experiment 38: Service Exposure / Privacy / Authentication

状态：stable defensive-deployment lesson complete; L0 exposure linter verified; localhost-only read-only audit path ready.

## Claim

> Changing a local LLM listener from loopback to a broader interface changes the trust boundary. Authentication, TLS, CORS, endpoint exposure, logs and host-action tools are separate controls and must not be conflated.

## Current pinned llama.cpp evidence

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current server documentation exposes:

```
--host
default 127.0.0.1

--port
default 8080

--api-key / --api-key-file
default none

--ssl-key-file / --ssl-cert-file

--metrics
default disabled

--slots
default enabled
```

Current Web UI is enabled by default.

Pinned documentation also explicitly warns that experimental built-in tools, MCP proxy and agent capabilities should not be enabled in untrusted environments.

## Network-boundary distinctions

```
127.0.0.1 / ::1
→ loopback scope

0.0.0.0 / ::
→ wildcard/all-interface listener
```

A wildcard listener does **not** prove Internet reachability because:
- firewall;
- NAT/router;
- VPN;
- host/network policy;

remain separate controls.

But it is a broader network surface than loopback.

## Control distinctions

```
authentication
!= TLS
!= CORS
!= firewall
```

Authentication answers who may use the API.

TLS protects traffic between TLS endpoints.

CORS is a browser-origin policy, not authentication/firewalling.

## Experiment 70 verification

### local-only.json

Verified findings:

```
[INFO] listen scope: loopback (127.0.0.1)
[INFO] no auth relies on loopback/local-host trust assumption
```

### lan-risk.json

Verified findings:

```
[INFO] wildcard-all-interfaces (0.0.0.0)
[HIGH] non-loopback listener without authentication
[REVIEW] non-loopback traffic has no declared TLS termination
[REVIEW] metrics enabled on broader listener scope
[REVIEW] slots endpoint enabled on broader listener scope
[INFO] wildcard CORS is not an authentication boundary
[PRIVACY] prompt logging enabled
```

The linter explicitly states that it does not inspect firewall/NAT/router state and is not a security certification.

## Experiment 71 safety guard

The bundled endpoint probe accepts only:

```
127.0.0.1
localhost
::1
```

Validation checked that it rejects:
- private-LAN addresses such as 192.168.x.x;
- wildcard 0.0.0.0;
- a URL shaped like `127.0.0.1@evil.example`, because the parsed hostname is the remote host.

The probe:
- prints status/content type only;
- reads/discards a bounded body prefix;
- never prints the API key;
- obtains a key only through a named environment variable.

Listener inventory is read-only and does not alter:
- firewall;
- NAT;
- router;
- port forwarding.

## Data/privacy boundary

Potentially sensitive evidence includes:
- raw prompts/responses;
- Authorization headers;
- API keys;
- cookies;
- process command lines with secrets;
- logs and tenant identifiers.

The course prefers:
- hashes;
- redacted config;
- pseudonymous IDs;
- configured/not-configured state.

## Endpoint boundary

Admin/observability surfaces such as:
- metrics;
- slots/cache;
- props/router controls;

do not automatically need the same audience as the chat API.

Least exposure is the default principle.

## Model-license boundary

```
runtime/software license
!=
model artifact license
```

Redistribution of model weights must be checked against the exact model/model-card terms separately.

This is a compliance checklist, not legal advice.

## Learner should reject

- LAN means trusted;
- 0.0.0.0 proves public-Internet exposure;
- CORS is authentication;
- API keys encrypt traffic;
- HTTPS proves llama-server itself terminates TLS;
- containers are automatically safe;
- raw secrets belong in reproducibility Evidence;
- text-only serving and shell/tool-enabled agents have the same trust boundary.
