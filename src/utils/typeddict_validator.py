"""Contains a TypedDict validator function."""

from __future__ import annotations

from typing import (
    Any,
    NamedTuple,
    TypedDict,
    TypeIs,
    TypeVar,
    Union,
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
        The expected type for the key.
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


T = TypeVar("T", bound=TypedDict)  # type: ignore[valid-type]


def validate_typeddict[T](d: dict[str, Any], td_type: type[T]) -> TypeIs[T]:
    """Validate a dictionary against a TypedDict type.

    This function checks if the given dictionary `d` conforms to the structure
    and types defined by the `TypedDict` `td_type`. It verifies:
    1. All required keys are present.
    2. No extra keys are present.
    3. Values for all present keys match their expected types.

    Parameters
    ----------
    d : dict[str, Any]
        The dictionary to validate.
    td_type : Type[T]
        The TypedDict class to validate against.

    Returns
    -------
    TypeGuard[T]
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
    - For `Any` type, any value is considered valid.
    - Validation of nested `TypedDict`s and elements within generic collections
      (like `list[int]`) is not currently implemented and will result in a
      `NotImplementedError` being raised.
    """
    errors: list[Exception] = []
    annotations = get_type_hints(td_type)

    all_keys = set(annotations.keys())
    # __required_keys__ and __optional_keys__ are standard attributes for TypedDict
    required_keys: frozenset[str] | set[str] = getattr(
        td_type, "__required_keys__", set()
    )
    # If __required_keys__ is not present (e.g. older Python or non-total dicts without it)
    # and td_type.__total__ is True, all annotated keys are required.
    # However, relying on __required_keys__ is generally safer for modern TypedDict.
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
        v = d[k]
        expected_type = annotations[k]
        origin_type = get_origin(expected_type)
        args_type = get_args(expected_type)

        if expected_type is Any:
            continue  # Any type matches anything

        if origin_type is Union:
            # For Union[A, B, NoneType], get_args might return (A, B, type(None))
            # isinstance(None, type(None)) is True
            is_valid_union_type = False
            for union_arg_type in args_type:
                if union_arg_type is type(None) and v is None:
                    is_valid_union_type = True
                    break
                # isinstance(value, type(None)) doesn't work for non-None values
                if union_arg_type is not type(None) and isinstance(
                    v, union_arg_type
                ):
                    is_valid_union_type = True
                    break
            if not is_valid_union_type:
                incorrect_type_details[k] = IncorrectTypeDetail(
                    expected=expected_type, actual=type(v)
                )
        elif hasattr(expected_type, "__annotations__") and hasattr(
            expected_type, "__total__"
        ):  # Check if it's a TypedDict
            # This is a placeholder for nested TypedDict validation
            raise NotImplementedError(
                f"Validation of nested TypedDict for key '{k}' is not yet implemented."
            )

        elif origin_type in {list, dict, set, tuple}:
            # This is a placeholder for generic collection element validation
            raise NotImplementedError(
                f"Validation of elements within generic collection for key '{k}' ({origin_type}) is not yet implemented."
            )

        elif not isinstance(v, expected_type):
            incorrect_type_details[k] = IncorrectTypeDetail(
                expected=expected_type, actual=type(v)
            )

    if incorrect_type_details:
        errors.append(DictIncorrectTypeError(incorrect_type_details))

    if errors:
        raise ExceptionGroup("TypedDict validation failed", errors)

    return True
