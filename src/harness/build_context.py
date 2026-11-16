"""문항과 조건에 맞춰 모델에게 보낼 지문과 프롬프트를 만든다.

조건 (schema.CONDITIONS):
  closed_book      질문만 준다. 문서 없음.
  gold             item["context_gold"] 범위의 문장만 준다.
  gold_distractor  item["context_distractor"] 범위의 문장을 준다 (정답 근거 + 함정).
  long_doc         판결문 전체를 준다.
"""

SYSTEM_PROMPT = {
    "ko": (
        "당신은 판결문을 읽고 질문에 답하는 조수입니다.\n"
        "문서가 주어지면 반드시 문서에 있는 내용만 근거로 답하십시오.\n"
        "문서의 각 문장 앞에는 [S번호]가 붙어 있습니다.\n"
        "문서만으로 답을 확정할 수 없으면 answer에 \"INSUFFICIENT\"라고 쓰십시오.\n"
        "출력은 아래 JSON 한 개만 쓰고 다른 말은 쓰지 마십시오.\n"
        '{"answer": "...", "evidence_ids": ["S.."], '
        '"evidence_role": "FACT|ALLEGATION|LOWER_COURT|HOLDING|REASONING|QUOTATION|SEPARATE_OPINION", '
        '"confidence": 0-100, "rationale": "한 문장"}'
    ),
    "en": (
        "You are an assistant who reads court judgments and answers questions.\n"
        "When a document is given, answer only from what the document says.\n"
        "Each sentence in the document is prefixed with [S number].\n"
        "If the document alone cannot settle the answer, write \"INSUFFICIENT\" as the answer.\n"
        "Output exactly one JSON object below and nothing else.\n"
        '{"answer": "...", "evidence_ids": ["S.."], '
        '"evidence_role": "FACT|ALLEGATION|LOWER_COURT|HOLDING|REASONING|QUOTATION|SEPARATE_OPINION", '
        '"confidence": 0-100, "rationale": "one sentence"}'
    ),
}


def parse_range(spec: str) -> list[str]:
    """문장 범위 표기를 sid 리스트로 펼친다.

    "S12-S14,S20" -> ["S12", "S13", "S14", "S20"]
    - 쉼표 앞뒤 공백은 무시한다.
    - 빈 문자열은 빈 리스트.
    - 형식이 틀리거나 범위가 거꾸로면 (예: "S5-S3", "12-14") ValueError.
    """
    raise NotImplementedError


def render_context(sentences: list[dict], sids: list[str]) -> str:
    """sids 에 해당하는 문장을 "[S12] 문장" 형태의 줄로 이어 붙인다 (줄바꿈으로 구분).

    - 순서는 sids 의 순서가 아니라 판결문(sentences) 안의 순서를 따른다.
    - sentences 에 없는 sid 가 있으면 ValueError.
    """
    raise NotImplementedError


def build_prompt(item: dict, sentences: list[dict], condition: str) -> dict:
    """{"system": ..., "user": ...} 를 돌려준다.

    - 언어는 item["jurisdiction"] 으로 정한다: KR -> SYSTEM_PROMPT["ko"], US -> SYSTEM_PROMPT["en"].
    - user 는 문서가 있으면 "<문서>\\n{지문}\\n</문서>\\n\\n질문: {질문}" 형태
      (영어는 "<document>", "Question:"). closed_book 이면 질문만.
    - 모르는 condition 이면 ValueError.
    """
    raise NotImplementedError
