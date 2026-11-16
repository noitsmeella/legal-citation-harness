import pytest

from harness.role_tagger import confusion, role_accuracy, tag_rule


def test_role_accuracy():
    assert role_accuracy(["HOLDING", "FACT"], ["HOLDING", "ALLEGATION"]) == 0.5
    assert role_accuracy([], []) == 0.0
    with pytest.raises(ValueError):
        role_accuracy(["FACT"], [])


def test_confusion():
    c = confusion(["HOLDING", "HOLDING", "FACT"], ["HOLDING", "ALLEGATION", "FACT"])
    assert c[("ALLEGATION", "HOLDING")] == 1
    assert c[("HOLDING", "HOLDING")] == 1


def test_tag_rule_catches_obvious_cues(kr_sentences):
    tagged = {s["sid"]: s["pred_role"] for s in tag_rule(kr_sentences, "ko")}
    assert tagged["S2"] == "ALLEGATION"   # "~라고 주장한다"
    assert tagged["S3"] == "LOWER_COURT"  # "원심은"
    assert tagged["S4"] == "QUOTATION"    # "판결 참조)"
