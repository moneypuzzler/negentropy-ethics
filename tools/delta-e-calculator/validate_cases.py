#!/usr/bin/env python3
"""Validate golden cases against calc.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALC = ROOT / "tools" / "delta-e-calculator" / "calc.py"
CASES = ROOT / "cases" / "golden-cases.json"


def run_case(case: dict) -> tuple[bool, str]:
    cmd = [
        sys.executable,
        str(CALC),
        "--di",
        str(case["delta_i"]),
        "--dp",
        str(case["delta_p"]),
        "--dc",
        str(case["delta_c"]),
        "--dx",
        str(case["delta_x"]),
        "--json",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, f"{case['id']}: calc failed: {proc.stderr.strip()}"

    result = json.loads(proc.stdout)
    if result["delta_e"] != case["expected_delta_e"]:
        return (
            False,
            f"{case['id']}: expected ΔE {case['expected_delta_e']} got {result['delta_e']}",
        )
    if case["expected_verdict_contains"] not in result["verdict"]:
        return (
            False,
            f"{case['id']}: verdict mismatch, expected contains '{case['expected_verdict_contains']}', got '{result['verdict']}'",
        )
    return True, f"{case['id']}: ok"


def main() -> int:
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    failed = 0
    for case in cases:
        ok, msg = run_case(case)
        print(msg)
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
