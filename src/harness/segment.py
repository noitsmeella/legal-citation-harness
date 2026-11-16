"""판결문을 문장으로 나누고 S1, S2 ... 번호를 붙인다.

나눈 결과는 data/segmented/{case_id}.jsonl 에 한 줄에 한 문장으로 저장한다.
    {"sid": "S1", "text": "..."}

분할 규칙 (docs/segmentation.md 와 같은 내용):
  1. 줄바꿈은 항상 문장 경계다. 빈 줄과 공백뿐인 조각은 버리고, 각 문장은 앞뒤 공백을 지운다.
  2. 마침표(.), 물음표(?), 느낌표(!) 뒤에 공백이 오면 그 자리에서 나눈다.
  3. 괄호 ( ) 안에서는 나누지 않는다.  예: "(대법원 2010. 1. 14. 선고 2009도1234 판결 참조)"
  4. [한국어만] 마침표 바로 앞 글자가 숫자면 나누지 않는다.  예: "2020. 3. 5. 서울에서"
  5. [영어만] 마침표로 끝나는 단어가 US_ABBREVIATIONS 에 있으면 나누지 않는다.  예: "v.", "Cir.", "Id."

긴 한국어 문장을 절 단위로 더 나누는 일은 자동으로 하지 않는다. 주석 단계에서 손으로 나눈다.
"""

US_ABBREVIATIONS = (
    "v.", "U.S.", "U.S.C.", "Id.", "id.", "Cir.", "No.", "Nos.", "Inc.", "Co.",
    "Corp.", "Ct.", "App.", "Supp.", "F.", "Fed.", "R.", "Crim.", "P.", "Dist.",
    "e.g.", "i.e.", "cf.", "Cf.", "Mr.", "Ms.", "Dr.", "Jr.", "St.", "Stat.", "Ann.",
)


def split_sentences(text: str, lang: str) -> list[str]:
    """text 를 문장 리스트로 나눈다. lang 은 "ko" 또는 "en".

    lang 이 둘 다 아니면 ValueError 를 일으킨다.
    """
    raise NotImplementedError


def assign_ids(sentences: list[str], start: int = 1) -> list[dict]:
    """문장 리스트에 번호를 붙인다.

    ["가.", "나."] -> [{"sid": "S1", "text": "가."}, {"sid": "S2", "text": "나."}]
    """
    raise NotImplementedError


def segment_file(in_path: str, out_path: str, lang: str) -> int:
    """원문 텍스트 파일(UTF-8)을 읽어 나눈 결과를 jsonl 로 저장하고, 문장 수를 돌려준다.

    jsonl 은 UTF-8, 한글이 그대로 보이게 저장한다 (json.dumps 의 ensure_ascii=False).
    """
    raise NotImplementedError


if __name__ == "__main__":
    # 사용 예: python -m harness.segment data/raw/KR-001.txt data/segmented/KR-001.jsonl ko
    raise NotImplementedError
