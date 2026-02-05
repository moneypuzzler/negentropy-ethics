import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "tools" / "delta-e-calculator" / "calc.py"


def run_calc(*args: str):
    proc = subprocess.run(
        [sys.executable, str(CALC), *args],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


class CalcTests(unittest.TestCase):
    def test_good_case_plain_output(self):
        code, out, err = run_calc("--di", "-3", "--dp", "-2", "--dc", "-3", "--dx", "-1")
        self.assertEqual(code, 0)
        self.assertIn("ΔE = -10", out)
        self.assertIn("verdict: good", out)
        self.assertEqual(err, "")

    def test_absolute_externalization_rule(self):
        code, out, err = run_calc("--di", "0", "--dp", "-1", "--dc", "-2", "--dx", "5", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["delta_e"], 7)
        self.assertTrue(data["verdict"].startswith("evil (absolute externalization rule"))
        self.assertEqual(err, "")

    def test_validation_error_out_of_range(self):
        code, out, err = run_calc("--di", "6", "--dp", "0", "--dc", "0", "--dx", "0")
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("must be within [-5, 5]", err)


if __name__ == "__main__":
    unittest.main()
