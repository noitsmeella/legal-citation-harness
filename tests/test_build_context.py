import pytest

from harness.build_context import build_prompt, parse_range, render_context


def test_parse_range():
    assert parse_range("S12-S14,S20") == ["S12", "S13", "S14", "S20"]
    assert parse_range(" S1 , S3-S4 ") == ["S1", "S3", "S4"]
    assert parse_range("") == []


@pytest.mark.parametrize("bad", ["S5-S3", "12-14", "S1-", "X1"])
def test_parse_range_errors(bad):
    with pytest.raises(ValueError):
        parse_range(bad)


def test_render_context_uses_document_order(kr_sentences):
    out = render_context(kr_sentences, ["S6", "S2"])
    lines = out.split("\n")
    assert lines[0].startswith("[S2] 피고인은")
    assert lines[1].startswith("[S6] 그런데도")


def test_render_context_unknown_sid(kr_sentences):
    with pytest.raises(ValueError):
        render_context(kr_sentences, ["S99"])


def test_closed_book_has_no_document(item_b, kr_sentences):
    p = build_prompt(item_b, kr_sentences, "closed_book")
    assert "[S" not in p["user"]
    assert item_b["question"] in p["user"]
    assert "INSUFFICIENT" in p["system"]


def test_gold_vs_distractor(item_b, kr_sentences):
    gold = build_prompt(item_b, kr_sentences, "gold")["user"]
    dist = build_prompt(item_b, kr_sentences, "gold_distractor")["user"]
    assert "[S5]" in gold and "[S2]" not in gold
    assert "[S2]" in dist and "[S3]" in dist


def test_long_doc_has_everything(item_b, kr_sentences):
    user = build_prompt(item_b, kr_sentences, "long_doc")["user"]
    assert "[S1]" in user and "[S7]" in user


def test_english_prompt_for_us(item_b, kr_sentences):
    item_b["jurisdiction"] = "US"
    p = build_prompt(item_b, kr_sentences, "gold")
    assert "court judgments" in p["system"]
    assert "Question:" in p["user"]


def test_unknown_condition(item_b, kr_sentences):
    with pytest.raises(ValueError):
        build_prompt(item_b, kr_sentences, "open_book")
