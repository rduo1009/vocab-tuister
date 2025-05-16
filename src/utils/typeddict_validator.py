"""Contains a TypedDict validator function."""

from __future__ import annotations

from typing import (  # type: ignore[attr-defined]
    Any,
    NamedTuple,
    NotRequired,
    ReadOnly,
    TypeIs,
    Union,
    _TypedDictMeta,  # noqa: PLC2701
    get_args,
    get_origin,
    get_type_hints,
)


class IncorrectTypeDetail(NamedTuple):
    """
    Details of an incorrect type found in a dictionary.

    Attributes
    ----------
    expected : Any
        The expected type for the key, as defined in the TypedDict.
    actual : Any
        The actual type found for the key.
    """

    expected: Any
    actual: Any


class DictMissingKeyError(Exception):
    """
    Exception raised when a dictionary is missing required keys.

    Attributes
    ----------
    missing_keys : tuple[str, ...]
        A tuple of keys that are missing from the dictionary.
    message : str
        Explanation of the error.
    """

    def __init__(
        self,
        missing_keys: tuple[str, ...],
        message: str = "Dictionary is missing required keys.",
    ) -> None:
        self.missing_keys: tuple[str, ...] = missing_keys
        self.message: str = (
            f"{message} Missing keys: {', '.join(missing_keys)}"
        )
        super().__init__(self.message)


class DictExtraKeyError(Exception):
    """
    Exception raised when a dictionary contains unexpected extra keys.

    Attributes
    ----------
    extra_keys : tuple[str, ...]
        A tuple of keys that are extra in the dictionary.
    message : str
        Explanation of the error.
    """

    def __init__(
        self,
        extra_keys: tuple[str, ...],
        message: str = "Dictionary contains unexpected extra keys.",
    ) -> None:
        self.extra_keys: tuple[str, ...] = extra_keys
        self.message: str = f"{message} Extra keys: {', '.join(extra_keys)}"
        super().__init__(self.message)


class DictIncorrectTypeError(Exception):
    """
    Exception raised when dictionary keys have values of incorrect types.

    Attributes
    ----------
    incorrect_types : dict[str, IncorrectTypeDetail]
        A dictionary where keys are the dictionary keys that have incorrect types,
        and values are IncorrectTypeDetail NamedTuples.
    message : str
        Explanation of the error.
    """

    def __init__(
        self,
        incorrect_types: dict[str, IncorrectTypeDetail],
        message: str = "Dictionary has keys with incorrect types.",
    ) -> None:
        self.incorrect_types: dict[str, IncorrectTypeDetail] = incorrect_types
        formatted_errors = [
            f"Key '{k}': expected {v.expected}, got {v.actual}"
            for k, v in incorrect_types.items()
        ]
        self.message: str = (
            f"{message} Incorrect types: {'; '.join(formatted_errors)}"
        )
        super().__init__(self.message)


def _unwrap_readonly(type_hint: Any) -> Any:
    """Unwrap ReadOnly[T] to T, otherwise return the type_hint as is.

    Parameters
    ----------
    type_hint : Any
        The type hint to potentially unwrap.

    Returns
    -------
    Any
        The unwrapped type if type_hint was ReadOnly[T], otherwise type_hint.
    """
    origin = get_origin(type_hint)
    if origin is ReadOnly:
        args = get_args(type_hint)
        if args:  # ReadOnly[T] should have one argument T
            return args[0]
    return type_hint


def _unwrap_notrequired(type_hint: Any) -> Any:
    """Unwrap NotRequired[T] to T, otherwise return the type_hint as is.

    Parameters
    ----------
    type_hint : Any
        The type hint to potentially unwrap.

    Returns
    -------
    Any
        The unwrapped type if type_hint was NotRequired[T], otherwise type_hint.
    """
    origin = get_origin(type_hint)
    if origin is NotRequired:  # Ensure NotRequired is imported
        args = get_args(type_hint)
        if args:  # NotRequired[T] should have one argument T
            return args[0]
    return type_hint


def validate_typeddict[T: _TypedDictMeta](  # noqa: PLR0914
    d: dict[str, Any], td_type: type[T]
) -> TypeIs[T]:
    """Validate a dictionary against a TypedDict type.

    This function checks if the given dictionary `d` conforms to the structure
    and types defined by the `TypedDict` `td_type`. It verifies:
    1. All required keys are present (respecting `NotRequired`).
    2. No extra keys are present.
    3. Values for all present keys match their expected types, including handling
       for `ReadOnly`, `NotRequired`, `Union`, and `Any`.

    Parameters
    ----------
    d : dict[str, Any]
        The dictionary to validate.
    td_type : Type[T]
        The TypedDict class to validate against.

    Returns
    -------
    TypeIs[T]
        Returns `True` if the dictionary `d` is a valid instance of `td_type`.
        Otherwise, it raises an `ExceptionGroup` containing specific errors.

    Raises
    ------
    ExceptionGroup
        An `ExceptionGroup` is raised if validation fails. The group contains
        a list of specific errors encountered during validation, which can be
        instances of:
        - `DictMissingKeyError`: If required keys are missing.
        - `DictExtraKeyError`: If unexpected keys are present.
        - `DictIncorrectTypeError`: If values have incorrect types.
    NotImplementedError
        If validation for nested TypedDicts or generic collection elements is
        attempted.

    Notes
    -----
    - For `Union` types, the value must match at least one of the types in the Union.
      `ReadOnly` types within a `Union` are also handled.
    - For `Any` type, any value is considered valid.
    - `ReadOnly[T]` fields are validated against type `T`.
    - `NotRequired[T]` fields, if present, are validated against type `T`.
    - Validation of nested `TypedDict`s and elements within generic collections
      (like `list[int]`) is not currently implemented and will result in a
      `NotImplementedError`.
    """
    errors: list[Exception] = []
    # Get all annotations from the TypedDict, include_extras is important for ReadOnly/NotRequired
    annotations = get_type_hints(td_type, include_extras=True)

    all_keys = set(annotations.keys())
    # __required_keys__ should correctly list only keys not marked as NotRequired
    # if the TypedDict is total=True.
    required_keys = set(getattr(td_type, "__required_keys__", set()))

    if not hasattr(td_type, "__required_keys__") and getattr(
        td_type, "__total__", True
    ):
        required_keys = all_keys

    dict_keys = set(d.keys())

    # 1. Check for missing keys
    missing = required_keys - dict_keys
    if missing:
        errors.append(DictMissingKeyError(tuple(sorted(missing))))

    # 2. Check for extra keys
    extra = dict_keys - all_keys
    if extra:
        errors.append(DictExtraKeyError(tuple(sorted(extra))))

    # 3. Type Checking for common keys
    common_keys = dict_keys.intersection(all_keys)
    incorrect_type_details: dict[str, IncorrectTypeDetail] = {}

    for k in common_keys:
        value = d[k]
        # This is the type as defined in the TypedDict (e.g., NotRequired[ReadOnly[int]])
        original_expected_type = annotations[k]

        # If a key is present, its NotRequired status is fulfilled. Unwrap to get the inner type.
        # e.g., NotRequired[ReadOnly[int]] -> ReadOnly[int]
        # e.g., NotRequired[str] -> str
        type_after_notrequired_unwrap = _unwrap_notrequired(
            original_expected_type
        )

        # Then unwrap ReadOnly to get the actual type for validation.
        # e.g., ReadOnly[int] -> int (from previous step or directly)
        # e.g., str -> str (no change if not ReadOnly)
        effective_expected_type = _unwrap_readonly(
            type_after_notrequired_unwrap
        )

        origin_effective_type = get_origin(effective_expected_type)
        args_effective_type = get_args(effective_expected_type)

        if effective_expected_type is Any:
            continue

        if origin_effective_type is Union:
            is_valid_union_member = False
            for union_member_type in args_effective_type:
                # A Union member itself could be ReadOnly, e.g., Union[ReadOnly[int], str]
                # So, unwrap it too for the isinstance check.
                # NotRequired is not expected inside a Union's args like Union[NotRequired[T], Y]
                # as Optional[T] (Union[T, None]) is the way for optionality within a Union.
                effective_union_member_type = _unwrap_readonly(
                    union_member_type
                )

                if effective_union_member_type is type(None) and value is None:
                    is_valid_union_member = True
                    break
                if effective_union_member_type is not type(
                    None
                ) and isinstance(value, effective_union_member_type):
                    is_valid_union_member = True
                    break
            if not is_valid_union_member:
                incorrect_type_details[k] = IncorrectTypeDetail(
                    expected=original_expected_type,  # Report original annotation
                    actual=type(value),
                )
        elif (
            isinstance(effective_expected_type, type)
            and hasattr(effective_expected_type, "__annotations__")
            and hasattr(effective_expected_type, "__total__")
        ):
            raise NotImplementedError(
                f"Validation of nested TypedDict for key '{k}' ('{effective_expected_type.__name__}') is not yet implemented."
            )
        elif origin_effective_type in {list, dict, set, tuple}:
            raise NotImplementedError(
                f"Validation of elements within generic collection for key '{k}' ({origin_effective_type}) is not yet implemented."
            )
        elif not isinstance(value, effective_expected_type):
            incorrect_type_details[k] = IncorrectTypeDetail(
                expected=original_expected_type,  # Report original annotation
                actual=type(value),
            )

    if incorrect_type_details:
        errors.append(DictIncorrectTypeError(incorrect_type_details))

    if errors:
        raise ExceptionGroup("TypedDict validation failed", errors)

    return True
