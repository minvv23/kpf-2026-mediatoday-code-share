import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from localcritique import loader, sample_data  # noqa: E402


@pytest.fixture
def articles():
    return loader.clean(sample_data.make(n_days=1))


@pytest.fixture
def split(articles):
    return loader.split_by_type(loader.editorials(articles))
