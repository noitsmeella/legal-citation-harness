# 데이터

| 경로 | 내용 | 만드는 방법 |
|---|---|---|
| `candidates.csv` | 판결문 후보와 선정 기준 채점 (떨어진 후보 포함) | 손으로 |
| `cases.csv` | 최종 선정 판결의 메타데이터 | 손으로 |
| `raw/{case_id}.txt` | 판결문 원문 (UTF-8) | 웹에서 복사 |
| `segmented/{case_id}.jsonl` | 문장 분할 결과 + 역할 라벨 | `segment.py` 후 손으로 라벨 |
| `items.jsonl` | 문항 | 손으로 (스프레드시트 → 변환) |
| `claims/{case_id}.jsonl` | 검증기 평가용 주장 쌍 | 손으로 |

## case_id 규칙

`KR-001`, `US-001`처럼 관할 + 세 자리 번호. 한 번 정한 번호는 바꾸지 않는다. 떨어진 후보는 `candidates.csv`에만 남는다.

## 선정 기준 (candidates.csv의 c1~c7, 해당하면 1)

| 열 | 기준 |
|---|---|
| c1_reversed | 원심 파기(파기환송) 또는 Reversed / Vacated |
| c2_allegation | 당사자 주장이 명시적으로 서술됨 |
| c3_lower_court | 원심 판단이 서술됨 |
| c4_citation | 인용 판례 2개 이상, 그중 구별된 판례 있음 |
| c5_dissent | 반대·별개·보충의견 있음 |
| c6_temporal | 개정 전 조문이나 변경된 법리 언급 |
| c7_recent | 2020년 이후 선고 |

4점 이상을 채택 후보로 본다. 분량(한국 5~20쪽, 미국 10~40쪽)은 메모에 적는다.

## segmented 형식

```json
{"sid": "S12", "text": "원심은 …라고 판단하였다.", "role": "LOWER_COURT", "attr": "배척", "note": ""}
```

`role`과 `attr`은 `segment.py` 실행 후 손으로 채운다. 값은 `docs/codebook.md`를 따른다.

## items 형식

한 줄에 문항 하나. 필드 설명과 검사 규칙은 `src/harness/schema.py`의 `validate_item`에 있다. 예시는 `tests/conftest.py`의 `item_b`(가상 판결문 기반)를 본다.

| 필드 | 설명 |
|---|---|
| item_id | `{case_id}-{유형}{번호}`, 예: `KR-001-B1` |
| item_type | A 명확 · B 언급-채택 · C 인용-채택 · D 반대의견 · E 시간적 · F 불충분 |
| question_target | COURT (법원의 판단을 묻는 질문) 또는 PARTY (당사자의 주장을 묻는 귀속 질문) |
| gold_answer | 정답. F 유형은 `INSUFFICIENT` |
| gold_evidence_ids / gold_evidence_role | 정답 근거 문장과 그 역할 |
| distractor_ids / distractor_roles | 함정 문장과 그 역할 |
| context_gold | gold 조건에서 줄 문장 범위, 예: `S38-S45` |
| context_distractor | gold_distractor 조건에서 줄 범위, 예: `S12-S16,S38-S45` |
| evidence_position | 판결문 안에서 근거 위치: early / middle / late |

## claims 형식

```json
{"claim_id": "KR-001-C1", "case_id": "KR-001", "claim": "대법원은 피고인의 행위를 정당방위로 인정하였다.", "claim_target": "COURT", "gold_verdict": "MISATTRIBUTED", "source_item_id": "KR-001-B1"}
```

문항 하나에서 옳은 주장(SUPPORTED)과 함정에 기반한 틀린 주장(MISATTRIBUTED)을 한 쌍씩 만든다.
