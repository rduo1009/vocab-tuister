import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.compact_function import compact


def test_empty_list():
    assert compact([]) == []


def test_single_element():
    assert compact([1]) == [1]
    assert compact(["a"]) == ["a"]


def test_numbers():
    assert compact([1, 2, 3]) == [6]
    assert compact([1.5, 2.5, 3.0]) == [7.0]
    assert compact([-1, 1, -2, 2]) == [0]


def test_strings():
    assert compact(["a", "b", "c"]) == ["abc"]
    assert compact(["test", "ing"]) == ["testing"]
    assert compact(["", "x", ""]) == ["x"]


def test_mixed_types():
    result = compact([1, "a", 2, "b", 3])
    assert result == [6, "ab"]


def test_lists():
    assert compact([[1], [2], [3]]) == [[1, 2, 3]]
    assert compact([[1, 2], [3, 4]]) == [[1, 2, 3, 4]]


def test_non_addable_types():
    class NoAdd:
        pass

    obj1, obj2 = NoAdd(), NoAdd()
    assert compact([obj1, obj2]) == [obj1, obj2]


def test_partial_addition():
    assert compact([1, "a", 2, 3, "b", "c"]) == [6, "abc"]
    assert compact(["x", 1, "y", 2, "z", 3]) == ["xyz", 6]
