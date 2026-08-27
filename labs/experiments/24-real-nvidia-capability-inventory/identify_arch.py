#!/usr/bin/env python3
import csv
import io
import subprocess

def architecture(major, minor):
    cc = major + minor / 10
    if major == 1:
        return "Tesla / early CUDA"
    if major == 2:
        return "Fermi"
    if major == 3:
        return "Kepler"
    if major == 5:
        return "Maxwell"
    if major == 6:
        return "Pascal"
    if major == 7 and minor == 0:
        return "Volta"
    if major == 7 and minor == 5:
        return "Turing"
    if major == 8 and minor in (0, 6):
        return "Ampere"
    if major == 8 and minor == 9:
        return "Ada Lovelace"
    if major == 9 and minor == 0:
        return "Hopper"
    if major in (10, 12):
        return "Blackwell (current mapping; exact branch/SKU still required)"
    return "Unknown/newer mapping — check current NVIDIA compute-capability docs"

def main():
    cmd = [
        "nvidia-smi",
        "--query-gpu=name,compute_cap",
        "--format=csv,noheader,nounits",
    ]
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or "nvidia-smi query failed")

    for row in csv.reader(io.StringIO(p.stdout)):
        if len(row) < 2:
            continue
        name = row[0].strip()
        cc_text = row[1].strip()
        try:
            major_s, minor_s = cc_text.split(".", 1)
            major, minor = int(major_s), int(minor_s)
        except Exception:
            print(f"{name}: compute_cap={cc_text!r} → unable to parse")
            continue
        print(f"{name}: compute capability {major}.{minor} → {architecture(major, minor)}")

if __name__ == "__main__":
    main()
