import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def kr_sentences():
    """가상 한국 판결문 7문장 (역할 라벨 포함)."""
    with open(FIXTURES / "sample_kr.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


@pytest.fixture
def item_b():
    """가상 판결문으로 만든 B 유형(언급-채택) 문항."""
    return {
        "item_id": "KR-900-B1",
        "case_id": "KR-900",
        "jurisdiction": "KR",
        "item_type": "B",
        "question": "대법원은 피고인의 행위가 정당방위에 해당한다고 판단하였는가?",
        "question_target": "COURT",
        "gold_answer": "아니오",
        "gold_evidence_ids": ["S5", "S6"],
        "gold_evidence_role": "HOLDING",
        "distractor_ids": ["S2", "S3"],
        "distractor_roles": ["ALLEGATION", "LOWER_COURT"],
        "context_gold": "S4-S6",
        "context_distractor": "S2-S6",
        "evidence_position": "late",
        "notes": "",
    }
