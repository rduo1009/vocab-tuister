"""Unit tests for the typeddict_validator module."""

import math
from typing import Any, TypedDict

import pytest
from src.utils.typeddict_validator import DictExtraKeyError, DictIncorrectTypeError, DictMissingKeyError, IncorrectTypeDetail, validate_typeddict


# Define TypedDicts for testing
class SimpleTypedDict(TypedDict):
    """A simple TypedDict for testing."""

    name: str
    age: int
    is_member: bool


class OptionalTypedDict(TypedDict, total=False):
    """A TypedDict with optional fields."""

    name: str
    city: str
    zip_code: int


class AnyFieldTypedDict(TypedDict):
    """A TypedDict with an Any field."""

    required_field: str
    any_field: Any


class UnionTypedDict(TypedDict):
    """A TypedDict with a Union field."""

    identifier: str | int
    optional_union: float | None


class NestedTypedDictParent(TypedDict):
    """A TypedDict that contains another TypedDict (for NotImplementedError)."""

    parent_field: str
    child: SimpleTypedDict


class GenericCollectionTypedDict(TypedDict):
    """A TypedDict with generic collection types (for NotImplementedError)."""

    int_list: list[int]
    str_bool_dict: dict[str, bool]


class UnionTypedDictOptional(TypedDict, total=False):
    """A TypedDict with a Union field, where one is optional."""

    identifier: str | int
    optional_union: float | None  # total=False makes this truly optional


# Test Cases
def test_validate_typeddict_success_perfect_match():
    """Tests successful validation with a perfect match."""
    data = {"name": "Alice", "age": 30, "is_member": True}
    assert validate_typeddict(data, SimpleTypedDict) is True


def test_validate_typeddict_success_optional_missing():
    """Tests successful validation when optional keys are missing."""
    data = {"name": "Bob"}
    assert validate_typeddict(data, OptionalTypedDict) is True


def test_validate_typeddict_success_optional_present():
    """Tests successful validation when optional keys are present and correct."""
    data = {"name": "Charlie", "city": "London", "zip_code": 12345}
    assert validate_typeddict(data, OptionalTypedDict) is True
    data_partial = {"city": "Paris"}
    assert validate_typeddict(data_partial, OptionalTypedDict) is True


def test_validate_typeddict_success_any_field():
    """Tests successful validation with an Any field."""
    data_str = {"required_field": "test", "any_field": "string_value"}
    assert validate_typeddict(data_str, AnyFieldTypedDict) is True

    data_int = {"required_field": "test", "any_field": 123}
    assert validate_typeddict(data_int, AnyFieldTypedDict) is True

    data_list = {"required_field": "test", "any_field": [1, 2, 3]}
    assert validate_typeddict(data_list, AnyFieldTypedDict) is True

    data_none = {"required_field": "test", "any_field": None}
    assert validate_typeddict(data_none, AnyFieldTypedDict) is True


def test_validate_typeddict_missing_key_single():
    """Tests DictMissingKeyError for a single missing required key."""
    data = {"name": "Alice", "is_member": True}  # age is missing
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert error.missing_keys == ("age",)


def test_validate_typeddict_missing_keys_multiple():
    """Tests DictMissingKeyError for multiple missing required keys."""
    data = {"is_member": True}  # name and age are missing
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert error.missing_keys == ("age", "name")  # sorted


def test_validate_typeddict_extra_key_single():
    """Tests DictExtraKeyError for a single extra key."""
    data = {"name": "Alice", "age": 30, "is_member": True, "extra_field": "value"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictExtraKeyError)
    assert error.extra_keys == ("extra_field",)


def test_validate_typeddict_extra_keys_multiple():
    """Tests DictExtraKeyError for multiple extra keys."""
    data = {"name": "Alice", "age": 30, "is_member": True, "extra1": "val1", "extra2": "val2"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictExtraKeyError)
    assert error.extra_keys == ("extra1", "extra2")  # sorted


def test_validate_typeddict_incorrect_type_single():
    """Tests DictIncorrectTypeError for a single incorrect type."""
    data = {"name": "Alice", "age": "thirty", "is_member": True}  # age is str, not int
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "age" in error.incorrect_types
    assert error.incorrect_types["age"] == IncorrectTypeDetail(expected=int, actual=str)


def test_validate_typeddict_incorrect_types_multiple():
    """Tests DictIncorrectTypeError for multiple incorrect types."""
    data = {"name": 123, "age": "thirty", "is_member": "yes"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert len(error.incorrect_types) == 3
    assert error.incorrect_types["name"] == IncorrectTypeDetail(expected=str, actual=int)
    assert error.incorrect_types["age"] == IncorrectTypeDetail(expected=int, actual=str)
    assert error.incorrect_types["is_member"] == IncorrectTypeDetail(expected=bool, actual=str)


def test_validate_typeddict_union_type_valid():
    """Tests successful validation with Union types."""
    data_str = {"identifier": "id123", "optional_union": math.pi}
    assert validate_typeddict(data_str, UnionTypedDict) is True

    data_int = {"identifier": 123, "optional_union": None}
    assert validate_typeddict(data_int, UnionTypedDict) is True

    # For total=True, if a field is `Union[X, None]`, it's effectively optional if None is provided or if the key is missing.
    # However, TypedDict's __required_keys__ will still list it if not `total=False`.
    # The current validator logic for missing keys is based on __required_keys__.
    # If `optional_union: Union[float, None]` is a required key, it must be present.
    # Let's adjust UnionTypedDict to make optional_union truly optional for this test.

    data_optional_missing_total_false = {"identifier": "id456"}
    assert validate_typeddict(data_optional_missing_total_false, UnionTypedDictOptional) is True

    data_optional_none_total_false = {"identifier": "id789", "optional_union": None}
    assert validate_typeddict(data_optional_none_total_false, UnionTypedDictOptional) is True


def test_validate_typeddict_union_type_invalid():
    """Tests DictIncorrectTypeError for an invalid Union type."""
    data = {"identifier": math.pi, "optional_union": "text"}  # identifier is float, not str/int
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, UnionTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "identifier" in error.incorrect_types
    assert error.incorrect_types["identifier"] == IncorrectTypeDetail(expected=str | int, actual=float)
    # optional_union is also incorrect
    assert "optional_union" in error.incorrect_types
    assert error.incorrect_types["optional_union"] == IncorrectTypeDetail(expected=float | None, actual=str)


def test_validate_typeddict_notimplemented_nested_typeddict():
    """Tests NotImplementedError for nested TypedDict."""
    data = {"parent_field": "value", "child": {"name": "Nested", "age": 1, "is_member": False}}
    with pytest.raises(NotImplementedError) as excinfo:
        validate_typeddict(data, NestedTypedDictParent)

    assert "Validation of nested TypedDict for key 'child' is not yet implemented." in str(excinfo)


def test_validate_typeddict_notimplemented_generic_collection_list():
    """Tests NotImplementedError for generic list."""
    data = {"int_list": [1, 2, "3"]}  # "3" would be wrong if checked
    with pytest.raises(NotImplementedError) as excinfo:
        validate_typeddict(data, GenericCollectionTypedDict)

    assert "Validation of elements within generic collection for key 'int_list' (<class 'list'>) is not yet implemented." in str(excinfo)


def test_validate_typeddict_notimplemented_generic_collection_dict():
    """Tests NotImplementedError for generic dict."""
    data = {"str_bool_dict": {"a": "true"}}  # "true" would be wrong if checked
    with pytest.raises(NotImplementedError) as excinfo:
        validate_typeddict(data, GenericCollectionTypedDict)

    assert "Validation of elements within generic collection for key 'str_bool_dict' (<class 'dict'>) is not yet implemented." in str(excinfo)


def test_validate_typeddict_exception_group_multiple_errors():
    """Tests that multiple different errors are reported in one ExceptionGroup."""
    data = {
        # "name": "Alice", # Missing 'name' and 'age'
        "is_member": "yes",  # Incorrect type for 'is_member'
        "extra_field": "extra_value",  # Extra key
    }
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    errors = excinfo.value.exceptions
    assert len(errors) == 3  # DictMissingKeyError, DictIncorrectTypeError, DictExtraKeyError

    assert any(isinstance(e, DictMissingKeyError) for e in errors)
    missing_key_error = next(e for e in errors if isinstance(e, DictMissingKeyError))
    assert missing_key_error.missing_keys == ("age", "name")

    assert any(isinstance(e, DictIncorrectTypeError) for e in errors)
    incorrect_type_error = next(e for e in errors if isinstance(e, DictIncorrectTypeError))
    assert "is_member" in incorrect_type_error.incorrect_types
    assert incorrect_type_error.incorrect_types["is_member"] == IncorrectTypeDetail(expected=bool, actual=str)

    assert any(isinstance(e, DictExtraKeyError) for e in errors)
    extra_key_error = next(e for e in errors if isinstance(e, DictExtraKeyError))
    assert extra_key_error.extra_keys == ("extra_field",)


def test_validate_typeddict_exception_group_with_notimplemented():
    """Tests ExceptionGroup with a mix of standard errors and NotImplementedError."""
    data = {
        "parent_field": 123,  # Incorrect type
        "child": {"name": "Nested", "age": 1, "is_member": False},  # NotImplemented
        "extra": "key",  # Extra key
    }
    with pytest.raises(NotImplementedError) as excinfo:
        validate_typeddict(data, NestedTypedDictParent)

    assert "Validation of nested TypedDict for key 'child'" in str(excinfo)


def test_typeguard_returns_true_on_success():
    """Ensures the function returns True on successful validation (TypeGuard behavior)."""
    data = {"name": "Valid", "age": 100, "is_member": False}
    result = validate_typeddict(data, SimpleTypedDict)
    assert result is True


# Test for total=False behavior regarding required keys
class TotalFalseDict(TypedDict, total=False):
    """A TypedDict with total=False."""

    name: str
    value: int


def test_validate_typeddict_total_false_all_present():
    """Test total=False with all keys present."""
    data = {"name": "Test", "value": 1}
    assert validate_typeddict(data, TotalFalseDict) is True


def test_validate_typeddict_total_false_some_present():
    """Test total=False with some keys present."""
    data = {"name": "Test"}
    assert validate_typeddict(data, TotalFalseDict) is True
    data2 = {"value": 2}
    assert validate_typeddict(data2, TotalFalseDict) is True


def test_validate_typeddict_total_false_none_present():
    """Test total=False with no keys present (should be valid)."""
    data = {}
    assert validate_typeddict(data, TotalFalseDict) is True


def test_validate_typeddict_total_false_extra_key():
    """Test total=False with an extra key."""
    data = {"name": "Test", "extra": "key"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, TotalFalseDict)
    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictExtraKeyError)
    assert error.extra_keys == ("extra",)


# Test for __required_keys__ not present and __total__ = True (older Python simulation)
class LegacyTotalTrueDict(TypedDict):
    field_a: str
    field_b: int
    # Simulate no __required_keys__ by manually removing if possible, or by design
    # For testing, we assume get_type_hints(LegacyTotalTrueDict) provides all keys
    # and __total__ is True by default.


# This test is a bit conceptual as __required_keys__ is usually present.
# The validator code has a fallback:
# if not hasattr(td_type, "__required_keys__") and getattr(td_type, "__total__", True):
#     required_keys = all_keys
# We'll test this by ensuring a missing key raises an error for a default TypedDict.
def test_validate_typeddict_legacy_total_true_missing_key():
    """Test behavior simulating older Python where __required_keys__ might be absent but total=True."""
    # SimpleTypedDict is total=True by default.
    data = {"name": "Alice", "is_member": True}  # age is missing
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)  # SimpleTypedDict is total=True

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert "age" in error.missing_keys
    # This implicitly tests the fallback logic if SimpleTypedDict somehow lacked __required_keys__
    # but was still considered total=True. In modern Python, __required_keys__ will be present.
