"""동작 확인용 가상 사설 데이터."""
import random
from pathlib import Path

import pandas as pd

from .providers import CENTRAL, LOCAL

TOPICS = {
    "교통": ["광역철도 노선 확정", "버스 요금 인상", "도로 확장 사업"],
    "에너지": ["발전소 건설 계획", "송전선로 갈등", "전기요금 조정"],
    "교육": ["대학 정원 조정", "지역 학교 통폐합", "교원 수급 대책"],
    "산업": ["산업단지 조성", "기업 유치 경쟁", "지역 일자리 감소"],
}
CENTRAL_VIEW = ["국가 경쟁력", "재정 부담", "제도 개선", "효율성", "전국적 영향"]
LOCAL_VIEW = ["지역 주민", "지역 경제", "균형발전", "지역 소외", "현장 피해"]


def make(n_days: int = 2, seed: int = 0) -> pd.DataFrame:
    rnd = random.Random(seed)
    rows = []
    for day in range(n_days):
        for topic, subs in TOPICS.items():
            sub = rnd.choice(subs)
            for p in rnd.sample(CENTRAL, 4):
                view = rnd.choice(CENTRAL_VIEW)
                rows.append(dict(provider=p, title=f"[사설] {sub}, {view} 따져야",
                                 content=f"{sub} 문제를 두고 {view} 측면의 검토가 필요하다. " * 8,
                                 date=f"2026-01-0{day + 1} 0{rnd.randint(1, 6)}:00:00"))
            for p in rnd.sample(LOCAL, 3):
                view = rnd.choice(LOCAL_VIEW)
                rows.append(dict(provider=p, title=f"[사설] {sub}, {view} 먼저 살펴야",
                                 content=f"{sub} 논의에서 {view} 문제가 빠져 있다. {topic} 현안을 지역 시각에서 봐야 한다. " * 6,
                                 date=f"2026-01-0{day + 1} 0{rnd.randint(1, 6)}:00:00"))
    return pd.DataFrame(rows)


def write(path="sample/articles.csv", **kw) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    make(**kw).to_csv(p, index=False, encoding="utf-8-sig")
    return p
