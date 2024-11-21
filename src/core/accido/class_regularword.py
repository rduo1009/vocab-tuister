"""Representation of a Latin word that is undeclinable."""

from __future__ import annotations

import logging
from functools import total_ordering
from typing import TYPE_CHECKING

from .class_word import _Word
from .misc import EndingComponents

if TYPE_CHECKING:
    from .type_aliases import Meaning

logger: logging.Logger = logging.getLogger(__name__)


@total_ordering
class RegularWord(_Word):
    """Representation of a Latin word that is undeclinable.

    Attributes
    ----------
    word : str
    meaning : Meaning

    Examples
    --------
    >>> foo = RegularWord("sed", meaning="but")
    >>> foo.endings
    {'': 'sed'}

    Note that the arguments of RegularWord are keyword-only.
    """

    __slots__ = ("word",)

    def __init__(self, word: str, *, meaning: Meaning) -> None:
        """Initialise RegularWord.

        Parameters
        ----------
        word : str
        meaning : Meaning
        """
        logger.debug("RegularWord(%s, %s)", word, meaning)

        super().__init__()

        self.word: str = word
        self._first: str = self.word
        self.meaning: Meaning = meaning
        self.endings = {"": self.word}

    def get(self) -> str:
        """Return the word.

        Returns
        -------
        str
            The word.

        Examples
        --------
        >>> foo = RegularWord("sed", meaning="but")
        >>> foo.get()
        'sed'
        """
        logger.debug("%s.get()", self._first)

        return self.word

    @staticmethod
    def _create_components(
        key: str,  # noqa: ARG004
    ) -> EndingComponents:
        return EndingComponents(string="")

    def __repr__(self) -> str:
        return f"RegularWord({self.word}, {self.meaning})"

    def __str__(self) -> str:
        return f"{self.meaning}: {self.word}"
