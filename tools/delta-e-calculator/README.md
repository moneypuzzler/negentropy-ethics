# ΔE Calculator

CLI로 ΔE를 계산하는 도구이며, 골든 케이스 검증 스크립트를 포함합니다.

## 사용법

```bash
python3 tools/delta-e-calculator/calc.py --di -3 --dp -2 --dc -3 --dx -1
```

JSON 출력:

```bash
python3 tools/delta-e-calculator/calc.py --di 4 --dp 3 --dc 3 --dx 2 --json
```

## 골든 케이스 검증

```bash
python3 tools/delta-e-calculator/validate_cases.py
```

## 규칙

- 입력 범위: 각 항목 -5 ~ +5
- 공식: `ΔE = ΔI + ΔP + ΔC + 2×ΔX`
- 절대 규칙: `ΔX ≥ +3` 이면 자동 `evil`
