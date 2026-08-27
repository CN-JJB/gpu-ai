#!/usr/bin/env python3
import json
import sys
from pathlib import Path

IDENTITY_KEYS = [
    "model_sha256",
    "runtime_version",
    "device_identity",
    "pp_tokens",
    "tg_tokens",
    "repetitions",
]

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def get_path(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def flatten(prefix, obj):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            out.update(flatten(key, v))
    else:
        out[prefix] = obj
    return out

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: validate_ab.py baseline-manifest.json candidate-manifest.json")

    a = load(sys.argv[1])
    b = load(sys.argv[2])

    identity_fail = []
    for k in IDENTITY_KEYS:
        av = a.get("identity", {}).get(k)
        bv = b.get("identity", {}).get(k)
        if av != bv:
            identity_fail.append((k, av, bv))

    if identity_fail:
        print("IDENTITY CHECK: FAIL")
        for k, av, bv in identity_fail:
            print(f"- {k}: baseline={av!r}, candidate={bv!r}")
    else:
        print("IDENTITY CHECK: PASS")

    declared_a = a.get("intentional_variable")
    declared_b = b.get("intentional_variable")
    if declared_a != declared_b:
        print("ONE-VARIABLE CHECK: FAIL")
        print(f"- intentional_variable differs: {declared_a!r} vs {declared_b!r}")
        raise SystemExit(1)

    declared = declared_a
    if not isinstance(declared, str) or not declared.startswith("config."):
        print("ONE-VARIABLE CHECK: FAIL")
        print("- intentional_variable must be a dotted config.* path")
        raise SystemExit(1)

    af = flatten("config", a.get("config", {}))
    bf = flatten("config", b.get("config", {}))
    keys = sorted(set(af) | set(bf))
    diffs = [k for k in keys if af.get(k) != bf.get(k)]

    if diffs == [declared]:
        print("ONE-VARIABLE CHECK: PASS")
        print(f"- changed: {declared}")
    else:
        print("ONE-VARIABLE CHECK: FAIL")
        print(f"- declared: {declared}")
        print(f"- actual config differences: {diffs}")

    placeholder = []
    for name, obj in [("baseline", a), ("candidate", b)]:
        for path, value in flatten("", obj).items():
            if isinstance(value, str) and value.strip().upper() == "REPLACE":
                placeholder.append(f"{name}:{path}")
    if placeholder:
        print("PLACEHOLDER CHECK: FAIL")
        for p in placeholder:
            print(f"- {p}")
    else:
        print("PLACEHOLDER CHECK: PASS")

    ok = not identity_fail and diffs == [declared] and not placeholder
    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
