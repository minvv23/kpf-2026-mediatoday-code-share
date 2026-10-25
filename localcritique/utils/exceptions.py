"""패키지 공통 예외."""


class LocalCritiqueError(Exception):
    """기본 예외."""


class DataError(LocalCritiqueError):
    """입력 데이터가 비었거나 형식이 맞지 않음."""


class NotEnoughArticles(DataError):
    """군집화·비교에 필요한 기사 수가 부족함."""


class ExportError(LocalCritiqueError):
    """결과물 저장 실패."""
