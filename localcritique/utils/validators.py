"""입력 검사."""
import pandas as pd

from .exceptions import DataError

REQUIRED_COLUMNS = ["title", "content", "provider", "date"]


def check_columns(df: pd.DataFrame, required=REQUIRED_COLUMNS) -> pd.DataFrame:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise DataError(f"필수 열이 없습니다: {missing}")
    return df


def check_not_empty(df: pd.DataFrame, name: str = "data") -> pd.DataFrame:
    if df is None or df.empty:
        raise DataError(f"{name}가 비어 있습니다.")
    return df


def check_range(value: float, lo: float, hi: float, name: str) -> float:
    if not lo <= value <= hi:
        raise ValueError(f"{name}은 {lo}~{hi} 사이여야 합니다: {value}")
    return value
