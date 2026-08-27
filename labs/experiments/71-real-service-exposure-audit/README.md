# Experiment 71 — Read-Only Local Service Exposure Audit

硬件等级：L0/L1。

## Goal

Inventory an existing local service without changing network configuration.

This lab does **not**:
- open firewall ports;
- change router/NAT;
- create port forwarding;
- bind the server publicly.

## 1. Listener inventory

Linux/macOS:

```bash
./audit-listeners.sh | tee listeners.txt
```

Windows PowerShell:

```powershell
./audit-listeners.ps1 | Tee-Object listeners.txt
```

Record the actual socket:
- address;
- port;
- owning process/PID where available.

## 2. Local endpoint status probe

Only localhost/loopback is accepted by the course script:

```bash
python3 probe_local_endpoints.py \
  --base http://127.0.0.1:8080
```

If authentication is enabled:

```bash
export LOCAL_LLM_KEY='...'
python3 probe_local_endpoints.py \
  --base http://127.0.0.1:8080 \
  --api-key-env LOCAL_LLM_KEY
```

The script:
- never prints the key;
- does not print endpoint bodies;
- only records status/content type.

## 3. Do not dump full process args blindly

A full process command line can contain:
- API keys;
- private file paths.

Record secrets as:
```
configured / source=env-or-file
```
not raw values.

## 4. Fill result

Use:
`RESULT-TEMPLATE.md`

## 5. Network scope

If listener is:
- 127.0.0.1 / ::1 → loopback evidence;
- 0.0.0.0 / :: → wildcard listener evidence;
- LAN address → interface-specific evidence.

Do not claim Internet reachability from socket binding alone.

Firewall/NAT remain separate unknowns unless independently audited.

## 6. License

Record:
- llama.cpp/runtime license;
- exact model artifact/model-card license;
- whether you are only using locally or redistributing.

This is a compliance checklist, not legal advice.
