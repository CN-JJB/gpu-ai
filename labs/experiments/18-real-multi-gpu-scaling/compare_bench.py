#!/usr/bin/env python3
import argparse
import json
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

def classify_test(row):
    test = str(row.get("test", "")).lower()
    n_prompt = row.get("n_prompt")
    n_gen = row.get("n_gen")

    if test.startswith("pp") or (isinstance(n_prompt, (int, float)) and n_prompt > 0 and (not n_gen or n_gen == 0)):
        return "PP"
    if test.startswith("tg") or (isinstance(n_gen, (int, float)) and n_gen > 0 and (not n_prompt or n_prompt == 0)):
        return "TG"
    return None

def extract(path):
    rows = load_json(path)
    out = {}
    for row in rows:
        kind = classify_test(row)
        if not kind:
            continue
        avg = row.get("avg_ts")
        if avg is None:
            continue
        out.setdefault(kind, []).append(float(avg))
    return {k: sum(v)/len(v) for k, v in out.items() if v}

def main():
    p = argparse.ArgumentParser(description="Compare llama-bench JSON/JSONL PP and TG throughput.")
    p.add_argument("files", nargs="+", help="single.json layer.json ...")
    a = p.parse_args()

    results = [(Path(f).stem, extract(f)) for f in a.files]
    if not results:
        raise SystemExit("no input")

    baseline = results[0][1]

    print("| run | PP t/s | PP speedup | TG t/s | TG speedup |")
    print("|---|---:|---:|---:|---:|")
    for name, vals in results:
        pp = vals.get("PP")
        tg = vals.get("TG")
        pp_s = pp / baseline["PP"] if pp is not None and baseline.get("PP") else None
        tg_s = tg / baseline["TG"] if tg is not None and baseline.get("TG") else None

        def fmt(v, suffix=""):
            return "n/a" if v is None else f"{v:.3f}{suffix}"

        print(f"| {name} | {fmt(pp)} | {fmt(pp_s, 'x')} | {fmt(tg)} | {fmt(tg_s, 'x')} |")

if __name__ == "__main__":
    main()
