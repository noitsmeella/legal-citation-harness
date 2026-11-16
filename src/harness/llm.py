"""모델 호출, 응답 캐시, 호출 로그.

원칙:
  - 같은 (모델, 조건, 문항, 프롬프트) 조합은 두 번 호출하지 않는다. runs/cache/{key}.json 을 먼저 본다.
  - 모든 호출은 runs/log.jsonl 에 한 줄씩 남긴다.
    필드: run_id, timestamp, model, model_version, condition, item_id, temperature,
          prompt_tokens, output_tokens, latency_ms, raw_output
  - API 키는 .env 에서 읽는다 (python-dotenv). 코드에 키를 쓰지 않는다.
  - 실패하면 잠깐 쉬었다가 다시 시도한다 (최대 3회, 대기 시간은 2배씩).
"""

CACHE_DIR = "runs/cache"
LOG_PATH = "runs/log.jsonl"


def cache_key(model: str, condition: str, item_id: str, prompt: dict) -> str:
    """입력이 같으면 항상 같은 문자열, 하나라도 다르면 다른 문자열을 돌려준다.

    힌트: json.dumps(..., sort_keys=True, ensure_ascii=False) 한 결과를 hashlib.sha256 으로.
    """
    raise NotImplementedError


def load_cache(key: str) -> dict | None:
    """캐시가 있으면 읽어서 돌려주고, 없으면 None."""
    raise NotImplementedError


def save_cache(key: str, record: dict) -> None:
    """record 를 runs/cache/{key}.json 에 저장한다."""
    raise NotImplementedError


def call_model(model: str, system: str, user: str, temperature: float = 0.0) -> dict:
    """모델을 호출하고 {"raw_output", "model_version", "prompt_tokens", "output_tokens", "latency_ms"} 를 돌려준다.

    model 이름 앞부분으로 회사를 고른다 (예: "ollama:exaone..." 은 로컬 Ollama).
    처음에는 한 회사만 구현하고, 나머지는 하나씩 추가한다.
    """
    raise NotImplementedError
