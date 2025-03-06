"""General functions used by ``vocab-tester`` and its tests."""

from typing import TYPE_CHECKING

from .. import _seed
from . import logger
from .compact_function import compact as compact
from .compare_function import compare as compare
from .duplicates import (
    contains_duplicates as contains_duplicates,
    remove_duplicates as remove_duplicates,
)

# Seed has been set
if _seed is not None and not TYPE_CHECKING:
    from .set_functions import (
        set_choice_pop_sort as set_choice_pop,
        set_choice_sort as set_choice,
    )

else:
    from .set_functions import (
        set_choice as set_choice,
        set_choice_pop as set_choice_pop,
    )

__all__ = [
    "compact",
    "compare",
    "contains_duplicates",
    "logger",
    "remove_duplicates",
    "set_choice",
    "set_choice_pop",
]
