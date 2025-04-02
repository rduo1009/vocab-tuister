"""Representation of a Latin word that is undeclinable."""

from __future__ import annotations

import logging
from functools import total_ordering
from typing import TYPE_CHECKING
from warnings import deprecated

from ._class_word import _Word
from .misc import EndingComponents, MultipleMeanings

if TYPE_CHECKING:
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

    __slots__ = ("word",)

    def __init__(self, word: str, *, meaning: Meaning) -> None:
        """Initialise RegularWord.

        Parameters
        ----------
        word : str
        meaning : Meaning
        """
        logger.debug("RegularWord(%s, meaning=%s)", word, meaning)

        super().__init__()

        self.word = word
        self._first = self.word
        self.meaning = meaning
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

    def create_components_normalmeth(self, key: str) -> EndingComponents:  # noqa: ARG002, PLR6301
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
        return EndingComponents(string="")

    @deprecated(
        "A regular method was favoured over a staticmethod. Use `create_components_normalmeth` instead."
    )
    @staticmethod
    def create_components(key: str) -> EndingComponents:
        """Generate an ``EndingComponents`` object based on endings keys.

        Deprecated in favour of ``create_components_normalmeth``.
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
        placeholder_regularword = RegularWord("sed", meaning="but")
        return RegularWord.create_components_normalmeth(
            placeholder_regularword, key
        )

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
