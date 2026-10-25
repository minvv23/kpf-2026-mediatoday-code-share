"""단어 빈도(TF-IDF) 벡터."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .utils.text_utils import tokenize


class Vectorizer:
    def __init__(self, max_features: int = 20000):
        self.model = TfidfVectorizer(tokenizer=tokenize, lowercase=False, max_features=max_features,
                                     token_pattern=None)

    def fit_transform(self, texts: list[str]) -> np.ndarray:
        return self.model.fit_transform(texts).toarray()


def doc_text(df) -> list[str]:
    return (df["clean_title"] + " " + df["content"].str.slice(0, 500)).tolist()


def to_vectors(central) -> np.ndarray:
    """중앙지 사설 군집화용 벡터."""
    return Vectorizer().fit_transform(doc_text(central))
