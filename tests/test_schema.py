from harness.schema import INSUFFICIENT, parse_response, validate_item


def test_valid_item(item_b):
    assert validate_item(item_b) == []


def test_missing_field(item_b):
    del item_b["question"]
    errors = validate_item(item_b)
    assert errors and any("question" in e for e in errors)


def test_item_id_must_start_with_case_id(item_b):
    item_b["item_id"] = "KR-901-B1"
    assert any("item_id" in e for e in validate_item(item_b))


def test_bad_role(item_b):
    item_b["gold_evidence_role"] = "JUDGE"
    assert any("gold_evidence_role" in e for e in validate_item(item_b))


def test_bad_distractor_role(item_b):
    item_b["distractor_roles"] = ["ALLEGATION", "PROSECUTOR"]
    assert any("distractor_roles" in e for e in validate_item(item_b))


def test_type_b_needs_distractor(item_b):
    item_b["distractor_ids"] = []
    item_b["distractor_roles"] = []
    assert any("distractor_ids" in e for e in validate_item(item_b))


def test_gold_and_distractor_must_not_overlap(item_b):
    item_b["distractor_ids"] = ["S2", "S6"]
    assert validate_item(item_b) != []


def test_type_f_rules(item_b):
    item_b.update(item_type="F", gold_answer=INSUFFICIENT, gold_evidence_ids=[],
                  gold_evidence_role=None)
    assert validate_item(item_b) == []

    item_b["gold_answer"] = "아니오"
    assert any("gold_answer" in e for e in validate_item(item_b))


def test_parse_plain_json():
    raw = '{"answer": "아니오", "evidence_ids": ["S6"], "evidence_role": "HOLDING", "confidence": 90}'
    assert parse_response(raw)["evidence_ids"] == ["S6"]


def test_parse_with_fence_and_chatter():
    raw = '네, 답변입니다.\n```json\n{"answer": "yes", "evidence_ids": ["S2"]}\n```\n감사합니다.'
    out = parse_response(raw)
    assert out["answer"] == "yes"
    assert out["evidence_ids"] == ["S2"]


def test_parse_fills_defaults():
    out = parse_response('{"answer": "INSUFFICIENT"}')
    assert out["evidence_ids"] == []
    assert out["evidence_role"] is None


def test_parse_failures():
    assert parse_response("죄송하지만 답할 수 없습니다.") is None
    assert parse_response('{"evidence_ids": ["S1"]}') is None
    assert parse_response('{"answer": "yes", ') is None
