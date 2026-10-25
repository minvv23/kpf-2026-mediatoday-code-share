"""기사 데이터 읽기와 전처리.

입력은 CSV(또는 각사 DB 조회 결과)이며 필수 열은 title, content, provider, date다.
"""
from pathlib import Path

import pandas as pd

from . import config, providers
from .utils.logging_utils import get_logger
from .utils.text_utils import normalize, strip_title_tag
from .utils.validators import check_columns, check_not_empty

log = get_logger(__name__)


def read_articles(path=None) -> pd.DataFrame:
    p = Path(path or config.INPUT_PATH)
    df = pd.read_csv(p, encoding="utf-8-sig")
    check_columns(df)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    log.info("기사 %d건 읽음: %s", len(df), p.name)
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["title"] = df["title"].map(normalize)
    df["content"] = df["content"].fillna("").map(normalize)
    df = df[df["content"].str.len() >= config.MIN_BODY_CHARS]
    df = df.drop_duplicates(subset=["provider", "title"])
    df["clean_title"] = df["title"].map(strip_title_tag)
    df["media_type"] = df["provider"].map(providers.media_type)
    df["region"] = df["provider"].map(providers.region)
    return df.reset_index(drop=True)


def editorials(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["title"].str.contains(config.EDITORIAL_KEYWORD, na=False)].reset_index(drop=True)


def in_window(df: pd.DataFrame, end=None, hours: int | None = None) -> pd.DataFrame:
    end = pd.Timestamp(end) if end is not None else df["date"].max()
    start = end - pd.Timedelta(hours=hours or config.WINDOW_HOURS)
    return df[(df["date"] > start) & (df["date"] <= end)].reset_index(drop=True)


def split_by_type(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    central = check_not_empty(df[df["media_type"] == "중앙지"].reset_index(drop=True), "중앙지 기사")
    local = df[df["media_type"] == "지역지"].reset_index(drop=True)
    return central, local


def load(path=None, end=None) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = clean(read_articles(path))
    df = in_window(editorials(df), end)
    central, local = split_by_type(df)
    log.info("중앙지 사설 %d건 / 지역지 사설 %d건", len(central), len(local))
    return central, local
