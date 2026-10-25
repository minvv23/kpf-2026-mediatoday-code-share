"""텍스트 정리 함수."""
import html
import re
import unicodedata

_WS = re.compile(r"[ \t 　]+")
_MULTI_NL = re.compile(r"\n{3,}")
_TAG = re.compile(r"^\s*\[[^\]]*\]\s*")
_SENT_END = re.compile(r"(?<=[.!?])\s+")

STOPWORDS = {
    "그리고", "그러나", "하지만", "그래서", "또한", "이번", "지난", "오늘", "현재", "관련", "대한", "위해",
    "있는", "있다", "했다", "한다", "것으로", "것이", "수", "등", "및", "이", "그", "저", "더", "또",
}


def normalize(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(unicodedata.normalize("NFC", str(text)))
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _WS.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return _MULTI_NL.sub("\n\n", text).strip()


def strip_title_tag(title: str) -> str:
    """'[사설] 제목' 같은 머리표를 지운다."""
    return _TAG.sub("", normalize(title))


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_END.split(normalize(text)) if s.strip()]


def tokenize(text: str) -> list[str]:
    """공백 기준 단순 토큰화 (형태소 분석 없음)."""
    tokens = re.findall(r"[0-9A-Za-z가-힣]+", normalize(text).lower())
    return [t for t in tokens if len(t) > 1 and t not in STOPWORDS]


def lead(text: str, n: int = 2) -> str:
    """본문 앞 n문장."""
    return " ".join(split_sentences(text)[:n])


def truncate(text: str, n: int = 80) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"
