# 분석 계획서

> 본 실험 전에 동결한다. 동결 후 바꾼 것은 맨 아래에 날짜와 이유를 적는다.
> 동결일: TODO

## 데이터

문항 수, 유형·관할별 개수, 코드북 버전: TODO

## 조건과 모델

| 조건 | 적용 문항 |
|---|---|
| closed_book | 전체 |
| gold | 전체 |
| gold_distractor | B~F |
| long_doc | 지정한 N문항 |

모델 이름, 버전 문자열, 접근 경로, temperature: TODO

## 가설

| | 내용 | 구분 |
|---|---|---|
| H1 | gold_distractor 정답률 < gold 정답률. 차이는 A보다 B·C·D에서 크다 | 주 |
| H2 | 함정 역할에 따라 오류율이 다르다. ALLEGATION·LOWER_COURT에서 가장 높을 것 | 주 |
| H3 | long_doc에서 근거가 중간에 있을 때 근거 정확도가 가장 낮다 | 탐색 |
| H4 | 모델 간 오류 유형 분포는 정답률 순위와 다를 수 있다 | 탐색 |
| H5 | 답은 맞고 근거는 틀린(RWR) 응답이 있어 정답률만으로 순위가 바뀐다 | 탐색 |
| H6 | 한국 데이터에서 LOWER_COURT 함정의 효과가 더 크다 | 탐색 |
| H7 | 역할 사용 검증기의 MISATTRIBUTED 재현율 > 기준선 | 주 (B층) |

## 지표

`src/harness/score.py` 정의를 따른다: answer_correct, evidence_exact, evidence_f1, role_correct, hit_distractor, rwr, 파싱 실패율. 검증기는 판정별 정밀도·재현율.

## 모형

기본은 기술통계와 혼동행렬. 여유가 있으면:

```
correct ~ condition * jurisdiction + item_type + model + (1 | item_id) + (1 | case_id)
```

표본이 작으므로 p값보다 효과크기와 95% 신뢰구간을 보고한다.

## 제외·재시도 규칙

JSON 파싱 실패 시 1회 재요청. 그래도 실패하면 오답으로 처리하고 파싱 실패율을 따로 보고한다.

## 동결 후 변경

| 날짜 | 변경 | 이유 |
|---|---|---|
