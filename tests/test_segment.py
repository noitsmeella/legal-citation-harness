import json

import pytest

from harness.segment import assign_ids, segment_file, split_sentences


def test_ko_basic():
    text = "피고인은 정당방위를 주장한다. 그러나 원심은 이를 배척하였다."
    assert split_sentences(text, "ko") == [
        "피고인은 정당방위를 주장한다.",
        "그러나 원심은 이를 배척하였다.",
    ]


def test_ko_date_is_not_a_boundary():
    text = "피고인은 2020. 3. 5. 서울에서 피해자를 폭행하였다. 원심은 유죄를 선고하였다."
    assert split_sentences(text, "ko") == [
        "피고인은 2020. 3. 5. 서울에서 피해자를 폭행하였다.",
        "원심은 유죄를 선고하였다.",
    ]


def test_ko_no_split_inside_parentheses():
    text = (
        "정당방위의 요건은 엄격히 보아야 한다(대법원 2010. 1. 14. 선고 2009도1234 판결 참조). "
        "원심은 이와 달리 판단하였다."
    )
    out = split_sentences(text, "ko")
    assert len(out) == 2
    assert out[0].endswith("참조).")


def test_en_abbreviations():
    text = (
        "See United States v. Smith, 123 F.3d 456, 460 (9th Cir. 1999). "
        "The district court denied the motion."
    )
    assert split_sentences(text, "en") == [
        "See United States v. Smith, 123 F.3d 456, 460 (9th Cir. 1999).",
        "The district court denied the motion.",
    ]


def test_en_digit_before_period_still_splits():
    # 숫자 규칙은 한국어에만 적용된다
    assert split_sentences("Id. at 461. We therefore reverse.", "en") == [
        "Id. at 461.",
        "We therefore reverse.",
    ]


def test_newlines_and_blank_lines():
    text = "주    문\n\n상고를 기각한다.\n\n   \n이    유\n"
    assert split_sentences(text, "ko") == ["주    문", "상고를 기각한다.", "이    유"]


def test_question_mark():
    assert split_sentences("Was this self-defense? We think not.", "en") == [
        "Was this self-defense?",
        "We think not.",
    ]


def test_unknown_lang():
    with pytest.raises(ValueError):
        split_sentences("text", "jp")


def test_assign_ids():
    assert assign_ids(["가.", "나."]) == [
        {"sid": "S1", "text": "가."},
        {"sid": "S2", "text": "나."},
    ]
    assert assign_ids(["다."], start=10) == [{"sid": "S10", "text": "다."}]


def test_segment_file(tmp_path):
    src = tmp_path / "KR-001.txt"
    src.write_text("상고를 기각한다.\n원심판단은 정당하다. 상고이유는 받아들이지 않는다.", encoding="utf-8")
    out = tmp_path / "KR-001.jsonl"

    n = segment_file(str(src), str(out), "ko")

    assert n == 3
    lines = out.read_text(encoding="utf-8").splitlines()
    assert json.loads(lines[2]) == {"sid": "S3", "text": "상고이유는 받아들이지 않는다."}
    assert "상고" in lines[0]  # 한글이 \uXXXX 로 깨지지 않고 그대로 저장되어야 한다
