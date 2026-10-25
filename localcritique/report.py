"""비교 초안 만들기.

기본형은 템플릿으로 기사 제목과 앞부분을 나란히 배치한 초안만 만든다.
문장 생성은 prompt.py의 프롬프트와 이 초안을 각사 LLM에 넣어 진행한다.
"""
from dataclasses import dataclass

import pandas as pd

from .divergence import IssueFlag
from .utils.text_utils import lead, truncate


@dataclass
class Draft:
    cluster: int
    title: str
    body: str


def _section(name: str, df: pd.DataFrame, n: int = 3) -> str:
    lines = [f"[{name}]"]
    for _, r in df.head(n).iterrows():
        lines.append(f"- {r['provider']} 「{truncate(r['clean_title'], 50)}」: {truncate(lead(r['content']), 160)}")
    return "\n".join(lines)


def make_draft(flag: IssueFlag, central: pd.DataFrame, local: pd.DataFrame) -> Draft:
    cg = central[central["cluster"] == flag.cluster]
    lg = local[local["cluster"] == flag.cluster]
    providers = "·".join(lg["provider"].unique()[:2])
    title = f"{providers} 등 지역 신문과 중앙지의 시각 비교: {truncate(cg['clean_title'].iloc[0], 30)}"
    body = "\n\n".join([
        "[이슈 개요]\n" + truncate(lead(cg["content"].iloc[0], 2), 240),
        _section("중앙지", cg),
        _section("지역 신문", lg),
        "[주요 단어]\n중앙지: " + ", ".join(flag.central_words) + "\n지역 신문: " + ", ".join(flag.local_words),
    ])
    return Draft(flag.cluster, title, body)
