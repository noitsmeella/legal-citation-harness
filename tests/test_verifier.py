from harness.verifier import decide, retrieve_candidates


def test_retrieve_finds_related_sentences(kr_sentences):
    top = retrieve_candidates("법원은 정당방위를 인정하였다", kr_sentences, k=3)
    assert 1 <= len(top) <= 3
    assert all("정당방위" in s["text"] for s in top)


def test_decide_unsupported():
    assert decide("COURT", [])["verdict"] == "UNSUPPORTED"


def test_decide_supported(kr_sentences):
    matches = [s for s in kr_sentences if s["sid"] == "S6"]
    assert decide("COURT", matches)["verdict"] == "SUPPORTED"


def test_decide_misattributed(kr_sentences):
    # "법원이 정당방위를 인정했다"는 주장의 근거가 원심 판단(S3)뿐인 경우
    matches = [s for s in kr_sentences if s["sid"] == "S3"]
    out = decide("COURT", matches)
    assert out["verdict"] == "MISATTRIBUTED"
    assert any("LOWER_COURT" in w for w in out["warnings"])


def test_decide_baseline_ignores_roles(kr_sentences):
    matches = [s for s in kr_sentences if s["sid"] == "S3"]
    assert decide("COURT", matches, use_roles=False)["verdict"] == "SUPPORTED"
