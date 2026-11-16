# 담화 역할 코드북 v0.1

> 상태: 초안. 예문은 실제 선정 판결의 문장으로 바꿔 채운다. 바뀐 내용은 맨 아래 변경 기록에 남긴다.

## 목적

판결문의 각 문장이 **누구의 말인지, 어떤 기능을 하는지**를 표시한다. 이 표시는 (A) 문항의 정답 근거와 함정을 정하는 기준, (B) 검증기의 역할 분류 정답지로 쓰인다.

## 분류 단위

- 기본은 `segment.py`가 나눈 문장이다.
- 한 문장에 두 역할이 섞이면 절 단위로 손으로 나눈다. 나눈 조각은 `S12a`, `S12b`처럼 표기한다.
- 판결문 머리(사건번호, 당사자 표시)와 주문 제목 같은 표지는 라벨하지 않는다 (`role` 빈칸).

## 역할 7개

| 역할 | 정의 | 하위 속성 (`attr`) |
|---|---|---|
| FACT | 법원이 인정한 사실관계 | |
| ALLEGATION | 당사자의 주장, 상고이유 | 발화자: 검사 / 피고인 / 원고 / 피고 |
| LOWER_COURT | 원심·1심 판단의 서술 | 결과: 유지 / 배척 |
| HOLDING | 당해 법원의 판시·결론 | |
| REASONING | 당해 법원의 판단 이유 | |
| QUOTATION | 인용된 판례·법령 | 목적: 채택 / 구별 |
| SEPARATE_OPINION | 법관의 개별 의견 | 유형: 반대 / 별개 / 보충 |

### FACT
- 포함: "원심이 적법하게 채택한 증거에 의하면 ~ 사실을 알 수 있다", "The record shows…"
- 제외: 당사자가 주장하는 사실 (→ ALLEGATION)
- 예문 (KR): TODO
- 예문 (US): TODO

### ALLEGATION
- 단서: "상고이유 주장의 요지는", "피고인은 ~라고 주장한다", "Appellant contends", "The government argues"
- 예문 (KR): TODO
- 예문 (US): TODO

### LOWER_COURT
- 단서: "원심은 ~라고 판단하였다", "제1심은", "The district court held / found"
- 예문 (KR): TODO
- 예문 (US): TODO

### HOLDING
- 단서: "~라고 봄이 상당하다", "원심판결을 파기하고", "We hold", "Accordingly, we affirm / reverse"
- 예문 (KR): TODO
- 예문 (US): TODO

### REASONING
- 단서: "~이므로", "따라서", "Because", "This is so because"
- 예문 (KR): TODO
- 예문 (US): TODO

### QUOTATION
- 단서: "(대법원 ○. ○. ○. 선고 ○도○ 판결 등 참조)", "See", "Cf.", "distinguishable"
- 예문 (KR): TODO
- 예문 (US): TODO

### SEPARATE_OPINION
- 단서: "대법관 ○○○의 반대의견은 다음과 같다", "dissenting", "concurring"
- 보충의견은 다수의견을 지지하는 의견이므로 문항에서 함정으로 쓸 때 주의한다.
- 예문 (KR): TODO
- 예문 (US): TODO

## 헷갈리는 쌍의 구분 규칙

1. **ALLEGATION vs LOWER_COURT**: 주어가 당사자면 ALLEGATION, 원심·제1심 법원이면 LOWER_COURT. 법원이 당사자 주장을 요약만 하는 문장도 ALLEGATION.
2. **REASONING vs HOLDING**: 결론 자체("~라고 판단한다", 주문 관련)는 HOLDING, 그 결론에 이르는 이유는 REASONING. 한 문장에 둘 다 있으면 절로 나눈다.
3. **QUOTATION 채택 vs 구별**: 당해 법원이 그 법리를 따르면 채택, "이 사건과는 사안이 달라" 등으로 배제하면 구별.

## 애매할 때

문장의 **문법상 주어가 누구인지**로 먼저 판단한다. 그래도 애매하면 `note`에 이유를 적고 넘어간다. 애매한 사례는 지도교수 면담 때 질문으로 가져간다.

## 변경 기록

| 버전 | 날짜 | 바뀐 점 |
|---|---|---|
| v0.1 | 2026-11 | 초안. 계획서의 6역할에 LOWER_COURT를 추가하고 반대의견을 SEPARATE_OPINION으로 확장 |
