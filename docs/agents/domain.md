# Domain Docs

本仓库采用 single-context 领域文档布局：

- Canonical glossary: `/CONTEXT.md`
- ADRs: `/docs/adr/`

消费规则：
- 普通任务只需读取相关术语，不要把整个领域文档复制进工作产物。
- 修改术语或领域边界时使用 `domain-modeling`。
- `CONTEXT.md` 只存概念语言，不存实现细节。
- ADR 仅用于难以逆转、缺少背景会令人意外、且确有权衡的决定。
