"""중앙지 사설 이슈 군집화 (KMeans + 실루엣 점수로 k 선택)."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from . import config
from .utils.exceptions import NotEnoughArticles
from .utils.logging_utils import get_logger

log = get_logger(__name__)


def choose_k(X: np.ndarray, k_min: int | None = None, k_max: int | None = None) -> int:
    k_min = k_min or config.K_MIN
    k_max = min(k_max or config.K_MAX, len(X) - 1)
    if k_max < k_min:
        raise NotEnoughArticles(f"군집화에 필요한 기사가 부족합니다 ({len(X)}건).")
    best_k, best_s = k_min, -1.0
    for k in range(k_min, k_max + 1):
        labels = KMeans(n_clusters=k, n_init=10, random_state=config.RANDOM_STATE).fit_predict(X)
        s = silhouette_score(X, labels)
        log.debug("k=%d silhouette=%.4f", k, s)
        if s > best_s:
            best_k, best_s = k, s
    log.info("선택된 군집 수 k=%d (silhouette %.4f)", best_k, best_s)
    return best_k


def cluster(X: np.ndarray, k: int | None = None) -> KMeans:
    k = k or choose_k(X)
    return KMeans(n_clusters=k, n_init=10, random_state=config.RANDOM_STATE).fit(X)


def summarize(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    df = df.assign(cluster=labels)
    g = df.groupby("cluster")
    return pd.DataFrame({
        "n_articles": g.size(),
        "n_providers": g["provider"].nunique(),
        "sample_title": g["clean_title"].first(),
    }).sort_values("n_articles", ascending=False)
