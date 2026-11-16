# 강의 연동 명세 (C층)

강의 시스템(예: edu.kail.kr)이 검증기를 호출할 때 쓰는 입출력 규격이다. 실제 연결은 이 프로젝트 범위 밖이며, 이 명세와 오프라인 시연까지가 범위다.

## 호출

```python
from harness.verifier import verify
result = verify(claim, sentences, claim_target="COURT")
```

## 요청

```json
{
  "claim": "대법원은 피고인의 행위를 정당방위로 인정하였다.",
  "claim_target": "COURT",
  "case_id": "KR-001",
  "source": {"lecture_id": "형법-07", "timestamp": "00:12:34"}
}
```

| 필드 | 필수 | 설명 |
|---|---|---|
| claim | 예 | 강의록에서 뽑은 판례 관련 주장 한 문장 |
| claim_target | 예 | COURT 또는 PARTY |
| case_id | 예 | `data/segmented/`에 있는 판결 |
| source | 아니오 | 강의 위치. 결과에 그대로 돌려준다 |

## 응답

```json
{
  "verdict": "MISATTRIBUTED",
  "evidence": [
    {"sid": "S3", "text": "원심은 … 정당방위를 인정하고 무죄를 선고하였다.", "role": "LOWER_COURT"}
  ],
  "reason": "주장 내용은 원심 판단에 있으나, 대법원은 이를 배척하였다.",
  "warnings": ["source role: LOWER_COURT"],
  "court_view": [
    {"sid": "S6", "text": "그런데도 … 원심판단에는 정당방위에 관한 법리를 오해한 잘못이 있다.", "role": "HOLDING"}
  ],
  "source": {"lecture_id": "형법-07", "timestamp": "00:12:34"},
  "verifier_version": "0.1.0"
}
```

| verdict | 강의 화면에서의 표시 (제안) |
|---|---|
| SUPPORTED | 근거 문장 링크 |
| MISATTRIBUTED | 경고: "이 내용은 ○○의 주장/판단입니다" + 법원 판단 함께 표시 |
| UNSUPPORTED | 경고: "판결문에서 근거를 찾지 못했습니다" |
| ABSTAIN | 안내: "확인 필요" |

## 시연 계획

강의록에서 판례 인용 15~20건을 뽑아 `cli.py`로 돌리고, 판정과 사람의 판단을 표로 비교한다.
