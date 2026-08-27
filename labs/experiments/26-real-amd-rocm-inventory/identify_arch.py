#!/usr/bin/env python3
import re
import shutil
import subprocess

def map_gfx(gfx):
    if re.fullmatch(r"gfx8\d+", gfx):
        return "GCN / Polaris-era (exact GCN generation still needs ASIC lookup)"
    if gfx in {"gfx900", "gfx902", "gfx904", "gfx906", "gfx909"}:
        return "Vega / GCN5-era"
    if gfx == "gfx908":
        return "CDNA / MI100"
    if gfx == "gfx90a":
        return "CDNA2 / MI200"
    if gfx == "gfx942":
        return "CDNA3 / MI300"
    if gfx == "gfx950":
        return "CDNA4 / MI350"
    if gfx.startswith("gfx101"):
        return "RDNA"
    if gfx.startswith("gfx103"):
        return "RDNA2"
    if gfx.startswith("gfx110"):
        return "RDNA3"
    if gfx.startswith("gfx115"):
        return "RDNA3.5"
    if gfx.startswith("gfx120"):
        return "RDNA4"
    return "Unknown/new/current target — check AMD ROCm architecture docs"

def main():
    if not shutil.which("rocminfo"):
        raise SystemExit("rocminfo not found; install/use ROCm tools or inspect saved inventory manually")

    p = subprocess.run(["rocminfo"], text=True, capture_output=True)
    text = p.stdout + "\n" + p.stderr
    targets = sorted(set(re.findall(r"\bgfx[0-9a-z]+\b", text)))

    if not targets:
        raise SystemExit("no gfx target found in rocminfo output")

    for gfx in targets:
        print(f"{gfx} → {map_gfx(gfx)}")

if __name__ == "__main__":
    main()
