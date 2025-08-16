import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido._syllables import count_syllables


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("amo", 2),  # a-mo
        ("bene", 2),  # be-ne
        ("video", 3),  # vi-de-o
        ("aureus", 2),  # au-reus
        ("poena", 2),  # poe-na
        ("caelum", 2),  # cae-lum
        ("imperator", 4),  # im-pe-ra-tor
        ("amicitia", 5),  # a-mi-ci-ti-a
        ("intellego", 4),  # in-tel-le-go
        ("rex", 1),  # rex
        ("lux", 1),  # lux
        ("cor", 1),  # cor
        ("dea", 2),  # de-a
        ("deae", 2),  # de-ae
        ("proelio", 3),  # proe-li-o
        ("mihi", 2),  # mi-hi
        ("nihil", 2),  # ni-hil
    ],
)
def test_count_syllables(word, expected):
    assert count_syllables(word) == expected
