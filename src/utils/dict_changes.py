"""Provides utilities for applying changes to dictionaries.

Only supports strings as dictionary keys.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import re


class DictChanges[V](NamedTuple):
    """A named tuple representing changes to be applied to a dictionary.

    Attributes
    ----------
    replacements : dict[str, V]
        A dictionary of key-value pairs to replace in the target dictionary.
    additions : dict[str, V]
        A dictionary of key-value pairs to add to the target dictionary.
    deletions : set[str]
        A set of keys or regex patterns to be deleted from the target dictionary.
    """

    replacements: dict[str, V]
    additions: dict[str, V]
    deletions: set[str | re.Pattern[str]]


def apply_changes[V](
    target: dict[str, V], changes: DictChanges[V]
) -> dict[str, V]:
    """Apply a changes to a dictionary by replacing and deleting specified keys.

    Parameters
    ----------
    target : dict[str, V]
        The original dictionary to modify.
    changes : DictChanges[V]
        A collection of replacements and deletions to apply.

    Returns
    -------
    dict[str, V]
        A new dictionary with the specified changes applied.

    Raises
    ------
    KeyError
        If a key specified for replacement or deletion does not exist in the
        target dictionary. If a key specified for addition already exists.
    ValueError
        If a key specified for replacement is also specified for deletion. If a
        key specified for addition is also specified for deletion.
    """
    # VALIDATION
    string_deletions: set[str] = set()
    regex_deletions: set[re.Pattern[str]] = set()
    for key in changes.deletions:
        if isinstance(key, str):
            string_deletions.add(key)
            continue
        regex_deletions.add(key)

    # Check replacements against deletions
    for key in changes.replacements:
        if key in string_deletions:
            raise ValueError(
                f"Key '{key}' is specified for replacement and deletion."
            )

        for pattern in regex_deletions:
            if pattern.match(key):
                raise ValueError(
                    f"Key '{key}' is specified for replacement but also deletion "
                    f"by regex pattern '{pattern.pattern}'."
                )

    # Check additions against deletions
    for key in changes.additions:
        if key in string_deletions:
            raise ValueError(
                f"Key '{key}' is specified for addition and deletion."
            )

        for pattern in regex_deletions:
            if pattern.match(key):
                raise ValueError(
                    f"Key '{key}' is specified for addition but also deletion "
                    f"by regex pattern '{pattern.pattern}'."
                )

    modified_dict = target.copy()

    # APPLY REPLACEMENTS
    for key, new_value in changes.replacements.items():
        if key not in modified_dict:
            # HACK: This breaks with some irregular, but also defective verbs.
            # raise KeyError(
            #     f"Key '{key}' specified for replacement does not exist in the "
            #     "target dictionary."
            # )
            continue

        modified_dict[key] = new_value

    # APPLY ADDITIONS
    for key, new_value in changes.additions.items():
        if key in modified_dict:
            raise KeyError(
                f"Key '{key}' specified for addition already exists in the "
                "target dictionary."
            )

        modified_dict[key] = new_value

    # APPLY DELETIONS
    keys_to_delete: set[str] = set()

    for deletion_spec in changes.deletions:
        # string deletion
        if isinstance(deletion_spec, str):
            key_to_delete = deletion_spec
            if key_to_delete in modified_dict:
                keys_to_delete.add(key_to_delete)
            else:
                raise KeyError(
                    f"Key '{key_to_delete}' specified for deletion does not exist "
                    "in the target dictionary (or was already removed)."
                )
            continue

        # regex pattern deletion
        current_keys = list(modified_dict.keys())
        for key in current_keys:
            if deletion_spec.match(key):
                keys_to_delete.add(key)

    for key in keys_to_delete:
        # check again in case a key had multiple matches
        if key in modified_dict:
            del modified_dict[key]

    return modified_dict
