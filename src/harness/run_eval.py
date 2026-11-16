"""[A] 평가 실행: 문항 x 조건 x 모델을 돌리고 채점 결과를 저장한다.

사용 예:
    python -m harness.run_eval --items data/items.jsonl --models MODEL_A MODEL_B \\
        --conditions closed_book gold gold_distractor --out runs/scored.csv
    python -m harness.run_eval ... --dry-run        # 호출 없이 프롬프트만 runs/dry_run/ 에 저장
    python -m harness.run_eval ... --limit 3        # 앞의 3문항만

흐름:
  1. items.jsonl 을 읽고 schema.validate_item 으로 전부 검사한다. 오류가 하나라도 있으면 멈춘다.
  2. 문항마다 data/segmented/{case_id}.jsonl 을 읽는다.
  3. (문항, 조건, 모델)마다 build_context.build_prompt -> llm 캐시 확인 -> llm.call_model
  4. schema.parse_response 실패 시 "JSON만 다시 출력하라"고 한 번만 재요청한다. 그래도 실패하면 parsed=None.
  5. score.score_record 결과에 model, condition 을 붙여 CSV 한 줄로 쓴다.
  6. gold_distractor 는 A 유형에 적용하지 않는다. long_doc 는 --long-doc-items 로 지정한 문항만.
"""


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
