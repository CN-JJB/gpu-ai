# Research Note 0020 — Service Exposure / Privacy / Authentication Boundary

日期：2026-08-27

## Research question

A local LLM becomes a network service when it listens on a socket.

That changes the trust boundary.

The important questions are not:

> Can I reach the Web UI?

but:

```
who can reach it?
who can authenticate?
is traffic protected?
what endpoints expose state?
what gets logged?
what tools/actions are enabled?
what model/license data may be redistributed?
```

This slice is defensive/read-only.

It does not instruct learners to expose a service to the public Internet.

---

# Current pinned llama.cpp evidence

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current server documentation states:

```
--host
default: 127.0.0.1

--port
default: 8080

--api-key
default: none

--metrics
default: disabled

--slots
default: enabled
```

It also supports:
- API-key file;
- TLS key/certificate;
- CORS configuration;
- Web UI;
- optional tools/MCP/agent capabilities.

The pinned documentation explicitly warns not to enable experimental built-in tools/MCP proxy/agent in untrusted environments.

---

# Part I — Loopback is a trust boundary

Common loopback addresses:

```
127.0.0.1
::1
```

A process bound only to loopback is normally reachable from the same host, not directly from other LAN machines.

This dramatically reduces network exposure.

It does not eliminate:
- malicious local users/processes;
- browser-origin issues;
- proxy/tunnel exposure;
- prompt/log privacy risk.

But it is a strong default for a personal local service.

---

# Part II — 0.0.0.0 / :: changes scope

Binding to:

```
0.0.0.0
```

means listening on all available IPv4 interfaces.

Binding to:

```
::
```

can similarly expose an IPv6 wildcard listener, with exact dual-stack behavior OS-dependent.

This can make the service reachable from:
- LAN;
- VPN;
- container/host networks;
- other attached interfaces;

subject to firewall/routing.

Do not equate:

```
bind all interfaces
```

with:

```
public Internet exposed
```

because firewall/NAT/routing still matter.

But it is a larger attack surface than loopback.

---

# Part III — LAN is not automatically trusted

A home LAN can include:
- guests;
- IoT devices;
- compromised machines;
- shared Wi-Fi users.

A local-model server may contain:
- private prompts;
- documents/RAG context;
- code;
- API credentials accidentally pasted into chats.

"Only on my LAN" is a policy decision, not an authentication mechanism.

---

# Part IV — Authentication

Current pinned llama-server can require API keys.

No API key by default is reasonable for:
- loopback-only personal use;

but becomes a serious design question when the listener is reachable by other machines.

Authentication answers:

> Who may use the API?

It does not itself provide:
- encryption;
- rate limiting;
- per-tenant fairness;
- authorization by operation;
- secret-safe logging.

---

# Part V — Secret placement

API keys can appear in:
- CLI args;
- environment variables;
- key files;
- reverse-proxy secrets.

Command-line secrets can sometimes be visible to:
- process inspection;
- shell history;
- audit tooling.

Prefer secret handling that avoids copying raw keys into course Evidence.

The real audit intentionally records only:

```
authentication configured?
yes/no/unknown
```

not the secret itself.

---

# Part VI — TLS

TLS protects traffic in transit between the TLS endpoints.

TLS can terminate:
- directly in llama-server using certificate/key options;
- in a reverse proxy/application gateway.

If TLS terminates upstream and proxy-to-backend runs over loopback/private host networking, document that architecture.

Do not infer:

```
HTTPS at browser
=
llama-server itself has TLS enabled
```

The important thing is the full path.

---

# Part VII — Authentication != TLS

Authentication without TLS on an untrusted network can expose:
- API key;
- prompts;
- responses;

to network observers.

TLS without authentication encrypts traffic but may still allow any reachable client to use the service.

They solve different problems.

---

# Part VIII — CORS is not access control

CORS controls what browser JavaScript origins may read/call through browser policy.

It is not:
- a firewall;
- authentication;
- a rule for curl/native clients.

A permissive or restrictive CORS setting must not be treated as the primary security boundary.

---

# Part IX — Metrics endpoint

Metrics can reveal operational data such as:
- request activity;
- token counts;
- slot pressure;
- throughput.

Even when metrics do not include prompt text, they can reveal:
- usage timing;
- workload intensity;
- model/service behavior.

Expose observability only to the intended monitoring boundary.

Current pinned `--metrics` is disabled by default.

---

# Part X — Slots / cache state

Current pinned `--slots` endpoint is enabled by default.

Slot-monitoring/cache endpoints can expose more internal serving state than a normal chat client needs.

If a service moves beyond loopback, audit:
- whether slots endpoint is reachable;
- who needs it;
- whether upstream access control covers it.

Least exposure:

```
only expose endpoints required by the client role
```

---

# Part XI — Web UI

A Web UI is an additional served surface.

It may be convenient for local use.

When reachable by other networks, it should be considered part of the externally accessible application, not "just static HTML".

Browser security, authentication and CORS interactions matter.

---

# Part XII — Tool / agent capabilities change the risk class

Pinned current llama-server includes experimental capabilities such as:
- file read/search/write;
- shell execution;
- MCP integrations;
- agent mode.

The upstream documentation itself warns against enabling these in untrusted environments.

This is a qualitatively different trust boundary:

```
text generation
```

vs:

```
model can invoke host/tool actions
```

Do not expose host-action tools merely because the chat endpoint was previously safe enough for LAN use.

---

# Part XIII — Prompt and response logs

Logs may contain:
- raw prompt text;
- generated text;
- tool arguments;
- file paths;
- user IDs;
- API request metadata.

For local privacy goals:

```
logging policy
```

is part of the system design.

Ask:
- Is request content logged?
- Where?
- How long retained?
- Who can read it?
- Is telemetry exported elsewhere?

---

# Part XIV — Evidence itself can leak data

Course Evidence should not blindly save:
- API keys;
- cookies;
- Authorization headers;
- private prompts;
- full process command lines containing secrets.

Use:
- redacted config;
- hashes;
- status-only endpoint probes;
- pseudonymous tenant IDs.

Reproducibility should not require leaking secrets.

---

# Part XV — Model files are sensitive in a different way

A model artifact may be:
- redistributable;
- restricted by license;
- gated;
- subject to attribution/notice terms;
- allowed for local use but not every form of redistribution.

Runtime/code license and model license are separate.

Example:

```
llama.cpp license
!=
model artifact license
```

Before sharing a course bundle or server image that includes weights, inspect the exact model license/model card.

This is a compliance check, not legal advice.

---

# Part XVI — Containers do not automatically create security

Running in:
- Docker;
- Podman;
- VM;

can isolate some resources depending on configuration.

But a container with:
- host mounts;
- host network;
- privileged mode;
- Docker socket;

can still have a broad trust boundary.

Do not teach:

> container = safe.

Record actual capabilities/mounts/network.

---

# Part XVII — Reverse proxy

A reverse proxy can centralize:
- TLS;
- authentication;
- rate limits;
- access logs;
- path filtering.

But it can also introduce:
- misconfiguration;
- another secret store;
- more logs;
- another network hop.

The proxy is part of the trusted computing path.

---

# Part XVIII — Least exposure workflow

For a personal local LLM:

1. Start loopback-only unless another scope is needed.
2. Identify exact clients that need access.
3. If expanding to LAN:
   - add authentication;
   - decide TLS/trusted network path;
   - limit endpoints;
   - inspect firewall/routing.
4. Keep observability on a narrower admin path where practical.
5. Do not enable host-action tools on untrusted surfaces.
6. Audit logs/secrets.

This is architecture guidance, not a command sequence to open firewalls.

---

# Part XIX — Listener evidence

OS listener inventory answers:

```
what address/port is actually listening?
```

This is stronger than remembering what command you intended to run.

Examples of read-only tools:
- Linux `ss`;
- macOS/Linux `lsof`;
- Windows PowerShell `Get-NetTCPConnection`.

The real lab does not change:
- firewall;
- router;
- NAT;
- port forwarding.

---

# Part XX — Endpoint evidence

A status-only probe can ask on localhost:
- health endpoint status;
- metrics status;
- slots status;
- models status.

The course probe discards response bodies so it does not accidentally persist slot/prompt state.

If authentication is enabled, it reads an API key from an environment variable and never prints it.

---

# Claims to avoid

- "LAN means trusted";
- "0.0.0.0 means definitely public Internet";
- "CORS is authentication";
- "API key encrypts traffic";
- "HTTPS proves the backend itself terminates TLS";
- "metrics never reveal useful sensitive metadata";
- "container means secure";
- "client evidence should include raw secrets";
- "runtime license automatically covers model weights";
- "text-only serving and shell/tool-enabled agents have the same risk".
