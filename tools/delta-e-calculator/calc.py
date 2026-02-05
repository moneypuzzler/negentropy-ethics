#!/usr/bin/env python3
"""Negentropy Ethics ΔE calculator (CLI)."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass


@dataclass
class Score:
    delta_i: int
    delta_p: int
    delta_c: int
    delta_x: int

    def validate(self) -> None:
        for name, value in {
            "ΔI": self.delta_i,
            "ΔP": self.delta_p,
            "ΔC": self.delta_c,
            "ΔX": self.delta_x,
        }.items():
            if value < -5 or value > 5:
                raise ValueError(f"{name} must be within [-5, 5], got {value}")

    @property
    def delta_e(self) -> int:
        return self.delta_i + self.delta_p + self.delta_c + 2 * self.delta_x

    @property
    def verdict(self) -> str:
        if self.delta_x >= 3:
            return "evil (absolute externalization rule: ΔX ≥ +3)"
        if self.delta_e < 0:
            return "good"
        if self.delta_e > 0:
            return "evil"
        return "neutral"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute ΔE score and verdict")
    parser.add_argument("--di", type=int, required=True, help="ΔI in [-5,5]")
    parser.add_argument("--dp", type=int, required=True, help="ΔP in [-5,5]")
    parser.add_argument("--dc", type=int, required=True, help="ΔC in [-5,5]")
    parser.add_argument("--dx", type=int, required=True, help="ΔX in [-5,5]")
    parser.add_argument("--json", action="store_true", help="print JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    score = Score(delta_i=args.di, delta_p=args.dp, delta_c=args.dc, delta_x=args.dx)
    try:
        score.validate()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = {
        "delta_i": score.delta_i,
        "delta_p": score.delta_p,
        "delta_c": score.delta_c,
        "delta_x": score.delta_x,
        "delta_e": score.delta_e,
        "verdict": score.verdict,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ΔE = {score.delta_e}")
        print(f"verdict: {score.verdict}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
