# Experiment 70 — Service Exposure Configuration Linter

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/service-exposure.svg" alt="服务暴露面从 bind address、网络边界、认证到访问路径逐层扩大；配置 linter 的目标是阻止无意的公网/局域网暴露。">
  <figcaption>服务暴露面从 bind address、网络边界、认证到访问路径逐层扩大；配置 linter 的目标是阻止无意的公网/局域网暴露。</figcaption>
</figure>

## Goal

Compare two synthetic service configurations.

## Local-only

```bash
python3 audit_config.py local-only.json
```

Expected:
- loopback scope;
- no-auth relies on local-host trust assumption;
- no external-exposure HIGH finding.

## Broad listener

```bash
python3 audit_config.py lan-risk.json
```

Expected findings include:
- wildcard/all-interface listener;
- no authentication;
- no declared TLS termination;
- metrics/slots broader exposure;
- prompt logging privacy review.

## Important

The linter does **not** inspect:
- firewall;
- router/NAT;
- VPN;
- cloud security group.

It cannot certify Internet reachability or security.

It is a checklist teaching tool.


## Why this experiment

很多暴露事故不是复杂漏洞，而是“把本机默认配置原样搬到 LAN/公网”。这个 linter 让你把 listener、auth、TLS、metrics、logging 这些控制面分开检查。

## Hypothesis

同一个无认证服务，在 loopback-only 与 wildcard listener 下风险含义完全不同；scope 一扩大，原来的“本机信任假设”就不再成立。

## Fixed variables

只比较两份给定 config，不改变 firewall/router/VPN 等外部环境；因为本工具根本看不到它们。

## What to observe

1. local-only 为什么没有 external-exposure HIGH。
2. wildcard listener 为什么会触发更多 review 项。
3. auth、TLS、metrics/slots exposure、prompt logging 为什么是不同维度。
4. linter 为什么不能宣布“公网可访问”或“安全”。

## Troubleshooting

- 不要把 0.0.0.0 直接翻译成“公网开放”。
- 不要把 CORS 当 auth。
- 不要把隐藏 metrics endpoint 当成传输加密。
- 如果真实配置含 secret，证据里只保留“已配置/来源”，不要提交 secret 值。

## Evidence to save

保存两次 linter 输出，并画一张 trust-boundary 图：localhost → LAN → VPN/public。

## What this proves

你会审计服务配置层的暴露面，并能说明哪些结论需要网络路径证据才能继续。

## What this does NOT prove

它不测试 firewall、NAT、VPN、云安全组，也不能做渗透测试或安全认证。

## No-hardware path

完整 L0 实验。

## Transfer question

如果服务 bind 0.0.0.0，但主机 firewall 只允许本机访问，linter 应该说“公网暴露”吗？为什么？
