import os
import sys  # noqa: E401

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.accido.misc import MultipleMeanings


def test_repr():
    multiple_endings = MultipleMeanings(("a", "b", "c"))
    assert repr(multiple_endings) == "MultipleMeanings(a, b, c)"
