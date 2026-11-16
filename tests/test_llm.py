from harness.llm import cache_key


def test_cache_key_is_deterministic():
    p = {"system": "s", "user": "u"}
    assert cache_key("m", "gold", "KR-900-B1", p) == cache_key("m", "gold", "KR-900-B1", dict(p))


def test_cache_key_changes_with_any_input():
    p = {"system": "s", "user": "u"}
    base = cache_key("m", "gold", "KR-900-B1", p)
    assert base != cache_key("m2", "gold", "KR-900-B1", p)
    assert base != cache_key("m", "long_doc", "KR-900-B1", p)
    assert base != cache_key("m", "gold", "KR-900-B2", p)
    assert base != cache_key("m", "gold", "KR-900-B1", {"system": "s", "user": "u2"})
