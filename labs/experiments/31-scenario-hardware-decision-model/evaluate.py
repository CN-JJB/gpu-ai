#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SCENARIOS = {
    "interactive": {
        "required_gib": 18.0,
        "accepted_support": {"official-current", "official-pinned"},
        "weights": {
            "margin": 0.10,
            "tg": 0.35,
            "pp": 0.15,
            "cost": 0.25,
            "risk": 0.10,
            "evidence": 0.05,
        },
    },
    "long_context": {
        "required_gib": 22.0,
        "accepted_support": {"official-current", "official-pinned"},
        "weights": {
            "margin": 0.35,
            "tg": 0.20,
            "pp": 0.05,
            "cost": 0.15,
            "risk": 0.15,
            "evidence": 0.10,
        },
    },
}

def norm(values, x):
    lo, hi = min(values), max(values)
    return 1.0 if hi == lo else (x - lo) / (hi - lo)

def inv_norm(values, x):
    return 1.0 - norm(values, x)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", choices=SCENARIOS, default="interactive")
    a = p.parse_args()

    cfg = SCENARIOS[a.scenario]
    data = json.loads(Path(__file__).with_name("candidates.json").read_text())

    print("SYNTHETIC ONLY — no real hardware recommendation")
    print(f"scenario={a.scenario}, required_memory={cfg['required_gib']} GiB")
    print()

    survivors = []
    for c in data:
        capacity_ok = c["usable_memory_gib"] >= cfg["required_gib"]
        support_ok = c["support"] in cfg["accepted_support"]
        status = "PASS" if capacity_ok and support_ok else "FAIL"
        reasons = []
        if not capacity_ok:
            reasons.append("capacity")
        if not support_ok:
            reasons.append("software")
        print(f"{c['name']}: gate={status}" + (f" ({','.join(reasons)})" if reasons else ""))
        if status == "PASS":
            c = dict(c)
            c["margin"] = c["usable_memory_gib"] - cfg["required_gib"]
            # synthetic decode proxy assumes required weight bytes roughly track workload size
            c["tg_proxy"] = c["bandwidth_gib_s"] / cfg["required_gib"]
            survivors.append(c)

    print()
    if not survivors:
        print("No candidate passes hard gates.")
        return

    metrics = {
        "margin": [c["margin"] for c in survivors],
        "tg": [c["tg_proxy"] for c in survivors],
        "pp": [c["pp_index"] for c in survivors],
        "cost": [c["tco"] for c in survivors],
        "risk": [c["risk"] for c in survivors],
        "evidence": [c["evidence"] for c in survivors],
    }

    ranked = []
    for c in survivors:
        parts = {
            "margin": norm(metrics["margin"], c["margin"]),
            "tg": norm(metrics["tg"], c["tg_proxy"]),
            "pp": norm(metrics["pp"], c["pp_index"]),
            "cost": inv_norm(metrics["cost"], c["tco"]),
            "risk": inv_norm(metrics["risk"], c["risk"]),
            "evidence": norm(metrics["evidence"], c["evidence"]),
        }
        score = sum(parts[k] * cfg["weights"][k] for k in cfg["weights"])
        ranked.append((score, c, parts))

    ranked.sort(reverse=True, key=lambda x: x[0])
    print("rank among PASS candidates only:")
    for i, (score, c, parts) in enumerate(ranked, 1):
        print(f"{i}. {c['name']}: scenario_score={score:.3f}, "
              f"margin={c['margin']:.1f} GiB, tg_proxy={c['tg_proxy']:.2f}, "
              f"TCO={c['tco']}, support={c['support']}")

    print()
    print("Important: score has meaning only inside this synthetic scenario.")
    print("Change workload, gates or weights and the ranking can change.")

if __name__ == "__main__":
    main()
