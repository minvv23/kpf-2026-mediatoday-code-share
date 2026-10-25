"""지역지 사설을 중앙지 이슈 군집에 붙인다.

군집마다 대표 제목(첫 기사 제목)을 하나 정하고, 지역지 사설 제목과 겹치는 단어가
기준 개수 이상인 첫 번째 군집에 배정한다. 겹치는 군집이 없으면 제외한다.
"""
import pandas as pd

from . import config
from .utils.text_utils import tokenize


def representative_titles(central: pd.DataFrame) -> dict[int, set[str]]:
    """군집 번호 → 대표 제목 단어 집합."""
    return {int(cid): set(tokenize(g["clean_title"].iloc[0])) for cid, g in central.groupby("cluster")}


def shared_words(title: str, rep: set[str]) -> int:
    return len(set(tokenize(title)) & rep)


def assign(title: str, reps: dict[int, set[str]], min_shared: int) -> tuple[int, int]:
    for cid, rep in reps.items():
        n = shared_words(title, rep)
        if n >= min_shared:
            return cid, n
    return -1, 0


def match(central: pd.DataFrame, local: pd.DataFrame, min_shared: int | None = None) -> pd.DataFrame:
    reps = representative_titles(central)
    k = config.MIN_SHARED_WORDS if min_shared is None else min_shared
    pairs = [assign(t, reps, k) for t in local["clean_title"]]
    out = local.assign(cluster=[c for c, _ in pairs], shared=[n for _, n in pairs])
    return out[out["cluster"] >= 0].reset_index(drop=True)


def match_table(central: pd.DataFrame, matched: pd.DataFrame) -> pd.DataFrame:
    """군집별 중앙지·지역지 기사 수."""
    c = central.groupby("cluster").size().rename("central")
    l = matched.groupby("cluster").size().rename("local")
    return pd.concat([c, l], axis=1).fillna(0).astype(int).sort_values("local", ascending=False)
