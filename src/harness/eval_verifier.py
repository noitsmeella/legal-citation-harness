"""[B] 검증기 평가: data/claims/*.jsonl 의 주장 쌍으로 판정 정확도를 잰다.

주장 파일 형식 (한 줄에 하나):
  {"claim_id", "case_id", "claim", "claim_target", "gold_verdict", "source_item_id"}

비교:
  - 역할 사용 검증기 (use_roles=True)  vs  내용 일치만 보는 기준선 (use_roles=False)
  - 역할 라벨: 사람이 붙인 것 vs role_tagger 가 붙인 것

보고 지표: 전체 정확도, 판정별 정밀도·재현율, 특히 MISATTRIBUTED 의 재현율 (오귀속을 얼마나 잡는가).
"""


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
