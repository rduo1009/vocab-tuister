import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.duplicates import contains_duplicates, remove_duplicates


class TestContainsDuplicates:
    def test_contains_duplicates_empty(self):
        assert not contains_duplicates([])
        assert not contains_duplicates(())

    def test_contains_duplicates_single(self):
        assert not contains_duplicates([1])
        assert not contains_duplicates(("a",))

    def test_contains_duplicates_hashable(self):
        assert contains_duplicates([1, 2, 1])
        assert contains_duplicates(("a", "b", "a"))
        assert not contains_duplicates([1, 2, 3])
        assert not contains_duplicates(("a", "b", "c"))

    def test_contains_duplicates_unhashable(self):
        assert contains_duplicates([[1], [2], [1]])
        assert contains_duplicates(([1], [2], [1]))
        assert not contains_duplicates([[1], [2], [3]])
        assert not contains_duplicates(([1], [2], [3]))


class TestRemoveDuplicates:
    def test_remove_duplicates_empty(self):
        assert remove_duplicates([]) == []
        assert remove_duplicates(()) == ()

    def test_remove_duplicates_single(self):
        assert remove_duplicates([1]) == [1]
        assert remove_duplicates(("a",)) == ("a",)

    def test_remove_duplicates_hashable(self):
        assert sorted(remove_duplicates([1, 2, 1, 3, 2])) == [1, 2, 3]
        assert sorted(remove_duplicates(("a", "b", "a", "c"))) == ["a", "b", "c"]

    def test_remove_duplicates_unhashable(self):
        result = remove_duplicates([[1], [2], [1], [3], [2]])
        assert len(result) == 3
        assert [1] in result
        assert [2] in result
        assert [3] in result

    def test_remove_duplicates_preserves_type(self):
        list_result = remove_duplicates([1, 2, 1])
        assert isinstance(list_result, list)

        tuple_result = remove_duplicates((1, 2, 1))
        assert isinstance(tuple_result, tuple)
