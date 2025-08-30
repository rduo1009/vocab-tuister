"""Representation of a Latin word that is undeclinable."""

from __future__ import annotations

import logging
from functools import total_ordering
from typing import TYPE_CHECKING

from ._class_word import _Word
from .misc import EndingComponents, MultipleMeanings

if TYPE_CHECKING:
    from src.core.accido.type_aliases import Endings

    from .type_aliases import Meaning

logger = logging.getLogger(__name__)


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

    Note that the arguments of ``RegularWord`` are keyword-only.
    """

    __slots__: tuple[str, ...] = ("word",)

    def __init__(self, word: str, *, meaning: Meaning) -> None:
        """Initialise RegularWord.

        Parameters
        ----------
        word : str
        meaning : Meaning
        """
        logger.debug("RegularWord(%s, meaning=%s)", word, meaning)

        super().__init__()

        self.word: str = word
        self._first: str = self.word
        self.meaning: Meaning = meaning
        self.endings: Endings = {"": self.word}

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

    def create_components_instance(self, key: str) -> EndingComponents:  # noqa: PLR6301
        """Generate an ``EndingComponents`` object based on endings keys.

        In the case of a regular word, the returned ``EndingComponents`` object
        will be empty.
        Note that this function should not usually be used by the user.

        Parameters
        ----------
        key : str
            The endings key.

        Returns
        -------
        EndingComponents
            The ``EndingComponents`` object created.
        """
        del key

        return EndingComponents(string="")

    def __repr__(self) -> str:
        return f"RegularWord({self.word}, meaning={self.meaning})"

    def __str__(self) -> str:
        return f"{self.meaning}: {self.word}"

    def __add__(self, other: object) -> RegularWord:
        if not isinstance(other, RegularWord) or self.word != other.word:
            return NotImplemented

        if self.meaning == other.meaning:
            return RegularWord(self.word, meaning=self.meaning)

        if isinstance(self.meaning, MultipleMeanings) or isinstance(
            other.meaning, MultipleMeanings
        ):
            new_meaning = self.meaning + other.meaning
        else:
            new_meaning = MultipleMeanings((self.meaning, other.meaning))

        return RegularWord(self.word, meaning=new_meaning)
