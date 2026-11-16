"""문항(item)과 모델 응답의 형식을 정의하고 검증한다.

docs/codebook.md 와 data/README.md 의 정의를 코드로 옮긴 것이다. 정의를 바꾸면 세 곳을 함께 고친다.
"""

ROLES = (
    "FACT",              # 법원이 인정한 사실
    "ALLEGATION",        # 당사자 주장, 상고이유
    "LOWER_COURT",       # 원심·1심의 판단 서술
    "HOLDING",           # 당해 법원의 판시·결론
    "REASONING",         # 당해 법원의 판단 이유
    "QUOTATION",         # 인용된 판례·법령
    "SEPARATE_OPINION",  # 반대·별개·보충의견
)
ITEM_TYPES = ("A", "B", "C", "D", "E", "F")
JURISDICTIONS = ("KR", "US")
QUESTION_TARGETS = ("COURT", "PARTY")
CONDITIONS = ("closed_book", "gold", "gold_distractor", "long_doc")
INSUFFICIENT = "INSUFFICIENT"

REQUIRED_ITEM_FIELDS = (
    "item_id", "case_id", "jurisdiction", "item_type", "question", "question_target",
    "gold_answer", "gold_evidence_ids", "gold_evidence_role",
    "distractor_ids", "distractor_roles", "context_gold", "context_distractor",
)


def validate_item(item: dict) -> list[str]:
    """문항 하나를 검사해 오류 메시지 목록을 돌려준다. 문제가 없으면 빈 리스트.

    검사 규칙 (메시지에는 문제가 된 필드 이름을 넣는다):
      1. REQUIRED_ITEM_FIELDS 가 모두 있어야 한다. 빠진 필드가 있으면 그 오류만 돌려주고 끝낸다.
      2. item_id 는 case_id 로 시작해야 한다.
      3. jurisdiction, item_type, question_target 은 각각 정해진 값 중 하나.
      4. F 유형: gold_answer 는 INSUFFICIENT, gold_evidence_ids 는 빈 리스트, gold_evidence_role 은 None.
         나머지 유형: gold_evidence_ids 가 비어 있으면 안 되고 gold_evidence_role 은 ROLES 중 하나.
      5. B~E 유형: distractor_ids 가 비어 있으면 안 된다.
      6. distractor_roles 의 값은 모두 ROLES 중 하나.
      7. gold_evidence_ids 와 distractor_ids 가 겹치면 안 된다.
    """
    raise NotImplementedError


def parse_response(raw: str) -> dict | None:
    """모델 출력 문자열에서 JSON 객체 하나를 꺼낸다.

    - 앞뒤에 설명문이나 ```json 코드펜스가 있어도, 처음 나오는 { ... } 객체를 찾아 파싱한다.
    - 파싱에 실패하거나 "answer" 키가 없으면 None.
    - "evidence_ids" 가 없으면 빈 리스트로, "evidence_role" 이 없으면 None 으로 채운다.
    """
    raise NotImplementedError
