#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("policy")
    p.add_argument("baseline")
    p.add_argument("candidate")
    p.add_argument("rollback")
    a=p.parse_args()

    policy=load(a.policy)
    base=load(a.baseline)
    cand=load(a.candidate)
    rb=load(a.rollback)

    checks=[]

    def check(name,ok,detail):
        checks.append((name,bool(ok),detail))

    check(
        "readiness",
        cand["readiness_ms"] <= policy["max_readiness_ms"],
        f"{cand['readiness_ms']} <= {policy['max_readiness_ms']} ms"
    )
    check(
        "first inference",
        cand["first_inference_ms"] <= policy["max_first_inference_ms"],
        f"{cand['first_inference_ms']} <= {policy['max_first_inference_ms']} ms"
    )
    check(
        "smoke",
        (not policy["require_smoke"]) or cand["smoke_ok"],
        f"smoke_ok={cand['smoke_ok']}"
    )

    tg_speedup=cand["tg_tok_s"]/base["tg_tok_s"]
    check(
        "TG speedup",
        tg_speedup >= policy["min_tg_speedup"],
        f"{tg_speedup:.4f}x >= {policy['min_tg_speedup']:.4f}x"
    )

    ppl_ratio=cand["ppl"]/base["ppl"]
    check(
        "PPL ratio",
        ppl_ratio <= policy["max_ppl_ratio"],
        f"{ppl_ratio:.4f} <= {policy['max_ppl_ratio']:.4f}"
    )

    check(
        "critical fixtures",
        (not policy["require_critical_fixtures"]) or cand["critical_fixtures_ok"],
        f"critical_fixtures_ok={cand['critical_fixtures_ok']}"
    )
    check(
        "TTFT p95",
        cand["ttft_p95_ms"] <= policy["max_ttft_p95_ms"],
        f"{cand['ttft_p95_ms']} <= {policy['max_ttft_p95_ms']} ms"
    )
    check(
        "SLO compliance",
        cand["slo_compliance"] >= policy["min_slo_compliance"],
        f"{cand['slo_compliance']:.4f} >= {policy['min_slo_compliance']:.4f}"
    )

    passed=all(ok for _,ok,_ in checks)

    print(f"CANDIDATE: {cand['label']}")
    for name,ok,detail in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    if passed:
        print("DECISION: ACCEPT")
        return

    print("DECISION: ROLLBACK")

    same_identity=rb["identity"]==base["identity"]
    rb_ready=rb["readiness_ms"] <= policy["max_readiness_ms"]
    rb_first=rb["first_inference_ms"] <= policy["max_first_inference_ms"]
    rb_smoke=(not policy["require_smoke"]) or rb["smoke_ok"]

    print("ROLLBACK VERIFICATION")
    print(f"[{'PASS' if same_identity else 'FAIL'}] baseline identity restored")
    print(f"[{'PASS' if rb_ready else 'FAIL'}] readiness")
    print(f"[{'PASS' if rb_first else 'FAIL'}] first inference")
    print(f"[{'PASS' if rb_smoke else 'FAIL'}] smoke")

    if same_identity and rb_ready and rb_first and rb_smoke:
        print("ROLLBACK: VERIFIED")
    else:
        print("ROLLBACK: FAILED")
        raise SystemExit(2)

if __name__=="__main__":
    main()
