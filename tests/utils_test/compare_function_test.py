import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from typing import TYPE_CHECKING

from src.utils.compare_function import compare

if TYPE_CHECKING:
    from collections.abc import Sequence


def test_equal_sequences():
    first = [1, 2, 3]
    second = [1, 2, 3]
    assert compare(first, second)


def test_unequal_sequences():
    first = [1, 2, 3]
    second = [1, 2, 4]
    assert not (compare(first, second))


def test_different_length_sequences():
    first = [1, 2, 3]
    second = [1, 2]
    assert not (compare(first, second))


def test_empty_sequences():
    first: Sequence[int] = []
    second: Sequence[int] = []
    assert compare(first, second)


def test_duplicate_elements():
    first = [1, 1, 2]
    second = [1, 2, 1]
    assert compare(first, second)


def test_different_order():
    first = [3, 1, 2]
    second = [1, 2, 3]
    assert compare(first, second)


def test_string_sequences():
    first = ["a", "b", "c"]
    second = ["c", "a", "b"]
    assert compare(first, second)


def test_mixed_type_sequences():
    first = [(1, 2), "abc", 3]
    second = [3, (1, 2), "abc"]
    assert compare(first, second)


def test_one_empty_sequence():
    first = [1, 2, 3]
    second: Sequence[int] = []
    assert not (compare(first, second))
