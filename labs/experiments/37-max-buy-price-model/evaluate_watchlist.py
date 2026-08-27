#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    d = json.loads(Path(__file__).with_name("scenario.json").read_text())
    b = d["budget"]
    ceiling = (
        b["total"]
        - b["platform_extra"]
        - b["psu_cooling"]
        - b["energy"]
        - b["repair_reserve"]
        - b["maintenance_reserve"]
        + b["expected_resale"]
    )
    watch_limit = ceiling * (1 + d["watch_band_pct"] / 100)

    print("SYNTHETIC ONLY")
    print(f"max_sticker={ceiling:.0f}")
    print(f"watch_limit={watch_limit:.0f}")
    print()

    for c in d["candidates"]:
        if c["fit"] != "PASS" or c["software"] != "PASS":
            status = "SKIP"
        elif c["performance"] != "PASS":
            status = "NEEDS EVIDENCE" if c["performance"] == "UNKNOWN" else "SKIP"
        elif not c["evidence_ok"]:
            status = "NEEDS EVIDENCE"
        elif c["ask"] <= ceiling:
            status = "BUY-CANDIDATE"
        elif c["ask"] <= watch_limit:
            status = "WATCH"
        else:
            status = "OVERPRICED"

        print(f"{c['name']}: ask={c['ask']} status={status}")

if __name__ == "__main__":
    main()
