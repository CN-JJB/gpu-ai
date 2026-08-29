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


## Why this experiment

服务暴露面不能只靠配置文件猜。这个实验用只读 listener 与本地 endpoint probe，让你观察“进程实际监听在哪里、哪些本地接口存在”，同时刻意不跨越 firewall/NAT/VPN 的证据边界。

## Hypothesis

loopback listener 只能证明本机监听范围；wildcard/LAN listener 表示更宽接口范围，但仍不能单独证明公网可达。Endpoint status 也只证明本地 HTTP 行为，不证明授权策略安全。

## Fixed variables

整个实验不修改服务配置、firewall、router、VPN 或 bind address。只观察当前状态。

## What to observe

1. exact address:port 与 owning process。
2. loopback / wildcard / interface-specific 三种 scope 的不同语义。
3. health/metrics/slots 等 endpoint 的本地 status。
4. auth 开启时如何只记录“configured/source”，而不泄露 secret。
5. firewall/NAT 为什么仍保持 UNKNOWN。

## Troubleshooting

- listener 工具缺失时记录缺失，不要改系统来配合实验。
- 进程参数可能含 secret，不要直接整行提交。
- 0.0.0.0 不是“公网已开放”的同义词。
- endpoint 401/403 可能说明 auth 生效，不应自动视为服务故障。

## Evidence to save

保存 listeners.txt、endpoint probe 输出和 RESULT-TEMPLATE。公开证据前检查 API key、Authorization header、私人路径与 prompt 是否已移除。

## What this proves

你能用只读证据描述本机服务的监听与本地 endpoint 暴露面。

## What this does NOT prove

它不证明 Internet reachability、TLS 安全、firewall 配置正确，也不是渗透测试。

## No-hardware fallback

没有运行中的服务时，先完成 Experiment 70 的配置审计；本实验留到有本地 server 时做。

## Transfer question

服务监听 0.0.0.0:8080，但路由器没有端口转发。你能从这个实验声称“公网可访问”吗？
