"""Representation of a Latin pronoun with endings."""

from __future__ import annotations

import logging
from functools import total_ordering
from typing import TYPE_CHECKING
from warnings import deprecated

from ._class_word import _Word
from .edge_cases import PRONOUNS
from .exceptions import InvalidInputError
from .misc import Case, EndingComponents, Gender, MultipleMeanings, Number

if TYPE_CHECKING:
    from .type_aliases import Ending, Meaning

logger = logging.getLogger(__name__)


@total_ordering
class Pronoun(_Word):
    """Representation of a Latin pronoun with endings.

    Attributes
    ----------
    pronoun : str
    meaning : Meaning
    endings : Endings

    Examples
    --------
    >>> foo = Pronoun("hic", meaning="this")
    >>> foo["Pmnomsg"]
    'hic'

    Note that the arguments of ``Pronoun`` are keyword-only.
    """

    __slots__ = ("femnom", "mascnom", "neutnom", "pronoun")

    def __init__(self, pronoun: str, *, meaning: Meaning) -> None:
        """Initialise ``Pronoun`` and determine the endings.

        Parameters
        ----------
        pronoun : str
        meaning : Meaning

        Raises
        ------
        InvalidInputError
            If `pronoun` is not in the pronoun table.

        Notes
        -----
        As pronouns in Latin have irregular endings with little pattern,
        the pronoun endings are manually written out in the ``edge_cases``
        module.
        """
        logger.debug("Pronoun(%s, meaning=%s)", pronoun, meaning)

        super().__init__()

        try:
            self.endings = PRONOUNS[pronoun]
        except KeyError as e:
            raise InvalidInputError(
                f"Pronoun '{pronoun}' not recognised."
            ) from e

        self.pronoun = pronoun
        self._first = self.pronoun
        self.meaning = meaning

        # HACK: hopefully this is the case!
        assert isinstance(self.endings["Pmnomsg"], str)
        assert isinstance(self.endings["Pfnomsg"], str)
        assert isinstance(self.endings["Pnnomsg"], str)

        self.mascnom = self.endings["Pmnomsg"]
        self.femnom = self.endings["Pfnomsg"]
        self.neutnom = self.endings["Pnnomsg"]

    def get(
        self, *, case: Case, number: Number, gender: Gender
    ) -> Ending | None:
        """Return the ending of the pronoun.

        The function returns ``None`` if no ending is found.

        Parameters
        ----------
        case : Case
            The case of the pronoun.
        number : Number
            The number of the pronoun.
        gender : Gender
            The gender of the pronoun.

        Returns
        -------
        Ending | None
            The ending found, or ``None`` if no ending is found

        Examples
        --------
        >>> foo = Pronoun("hic", meaning="this")
        >>> foo.get(
        ...     case=Case.NOMINATIVE,
        ...     number=Number.SINGULAR,
        ...     gender=Gender.MASCULINE,
        ... )
        'hic'

        Note that the arguments of ``get()`` are keyword-only.
        """
        logger.debug("%s.get(%s, %s, %s)", self._first, gender, case, number)
        short_gender = gender.shorthand
        short_case = case.shorthand
        short_number = number.shorthand

        return self.endings.get(f"P{short_gender}{short_case}{short_number}")

    def create_components_normalmeth(self, key: str) -> EndingComponents:  # noqa: PLR6301
        """Generate an ``EndingComponents`` object based on endings keys.

        This function should not usually be used by the user.

        Parameters
        ----------
        key : str
            The endings key.

        Returns
        -------
        EndingComponents
            The ``EndingComponents`` object created.

        Raises
        ------
        InvalidInputError
            If `key` is not a valid key for the word.
        """
        try:
            output = EndingComponents(
                gender=Gender(key[1]),
                case=Case(key[2:5]),
                number=Number(key[5:7]),
            )
        except (ValueError, IndexError) as e:
            raise InvalidInputError(f"Key '{key}' is invalid.") from e

        output.string = (
            f"{output.case.regular} {output.number.regular} "
            f"{output.gender.regular}"
        )
        return output

    @deprecated(
        "A regular method was favoured over a staticmethod. Use `create_components_normalmeth` instead."
    )
    @staticmethod
    def create_components(key: str) -> EndingComponents:
        """Generate an ``EndingComponents`` object based on endings keys.

        Deprecated in favour of ``create_components_normalmeth``.
        This function should not usually be used by the user.

        Parameters
        ----------
        key : str
            The endings key.

        Returns
        -------
        EndingComponents
            The ``EndingComponents`` object created.

        Raises
        ------
        InvalidInputError
            If `key` is not a valid key for the word.
        """
        placeholder_pronoun = Pronoun("hic", meaning="this")
        return Pronoun.create_components_normalmeth(placeholder_pronoun, key)

    def __repr__(self) -> str:
        return f"Pronoun({self.pronoun}, meaning={self.meaning})"

    def __str__(self) -> str:
        return f"{self.meaning}: {self.mascnom}, {self.femnom}, {self.neutnom}"

    def __add__(self, other: object) -> Pronoun:
        if not isinstance(other, Pronoun) or self.endings != other.endings:
            return NotImplemented

        if self.meaning == other.meaning:
            return Pronoun(self.pronoun, meaning=self.meaning)

        if isinstance(self.meaning, MultipleMeanings) or isinstance(
            other.meaning, MultipleMeanings
        ):
            new_meaning = self.meaning + other.meaning
        else:
            new_meaning = MultipleMeanings((self.meaning, other.meaning))

        return Pronoun(self.pronoun, meaning=new_meaning)
