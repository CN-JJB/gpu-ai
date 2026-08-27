#!/usr/bin/env python3
import json
from pathlib import Path

def main():
    base = Path(__file__).parent
    cases = json.loads((base / "cases.json").read_text(encoding="utf-8"))
    answers = json.loads((base / "student_answers.json").read_text(encoding="utf-8"))
    passed = 0
    for case in cases:
        got = answers.get(case["id"])
        exp = case["expected"]
        ok = got == exp
        passed += int(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {case['id']}: got={got}, expected={exp}")
        print("       ", case["summary"])
    print()
    print(f"score: {passed}/{len(cases)}")
    raise SystemExit(0 if passed == len(cases) else 1)

if __name__ == "__main__":
    main()
