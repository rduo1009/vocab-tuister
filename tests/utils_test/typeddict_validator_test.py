"""Unit tests for the typeddict_validator module."""

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


# --- New TypedDicts for testing specific fixes ---


# For required_keys fix (NotRequired in total=True TypedDicts)
class TotalTrueExplicitNotRequired(TypedDict):  # total=True is default
    req_field: str
    opt_field: NotRequired[int]
    req_union_can_be_none: Union[bool, None]  # This field is required, value can be bool or None


class TotalTrueNotRequiredReadOnly(TypedDict):  # total=True is default
    req_ro_field: ReadOnly[str]
    opt_ro_field: NotRequired[ReadOnly[int]]


# For enhanced Union handling with ReadOnly/NotRequired wrappers
class AdvancedUnionTD(TypedDict):
    # Field where Union is wrapped by ReadOnly
    field_ro_union: ReadOnly[Union[str, int, None]]
    # Field where Union is wrapped by NotRequired
    field_nr_union: NotRequired[Union[str, bool]]
    # Field where Union is wrapped by NotRequired then ReadOnly
    field_nr_ro_union: NotRequired[ReadOnly[Union[float, None]]]
    # Field where Union is wrapped by ReadOnly then NotRequired
    # If present, value must conform to Union[int, bool]
    field_ro_nr_union: ReadOnly[NotRequired[Union[int, bool]]]

    # Field where Union members are ReadOnly
    field_union_with_ro_member: Union[ReadOnly[str], int]  # type: ignore[valid-type]
    field_union_with_multiple_ro_members: Union[ReadOnly[bool], ReadOnly[float], None]  # type: ignore[valid-type]


# --- Test Cases ---


# ... (Keep existing tests from test_validate_typeddict_success_perfect_match to test_validate_typeddict_success_any_field) ...
def test_validate_typeddict_success_perfect_match():
    """Tests successful validation with a perfect match."""
    data = {"name": "Alice", "age": 30, "is_member": True}
    assert validate_typeddict(data, SimpleTypedDict) is True


def test_validate_typeddict_success_optionalfields_td_missing():
    """Tests successful validation for OptionalTypedDict (total=False) when keys are missing."""
    data = {"name": "Bob"}
    assert validate_typeddict(data, OptionalTypedDict) is True


def test_validate_typeddict_success_optionalfields_td_present():
    """Tests successful validation for OptionalTypedDict (total=False) when keys are present."""
    data = {"name": "Charlie", "city": "London", "zip_code": 12345}
    assert validate_typeddict(data, OptionalTypedDict) is True
    data_partial = {"city": "Paris"}
    assert validate_typeddict(data_partial, OptionalTypedDict) is True


# MODIFIED for required_keys fix: `notes` field should now be correctly optional
def test_validate_typeddict_success_required_optional_fields():
    """
    Tests successful validation for RequiredOptionalTypedDict.
    'notes: NotRequired[str]' should be truly optional.
    """
    data1 = {"id": 1, "description": "Test"}  # 'notes' is missing, should be fine
    assert validate_typeddict(data1, RequiredOptionalTypedDict) is True

    data2 = {"id": 2, "description": None, "notes": "Some notes"}
    assert validate_typeddict(data2, RequiredOptionalTypedDict) is True

    data3 = {"id": 3, "description": "Another test", "notes": "More notes"}
    assert validate_typeddict(data3, RequiredOptionalTypedDict) is True

    # Test case where only required fields are present and NotRequired is missing
    data4 = {"id": 4, "description": None}
    assert validate_typeddict(data4, RequiredOptionalTypedDict) is True


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


# ... (Keep existing error tests from test_validate_typeddict_missing_key_single to test_validate_typeddict_union_type_invalid) ...
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
    assert error.missing_keys == ("age", "name")


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
    assert error.extra_keys == ("extra1", "extra2")


def test_validate_typeddict_incorrect_type_single():
    """Tests DictIncorrectTypeError for a single incorrect type."""
    data = {"name": "Alice", "age": "thirty", "is_member": True}
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
    data_str_float = {"identifier": "id123", "status_value": math.pi}
    assert validate_typeddict(data_str_float, UnionTypedDict) is True
    data_int_none = {"identifier": 123, "status_value": None}
    assert validate_typeddict(data_int_none, UnionTypedDict) is True
    data_optional_missing_total_false = {"identifier": "id456"}
    assert validate_typeddict(data_optional_missing_total_false, UnionTypedDictTotalFalse) is True
    data_optional_none_total_false = {"identifier": "id789", "optional_union_val": None}
    assert validate_typeddict(data_optional_none_total_false, UnionTypedDictTotalFalse) is True


def test_validate_typeddict_union_type_invalid():
    """Tests DictIncorrectTypeError for an invalid Union type."""
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


# MODIFIED for required_keys fix: `description` field should now be correctly optional
def test_validate_typeddict_readonly_complex_success():
    """
    Tests successful validation for TypedDict with various ReadOnly fields.
    'description: NotRequired[ReadOnly[str]]' should be truly optional.
    """
    # ReadOnlyComplexTD:
    #   id: ReadOnly[str]
    #   value: ReadOnly[Optional[int]]
    #   description: NotRequired[ReadOnly[str]]
    #   config: ReadOnly[Union[str, bool, None]]

    data1 = {"id": "item1", "value": 123, "config": "active"}  # 'description' missing, should be OK
    assert validate_typeddict(data1, ReadOnlyComplexTD) is True

    data2 = {"id": "item2", "value": None, "description": "A test item", "config": True}
    assert validate_typeddict(data2, ReadOnlyComplexTD) is True

    data3 = {"id": "item3", "value": 456, "description": "Another item", "config": None}
    assert validate_typeddict(data3, ReadOnlyComplexTD) is True

    data4 = {"id": "item4", "value": 789, "config": False}  # 'description' missing, should be OK
    assert validate_typeddict(data4, ReadOnlyComplexTD) is True


def test_validate_typeddict_readonly_simple_incorrect_type():
    """Tests DictIncorrectTypeError for a ReadOnly field with an incorrect type."""
    data = {"name": "test", "count": "many"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlySimpleTD)
    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "count" in error.incorrect_types
    assert error.incorrect_types["count"].expected == ReadOnly[int]
    assert error.incorrect_types["count"].actual == str


# MODIFIED for required_keys fix: `description` can be legitimately missing.
def test_validate_typeddict_readonly_optional_incorrect_type():
    """Tests DictIncorrectTypeError for a ReadOnly[Optional[T]] field."""
    # ReadOnlyComplexTD.value: ReadOnly[Optional[int]]
    # `description` is NotRequired, so it can be omitted.
    data = {"id": "itemX", "value": "not_an_int", "config": "cfg"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlyComplexTD)
    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "value" in error.incorrect_types
    assert error.incorrect_types["value"].expected == ReadOnly[Optional[int]]  # Original annotation
    assert error.incorrect_types["value"].actual == str


# MODIFIED for required_keys fix: `description` can be legitimately missing.
def test_validate_typeddict_readonly_union_incorrect_type():
    """Tests DictIncorrectTypeError for a ReadOnly[Union[A,B,...]] field."""
    # ReadOnlyComplexTD.config: ReadOnly[Union[str, bool, None]]
    # `description` is NotRequired, so it can be omitted.
    data = {"id": "itemY", "value": 10, "config": 123.45}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlyComplexTD)
    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictIncorrectTypeError)
    assert "config" in error.incorrect_types
    assert error.incorrect_types["config"].expected == ReadOnly[Union[str, bool, None]]  # Original
    assert error.incorrect_types["config"].actual == float


def test_validate_typeddict_readonly_required_field_missing():
    """Tests DictMissingKeyError for a required ReadOnly field."""
    data = {"name": "only_name"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, ReadOnlySimpleTD)
    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert error.missing_keys == ("count",)


# --- NEW TESTS FOR `required_keys` FIX (Total=True with NotRequired) ---
def test_total_true_explicit_notrequired_success_and_missing_handling():
    """Tests TotalTrueExplicitNotRequired for correct handling of NotRequired fields."""
    # opt_field is NotRequired[int]
    # req_union_can_be_none is Union[bool, None] (so it's required, can be None)

    # Case 1: opt_field missing (should be valid)
    data_opt_missing = {"req_field": "test", "req_union_can_be_none": True}
    assert validate_typeddict(data_opt_missing, TotalTrueExplicitNotRequired) is True

    data_opt_missing_none = {"req_field": "test", "req_union_can_be_none": None}
    assert validate_typeddict(data_opt_missing_none, TotalTrueExplicitNotRequired) is True

    # Case 2: opt_field present and correct
    data_opt_present = {"req_field": "test", "opt_field": 123, "req_union_can_be_none": False}
    assert validate_typeddict(data_opt_present, TotalTrueExplicitNotRequired) is True

    # Case 3: opt_field present but incorrect type
    data_opt_incorrect = {"req_field": "test", "opt_field": "wrong", "req_union_can_be_none": True}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data_opt_incorrect, TotalTrueExplicitNotRequired)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictIncorrectTypeError)
    assert err.incorrect_types["opt_field"].expected == NotRequired[int]
    assert err.incorrect_types["opt_field"].actual == str

    # Case 4: req_field missing
    data_req_missing = {"opt_field": 123, "req_union_can_be_none": None}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data_req_missing, TotalTrueExplicitNotRequired)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictMissingKeyError)
    assert err.missing_keys == ("req_field",)

    # Case 5: req_union_can_be_none missing (it's required despite being Union with None)
    data_req_union_missing = {"req_field": "test", "opt_field": 123}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data_req_union_missing, TotalTrueExplicitNotRequired)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictMissingKeyError)
    assert err.missing_keys == ("req_union_can_be_none",)


def test_total_true_notrequired_readonly_success_and_missing():
    """Tests TotalTrueNotRequiredReadOnly for NotRequired[ReadOnly[T]] fields."""
    # opt_ro_field: NotRequired[ReadOnly[int]]

    # Case 1: opt_ro_field missing (should be valid)
    data_opt_missing = {"req_ro_field": "test"}
    assert validate_typeddict(data_opt_missing, TotalTrueNotRequiredReadOnly) is True

    # Case 2: opt_ro_field present and correct
    data_opt_present = {"req_ro_field": "test", "opt_ro_field": 100}
    assert validate_typeddict(data_opt_present, TotalTrueNotRequiredReadOnly) is True

    # Case 3: opt_ro_field present but incorrect type
    data_opt_incorrect = {"req_ro_field": "test", "opt_ro_field": "wrong_type"}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data_opt_incorrect, TotalTrueNotRequiredReadOnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictIncorrectTypeError)
    assert err.incorrect_types["opt_ro_field"].expected == NotRequired[ReadOnly[int]]
    assert err.incorrect_types["opt_ro_field"].actual == str

    # Case 4: req_ro_field missing
    data_req_missing = {"opt_ro_field": 100}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data_req_missing, TotalTrueNotRequiredReadOnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictMissingKeyError)
    assert err.missing_keys == ("req_ro_field",)


# --- NEW TESTS FOR ENHANCED UNION HANDLING ---
def test_advanced_union_readonly_wrapped_union_success_and_fail():
    """Tests a field like: ReadOnly[Union[str, int, None]]."""

    class TempROUnionOnly(TypedDict):  # Define a local, minimal TypedDict
        field_ro_union: ReadOnly[Union[str, int, None]]

    # Success cases
    assert validate_typeddict({"field_ro_union": "text"}, TempROUnionOnly) is True
    assert validate_typeddict({"field_ro_union": 123}, TempROUnionOnly) is True
    assert validate_typeddict({"field_ro_union": None}, TempROUnionOnly) is True

    # Failure case
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({"field_ro_union": 123.45}, TempROUnionOnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictIncorrectTypeError)
    assert err.incorrect_types["field_ro_union"].expected == ReadOnly[Union[str, int, None]]
    assert err.incorrect_types["field_ro_union"].actual == float


def test_advanced_union_notrequired_wrapped_union_success_and_fail():
    """Tests AdvancedUnionTD field_nr_union: NotRequired[Union[str, bool]]."""

    # field_nr_union is NotRequired, so other fields (if any) would need to be present.
    # For this TD, if field_nr_union is the only field, an empty dict is not valid
    # because the TD itself is total=True by default, meaning field_ro_union etc. are required.
    # Let's assume we provide all other required fields for simplicity or use a total=False TD.
    # For this test, we focus on `field_nr_union` if present.
    # To make it simpler, let's define a minimal TD for this one field:
    class TempNROnly(TypedDict):
        field_nr_union: NotRequired[Union[str, bool]]

    # Success cases
    assert validate_typeddict({}, TempNROnly) is True  # Missing is OK
    assert validate_typeddict({"field_nr_union": "text"}, TempNROnly) is True
    assert validate_typeddict({"field_nr_union": True}, TempNROnly) is True

    # Failure case
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({"field_nr_union": 123}, TempNROnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictIncorrectTypeError)
    assert err.incorrect_types["field_nr_union"].expected == NotRequired[Union[str, bool]]
    assert err.incorrect_types["field_nr_union"].actual == int


def test_advanced_union_nr_ro_wrapped_union_success_and_fail():
    """Tests AdvancedUnionTD field_nr_ro_union: NotRequired[ReadOnly[Union[float, None]]]."""

    class TempNRROOnly(TypedDict):
        field_nr_ro_union: NotRequired[ReadOnly[Union[float, None]]]

    # Success cases
    assert validate_typeddict({}, TempNRROOnly) is True  # Missing is OK
    assert validate_typeddict({"field_nr_ro_union": 123.45}, TempNRROOnly) is True
    assert validate_typeddict({"field_nr_ro_union": None}, TempNRROOnly) is True

    # Failure case
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({"field_nr_ro_union": "text"}, TempNRROOnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictIncorrectTypeError)
    assert err.incorrect_types["field_nr_ro_union"].expected == NotRequired[ReadOnly[Union[float, None]]]
    assert err.incorrect_types["field_nr_ro_union"].actual == str


def test_advanced_union_ro_nr_wrapped_union_success_and_fail():
    """Tests AdvancedUnionTD field_ro_nr_union: ReadOnly[NotRequired[Union[int, bool]]]."""

    # This field is required because ReadOnly[...] is not NotRequired[...]
    # The NotRequired is *inside* ReadOnly.
    # If the key is present, its value must match Union[int, bool].
    class TempRONROnly(TypedDict):
        field_ro_nr_union: ReadOnly[NotRequired[Union[int, bool]]]

    # Success cases
    assert validate_typeddict({"field_ro_nr_union": 123}, TempRONROnly) is True
    assert validate_typeddict({"field_ro_nr_union": True}, TempRONROnly) is True

    # Failure case (wrong type)
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({"field_ro_nr_union": "text"}, TempRONROnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictIncorrectTypeError)
    assert "field_ro_nr_union" in err.incorrect_types
    assert err.incorrect_types["field_ro_nr_union"].expected == ReadOnly[NotRequired[Union[int, bool]]]
    assert err.incorrect_types["field_ro_nr_union"].actual == str

    # Failure case (missing key - this field IS required by the TypedDict structure)
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({}, TempRONROnly)
    err = excinfo.value.exceptions[0]
    assert isinstance(err, DictMissingKeyError)
    assert err.missing_keys == ("field_ro_nr_union",)


def test_advanced_union_members_wrapped_success_and_fail():
    """Tests AdvancedUnionTD fields with ReadOnly members in Union."""

    # field_union_with_ro_member: Union[ReadOnly[str], int]
    # field_union_with_multiple_ro_members: Union[ReadOnly[bool], ReadOnly[float], None]
    class TempUnionMembers(TypedDict):
        field1: Union[ReadOnly[str], int]  # type: ignore[valid-type]
        field2: Union[ReadOnly[bool], ReadOnly[float], None]  # type: ignore[valid-type]

    # Success cases for field1
    assert validate_typeddict({"field1": "text", "field2": None}, TempUnionMembers) is True
    assert validate_typeddict({"field1": 123, "field2": None}, TempUnionMembers) is True

    # Success cases for field2
    assert validate_typeddict({"field1": 1, "field2": True}, TempUnionMembers) is True
    assert validate_typeddict({"field1": 1, "field2": math.pi}, TempUnionMembers) is True
    assert validate_typeddict({"field1": 1, "field2": None}, TempUnionMembers) is True

    # Failure case for field1
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({"field1": 123.45, "field2": None}, TempUnionMembers)
    errs = {type(e) for e in excinfo.value.exceptions}
    assert DictIncorrectTypeError in errs
    incorrect_type_error = next(e for e in excinfo.value.exceptions if isinstance(e, DictIncorrectTypeError))
    assert "field1" in incorrect_type_error.incorrect_types
    assert incorrect_type_error.incorrect_types["field1"].expected == Union[ReadOnly[str], int]
    assert incorrect_type_error.incorrect_types["field1"].actual == float

    # Failure case for field2
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict({"field1": "s", "field2": "string"}, TempUnionMembers)
    errs = {type(e) for e in excinfo.value.exceptions}
    assert DictIncorrectTypeError in errs
    incorrect_type_error = next(e for e in excinfo.value.exceptions if isinstance(e, DictIncorrectTypeError))
    assert "field2" in incorrect_type_error.incorrect_types
    assert incorrect_type_error.incorrect_types["field2"].expected == Union[ReadOnly[bool], ReadOnly[float], None]
    assert incorrect_type_error.incorrect_types["field2"].actual == str


# --- NotImplementedError Cases (including ReadOnly variants) ---
# ... (Keep existing NotImplementedError tests) ...
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
# ... (Keep existing General Behavior tests) ...
def test_validate_typeddict_exception_group_multiple_errors():
    """Tests that multiple different errors are reported in one ExceptionGroup."""
    data = {"is_member": "yes", "extra_field": "extra_value"}
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
    Tests that if a NotImplementedError occurs for a field, validation stops for that field.
    """
    data = {"parent_field": 123, "child": {"name": "Nested", "age": 1, "is_member": False}, "extra": "key"}
    with pytest.raises(NotImplementedError, match="Validation of nested TypedDict for key 'child'"):
        validate_typeddict(data, NestedTypedDictParent)


def test_typeguard_returns_true_on_success():
    """Ensures the function returns True on successful validation (TypeGuard behavior)."""
    data = {"name": "Valid", "age": 100, "is_member": False}
    result = validate_typeddict(data, SimpleTypedDict)
    assert result is True


# --- total=False Tests ---
# ... (Keep existing total=False tests) ...
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
    data = {"name": "Alice", "is_member": True}
    with pytest.raises(ExceptionGroup) as excinfo:
        validate_typeddict(data, SimpleTypedDict)
    assert len(excinfo.value.exceptions) == 1
    error = excinfo.value.exceptions[0]
    assert isinstance(error, DictMissingKeyError)
    assert "age" in error.missing_keys
