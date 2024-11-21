"""General functions used by vocab-tester and its tests."""

from . import logger
from .compare import compare
from .duplicates import contains_duplicates, remove_duplicates
from .set_functions import set_choice, set_choice_pop

__all__ = [
    "compare",
    "contains_duplicates",
    "logger",
    "remove_duplicates",
    "set_choice",
    "set_choice_pop",
]
