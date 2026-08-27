#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--out", type=Path, default=Path("PACKET.json"))
    a = p.parse_args()

    records = []
    seen = set()

    for path in a.files:
        resolved = str(path.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)

        if not path.is_file():
            raise SystemExit(f"not a file: {path}")

        records.append({
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    packet = {
        "packet_schema_version": 1,
        "file_count": len(records),
        "files": records,
    }

    a.out.write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"wrote {a.out} with {len(records)} files")
    for r in records:
        print(f"{r['sha256']}  {r['path']}")

if __name__ == "__main__":
    main()
