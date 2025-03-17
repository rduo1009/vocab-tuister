"""Contains functions that pick items from sets."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import optype as op


def set_choice[T](s: set[T]) -> T:
    """Choose a random element from a set.

    Parameters
    ----------
    s : set[T]
        The set to choose from.

    Returns
    -------
    T
        A random element from the set.
    """
    return random.choice(tuple(s))


def set_choice_pop[T](s: set[T]) -> T:
    """Choose a random element from a set and removes it from the set.

    Parameters
    ----------
    s : set[T]
        The set to choose from.

    Returns
    -------
    T
        A random element from the set.
    """
    value = random.choice(tuple(s))
    s.remove(value)
    return value


def set_choice_sort[T: op.CanLt[Any]](s: set[T]) -> T:
    """Choose a random element from a set after sorting the set.

    The set is sorted to make the result deterministic if ``random.seed()``
    is used.

    Parameters
    ----------
    s : set[T]
        The set to choose from.

    Returns
    -------
    T
        A random element from the set.
    """
    return random.choice(sorted(s))


def set_choice_pop_sort[T: op.CanLt[Any]](s: set[T]) -> T:
    """Pop a random element from a set after sorting the set.

    The set is sorted to make the result deterministic if ``random.seed()``
    is used.

    Parameters
    ----------
    s : set[T]
        The set to choose from.

    Returns
    -------
    T
        A random element from the set.
    """
    value = random.choice(sorted(s))
    s.remove(value)
    return value
