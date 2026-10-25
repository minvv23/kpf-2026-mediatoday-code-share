"""설정 로더.

우선순위: 환경변수 > config/settings.yaml > 기본값.
기본값은 동작 확인용이며, 실제 운영 값은 각사 환경에 맞게 정한다.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv가 없으면 환경변수만 사용
    pass

ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = Path(os.getenv("SETTINGS_PATH", ROOT / "config" / "settings.yaml"))


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


_FILE = _load_yaml(SETTINGS_PATH)


def get(name: str, default=None, cast=str):
    """환경변수, 설정 파일, 기본값 순서로 값을 찾는다."""
    raw = os.getenv(name)
    if raw is None or raw == "":
        raw = _FILE.get(name.lower(), default)
    if raw is None:
        return None
    if cast is bool:
        return str(raw).lower() in ("1", "true", "yes", "y")
    return cast(raw)


# 경로
INPUT_PATH = Path(get("INPUT_PATH", "./sample/articles.csv"))
OUTPUT_DIR = Path(get("OUTPUT_DIR", "./output"))
LOG_LEVEL = get("LOG_LEVEL", "INFO")

# 기사 필터
EDITORIAL_KEYWORD = get("EDITORIAL_KEYWORD", "사설")
MIN_BODY_CHARS = get("MIN_BODY_CHARS", 200, int)
WINDOW_HOURS = get("WINDOW_HOURS", 24, int)

# 군집화
K_MIN = get("K_MIN", 2, int)
K_MAX = get("K_MAX", 10, int)
RANDOM_STATE = get("RANDOM_STATE", 0, int)

# 매칭·차이 판정 (각사 데이터로 정할 값)
MIN_SHARED_WORDS = get("MIN_SHARED_WORDS", 1, int)
DIVERGENCE_MIN = get("DIVERGENCE_MIN", 0.5, float)
MIN_LOCAL_PER_ISSUE = get("MIN_LOCAL_PER_ISSUE", 1, int)
MAX_REPORTS = get("MAX_REPORTS", 1, int)


def summary() -> dict:
    return {
        "input": str(INPUT_PATH),
        "output_dir": str(OUTPUT_DIR),
        "window_hours": WINDOW_HOURS,
        "k_range": (K_MIN, K_MAX),
        "min_shared_words": MIN_SHARED_WORDS,
        "divergence_min": DIVERGENCE_MIN,
        "max_reports": MAX_REPORTS,
    }
