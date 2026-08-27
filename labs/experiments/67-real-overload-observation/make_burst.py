#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--prompt-file",type=Path,required=True)
    p.add_argument("--requests",type=int,default=8)
    p.add_argument("--spacing-ms",type=int,default=50)
    p.add_argument("--n-predict",type=int,default=64)
    p.add_argument("--out",type=Path,default=Path("workload-burst.jsonl"))
    a=p.parse_args()

    if not 1 <= a.requests <= 64:
        raise SystemExit("requests must be 1..64 for this bounded local lab")
    if a.spacing_ms < 0:
        raise SystemExit("spacing-ms must be >=0")
    if not a.prompt_file.is_file():
        raise SystemExit("prompt file does not exist")

    lines=[]
    for i in range(a.requests):
        lines.append(json.dumps({
            "id":f"r{i:02d}",
            "delay_ms":i*a.spacing_ms,
            "prompt_file":str(a.prompt_file),
            "n_predict":a.n_predict,
        }))

    a.out.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"wrote {a.out} with {a.requests} bounded requests")

if __name__=="__main__":
    main()
