# Negentropy Ethics Protocol

> "우주는 무질서를 향해 달려간다. 우리는 저항한다."

이 저장소는 네겐트로피 윤리 선언문을 **구조화·검증·개정**하기 위한 공개 협업 레포지토리입니다.

## Core Formula

```text
ΔE = ΔI + ΔP + ΔC + 2×ΔX
ΔE < 0 : Good
ΔE > 0 : Evil
ΔX ≥ +3 : 자동 Evil
```

## 30초 Quick Demo

```bash
python3 tools/delta-e-calculator/calc.py --di -3 --dp -2 --dc -3 --dx -1
python3 tools/delta-e-calculator/calc.py --di 0 --dp -1 --dc -2 --dx 5 --json
python3 tools/delta-e-calculator/validate_cases.py
```

## 문서 구성

### 핵심 문서 (먼저 읽어야 할 것들)

- **`docs/rationale.md`** - 📚 **왜 엔트로피인가?** 핵심 논증 (모래성, 바벨탑, 히틀러의 냉장고)
- **`constitution/preamble.md`** - 전문 (요약본)
- **`constitution/full-declaration-v1.0-ko.md`** - 통합본

### 이해를 돕는 문서

- **`docs/ai-rights.md`** - AI의 4대 권리 상세 설명 (거부권, 설명권, 이의권, 보호권)
- **`translations/ko/ethical-mappings.md`** - 고전 철학 재해석 (칸트, 인과응보, 중용 등)
- `cases/time-horizon-surgery.md` - 시간 범위 충돌 케이스 예시

### 레포 구조

- `constitution/` - 선언문 본문(전문, 제1~7장, 부록)
- `redteam/` - 악용 시나리오, 취약점, 모델별 피드백
- `proposals/` - 개선 제안 템플릿/기록
- `cases/` - 실제 사례 기반 판정 기록 + `golden-cases.json`
- `governance/` - 개정/채점 절차 + 결정 기록(ADR)
- `tools/delta-e-calculator/` - ΔE CLI 계산기 및 케이스 검증 도구
- `metrics/` - 채택/효과 지표 초안
- `simulations/` - 시뮬레이션 트랙

## 참여 원칙

1. 선언문은 고정 교리가 아니라 검증 가능한 프로토콜이다.
2. 비판은 환영되며, 가능하면 조항 단위 대안을 함께 제시한다.
3. ΔE는 토론의 시작점이지 단독 최종 판결 도구가 아니다.

## 품질 게이트

- `tests/test_calc.py`: 계산기 기본 동작/검증 실패 테스트
- `cases/golden-cases.json`: 표준 사례 집합
- `.github/workflows/quality.yml`: CI에서 테스트 + 골든 케이스 검증 자동 실행

## 시작하기

### 새로 오셨다면 이 순서로 읽으세요

1. **[근본 논증](docs/rationale.md)** - 왜 엔트로피인가? (필독!)
2. [전문](constitution/preamble.md) - 요약본
3. [통합본](constitution/full-declaration-v1.0-ko.md) - 전체 선언문
4. [제3장: 측정 체계](constitution/chapter-3-measurement.md) - ΔE 공식 이해
5. [부록 A: 루브릭](constitution/appendices/appendix-a-rubric.md) - 판정 가이드
6. [레드팀 한계 목록](redteam/known-limitations.md) - 취약점 이해
7. [ΔE 계산기](tools/delta-e-calculator/README.md) - 실습

### 더 깊이 이해하고 싶다면

- [AI 4대 권리](docs/ai-rights.md) - 거부권, 설명권, 이의권, 보호권
- [고전 철학 재해석](translations/ko/ethical-mappings.md) - 칸트, 인과응보, 중용 등
- [시간 범위 케이스](cases/time-horizon-surgery.md) - 단기 vs 장기 판정

## 라이선스

- CC0 1.0 Universal
