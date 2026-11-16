"""[B] 판결문 문장마다 담화 역할을 자동으로 붙인다.

두 가지 방식을 만들어 비교한다:
  rule  단서 표현 규칙 (예: "상고이유", "원심은", "참조)", "반대의견", "We hold")
  llm   모델에게 코드북 정의를 주고 분류시키기

사람이 붙인 라벨(data/segmented 의 "role")을 정답으로 정확도를 잰다.
"""

from harness.schema import ROLES  # noqa: F401  (구현할 때 쓴다)


def tag_rule(sentences: list[dict], lang: str) -> list[dict]:
    """규칙으로 역할을 붙인다. 각 문장 dict 에 "pred_role" 키를 더한 새 리스트를 돌려준다.

    규칙에 걸리지 않는 문장은 바로 앞 문장의 역할을 따른다 (첫 문장이면 "FACT").
    """
    raise NotImplementedError


def tag_llm(sentences: list[dict], lang: str, model: str) -> list[dict]:
    """모델로 역할을 붙인다. 여러 문장을 한 번에 보내 호출 수를 줄인다."""
    raise NotImplementedError


def role_accuracy(pred: list[str], gold: list[str]) -> float:
    """두 리스트에서 같은 위치의 값이 일치하는 비율. 길이가 다르면 ValueError, 둘 다 비면 0.0."""
    raise NotImplementedError


def confusion(pred: list[str], gold: list[str]) -> dict:
    """{(gold_role, pred_role): count} 형태의 혼동 표. 어떤 역할끼리 헷갈리는지 본다."""
    raise NotImplementedError
