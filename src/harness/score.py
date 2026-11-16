"""모델 응답 하나를 문항의 정답과 비교해 채점한다.

지표 정의는 docs/analysis_plan.md 와 같다.
"""

YES_FORMS = ("예", "네", "yes", "y", "true")
NO_FORMS = ("아니오", "아니요", "no", "n", "false")


def normalize_answer(s: str) -> str:
    """비교용으로 답을 정리한다.

    - 앞뒤 공백 제거, 영문 소문자화, 끝의 마침표 제거.
    - YES_FORMS 에 있으면 "yes", NO_FORMS 에 있으면 "no" 로 바꾼다.
    """
    raise NotImplementedError


def answer_correct(pred: str, gold: str) -> bool:
    """정리한 뒤 같으면 True."""
    raise NotImplementedError


def evidence_exact(pred_ids: list[str], gold_ids: list[str]) -> bool:
    """두 sid 집합이 정확히 같으면 True. 둘 다 비어 있어도 True."""
    raise NotImplementedError


def evidence_f1(pred_ids: list[str], gold_ids: list[str]) -> float:
    """sid 집합의 F1. 둘 다 비면 1.0, 한쪽만 비면 0.0."""
    raise NotImplementedError


def hit_distractor(pred_ids: list[str], distractor_ids: list[str]) -> bool:
    """모델이 고른 근거에 함정 문장이 하나라도 있으면 True."""
    raise NotImplementedError


def score_record(item: dict, parsed: dict | None) -> dict:
    """응답 하나의 채점 결과를 돌려준다.

    반환 키: item_id, parse_ok, answer_correct, evidence_exact, evidence_f1,
            role_correct, hit_distractor, rwr
    - parsed 가 None 이면 parse_ok=False, 나머지 bool 은 False, evidence_f1 은 0.0.
    - role_correct: parsed["evidence_role"] == item["gold_evidence_role"]
    - rwr (Right answer, Wrong Reason): 답은 맞았는데 evidence_exact 가 False.
    """
    raise NotImplementedError
