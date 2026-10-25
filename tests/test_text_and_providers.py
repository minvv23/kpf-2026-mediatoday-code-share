from localcritique import providers
from localcritique.utils import text_utils as t


def test_strip_title_tag():
    assert t.strip_title_tag("[사설] 제목입니다") == "제목입니다"


def test_html_unescape():
    assert t.normalize("&quot;인용&quot;") == '"인용"'


def test_tokenize_stopwords():
    assert "그리고" not in t.tokenize("그리고 지역 경제")


def test_media_type():
    assert providers.media_type("조선일보") == "중앙지"
    assert providers.media_type("대전일보") == "지역지"
    assert providers.media_type("없는신문") == "기타"
