"""중앙지·지역지 단어 차이로 본 단순 분기 점수.

군집 안에서 중앙지 기사 묶음과 지역지 기사 묶음의 주요 단어가 얼마나 다른지를 0~1로 잰다.
점수가 기준 이상이고 지역지 기사가 일정 수 이상이면 비교 대상 이슈로 표시한다.
"""
from collections import Counter
from dataclasses import dataclass

import pandas as pd

from . import config
from .utils.text_utils import tokenize


@dataclass
class IssueFlag:
    cluster: int
    n_central: int
    n_local: int
    score: float
    central_words: list[str]
    local_words: list[str]

    @property
    def flagged(self) -> bool:
        return self.n_local >= config.MIN_LOCAL_PER_ISSUE and self.score >= config.DIVERGENCE_MIN


def top_words(texts: list[str], n: int = 15) -> list[str]:
    c = Counter()
    for t in texts:
        c.update(tokenize(t))
    return [w for w, _ in c.most_common(n)]


def word_divergence(a: list[str], b: list[str]) -> float:
    """1 - Jaccard 유사도."""
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return 1 - len(sa & sb) / len(sa | sb)


def score_cluster(cid: int, central: pd.DataFrame, local: pd.DataFrame) -> IssueFlag:
    cw = top_words((central["clean_title"] + " " + central["content"]).tolist())
    lw = top_words((local["clean_title"] + " " + local["content"]).tolist())
    return IssueFlag(cid, len(central), len(local), round(word_divergence(cw, lw), 3), cw[:8], lw[:8])


def score_all(central: pd.DataFrame, matched: pd.DataFrame) -> list[IssueFlag]:
    out = []
    for cid, cg in central.groupby("cluster"):
        lg = matched[matched["cluster"] == cid]
        if len(lg):
            out.append(score_cluster(int(cid), cg, lg))
    return sorted(out, key=lambda f: (f.flagged, f.score), reverse=True)
