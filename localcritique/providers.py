"""매체 분류.

아래 목록은 예시다. 실제 분석 대상 매체와 권역 구분은 각사 기준에 맞춰 바꿔 쓴다.
"""
CENTRAL = ["조선일보", "중앙일보", "동아일보", "한겨레", "경향신문", "한국일보", "서울신문", "국민일보", "세계일보"]

LOCAL_BY_REGION = {
    "수도권": ["경기일보", "경인일보", "인천일보"],
    "충청권": ["대전일보", "충청투데이", "중도일보"],
    "호남권": ["광주일보", "무등일보", "전북일보"],
    "영남권": ["매일신문", "영남일보", "부산일보", "국제신문"],
    "강원권": ["강원일보", "강원도민일보"],
    "제주권": ["제주일보", "한라일보"],
}

LOCAL = [p for ps in LOCAL_BY_REGION.values() for p in ps]
REGION_OF = {p: r for r, ps in LOCAL_BY_REGION.items() for p in ps}


def media_type(provider: str) -> str:
    if provider in CENTRAL:
        return "중앙지"
    if provider in REGION_OF:
        return "지역지"
    return "기타"


def region(provider: str) -> str:
    return REGION_OF.get(provider, "전국" if provider in CENTRAL else "")
