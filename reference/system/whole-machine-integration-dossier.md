# Whole-Machine System Integration Card

<figure>
  <img src="../../assets/diagrams/system-integration-hard-gates.svg" alt="Whole-Machine System Integration Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Whole-Machine System Integration Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## 1. Workload identity

- target use:
- model/artifact SHA:
- quant/backend:
- context:
- concurrency:
- serving SLO:
- privacy/network scope:
- budget:

## 2. Hard gates

| Domain | Requirement | Evidence | PASS/FAIL |
|---|---|---|---|
| model/VRAM | | | |
| runtime/backend | | | |
| multi-GPU/topology | | | |
| host RAM | | | |
| storage | | | |
| PSU/cables | | | |
| thermal/sustained | | | |
| serving/SLO | | | |
| privacy/network | | | |
| budget | | | |

Known FAIL:

```text
→ REVISE
```

## 3. Purchase-critical unknowns

| Unknown | Why it matters | How to resolve |
|---|---|---|
| | | |

Any unresolved critical unknown:

```text
→ BLOCKED
```

## 4. Preferences

Rank only after feasibility:
- TG/TTFT;
- J/token;
- noise;
- size;
- price;
- maintenance;
- upgrade room.

Do not let preferences override a hard FAIL.

## 5. Evidence links

- model dossier:
- workload manifest:
- hardware/used-GPU packet:
- multi-GPU topology:
- memory packet:
- storage packet:
- PSU packet:
- thermal packet:
- serving packet:
- release/rollback packet:
- Evidence Packet index:

## 6. Final decision

- ACCEPT
- REVISE
- BLOCKED

## 7. Revision plan

Do not auto-purchase/change hardware. List alternative revisions and the new evidence each would require.
