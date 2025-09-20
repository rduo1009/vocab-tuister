"""Contains a TypedDict validator function."""

# pyright: basic

from __future__ import annotations

from typing import (
    Any,
    NamedTuple,
    NotRequired,
    ReadOnly,
    TypeIs,
    Union,
    _TypedDictMeta,  # noqa: PLC2701 # pyright: ignore[reportAttributeAccessIssue]
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


# FIXME: Should this really raise errors? We need a typeis after all
def validate_typeddict[T: _TypedDictMeta](  # noqa: PLR0914, PLR0915
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
        Otherwise, it raises the first validation error encountered.

    Raises
    ------
    DictMissingKeyError
        If one or more required keys are missing. The error will list all missing keys.
    DictExtraKeyError
        If one or more unexpected (extra) keys are present. The error will list all extra keys.
    DictIncorrectTypeError
        If a value has an incorrect type for its key. Reports the first such incorrect type encountered.
    NotImplementedError
        If validation for nested TypedDicts or generic collection elements is
        attempted (e.g., for a key whose type is another TypedDict or a generic like `list[int]`).

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
    # Get all annotations from the TypedDict, include_extras is important for ReadOnly/NotRequired
    annotations = get_type_hints(td_type, include_extras=True)
    all_keys = set(annotations.keys())

    # Determine required keys based on the TypedDict's totality and field annotations.
    is_total = getattr(td_type, "__total__", True)

    if is_total:
        required_keys = {
            k
            for k, ann_type in annotations.items()
            if get_origin(ann_type) is not NotRequired
        }
    else:
        required_keys = (
            set()
        )  # For total=False, keys are optional unless marked Required.
        # Assuming Required is not handled here based on original comment.

    dict_keys = set(d.keys())

    # 1. Check for missing keys
    missing = required_keys - dict_keys
    if missing:
        raise DictMissingKeyError(tuple(sorted(missing)))

    # 2. Check for extra keys
    extra = dict_keys - all_keys
    if extra:
        raise DictExtraKeyError(tuple(sorted(extra)))

    # 3. Type Checking for common keys
    common_keys = dict_keys.intersection(all_keys)

    for k in common_keys:  # noqa: PLR1702
        value = d[k]
        original_expected_type = annotations[k]

        type_being_unwrapped = original_expected_type
        while True:
            origin = get_origin(type_being_unwrapped)
            if origin is NotRequired:
                type_being_unwrapped = _unwrap_notrequired(
                    type_being_unwrapped
                )
            elif origin is ReadOnly:
                type_being_unwrapped = _unwrap_readonly(type_being_unwrapped)
            else:
                break
        core_structural_type = type_being_unwrapped

        origin_of_core_structure = get_origin(core_structural_type)
        args_of_core_structure = get_args(core_structural_type)

        if core_structural_type is Any:
            continue

        if origin_of_core_structure is Union:
            is_valid_union_member = False
            for union_member_type_from_args in args_of_core_structure:
                effective_union_member_type = union_member_type_from_args
                while True:
                    member_origin = get_origin(effective_union_member_type)
                    if member_origin is NotRequired:
                        effective_union_member_type = _unwrap_notrequired(
                            effective_union_member_type
                        )
                    elif member_origin is ReadOnly:
                        effective_union_member_type = _unwrap_readonly(
                            effective_union_member_type
                        )
                    else:
                        break

                if effective_union_member_type is type(None) and value is None:
                    is_valid_union_member = True
                    break
                if effective_union_member_type is not type(None):
                    try:
                        # isinstance can fail with non-type arguments (e.g. unsubscripted generics like Union)
                        if isinstance(value, effective_union_member_type):
                            is_valid_union_member = True
                            break
                    except TypeError:
                        # If effective_union_member_type is not a valid type for isinstance,
                        # this path might be problematic. This function assumes simple types or
                        # valid subscripted generics as union members.
                        # A common case for TypeError here is if effective_union_member_type is something like `list` (bare)
                        # when expecting `list[int]`. However, the current logic handles list/dict/set/tuple later.
                        # This specific check is for members of a Union.
                        pass  # Could log a warning or handle more gracefully if needed.

            if not is_valid_union_member:
                raise DictIncorrectTypeError({
                    k: IncorrectTypeDetail(
                        expected=original_expected_type, actual=type(value)
                    )
                })
        elif (
            isinstance(core_structural_type, type)
            and hasattr(core_structural_type, "__annotations__")
            and hasattr(core_structural_type, "__total__")
        ):
            raise NotImplementedError(
                f"Validation of nested TypedDict for key '{k}' ('{core_structural_type.__name__}') is not yet implemented."
            )
        elif origin_of_core_structure in {list, dict, set, tuple}:
            raise NotImplementedError(
                f"Validation of elements within generic collection for key '{k}' ({origin_of_core_structure}) is not yet implemented."
            )
        else:
            # Fallback for simple types (int, str, etc.) and other non-Union complex types
            # that are not explicitly handled generic collections or nested TypedDicts.
            # This also includes cases where core_structural_type might be an unsubscripted generic
            # like `list` if `isinstance(value, list)` is the desired check.
            try:
                if not isinstance(value, core_structural_type):
                    raise DictIncorrectTypeError({
                        k: IncorrectTypeDetail(
                            expected=original_expected_type, actual=type(value)
                        )
                    })
            except TypeError as e:
                # This can happen if core_structural_type is not a class or tuple of classes,
                # e.g., if it's a complex type alias or a generic that wasn't fully resolved
                # or handled by prior checks (like unsubscripted `List` from `typing.List`).
                # The original code had this implicit fallback.
                # For robustness, one might want to log or raise a more specific error here.
                # For now, mimic original behavior which might lead to DictIncorrectTypeError if this check is meaningful,
                # or pass through if isinstance itself errors for other reasons.
                # A simple way to make it raise for type mismatch:
                raise DictIncorrectTypeError({
                    k: IncorrectTypeDetail(
                        expected=original_expected_type, actual=type(value)
                    )
                }) from e

    return True
