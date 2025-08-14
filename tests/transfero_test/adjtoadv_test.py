# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.transfero.exceptions import InvalidWordError
from src.core.transfero.words import adj_to_adv


def test_adjtoadv():
    assert adj_to_adv("happy") == "happily"
    assert adj_to_adv("great") == "greatly"
    assert adj_to_adv("monotonous") == "monotonously"


def test_adjtoadv_error():
    with pytest.raises(InvalidWordError) as error:
        adj_to_adv("house")
    assert str(error.value) == "Word 'house' is not an adjective."
