"""기사 생성용 프롬프트 (예시).

이 저장소는 LLM을 직접 호출하지 않는다. 아래 프롬프트와 비교 초안을 각사가 쓰는 LLM에 넣어 사용한다.
"""
from .report import Draft

PROMPT_TEMPLATE = """아래 자료를 바탕으로 중앙지와 지역 신문의 사설을 비교하는 기사를 써줘.

{body}
"""


def build_prompt(draft: Draft) -> str:
    return PROMPT_TEMPLATE.format(body=draft.body)
