"""General functions used by ``vocab-tester`` and its tests."""

from . import logger
from .compact import compact as compact
from .compare import compare as compare
from .duplicates import (
    contains_duplicates as contains_duplicates,
    remove_duplicates as remove_duplicates,
)
from .set_functions import (
    set_choice as set_choice,
    set_choice_pop as set_choice_pop,
)

__all__ = [
    "compare",
    "contains_duplicates",
    "logger",
    "remove_duplicates",
    "set_choice",
    "set_choice_pop",
]
