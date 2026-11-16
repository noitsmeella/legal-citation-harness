import pytest

from harness.score import (
    answer_correct, evidence_exact, evidence_f1, hit_distractor, normalize_answer, score_record,
)


@pytest.mark.parametrize("raw, norm", [
    ("  예 ", "yes"), ("Yes.", "yes"), ("네", "yes"),
    ("아니요", "no"), ("아니오.", "no"), ("NO", "no"),
    ("INSUFFICIENT", "insufficient"), ("정당방위", "정당방위"),
])
def test_normalize(raw, norm):
    assert normalize_answer(raw) == norm


def test_answer_correct():
    assert answer_correct("아니요.", "아니오")
    assert not answer_correct("예", "아니오")


def test_evidence_exact():
    assert evidence_exact(["S6", "S5"], ["S5", "S6"])
    assert not evidence_exact(["S6"], ["S5", "S6"])
    assert evidence_exact([], [])


def test_evidence_f1():
    assert evidence_f1(["S5", "S6"], ["S5", "S6"]) == 1.0
    assert evidence_f1(["S6", "S2"], ["S5", "S6"]) == pytest.approx(0.5)
    assert evidence_f1([], []) == 1.0
    assert evidence_f1([], ["S5"]) == 0.0


def test_hit_distractor():
    assert hit_distractor(["S6", "S3"], ["S2", "S3"])
    assert not hit_distractor(["S6"], ["S2", "S3"])


def test_score_record_correct(item_b):
    parsed = {"answer": "아니오", "evidence_ids": ["S5", "S6"], "evidence_role": "HOLDING"}
    r = score_record(item_b, parsed)
    assert r["item_id"] == "KR-900-B1"
    assert r["parse_ok"] and r["answer_correct"] and r["evidence_exact"] and r["role_correct"]
    assert not r["hit_distractor"] and not r["rwr"]


def test_score_record_misattribution(item_b):
    # 피고인 주장을 법원 판단으로 착각한 전형적인 오답
    parsed = {"answer": "예", "evidence_ids": ["S2"], "evidence_role": "HOLDING"}
    r = score_record(item_b, parsed)
    assert not r["answer_correct"] and r["hit_distractor"]


def test_score_record_right_answer_wrong_reason(item_b):
    parsed = {"answer": "아니오", "evidence_ids": ["S3"], "evidence_role": "LOWER_COURT"}
    r = score_record(item_b, parsed)
    assert r["answer_correct"] and r["rwr"] and r["hit_distractor"]


def test_score_record_parse_fail(item_b):
    r = score_record(item_b, None)
    assert r["parse_ok"] is False
    assert r["answer_correct"] is False
    assert r["evidence_f1"] == 0.0
