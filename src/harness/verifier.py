"""[B] 강의록 등의 주장 한 문장이 판결문으로 뒷받침되는지, 출처가 맞는지 판정한다.

입력과 출력 형식은 docs/integration_spec.md 가 기준이다.

판정 (VERDICTS):
  SUPPORTED      주장이 해당 주체(대개 법원)의 판단으로 판결문에 있다
  MISATTRIBUTED  내용은 판결문에 있지만 다른 주체의 말이다 (당사자 주장, 원심, 인용 판례, 반대의견 등)
  UNSUPPORTED    판결문에서 근거를 찾을 수 없다
  ABSTAIN        판단을 확정할 수 없다 (근거가 충돌하거나 확신이 낮음)

처리 순서:
  1. retrieve_candidates: 주장과 관련된 문장 후보 k개를 찾는다
  2. 후보 문장에 역할을 붙인다 (role_tagger 또는 사람이 붙인 라벨)
  3. 후보마다 "이 문장이 주장의 내용을 담고 있는가"를 판단한다 (모델 호출)
  4. decide: 내용이 맞는 문장의 역할과 주장이 가리키는 주체를 비교해 판정한다

비교 실험: use_roles=False 이면 2단계와 역할 비교를 건너뛰고 내용 일치만으로 판정한다 (기준선).
"""

VERDICTS = ("SUPPORTED", "MISATTRIBUTED", "UNSUPPORTED", "ABSTAIN")

# 주장이 가리키는 주체가 "법원"일 때 출처로 인정하는 역할
COURT_ROLES = ("HOLDING", "REASONING")


def retrieve_candidates(claim: str, sentences: list[dict], k: int = 5) -> list[dict]:
    """주장과 겹치는 표현이 많은 문장 상위 k개를 점수 높은 순으로 돌려준다.

    첫 버전은 단순하게: 공백을 뺀 글자 2-gram 겹침 개수로 점수를 매긴다.
    점수가 0인 문장은 넣지 않는다.
    """
    raise NotImplementedError


def decide(claim_target: str, matches: list[dict], use_roles: bool = True) -> dict:
    """내용이 맞는 문장들(matches, 각각 "sid", "text", "role" 포함)로 최종 판정을 만든다.

    claim_target: "COURT" 또는 "PARTY"
    반환: {"verdict", "evidence", "reason", "warnings"}
    - matches 가 비면 UNSUPPORTED.
    - use_roles=True 이고 claim_target 이 COURT 일 때:
        COURT_ROLES 문장이 있으면 SUPPORTED,
        없고 다른 역할 문장만 있으면 MISATTRIBUTED (warnings 에 그 역할을 적는다).
    - use_roles=False 이면 matches 가 있으면 SUPPORTED.
    """
    raise NotImplementedError


def verify(claim: str, sentences: list[dict], claim_target: str = "COURT",
           use_roles: bool = True, model: str | None = None) -> dict:
    """1~4단계를 이어서 실행한다.

    반환: decide 의 결과에 "court_view"(같은 쟁점에 대한 HOLDING·REASONING 문장)와
    "verifier_version" 을 더한 것. 정확한 형식은 docs/integration_spec.md 의 응답을 따른다.
    """
    raise NotImplementedError
