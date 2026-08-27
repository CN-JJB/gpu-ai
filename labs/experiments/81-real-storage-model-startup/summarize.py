#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file_probe",type=Path)
    p.add_argument("restart_result",type=Path)
    a=p.parse_args()

    fp=json.loads(a.file_probe.read_text(encoding="utf-8"))
    rr=json.loads(a.restart_result.read_text(encoding="utf-8"))

    print("STORAGE / STARTUP EVIDENCE SUMMARY")
    print(f"model bytes: {fp['file_bytes']}")
    print(f"read bytes/pass: {fp['bytes_per_pass']}")
    for r in fp["read_results"]:
        print(
            f"read pass {r['pass']} [{r['label']}]: "
            f"{r['duration_s']:.6f}s, {r['MiB_per_s']:.3f} MiB/s"
        )

    print()
    for r in rr["runs"]:
        print(r["name"])
        print(f"  first HTTP: {r['first_http_ms']:.3f} ms")
        print(f"  ready: {r['ready_ms']:.3f} ms")
        print(f"  first inference complete: {r['first_inference_complete_ms']:.3f} ms")
        print(f"  smoke duration: {r['smoke']['duration_ms']:.3f} ms")

    print()
    print("INTERPRETATION BOUNDARY")
    print("- first measured file/start run is not automatically cold")
    print("- second run is after prior same-model access and may benefit from cache")
    print("- read throughput and readiness are different measurements")
    print("- steady PP/TG must be benchmarked separately")

if __name__=="__main__":
    main()
