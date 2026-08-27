#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def load_json(path):
    text = Path(path).read_text(encoding="utf-8").strip()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
    except json.JSONDecodeError:
        pass

    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, list):
            rows.extend(obj)
        else:
            rows.append(obj)
    return rows

def kind(row):
    test = str(row.get("test", "")).lower()
    nprompt = row.get("n_prompt")
    ngen = row.get("n_gen")
    if test.startswith("pp") or (
        isinstance(nprompt, (int, float)) and nprompt > 0 and (not ngen or ngen == 0)
    ):
        return "PP"
    if test.startswith("tg") or (
        isinstance(ngen, (int, float)) and ngen > 0 and (not nprompt or nprompt == 0)
    ):
        return "TG"
    return None

def extract(path):
    vals = {}
    for row in load_json(path):
        k = kind(row)
        if not k or row.get("avg_ts") is None:
            continue
        vals.setdefault(k, []).append(float(row["avg_ts"]))
    return {k: sum(v)/len(v) for k, v in vals.items() if v}

def fmt(v):
    return "n/a" if v is None else f"{v:.3f}"

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_bench.py baseline.json candidate.json")

    a = extract(sys.argv[1])
    b = extract(sys.argv[2])

    print("| metric | baseline | candidate | speedup |")
    print("|---|---:|---:|---:|")
    for k in ("PP", "TG"):
        av = a.get(k)
        bv = b.get(k)
        speed = (bv / av) if av and bv is not None else None
        print(f"| {k} t/s | {fmt(av)} | {fmt(bv)} | {fmt(speed)}x |")

if __name__ == "__main__":
    main()
