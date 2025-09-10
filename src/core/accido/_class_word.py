"""Representation of a Latin word."""

# pyright: reportImplicitOverride=false, reportExplicitAny=false, reportAny=false

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import total_ordering
from typing import TYPE_CHECKING, Any

from .misc import MultipleEndings

if TYPE_CHECKING:
    from .misc import EndingComponents
    from .type_aliases import Ending, Endings, Meaning


@total_ordering
class _Word(ABC):  # noqa: PLW1641
    """Representation of an Latin word.

    This class is not intended to be used by the user. Rather, all of the
    other classes inherit from this class.

    Attributes
    ----------
    endings : Ending
    _first : str
        The first principal part. Used so that the word classes can be
        alphabetically sorted.
    meaning : Meaning
        The meaning of the word.
    """

    __slots__: tuple[str, ...] = ("_first", "endings", "meaning")

    endings: Endings
    _first: str
    meaning: Meaning

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Word):
            return NotImplemented
        return self.endings == other.endings and self.meaning == other.meaning

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, _Word):
            return NotImplemented
        return self._first < other._first

    def __getitem__(self, key: str) -> Ending:
        return self.endings[key]

    def find(self, form: str) -> list[EndingComponents]:
        """Find the ``EndingComponents`` objects that match the given form.

        Parameters
        ----------
        form : str
            The form to search for.

        Returns
        -------
        list[EndingComponents]
            The list of ``EndingComponents`` objects that represent the endings
            components that match `form`.
        """
        return [
            self.create_components_instance(key)
            for key, value in self.endings.items()
            if (isinstance(value, MultipleEndings) and form in value.get_all())
            or (not isinstance(value, MultipleEndings) and value == form)
        ]

    # Force implementation of these methods
    @abstractmethod
    def get(
        self, *args: Any, **kwargs: Any
    ) -> Ending | None:  # sourcery skip: docstrings-for-functions
        ...

    @abstractmethod
    def create_components_instance(self, key: str) -> EndingComponents: ...
