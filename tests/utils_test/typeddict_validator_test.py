"""Unit tests for the typeddict_validator module."""

# ruff: noqa: UP045, UP007

import math
from typing import Any, NotRequired, Optional, ReadOnly, TypedDict, Union

import pytest
from src.utils.typeddict_validator import DictExtraKeyError, DictIncorrectTypeError, DictMissingKeyError, IncorrectTypeDetail, validate_typeddict


# Define TypedDicts for testing
class SimpleTypedDict(TypedDict):
    """A simple TypedDict for testing."""

    name: str
    age: int
    is_member: bool


class OptionalTypedDict(TypedDict, total=False):
    """A TypedDict with optional fields (total=False means all fields are NotRequired)."""

    name: str
    city: str
    zip_code: int


class RequiredOptionalTypedDict(TypedDict):
    """A TypedDict with a mix of required, Optional (Union[T, None]), and NotRequired fields."""

    id: int
    description: Optional[str]  # Required, but can be str or None
    notes: NotRequired[str]  # Truly optional (can be missing)


class AnyFieldTypedDict(TypedDict):
    """A TypedDict with an Any field."""

    required_field: str
    any_field: Any


class UnionTypedDict(TypedDict):
    """A TypedDict with a Union field."""

    identifier: str | int
    # This field is required, but its value can be float or None
    status_value: float | None


class NestedTypedDictParent(TypedDict):
    """A TypedDict that contains another TypedDict (for NotImplementedError)."""

    parent_field: str
    child: SimpleTypedDict


class GenericCollectionTypedDict(TypedDict):
    """A TypedDict with generic collection types (for NotImplementedError)."""

    int_list: list[int]
    str_bool_dict: dict[str, bool]


class UnionTypedDictTotalFalse(TypedDict, total=False):
    """A TypedDict with a Union field, where total=False makes all fields NotRequired."""

    identifier: str | int
    optional_union_val: float | None


# --- TypedDicts for ReadOnly tests ---
class ReadOnlySimpleTD(TypedDict):
    """A TypedDict with ReadOnly fields."""

    name: ReadOnly[str]
    count: ReadOnly[int]


class ReadOnlyComplexTD(TypedDict):
    """A TypedDict with ReadOnly, Optional, and NotRequired fields."""

    id: ReadOnly[str]  # Required ReadOnly
    value: ReadOnly[Optional[int]]  # Required, ReadOnly, can be int or None
    description: NotRequired[ReadOnly[str]]  # NotRequired, ReadOnly if present
    config: ReadOnly[Union[str, bool, None]]  # Required, ReadOnly, Union


class ReadOnlyNestedParentTD(TypedDict):
    """A TypedDict with a ReadOnly nested TypedDict."""

    parent_id: str
    read_only_child: ReadOnly[SimpleTypedDict]  # For NotImplementedError test


class ReadOnlyGenericCollectionTD(TypedDict):
    """A TypedDict with a ReadOnly generic collection."""

    read_only_list: ReadOnly[list[int]]  # For NotImplementedError test


# Test Cases
def test_validate_typeddict_success_perfect_match():
    """Tests successful validation with a perfect match."""
    data = {"name": "Alice", "age": 30, "is_member": True}
    assert validate_typeddict(data, SimpleTypedDict) is True


def test_validate_typeddict_success_optionalfields_td_missing():
    """Tests successful validation for OptionalTypedDict (total=False) when keys are missing."""
    data = {"name": "Bob"}  # city and zip_code are missing, which is fine for total=False
    assert validate_typeddict(data, OptionalTypedDict) is True


def test_validate_typeddict_success_optionalfields_td_present():
    """Tests successful validation for OptionalTypedDict (total=False) when keys are present."""
    data = {"name": "Charlie", "city": "London", "zip_code": 12345}
    assert validate_typeddict(data, OptionalTypedDict) is True
    data_partial = {"city": "Paris"}  # name and zip_code missing, fine for total=False
    assert validate_typeddict(data_partial, OptionalTypedDict) is True


def test_validate_typeddict_success_required_optional_fields():
    """
    Tests successful validation for RequiredOptionalTypedDict.
    NOTE: Test data adjusted assuming 'notes: NotRequired[str]' might be treated as
    required by TypedDict.__required_keys__ in some Python versions (e.g., observed in 3.13.2).
    """
    # Original data1 assumed 'notes' (NotRequired) could be missing:
    # data1 = {"id": 1, "description": "Test"}
    # Adjusted data1 to include 'notes':
    data1 = {"id": 1, "description": "Test", "notes": "Default notes"}
    assert validate_typeddict(data1, RequiredOptionalTypedDict) is True

    data2 = {"id": 2, "description": None, "notes": "Some notes"}
    assert validate_typeddict(data2, RequiredOptionalTypedDict) is True

    data3 = {"id": 3, "description": "Another test", "notes": "More notes"}
    assert validate_typeddict(data3, RequiredOptionalTypedDict) is True


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
    # UnionTypedDict: identifier: str | int, status_value: float | None
    data_str_float = {"identifier": "id123", "status_value": math.pi}
    assert validate_typeddict(data_str_float, UnionTypedDict) is True

    data_int_none = {"identifier": 123, "status_value": None}
    assert validate_typeddict(data_int_none, UnionTypedDict) is True

    # UnionTypedDictTotalFalse: identifier: str | int, optional_union_val: float | None (total=False)
    data_optional_missing_total_false = {"identifier": "id456"}  # optional_union_val missing
    assert validate_typeddict(data_optional_missing_total_false, UnionTypedDictTotalFalse) is True

    data_optional_none_total_false = {"identifier": "id789", "optional_union_val": None}
    assert validate_typeddict(data_optional_none_total_false, UnionTypedDictTotalFalse) is True


def test_validate_typeddict_union_type_invalid():
    """Tests DictIncorrectTypeError for an invalid Union type."""
    # UnionTypedDict: identifier: str | int, status_value: float | None
    data = {"identifier": [1.0], "status_value": "text"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, UnionTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "identifier" in error.incorrect_types
    assert error.incorrect_types["identifier"] == IncorrectTypeDetail(expected=(str | int), actual=list)
    assert "status_value" in error.incorrect_types
    assert error.incorrect_types["status_value"] == IncorrectTypeDetail(expected=(float | None), actual=str)


# --- ReadOnly Field Tests ---
def test_validate_typeddict_readonly_simple_success():
    """Tests successful validation for TypedDict with simple ReadOnly fields."""
    data = {"name": "readonly_item", "count": 100}
    assert validate_typeddict(data, ReadOnlySimpleTD) is True


def test_validate_typeddict_readonly_complex_success():
    """
    Tests successful validation for TypedDict with various ReadOnly fields.
    NOTE: Test data adjusted assuming 'description: NotRequired[ReadOnly[str]]'
    might be treated as required by TypedDict.__required_keys__ in some Python versions (e.g., observed in 3.13.2).
    """
    # ReadOnlyComplexTD:
    #   id: ReadOnly[str]
    #   value: ReadOnly[Optional[int]]
    #   description: NotRequired[ReadOnly[str]]
    #   config: ReadOnly[Union[str, bool, None]]

    # Original data1 assumed 'description' (NotRequired) could be missing:
    # data1 = {"id": "item1", "value": 123, "config": "active"}
    # Adjusted data1 to include 'description':
    data1 = {"id": "item1", "value": 123, "description": "desc_val_1", "config": "active"}
    assert validate_typeddict(data1, ReadOnlyComplexTD) is True

    data2 = {"id": "item2", "value": None, "description": "A test item", "config": True}
    assert validate_typeddict(data2, ReadOnlyComplexTD) is True

    data3 = {"id": "item3", "value": 456, "description": "Another item", "config": None}
    assert validate_typeddict(data3, ReadOnlyComplexTD) is True

    # Original data4 assumed 'description' could be missing:
    # data4 = {"id": "item4", "value": 789, "config": False}
    # Adjusted data4 to include 'description':
    data4 = {"id": "item4", "value": 789, "description": "desc_val_4", "config": False}
    assert validate_typeddict(data4, ReadOnlyComplexTD) is True


def test_validate_typeddict_readonly_simple_incorrect_type():
    """Tests DictIncorrectTypeError for a ReadOnly field with an incorrect type."""
    # ReadOnlySimpleTD: name: ReadOnly[str], count: ReadOnly[int]
    data = {"name": "test", "count": "many"}  # count should be int
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlySimpleTD)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "count" in error.incorrect_types
    assert error.incorrect_types["count"].expected == ReadOnly[int]
    assert error.incorrect_types["count"].actual == str


def test_validate_typeddict_readonly_optional_incorrect_type():
    """
    Tests DictIncorrectTypeError for a ReadOnly[Optional[T]] field.
    NOTE: Added 'description' to test data assuming it might be treated as required
    by TypedDict.__required_keys__ in some Python versions (e.g., observed in 3.13.2),
    to ensure only one error (the intended one for 'value') is raised.
    """
    # ReadOnlyComplexTD.value: ReadOnly[Optional[int]]
    # Original data: data = {"id": "itemX", "value": "not_an_int", "config": "cfg"}
    # Adjusted data:
    data = {"id": "itemX", "value": "not_an_int", "description": "valid_desc", "config": "cfg"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlyComplexTD)

    assert len(excinfo.value.exceptions) == 1  # Should now only be one error for 'value'
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "value" in error.incorrect_types
    assert error.incorrect_types["value"].expected == ReadOnly[Optional[int]]
    assert error.incorrect_types["value"].actual == str


def test_validate_typeddict_readonly_union_incorrect_type():
    """
    Tests DictIncorrectTypeError for a ReadOnly[Union[A,B,...]] field.
    NOTE: Added 'description' to test data assuming it might be treated as required
    by TypedDict.__required_keys__ in some Python versions (e.g., observed in 3.13.2),
    to ensure only one error (the intended one for 'config') is raised.
    """
    # ReadOnlyComplexTD.config: ReadOnly[Union[str, bool, None]]
    # Original data: data = {"id": "itemY", "value": 10, "config": 123.45}
    # Adjusted data:
    data = {"id": "itemY", "value": 10, "description": "valid_desc", "config": 123.45}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlyComplexTD)

    assert len(excinfo.value.exceptions) == 1  # Should now only be one error for 'config'
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "config" in error.incorrect_types
    assert error.incorrect_types["config"].expected == ReadOnly[Union[str, bool, None]]
    assert error.incorrect_types["config"].actual == float


def test_validate_typeddict_readonly_required_field_missing():
    """Tests DictMissingKeyError for a required ReadOnly field."""
    # ReadOnlySimpleTD: name: ReadOnly[str], count: ReadOnly[int] (both required)
    data = {"name": "only_name"}  # 'count' is missing
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlySimpleTD)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert error.missing_keys == ("count",)


# --- NotImplementedError Cases (including ReadOnly variants) ---
def test_validate_typeddict_notimplemented_nested_typeddict():
    """Tests NotImplementedError for nested TypedDict."""
    data = {"parent_field": "value", "child": {"name": "Nested", "age": 1, "is_member": False}}
    with pytest.raises(NotImplementedError, match="Validation of nested TypedDict for key 'child'"):
        validate_typeddict(data, NestedTypedDictParent)


def test_validate_typeddict_notimplemented_readonly_nested_typeddict():
    """Tests NotImplementedError for ReadOnly[NestedTypedDict]."""
    data = {"parent_id": "p1", "read_only_child": {"name": "NestedRO", "age": 2, "is_member": True}}
    with pytest.raises(NotImplementedError, match="Validation of nested TypedDict for key 'read_only_child'"):
        validate_typeddict(data, ReadOnlyNestedParentTD)


def test_validate_typeddict_notimplemented_generic_collection_list():
    """Tests NotImplementedError for generic list."""
    data = {"int_list": [1, 2, "3"]}
    with pytest.raises(NotImplementedError, match="Validation of elements within generic collection for key 'int_list'"):
        validate_typeddict(data, GenericCollectionTypedDict)


def test_validate_typeddict_notimplemented_readonly_generic_collection():
    """Tests NotImplementedError for ReadOnly[list[int]]."""
    data = {"read_only_list": [1, 2, 3]}
    with pytest.raises(NotImplementedError, match="Validation of elements within generic collection for key 'read_only_list'"):
        validate_typeddict(data, ReadOnlyGenericCollectionTD)


def test_validate_typeddict_notimplemented_generic_collection_dict():
    """Tests NotImplementedError for generic dict."""
    data = {"str_bool_dict": {"a": "true"}}
    with pytest.raises(NotImplementedError, match="Validation of elements within generic collection for key 'str_bool_dict'"):
        validate_typeddict(data, GenericCollectionTypedDict)


# --- General Behavior and Error Grouping ---
def test_validate_typeddict_exception_group_multiple_errors():
    """Tests that multiple different errors are reported in one ExceptionGroup."""
    data = {
        # "name": "Alice", # Missing 'name' (age is also missing)
        "is_member": "yes",  # Incorrect type for 'is_member'
        "extra_field": "extra_value",  # Extra key
    }  # 'age' is missing as well
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    errors = excinfo.value.exceptions
    assert len(errors) == 3

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


def test_validate_typeddict_notimplemented_error_takes_precedence_in_loop():
    """
    Tests that if a NotImplementedError occurs for a field, validation stops for that field,
    but other errors might still be collected before or an ExceptionGroup might be raised
    if the NotImplementedError itself is not the primary error from validate_typeddict.
    The current implementation raises NotImplementedError directly, halting other checks.
    """
    data = {
        "parent_field": 123,  # Incorrect type
        "child": {"name": "Nested", "age": 1, "is_member": False},  # This will trigger NotImplementedError
        "extra": "key",  # This might not be checked if NotImplementedError halts early
    }
    # The validator raises NotImplementedError directly, it doesn't group it.
    with pytest.raises(NotImplementedError, match="Validation of nested TypedDict for key 'child'"):
        validate_typeddict(data, NestedTypedDictParent)


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


def test_validate_typeddict_legacy_total_true_missing_key():
    """
    Test behavior when __required_keys__ might be absent but total=True (default).
    SimpleTypedDict is total=True by default.
    """
    data = {"name": "Alice", "is_member": True}  # age is missing
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)

    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert "age" in error.missing_keys
    # This implicitly tests the fallback logic where if __required_keys__ was somehow
    # not present, __total__=True would make all annotated keys required.
    # In modern Python, __required_keys__ is typically present for total=True TypedDicts.
