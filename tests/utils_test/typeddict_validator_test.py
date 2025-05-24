"""Unit tests for the typeddict_validator module."""

# pyright: basic
# ruff: noqa: UP045, UP007

import math
from typing import Any, NotRequired, Optional, ReadOnly, TypedDict, Union

import pytest
from src.utils.typeddict_validator import DictExtraKeyError, DictIncorrectTypeError, DictMissingKeyError, IncorrectTypeDetail, validate_typeddict


# --- Existing TypedDicts (abbreviated for brevity, ensure they are fully defined in your actual file) ---
class SimpleTypedDict(TypedDict):
    name: str
    age: int
    is_member: bool


class OptionalTypedDict(TypedDict, total=False):
    name: str
    city: str
    zip_code: int


class RequiredOptionalTypedDict(TypedDict):
    id: int
    description: Optional[str]
    notes: NotRequired[str]


class AnyFieldTypedDict(TypedDict):
    required_field: str
    any_field: Any


class UnionTypedDict(TypedDict):
    identifier: str | int
    status_value: float | None


class NestedTypedDictParent(TypedDict):
    parent_field: str
    child: SimpleTypedDict


class GenericCollectionTypedDict(TypedDict):
    int_list: list[int]
    str_bool_dict: dict[str, bool]


class UnionTypedDictTotalFalse(TypedDict, total=False):
    identifier: str | int
    optional_union_val: float | None


class ReadOnlySimpleTD(TypedDict):
    name: ReadOnly[str]
    count: ReadOnly[int]


class ReadOnlyComplexTD(TypedDict):
    id: ReadOnly[str]
    value: ReadOnly[Optional[int]]
    description: NotRequired[ReadOnly[str]]
    config: ReadOnly[Union[str, bool, None]]


class ReadOnlyNestedParentTD(TypedDict):
    parent_id: str
    read_only_child: ReadOnly[SimpleTypedDict]


class ReadOnlyGenericCollectionTD(TypedDict):
    read_only_list: ReadOnly[list[int]]


class TotalFalseDict(TypedDict, total=False):
    name: str
    value: int


class TotalTrueExplicitNotRequired(TypedDict):
    req_field: str
    opt_field: NotRequired[int]
    req_union_can_be_none: Union[bool, None]


class TotalTrueNotRequiredReadOnly(TypedDict):
    req_ro_field: ReadOnly[str]
    opt_ro_field: NotRequired[ReadOnly[int]]


class AdvancedUnionTD(TypedDict):
    field_ro_union: ReadOnly[Union[str, int, None]]
    field_nr_union: NotRequired[Union[str, bool]]
    field_nr_ro_union: NotRequired[ReadOnly[Union[float, None]]]
    field_ro_nr_union: ReadOnly[NotRequired[Union[int, bool]]]
    field_union_with_ro_member: Union[ReadOnly[str], int]  # type: ignore[valid-type]
    field_union_with_multiple_ro_members: Union[ReadOnly[bool], ReadOnly[float], None]  # type: ignore[valid-type]


# --- Test Cases ---


# --- Success Tests (largely unchanged) ---
def test_validate_typeddict_success_perfect_match():
    data = {"name": "Alice", "age": 30, "is_member": True}
    assert validate_typeddict(data, SimpleTypedDict) is True


def test_validate_typeddict_success_optionalfields_td_missing():
    data = {"name": "Bob"}
    assert validate_typeddict(data, OptionalTypedDict) is True


def test_validate_typeddict_success_optionalfields_td_present():
    data = {"name": "Charlie", "city": "London", "zip_code": 12345}
    assert validate_typeddict(data, OptionalTypedDict) is True
    data_partial = {"city": "Paris"}
    assert validate_typeddict(data_partial, OptionalTypedDict) is True


def test_validate_typeddict_success_required_optional_fields():
    data1 = {"id": 1, "description": "Test"}
    assert validate_typeddict(data1, RequiredOptionalTypedDict) is True
    data2 = {"id": 2, "description": None, "notes": "Some notes"}
    assert validate_typeddict(data2, RequiredOptionalTypedDict) is True
    data3 = {"id": 3, "description": "Another test", "notes": "More notes"}
    assert validate_typeddict(data3, RequiredOptionalTypedDict) is True
    data4 = {"id": 4, "description": None}
    assert validate_typeddict(data4, RequiredOptionalTypedDict) is True


def test_validate_typeddict_success_any_field():
    data_str = {"required_field": "test", "any_field": "string_value"}
    assert validate_typeddict(data_str, AnyFieldTypedDict) is True
    data_int = {"required_field": "test", "any_field": 123}
    assert validate_typeddict(data_int, AnyFieldTypedDict) is True
    data_list = {"required_field": "test", "any_field": [1, 2, 3]}
    assert validate_typeddict(data_list, AnyFieldTypedDict) is True
    data_none = {"required_field": "test", "any_field": None}
    assert validate_typeddict(data_none, AnyFieldTypedDict) is True


# --- Error Tests (modified for single error raising) ---
def test_validate_typeddict_missing_key_single():
    data = {"name": "Alice", "is_member": True}  # age is missing
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    assert excinfo.value.missing_keys == ("age",)


def test_validate_typeddict_missing_keys_multiple():
    data = {"is_member": True}  # name and age are missing
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    assert excinfo.value.missing_keys == ("age", "name")  # Assuming sorted output


def test_validate_typeddict_extra_key_single():
    data = {"name": "Alice", "age": 30, "is_member": True, "extra_field": "value"}
    with pytest.raises(DictExtraKeyError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    assert excinfo.value.extra_keys == ("extra_field",)


def test_validate_typeddict_extra_keys_multiple():
    data = {"name": "Alice", "age": 30, "is_member": True, "extra1": "val1", "extra2": "val2"}
    with pytest.raises(DictExtraKeyError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    assert excinfo.value.extra_keys == ("extra1", "extra2")  # Assuming sorted output


def test_validate_typeddict_incorrect_type_single():
    data = {"name": "Alice", "age": "thirty", "is_member": True}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    error = excinfo.value
    assert "age" in error.incorrect_types
    assert error.incorrect_types["age"] == IncorrectTypeDetail(expected=int, actual=str)


def test_validate_typeddict_incorrect_types_first_encountered():
    """Tests DictIncorrectTypeError for the first incorrect type encountered."""
    # Original data: {"name": 123, "age": "thirty", "is_member": "yes"}
    # Assuming dict iteration order or sorted key checking makes "name" or "age" first.
    # If "name" (value 123) is checked before "age" (value "thirty"):
    data_name_first_error = {"name": 123, "age": 30, "is_member": True}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data_name_first_error, SimpleTypedDict)
    error = excinfo.value
    assert "name" in error.incorrect_types
    assert len(error.incorrect_types) == 1
    assert error.incorrect_types["name"] == IncorrectTypeDetail(expected=str, actual=int)

    # If "age" (value "thirty") is checked before "name" (value 123):
    data_age_first_error = {"name": "Alice", "age": "thirty", "is_member": True}  # This is same as test_validate_typeddict_incorrect_type_single
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data_age_first_error, SimpleTypedDict)
    error = excinfo.value
    assert "age" in error.incorrect_types
    assert len(error.incorrect_types) == 1
    assert error.incorrect_types["age"] == IncorrectTypeDetail(expected=int, actual=str)

    # Test with the original "multiple" error data, asserting for one of them
    # The specific key depends on internal iteration order of `common_keys`
    # which is `dict_keys.intersection(all_keys)`.
    # If common_keys were sorted for iteration in validate_typeddict, 'age' would be first.
    # If it iterates based on dict key insertion order, 'name' could be first.
    # For robustness, it's better if validate_typeddict sorts common_keys before iterating for type checks.
    # Assuming the validator doesn't sort, this test might be flaky or needs to accept multiple outcomes.
    # Let's make a dict where 'age' is likely first if sorted, or if no specific order is guaranteed,
    # we test one specific scenario.
    data = {"name": 123, "age": "thirty", "is_member": "yes"}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    error = excinfo.value
    # We can only assert that *an* error occurred and it's one of the expected ones.
    assert len(error.incorrect_types) == 1
    first_error_key = next(iter(error.incorrect_types.keys()))
    if first_error_key == "name":
        assert error.incorrect_types["name"] == IncorrectTypeDetail(expected=str, actual=int)
    elif first_error_key == "age":
        assert error.incorrect_types["age"] == IncorrectTypeDetail(expected=int, actual=str)
    elif first_error_key == "is_member":
        assert error.incorrect_types["is_member"] == IncorrectTypeDetail(expected=bool, actual=str)
    else:
        pytest.fail(f"Unexpected key in error: {first_error_key}")


def test_validate_typeddict_union_type_valid():
    data_str_float = {"identifier": "id123", "status_value": math.pi}
    assert validate_typeddict(data_str_float, UnionTypedDict) is True
    data_int_none = {"identifier": 123, "status_value": None}
    assert validate_typeddict(data_int_none, UnionTypedDict) is True
    data_optional_missing_total_false = {"identifier": "id456"}
    assert validate_typeddict(data_optional_missing_total_false, UnionTypedDictTotalFalse) is True
    data_optional_none_total_false = {"identifier": "id789", "optional_union_val": None}
    assert validate_typeddict(data_optional_none_total_false, UnionTypedDictTotalFalse) is True


def test_validate_typeddict_union_type_invalid_first_encountered():
    # Data: {"identifier": [1.0], "status_value": "text"}
    # Assuming 'identifier' is checked first due to dict order or sorted key processing
    data = {"identifier": [1.0], "status_value": "text"}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data, UnionTypedDict)
    error = excinfo.value
    assert len(error.incorrect_types) == 1
    # Check if "identifier" is the key reported, assuming it's processed first.
    # If "status_value" could be processed first, this test would need adjustment or be made more flexible.
    first_error_key = next(iter(error.incorrect_types.keys()))
    if first_error_key == "identifier":
        assert error.incorrect_types["identifier"] == IncorrectTypeDetail(expected=(str | int), actual=list)
    elif first_error_key == "status_value":
        assert error.incorrect_types["status_value"] == IncorrectTypeDetail(expected=(float | None), actual=str)
    else:
        pytest.fail(f"Unexpected key in error: {first_error_key}")


# --- ReadOnly Field Tests (modified for single error) ---
def test_validate_typeddict_readonly_simple_success():
    data = {"name": "readonly_item", "count": 100}
    assert validate_typeddict(data, ReadOnlySimpleTD) is True


def test_validate_typeddict_readonly_complex_success():
    data1 = {"id": "item1", "value": 123, "config": "active"}
    assert validate_typeddict(data1, ReadOnlyComplexTD) is True
    data2 = {"id": "item2", "value": None, "description": "A test item", "config": True}
    assert validate_typeddict(data2, ReadOnlyComplexTD) is True


def test_validate_typeddict_readonly_simple_incorrect_type():
    data = {"name": "test", "count": "many"}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data, ReadOnlySimpleTD)
    error = excinfo.value
    assert "count" in error.incorrect_types
    assert error.incorrect_types["count"].expected == ReadOnly[int]
    assert error.incorrect_types["count"].actual == str


def test_validate_typeddict_readonly_optional_incorrect_type():
    data = {"id": "itemX", "value": "not_an_int", "config": "cfg"}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data, ReadOnlyComplexTD)
    error = excinfo.value
    assert "value" in error.incorrect_types
    assert error.incorrect_types["value"].expected == ReadOnly[Optional[int]]
    assert error.incorrect_types["value"].actual == str


def test_validate_typeddict_readonly_union_incorrect_type():
    data = {"id": "itemY", "value": 10, "config": 123.45}  # Error on 'config'
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data, ReadOnlyComplexTD)
    error = excinfo.value
    assert "config" in error.incorrect_types
    assert error.incorrect_types["config"].expected == ReadOnly[Union[str, bool, None]]
    assert error.incorrect_types["config"].actual == float


def test_validate_typeddict_readonly_required_field_missing():
    data = {"name": "only_name"}  # 'count' is missing
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data, ReadOnlySimpleTD)
    assert excinfo.value.missing_keys == ("count",)


# --- NEW TESTS FOR `required_keys` FIX (Total=True with NotRequired) ---
# (Error cases modified for single error raising)
def test_total_true_explicit_notrequired_cases():
    # Case 1 & 2: Success (opt_field missing or present and correct)
    assert validate_typeddict({"req_field": "test", "req_union_can_be_none": True}, TotalTrueExplicitNotRequired) is True
    assert validate_typeddict({"req_field": "test", "opt_field": 123, "req_union_can_be_none": False}, TotalTrueExplicitNotRequired) is True

    # Case 3: opt_field present but incorrect type
    data_opt_incorrect = {"req_field": "test", "opt_field": "wrong", "req_union_can_be_none": True}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data_opt_incorrect, TotalTrueExplicitNotRequired)
    err = excinfo.value
    assert err.incorrect_types["opt_field"].expected == NotRequired[int]
    assert err.incorrect_types["opt_field"].actual == str

    # Case 4: req_field missing
    data_req_missing = {"opt_field": 123, "req_union_can_be_none": None}
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data_req_missing, TotalTrueExplicitNotRequired)
    assert excinfo.value.missing_keys == ("req_field",)

    # Case 5: req_union_can_be_none missing
    data_req_union_missing = {"req_field": "test", "opt_field": 123}
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data_req_union_missing, TotalTrueExplicitNotRequired)
    assert excinfo.value.missing_keys == ("req_union_can_be_none",)


def test_total_true_notrequired_readonly_cases():
    assert validate_typeddict({"req_ro_field": "test"}, TotalTrueNotRequiredReadOnly) is True
    assert validate_typeddict({"req_ro_field": "test", "opt_ro_field": 100}, TotalTrueNotRequiredReadOnly) is True

    data_opt_incorrect = {"req_ro_field": "test", "opt_ro_field": "wrong_type"}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data_opt_incorrect, TotalTrueNotRequiredReadOnly)
    err = excinfo.value
    assert err.incorrect_types["opt_ro_field"].expected == NotRequired[ReadOnly[int]]
    assert err.incorrect_types["opt_ro_field"].actual == str

    data_req_missing = {"opt_ro_field": 100}
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data_req_missing, TotalTrueNotRequiredReadOnly)
    assert excinfo.value.missing_keys == ("req_ro_field",)


# --- NEW TESTS FOR ENHANCED UNION HANDLING (modified for single error) ---
def test_advanced_union_readonly_wrapped_union_success_and_fail():
    class TempROUnionOnly(TypedDict):
        field_ro_union: ReadOnly[Union[str, int, None]]

    assert validate_typeddict({"field_ro_union": "text"}, TempROUnionOnly) is True
    assert validate_typeddict({"field_ro_union": 123}, TempROUnionOnly) is True
    assert validate_typeddict({"field_ro_union": None}, TempROUnionOnly) is True

    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict({"field_ro_union": 123.45}, TempROUnionOnly)
    err = excinfo.value
    assert err.incorrect_types["field_ro_union"].expected == ReadOnly[Union[str, int, None]]
    assert err.incorrect_types["field_ro_union"].actual == float


def test_advanced_union_notrequired_wrapped_union_success_and_fail():
    class TempNROnly(TypedDict):
        field_nr_union: NotRequired[Union[str, bool]]

    assert validate_typeddict({}, TempNROnly) is True
    assert validate_typeddict({"field_nr_union": "text"}, TempNROnly) is True
    assert validate_typeddict({"field_nr_union": True}, TempNROnly) is True

    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict({"field_nr_union": 123}, TempNROnly)
    err = excinfo.value
    assert err.incorrect_types["field_nr_union"].expected == NotRequired[Union[str, bool]]
    assert err.incorrect_types["field_nr_union"].actual == int


def test_advanced_union_nr_ro_wrapped_union_success_and_fail():
    class TempNRROOnly(TypedDict):
        field_nr_ro_union: NotRequired[ReadOnly[Union[float, None]]]

    assert validate_typeddict({}, TempNRROOnly) is True
    assert validate_typeddict({"field_nr_ro_union": 123.45}, TempNRROOnly) is True
    assert validate_typeddict({"field_nr_ro_union": None}, TempNRROOnly) is True

    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict({"field_nr_ro_union": "text"}, TempNRROOnly)
    err = excinfo.value
    assert err.incorrect_types["field_nr_ro_union"].expected == NotRequired[ReadOnly[Union[float, None]]]
    assert err.incorrect_types["field_nr_ro_union"].actual == str


def test_advanced_union_ro_nr_wrapped_union_success_and_fail():
    class TempRONROnly(TypedDict):
        field_ro_nr_union: ReadOnly[NotRequired[Union[int, bool]]]

    assert validate_typeddict({"field_ro_nr_union": 123}, TempRONROnly) is True
    assert validate_typeddict({"field_ro_nr_union": True}, TempRONROnly) is True

    with pytest.raises(DictIncorrectTypeError) as excinfo:  # Wrong type
        validate_typeddict({"field_ro_nr_union": "text"}, TempRONROnly)
    err = excinfo.value
    assert err.incorrect_types["field_ro_nr_union"].expected == ReadOnly[NotRequired[Union[int, bool]]]
    assert err.incorrect_types["field_ro_nr_union"].actual == str

    with pytest.raises(DictMissingKeyError) as excinfo:  # Missing key
        validate_typeddict({}, TempRONROnly)
    assert excinfo.value.missing_keys == ("field_ro_nr_union",)


def test_advanced_union_members_wrapped_success_and_fail():
    class TempUnionMembers(TypedDict):
        field1: Union[ReadOnly[str], int]
        field2: Union[ReadOnly[bool], ReadOnly[float], None]

    assert validate_typeddict({"field1": "text", "field2": None}, TempUnionMembers) is True
    assert validate_typeddict({"field1": 1, "field2": True}, TempUnionMembers) is True

    with pytest.raises(DictIncorrectTypeError) as excinfo:  # field1 error
        validate_typeddict({"field1": 123.45, "field2": None}, TempUnionMembers)
    error = excinfo.value
    assert "field1" in error.incorrect_types
    assert error.incorrect_types["field1"].expected == Union[ReadOnly[str], int]
    assert error.incorrect_types["field1"].actual == float

    with pytest.raises(DictIncorrectTypeError) as excinfo:  # field2 error
        validate_typeddict({"field1": "s", "field2": "string"}, TempUnionMembers)
    error = excinfo.value
    assert "field2" in error.incorrect_types
    assert error.incorrect_types["field2"].expected == Union[ReadOnly[bool], ReadOnly[float], None]
    assert error.incorrect_types["field2"].actual == str


# --- NotImplementedError Cases (adjusted for "raise first error") ---
def test_validate_typeddict_notimplemented_nested_typeddict():
    # NestedTypedDictParent: parent_field: str, child: SimpleTypedDict
    # Both are required.
    data = {"parent_field": "value", "child": {"name": "Nested", "age": 1, "is_member": False}}
    with pytest.raises(NotImplementedError, match="Validation of nested TypedDict for key 'child'"):
        validate_typeddict(data, NestedTypedDictParent)


def test_validate_typeddict_notimplemented_readonly_nested_typeddict():
    # ReadOnlyNestedParentTD: parent_id: str, read_only_child: ReadOnly[SimpleTypedDict]
    # Both are required.
    data = {"parent_id": "p1", "read_only_child": {"name": "NestedRO", "age": 2, "is_member": True}}
    with pytest.raises(NotImplementedError, match="Validation of nested TypedDict for key 'read_only_child'"):
        validate_typeddict(data, ReadOnlyNestedParentTD)


# And the list test should now work if validator sorts common_keys:
def test_validate_typeddict_notimplemented_generic_collection_list():
    # GenericCollectionTypedDict: int_list: list[int], str_bool_dict: dict[str, bool]
    # If validator sorts keys, 'int_list' is checked before 'str_bool_dict'.
    # Both would raise NotImplementedError. The first one ('int_list') will be caught.
    data = {"int_list": [1, 2, "3"], "str_bool_dict": {"valid_key": True}}
    with pytest.raises(NotImplementedError, match="Validation of elements within generic collection for key "):
        validate_typeddict(data, GenericCollectionTypedDict)


def test_validate_typeddict_notimplemented_readonly_generic_collection():
    # ReadOnlyGenericCollectionTD: read_only_list: ReadOnly[list[int]]
    # This is the only field, so it's required.
    data = {"read_only_list": [1, 2, 3]}  # This will trigger NotImplementedError
    with pytest.raises(NotImplementedError, match="Validation of elements within generic collection for key 'read_only_list'"):
        validate_typeddict(data, ReadOnlyGenericCollectionTD)


def test_validate_typeddict_notimplemented_generic_collection_dict():
    # GenericCollectionTypedDict: int_list: list[int], str_bool_dict: dict[str, bool]
    # Both are required. Provide a valid int_list to reach the str_bool_dict check.
    data = {
        "int_list": [1, 2, 3],  # Must be present and valid to pass earlier checks
        "str_bool_dict": {"a": "true"},  # This will trigger NotImplementedError for dict element validation
    }
    with pytest.raises(NotImplementedError, match="Validation of elements within generic collection for key 'str_bool_dict'"):
        validate_typeddict(data, GenericCollectionTypedDict)


# --- General Behavior (modified) ---
def test_validate_typeddict_first_error_is_raised():
    """Tests that the first error according to validation order is raised."""
    # SimpleTypedDict: name: str, age: int, is_member: bool (all required)
    # Data has missing keys ("name", "age"), an extra key ("extra_field"),
    # and an incorrect type ("is_member": "yes").
    # Missing keys are checked first.
    data = {"is_member": "yes", "extra_field": "extra_value"}
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    # Expected: DictMissingKeyError for "name" and "age"
    assert excinfo.value.missing_keys == ("age", "name")  # Order might vary based on set to tuple conversion

    # Data with only extra key error
    data_extra = {"name": "A", "age": 1, "is_member": True, "extra_field": "extra"}
    with pytest.raises(DictExtraKeyError) as excinfo:
        validate_typeddict(data_extra, SimpleTypedDict)
    assert excinfo.value.extra_keys == ("extra_field",)

    # Data with only type error
    data_type = {"name": "A", "age": "wrong", "is_member": True}
    with pytest.raises(DictIncorrectTypeError) as excinfo:
        validate_typeddict(data_type, SimpleTypedDict)
    assert "age" in excinfo.value.incorrect_types


# test_validate_typeddict_notimplemented_error_takes_precedence_in_loop
# This test is removed as its specific scenario (error accumulation and precedence)
# is not applicable to the "raise first error" model. The NotImplementedError
# will be raised if it's the first error encountered during the type-checking phase
# for a specific key, and other tests for NotImplementedError cover this.


def test_typeguard_returns_true_on_success():
    data = {"name": "Valid", "age": 100, "is_member": False}
    result = validate_typeddict(data, SimpleTypedDict)
    assert result is True


# --- total=False Tests (modified for single error) ---
def test_validate_typeddict_total_false_all_present():
    data = {"name": "Test", "value": 1}
    assert validate_typeddict(data, TotalFalseDict) is True


def test_validate_typeddict_total_false_some_present():
    data = {"name": "Test"}
    assert validate_typeddict(data, TotalFalseDict) is True
    data2 = {"value": 2}
    assert validate_typeddict(data2, TotalFalseDict) is True


def test_validate_typeddict_total_false_none_present():
    data = {}
    assert validate_typeddict(data, TotalFalseDict) is True


def test_validate_typeddict_total_false_extra_key():
    data = {"name": "Test", "extra": "key"}
    with pytest.raises(DictExtraKeyError) as excinfo:
        validate_typeddict(data, TotalFalseDict)
    assert excinfo.value.extra_keys == ("extra",)


def test_validate_typeddict_legacy_total_true_missing_key():
    data = {"name": "Alice", "is_member": True}  # age missing from SimpleTypedDict
    with pytest.raises(DictMissingKeyError) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    assert "age" in excinfo.value.missing_keys
