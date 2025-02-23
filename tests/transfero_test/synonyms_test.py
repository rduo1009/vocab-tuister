import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.transfero.synonyms import find_synonyms


@pytest.mark.manual
def test_synonyms():
    words = ["house", "car", "happy", "sad", "disgust", "fortune"]
    for word in words:
        synonyms = find_synonyms(word)
        ic(synonyms)  # type: ignore[name-defined] # noqa: F821
