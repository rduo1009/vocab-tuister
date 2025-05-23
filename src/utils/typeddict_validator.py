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

    # Determine required keys based on the TypedDict's totality and field annotations.
    # This approach is generally more robust across Python versions and TypedDict variations
    # than relying solely on the __required_keys__ attribute (which might be inconsistent
    # or missing in some cases) or using an overly simple fallback.
    is_total = getattr(td_type, "__total__", True)

    if is_total:
        # For total=True TypedDicts (default), a key is required if its annotation
        # in the TypedDict definition is not NotRequired.
        required_keys = {
            k
            for k, ann_type in annotations.items()
            if get_origin(ann_type) is not NotRequired
        }
    else:
        # For total=False TypedDicts, all keys are optional by default.
        # A key becomes required only if explicitly marked with typing.Required.
        # As typing.Required is not yet a stable public API fully integrated
        # with get_origin checks across all supported Python versions for this purpose,
        # we currently assume no keys are required for total=False.
        # The standard __required_keys__ for total=False TypedDicts (without Required[] fields)
        # is an empty set, so this aligns.
        required_keys = set()

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
        original_expected_type = annotations[k]

        # Refined unwrapping for core structural type analysis
        type_being_unwrapped = original_expected_type

        # Iteratively unwrap NotRequired and ReadOnly until neither is the outermost type,
        # or the type becomes simple (no origin). This handles nested wrappers like
        # ReadOnly[NotRequired[T]] or NotRequired[ReadOnly[T]].
        while True:
            origin = get_origin(type_being_unwrapped)
            if origin is NotRequired:
                type_being_unwrapped = _unwrap_notrequired(
                    type_being_unwrapped
                )
            elif origin is ReadOnly:
                type_being_unwrapped = _unwrap_readonly(type_being_unwrapped)
            else:
                # No more NotRequired or ReadOnly wrappers at this level, or it's a base type.
                break

        core_structural_type = type_being_unwrapped

        origin_of_core_structure = get_origin(core_structural_type)
        args_of_core_structure = get_args(core_structural_type)

        if core_structural_type is Any:
            continue

        if origin_of_core_structure is Union:
            is_valid_union_member = False
            for union_member_type_from_args in args_of_core_structure:
                # Fully unwrap each member of the union before isinstance check
                effective_union_member_type = union_member_type_from_args
                while True:  # Iteratively unwrap this member
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
                # Ensure effective_union_member_type is a type or tuple of types for isinstance
                # For simple types, it will be the type itself.
                # For Union[A,B] (if it somehow wasn't caught by outer Union check and is a member),
                # this would need more complex handling, but usually, union members are simpler.
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
            isinstance(core_structural_type, type)  # Check if it's a class
            and hasattr(
                core_structural_type, "__annotations__"
            )  # TypedDicts have __annotations__
            and hasattr(
                core_structural_type, "__total__"
            )  # TypedDicts have __total__
        ):
            # This is a basic check for TypedDict. A more robust check might involve _TypedDictMeta
            # if isinstance(core_structural_type, _TypedDictMeta) but _TypedDictMeta is private.
            raise NotImplementedError(
                f"Validation of nested TypedDict for key '{k}' ('{core_structural_type.__name__}') is not yet implemented."
            )
        elif origin_of_core_structure in {
            list,
            dict,
            set,
            tuple,
        }:  # Check for common generic collections
            raise NotImplementedError(
                f"Validation of elements within generic collection for key '{k}' ({origin_of_core_structure}) is not yet implemented."
            )
        # Fallback for simple types (int, str, etc.) after all wrappers and structures are handled
        elif not isinstance(value, core_structural_type):
            incorrect_type_details[k] = IncorrectTypeDetail(
                expected=original_expected_type,  # Report original annotation
                actual=type(value),
            )

    if incorrect_type_details:
        errors.append(DictIncorrectTypeError(incorrect_type_details))

    if errors:
        raise ExceptionGroup("TypedDict validation failed", errors)

    return True
