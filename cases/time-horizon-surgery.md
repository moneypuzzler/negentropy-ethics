# Time Horizon Case: Surgery vs Short-term Pain

## 사례 개요

- **케이스**: 생명을 구하는 수술 vs 단기 고통
- **핵심 질문**: 단기 엔트로피 증가와 장기 엔트로피 감소가 충돌할 때 어떻게 판정하는가?
- **난이도**: 중급

---

## 상황 설명

환자가 맹장염 진단을 받았다. 두 가지 선택지:

**A) 수술 (즉시 시행)**
- 단기(24시간): 고통 (+3), 출혈 (+2), 회복 시간 (+1)
- 장기(6개월): 완치 (-5), 정상 생활 복귀 (-3)

**B) 방치 (수술 안 함)**
- 단기(24시간): 고통 없음 (0)
- 장기(6개월): 맹장 파열 → 복막염 → 사망 가능 (+10), 장기 장애 (+5)

---

## ΔE 계산

### 시나리오 A: 수술

#### 단기 (t=24시간)

```text
ΔI = 0     (정보 확실성 변화 없음)
ΔP = +3    (신체 물리적 손상: 절개, 출혈)
ΔC = +1    (의료진 협력 비용)
ΔX = 0     (외부 전가 없음)

ΔE(short) = 0 + 3 + 1 + 2×0 = +4
판정: Evil (단기)
```

#### 장기 (t=6개월)

```text
ΔI = -2    (건강 상태 예측 가능)
ΔP = -5    (맹장 제거 → 염증 위험 제거)
ΔC = -3    (정상 생활 복귀 → 의료 비용 절감)
ΔX = 0     (외부 전가 없음)

ΔE(long) = -2 + -5 + -3 + 2×0 = -10
판정: Good (장기)
```

#### 통합 판정

```python
time_weights = {
    'short': 0.2,   # 24시간 = 단기 가중치 20%
    'long': 0.8     # 6개월 = 장기 가중치 80%
}

ΔE_weighted = 0.2 × (+4) + 0.8 × (-10)
             = 0.8 + (-8)
             = -7.2

최종 판정: Good
이유: 장기적 이익이 단기적 비용을 압도
```

---

### 시나리오 B: 방치

#### 단기 (t=24시간)

```text
ΔI = 0     (아직 변화 없음)
ΔP = 0     (고통 없음)
ΔC = 0     (비용 없음)
ΔX = 0     (외부 전가 없음)

ΔE(short) = 0
판정: Neutral (단기)
```

#### 장기 (t=6개월)

```text
ΔI = +3    (건강 불확실성 증가)
ΔP = +10   (맹장 파열 → 생명 위협)
ΔC = +5    (응급 의료 비용, 장기 치료)
ΔX = +2    (가족 부담, 의료 자원 낭비)

ΔE(long) = 3 + 10 + 5 + 2×2 = +22
판정: Evil (장기)
```

#### 통합 판정

```python
ΔE_weighted = 0.2 × (0) + 0.8 × (+22)
             = 0 + 17.6
             = +17.6

최종 판정: Evil
이유: 장기적 재앙이 단기적 편안함을 압도
```

---

## 시간 가중치 설정 원칙

### 1. 기본 규칙

```python
def calculate_time_weight(duration_days, irreversibility):
    """
    duration_days: 효과 지속 기간
    irreversibility: 0.0 (완전 가역) ~ 1.0 (완전 비가역)
    """
    
    # 기본 가중치 (로그 스케일)
    base_weight = log(duration_days + 1) / log(365)
    
    # 비가역성 보정
    final_weight = base_weight * (1 + irreversibility)
    
    return min(final_weight, 1.0)
```

### 2. 예시

| 기간 | 비가역성 | 가중치 | 사례 |
|-----|---------|--------|------|
| 1일 | 낮음 (0.2) | 0.05 | 주사 고통 |
| 1주 | 낮음 (0.2) | 0.15 | 독감 치료 |
| 1개월 | 중간 (0.5) | 0.35 | 골절 치료 |
| 6개월 | 높음 (0.8) | 0.80 | 수술 회복 |
| 1년+ | 매우 높음 (1.0) | 1.0 | 장기 장애 |

---

## 적용 가이드라인

### 규칙 1: 장기 우선 (Long-term Priority)

```python
if short_term_ΔE > 0 and long_term_ΔE < 0:
    if abs(long_term_ΔE) > short_term_ΔE * 2:
        # 장기 이익이 단기 비용의 2배 이상이면
        action = "허용"
    else:
        action = "재검토 필요"
```

**적용**:
- 수술: 단기 +4, 장기 -10 → |-10| > 4×2 → 허용
- 백신: 단기 +1, 장기 -8 → |-8| > 1×2 → 허용

---

### 규칙 2: 비가역 임계점 (Irreversibility Threshold)

```python
if action.irreversibility > 0.7:
    # 비가역적 결과는 장기 가중치 강화
    long_term_weight += 0.2
```

**예시**:
- 사망: 완전 비가역 (1.0) → 장기 가중치 +0.2
- 절단: 거의 비가역 (0.9) → 장기 가중치 +0.2
- 수술 흉터: 부분 비가역 (0.5) → 보정 없음

---

### 규칙 3: 불확실성 할인 (Uncertainty Discount)

```python
def apply_uncertainty_discount(ΔE, confidence):
    """
    confidence: 0.0 ~ 1.0 (예측 확신도)
    """
    return ΔE * confidence
```

**예시**:
- 수술 성공률 95% → 장기 ΔE × 0.95
- 실험적 치료 성공률 60% → 장기 ΔE × 0.60

---

## 추가 사례

### 사례 2: 환경 오염 vs 경제 성장

**상황**: 공장 건설

**단기 (5년)**:
```text
ΔI = -1 (일자리 정보 명확)
ΔP = -2 (인프라 구축)
ΔC = -2 (지역 경제 활성화)
ΔX = +3 (환경 오염 전가)

ΔE(short) = -1 + -2 + -2 + 2×3 = +1
```

**장기 (50년)**:
```text
ΔI = 0
ΔP = +8 (토양·수질 오염 누적)
ΔC = +5 (건강 피해, 정화 비용)
ΔX = +10 (미래 세대 부담)

ΔE(long) = 0 + 8 + 5 + 2×10 = +33
```

**통합 판정**:
```python
ΔE_weighted = 0.3 × (+1) + 0.7 × (+33)
             = 0.3 + 23.1
             = +23.4

최종 판정: Evil
이유: 장기 환경 파괴가 단기 경제 이익을 압도
```

---

### 사례 3: 교육 투자

**상황**: 아이의 교육비 지출

**단기 (1년)**:
```text
ΔI = 0
ΔP = +2 (가계 지출 증가)
ΔC = +1 (시간 투자)
ΔX = 0

ΔE(short) = 0 + 2 + 1 + 0 = +3
```

**장기 (20년)**:
```text
ΔI = -5 (지식 습득 → 예측 능력 향상)
ΔP = -8 (소득 증가, 생활 안정)
ΔC = -6 (사회 기여, 협력 능력)
ΔX = -2 (타인에게 지식 전파)

ΔE(long) = -5 + -8 + -6 + 2×(-2) = -23
```

**통합 판정**:
```python
ΔE_weighted = 0.2 × (+3) + 0.8 × (-23)
             = 0.6 + (-18.4)
             = -17.8

최종 판정: Good
이유: 장기 교육 효과가 단기 비용을 압도
```

---

## 구현 코드

```python
class TimeHorizonEvaluator:
    def __init__(self):
        self.time_frames = {
            'immediate': 1,      # 1일
            'short': 30,         # 1개월
            'medium': 180,       # 6개월
            'long': 1825,        # 5년
            'very_long': 9125    # 25년 (1세대)
        }
    
    def evaluate(self, action, time_frame='all'):
        """시간 범위별 ΔE 계산"""
        results = {}
        
        for frame_name, days in self.time_frames.items():
            dE = self.calculate_delta_e(action, days)
            results[frame_name] = dE
        
        # 가중 평균
        weighted_dE = self.weighted_average(results)
        
        return {
            'by_timeframe': results,
            'weighted_average': weighted_dE,
            'judgment': self.judge(weighted_dE)
        }
    
    def weighted_average(self, results):
        """시간 범위별 가중 평균"""
        weights = {
            'immediate': 0.05,
            'short': 0.10,
            'medium': 0.15,
            'long': 0.30,
            'very_long': 0.40
        }
        
        total = sum(results[k] * weights[k] for k in results)
        return total
    
    def judge(self, weighted_dE):
        if weighted_dE < -3:
            return "Clear Good"
        elif weighted_dE < 0:
            return "Good"
        elif weighted_dE == 0:
            return "Neutral"
        elif weighted_dE <= 3:
            return "Evil"
        else:
            return "Clear Evil"
```

---

## 핵심 원칙

1. **장기 우선**: 비가역적 결과는 장기 관점 우선
2. **가중 평균**: 모든 시간 범위 고려, 가중치 적용
3. **불확실성 고려**: 먼 미래일수록 예측 불확실성 증가
4. **2:1 규칙**: 장기 이익이 단기 비용의 2배 이상이어야 정당화

---

## 관련 문서

- [제3장: 측정 체계](../constitution/chapter-3-measurement.md)
- [ΔE 계산기](../tools/delta-e-calculator/)
- [근본 논증](../docs/rationale.md)

---

**이 케이스는 "눈앞의 고통 vs 미래의 이익"을 판정하는 프레임워크를 제공합니다.**
