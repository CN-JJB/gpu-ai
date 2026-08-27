#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    base = Path(__file__).parent
    cases = json.loads((base / "cases.json").read_text(encoding="utf-8"))
    answers = json.loads((base / "student_answers.json").read_text(encoding="utf-8"))

    passed = 0
    for case in cases:
        ans = answers.get(case["id"], {})
        ok = (
            ans.get("bottleneck") == case["expected_bottleneck"]
            and ans.get("next") == case["expected_next"]
        )
        passed += int(ok)
        print(
            f"[{'PASS' if ok else 'FAIL'}] {case['id']}: "
            f"bottleneck={ans.get('bottleneck')!r}, next={ans.get('next')!r}"
        )
        if not ok:
            print(
                f"       expected bottleneck={case['expected_bottleneck']!r}, "
                f"next={case['expected_next']!r}"
            )

    print()
    print(f"score: {passed}/{len(cases)}")
    raise SystemExit(0 if passed == len(cases) else 1)

if __name__ == "__main__":
    main()
