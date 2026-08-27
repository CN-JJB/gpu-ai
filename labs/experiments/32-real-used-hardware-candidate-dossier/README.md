# Experiment 32 — Real Used-Hardware Candidate Dossier

硬件等级：L0/L1

这是买卡/买 Mac 前的 Evidence 模板，不需要先拥有硬件。

## 目标

For one exact listing/candidate, produce:

```
identity
→ workload
→ capacity gate
→ software gate
→ evidence gaps
→ TCO
→ risk
→ decision
```

## 使用

复制模板：

```bash
cp candidate-template.json my-candidate.json
```

填写所有你能确认的字段。

然后：

```bash
python3 evaluate_candidate.py my-candidate.json
```

脚本不会替你猜未知字段。

如果关键字段缺失，输出：

```
NEEDS EVIDENCE
```

## Evidence source等级

每个关键 claim 可以填：

```
E3 = official / local raw
E2 = reproducible / reputable
E1 = weak / seller
E0 = unknown
```

## Hard gates

### Capacity

填写：
- workload runtime footprint；
- candidate usable memory。

### Software

填写：
- support state；
- exact backend/version。

Allowed support states:
- official-current
- official-pinned
- community-enabled
- runtime-visible-only
- unsupported

是否接受 community-enabled 是你自己的 scenario constraint。

## Risk

不要只填“矿卡/非矿”。

记录：
- board condition；
- BIOS；
- repair；
- memory errors；
- corrosion；
- fan；
- seller test；
- return policy；
- software-lifespan risk。

## TCO

记录：
- asking price；
- platform/PSU/cooling extra；
- expected energy；
- repair reserve；
- expected resale。

## Decision

脚本只做结构性检查。

最终人工结论写进：
`RESULT-TEMPLATE.md`。