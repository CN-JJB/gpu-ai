#!/usr/bin/env python3
import argparse,json
from pathlib import Path

PLACEHOLDERS={"REPLACE","TODO","TBD"}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def walk(v,path=""):
    if isinstance(v,dict):
        for k,x in v.items():
            p=f"{path}.{k}" if path else k
            yield from walk(x,p)
    elif isinstance(v,list):
        for i,x in enumerate(v):
            yield from walk(x,f"{path}[{i}]")
    else:
        yield path,v

def placeholders(obj):
    return [
        p for p,v in walk(obj)
        if isinstance(v,str) and v.strip().upper() in PLACEHOLDERS
    ]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("policy")
    p.add_argument("baseline")
    p.add_argument("candidate")
    p.add_argument("--rollback")
    a=p.parse_args()

    pol=load(a.policy); base=load(a.baseline); cand=load(a.candidate)
    rb=load(a.rollback) if a.rollback else None

    errs=[]
    for name,obj in [("policy",pol),("baseline",base),("candidate",cand)]:
        ph=placeholders(obj)
        if ph:
            errs.append(f"{name} placeholders: {', '.join(ph)}")
    if rb:
        ph=placeholders(rb)
        if ph:
            errs.append(f"rollback placeholders: {', '.join(ph)}")

    # Numeric template/default sanity. Zero may be a valid measured error rate,
    # but TG/PPL denominators and timing/evaluation identities must be usable.
    numeric_errors=[]
    if base["performance"]["tg_tok_s"] <= 0:
        numeric_errors.append("baseline performance.tg_tok_s must be > 0")
    if base["quality"]["ppl"] <= 0:
        numeric_errors.append("baseline quality.ppl must be > 0")
    if cand["quality"]["ppl"] <= 0:
        numeric_errors.append("candidate quality.ppl must be > 0")
    if cand["performance"]["tg_tok_s"] < 0:
        numeric_errors.append("candidate performance.tg_tok_s must be >= 0")
    for name,obj in [("baseline",base),("candidate",cand)]:
        if obj["recovery"]["readiness_ms"] < 0:
            numeric_errors.append(f"{name} recovery.readiness_ms must be >= 0")
        if obj["recovery"]["first_inference_ms"] < 0:
            numeric_errors.append(f"{name} recovery.first_inference_ms must be >= 0")
        if not 0 <= obj["serving"]["slo_compliance"] <= 1:
            numeric_errors.append(f"{name} serving.slo_compliance must be in [0,1]")
        if not 0 <= obj["serving"]["error_rate"] <= 1:
            numeric_errors.append(f"{name} serving.error_rate must be in [0,1]")

    if pol["max_readiness_ms"] <= 0 or pol["max_first_inference_ms"] <= 0:
        numeric_errors.append("policy readiness/first-inference limits must be > 0")
    if pol["min_tg_speedup"] < 0 or pol["max_ppl_ratio"] <= 0:
        numeric_errors.append("policy speedup/PPL thresholds are invalid")
    if not 0 <= pol["min_slo_compliance"] <= 1:
        numeric_errors.append("policy min_slo_compliance must be in [0,1]")
    if not 0 <= pol["max_error_rate"] <= 1:
        numeric_errors.append("policy max_error_rate must be in [0,1]")

    errs.extend(numeric_errors)

    if errs:
        print("GATE: BLOCKED_MISSING_EVIDENCE")
        for e in errs: print("- "+e)
        raise SystemExit(3)

    checks=[]
    def ck(name,ok,detail):
        checks.append((name,bool(ok),detail))

    ck("candidate smoke",cand["recovery"]["smoke_ok"] or not pol["require_smoke"],str(cand["recovery"]["smoke_ok"]))
    ck("readiness",cand["recovery"]["readiness_ms"]<=pol["max_readiness_ms"],f"{cand['recovery']['readiness_ms']} ms")
    ck("first inference",cand["recovery"]["first_inference_ms"]<=pol["max_first_inference_ms"],f"{cand['recovery']['first_inference_ms']} ms")

    tg_speedup=cand["performance"]["tg_tok_s"]/base["performance"]["tg_tok_s"]
    ck("TG speedup",tg_speedup>=pol["min_tg_speedup"],f"{tg_speedup:.4f}x")

    ppl_ratio=cand["quality"]["ppl"]/base["quality"]["ppl"]
    ck("PPL ratio",ppl_ratio<=pol["max_ppl_ratio"],f"{ppl_ratio:.4f}")
    ck("critical fixtures",cand["quality"]["critical_fixtures_ok"] or not pol["require_critical_fixtures"],str(cand["quality"]["critical_fixtures_ok"]))

    ck("TTFT p95",cand["serving"]["ttft_p95_ms"]<=pol["max_ttft_p95_ms"],f"{cand['serving']['ttft_p95_ms']} ms")
    ck("SLO compliance",cand["serving"]["slo_compliance"]>=pol["min_slo_compliance"],f"{cand['serving']['slo_compliance']:.4f}")
    ck("error rate",cand["serving"]["error_rate"]<=pol["max_error_rate"],f"{cand['serving']['error_rate']:.4f}")

    for name,ok,detail in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    if all(x[1] for x in checks):
        print("GATE: ACCEPT")
        return

    print("GATE: ROLLBACK")

    if rb is None:
        print("ROLLBACK: NOT VERIFIED — no rollback release evidence supplied")
        raise SystemExit(2)

    identity_ok=rb["identity"]==base["identity"]
    ready_ok=rb["recovery"]["readiness_ms"]<=pol["max_readiness_ms"]
    smoke_ok=rb["recovery"]["smoke_ok"] or not pol["require_smoke"]

    print(f"[{'PASS' if identity_ok else 'FAIL'}] rollback baseline identity")
    print(f"[{'PASS' if ready_ok else 'FAIL'}] rollback readiness")
    print(f"[{'PASS' if smoke_ok else 'FAIL'}] rollback smoke")

    if identity_ok and ready_ok and smoke_ok:
        print("ROLLBACK: VERIFIED")
    else:
        print("ROLLBACK: FAILED")
        raise SystemExit(2)

if __name__=="__main__":
    main()
