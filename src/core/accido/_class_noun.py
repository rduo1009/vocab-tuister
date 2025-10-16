"""Representation of a Latin noun with endings."""

import logging
from functools import total_ordering
from typing import TYPE_CHECKING, Final, overload
from warnings import deprecated

from ._class_word import Word
from ._edge_cases import IRREGULAR_DECLINED_NOUNS, IRREGULAR_NOUNS
from ._syllables import count_syllables
from .exceptions import InvalidInputError
from .misc import (
    Case,
    ComponentsSubtype,
    EndingComponents,
    Gender,
    MultipleMeanings,
    Number,
)

if TYPE_CHECKING:
    from .type_aliases import Ending, Endings, Meaning, NounDeclension

logger = logging.getLogger(__name__)

CONSONANTS: Final[set[str]] = set("bcdfghjklmnpqrstvwxyz")


@total_ordering
class Noun(Word):
    """Representation of a Latin noun with endings.

    Attributes
    ----------
    nominative : str
    genitive : str | None
        The genitive, if applicable (only for regular nouns).
    meaning : Meaning
    declension : NounDeclension
        The declension of the noun. The value 0 represents an irregular
        declension.
    endings : Endings
    plurale_tantum : bool
        If the noun is a plurale tantum or not.
    gender : Gender | None
        The gender, if applicable (only for regular nouns).

    Examples
    --------
    >>> foo = Noun(
    ...     "ancilla", "ancillae", gender=Gender.FEMININE, meaning="slavegirl"
    ... )
    >>> foo["Nnomsg"]
    'ancilla'

    Note that all arguments of ``Noun`` are keyword-only.

    >>> foo = Noun("ego", meaning="I")
    >>> foo["Nnomsg"]
    'ego'

    Notes
    -----
    ``accido`` relies on the assumption that there are no neuter or plurale
    tantum fifth declension nouns (there doesn't seem to be any).
    """

    __slots__: tuple[str, ...] = (
        "_stem",
        "declension",
        "gender",
        "genitive",
        "i_stem",
        "nominative",
        "plurale_tantum",
        "principal_parts",
    )

    # fmt: off
    @overload
    def __init__(self, nominative: str, *, meaning: Meaning) -> None: ...
    @overload
    def __init__(self, nominative: str, genitive: str, *, gender: Gender, meaning: Meaning) -> None: ...
    # fmt: on

    def __init__(
        self,
        nominative: str,
        genitive: str | None = None,
        *,
        gender: Gender | None = None,
        meaning: Meaning,
    ) -> None:
        """Initialise ``Noun`` and determine the declension and endings.

        Parameters
        ----------
        nominative : str
        genitive : str | None
            The genitive, if applicable (only for regular nouns).
        gender : Gender | None
            The gender, if applicable (only for regular nouns).
        meaning : Meaning

        Raises
        ------
        InvalidInputError
            If the input is not valid (invalid value for `gender` or `genitive`).
        """
        logger.debug(
            "Noun(%s, %s, gender=%s, meaning=%s)",
            nominative,
            genitive,
            gender,
            meaning,
        )

        super().__init__()

        self.nominative: str = nominative
        self.genitive: str | None = genitive
        self.gender: Gender | None = gender
        self.meaning: Meaning = meaning
        self.plurale_tantum: bool = False

        self.principal_parts: tuple[str, ...] = (
            (self.nominative,)
            if self.genitive is None
            else (self.nominative, self.genitive)
        )

        self._first: str = self.nominative
        self.declension: NounDeclension

        if self.nominative in IRREGULAR_NOUNS:
            self.endings: Endings = IRREGULAR_NOUNS[nominative]
            self.declension = 0
            return

        assert self.genitive is not None
        assert self.gender is not None

        if not gender:
            raise InvalidInputError(
                f"Noun '{nominative}' is not irregular but gender not provided."
            )
        if not genitive:
            raise InvalidInputError(
                f"Noun '{nominative}' is not irregular but genitive not provided."
            )

        self._stem: str
        self._find_declension()

        self.i_stem: bool = (
            self._determine_if_i_stem() if self.declension == 3 else False
        )

        self.endings = self._determine_endings()

        if self.gender == Gender.NEUTER:
            self._neuter_endings()

        if self.plurale_tantum:
            self.endings = {
                k: v for k, v in self.endings.items() if not k.endswith("sg")
            }

    def _determine_if_i_stem(self) -> bool:
        assert self.genitive is not None

        if not self.plurale_tantum:
            if self.gender in {Gender.MASCULINE, Gender.FEMININE}:
                if (  # parisyllabic i-stem
                    self.nominative.endswith(("is", "es"))
                    and (
                        count_syllables(self.nominative)
                        == count_syllables(self.genitive)
                    )
                ) or (  # monosyllabic i-stem
                    count_syllables(self.nominative) == 1
                    and self.nominative[-1] in CONSONANTS
                    and self.nominative[-2] in CONSONANTS
                ):
                    return True

            elif self.nominative.endswith(("e", "al", "ar")):  # neuter i-stem
                return True

        elif self.genitive.endswith("ium"):  # plurale tantum has gen sg
            self._stem = self.genitive[:-3]  # moenium -> moen-
            return True

        return False

    def _find_declension(self) -> None:
        assert self.genitive is not None

        # The ordering of this is strange because
        # e.g. ending -ei ends in 'i' as well as 'ei'
        # so 5th declension check must come before 2nd declension check, etc.
        if self.genitive.endswith("ei") and self.nominative.endswith("es"):
            self.declension = 5
            self._stem = self.genitive[:-2]  # diei > di-
        elif self.genitive.endswith("ae"):
            self.declension = 1
            self._stem = self.genitive[:-2]  # puellae -> puell-
        elif self.genitive.endswith("i"):
            self.declension = 2
            self._stem = self.genitive[:-1]  # servi -> serv-
        elif self.genitive.endswith("is"):
            self.declension = 3
            self._stem = self.genitive[:-2]  # canis -> can-
        elif self.genitive.endswith("us"):
            self.declension = 4
            self._stem = self.genitive[:-2]  # manus -> man-

        elif self.genitive.endswith("uum"):
            self.declension = 4
            self._stem = self.genitive[:-3]  # manuum -> man-
            self.plurale_tantum = True
        elif self.genitive.endswith("arum"):
            self.declension = 1
            self._stem = self.genitive[:-4]  # puellarum -> puell-
            self.plurale_tantum = True
        elif self.genitive.endswith("orum"):
            self.declension = 2
            self._stem = self.genitive[:-4]  # servorum -> serv-
            self.plurale_tantum = True
        elif self.genitive.endswith("um"):
            self.declension = 3
            self._stem = self.genitive[:-2]  # canum -> can-
            self.plurale_tantum = True

        else:
            raise InvalidInputError(
                f"Invalid genitive form: '{self.genitive}'"
            )

    def _determine_endings(self) -> Endings:
        assert self.genitive is not None

        if self.nominative in IRREGULAR_DECLINED_NOUNS:
            return IRREGULAR_DECLINED_NOUNS[self.nominative]

        match self.declension:
            case 1:
                return {
                    "Nnomsg": self.nominative,  # puella
                    "Nvocsg": self.nominative,  # puella
                    "Naccsg": self._stem + "am",  # puellam
                    "Ngensg": self.genitive,  # puellae
                    "Ndatsg": self._stem + "ae",  # puellae
                    "Nablsg": self._stem + "a",  # puella
                    "Nnompl": self._stem + "ae",  # puellae
                    "Nvocpl": self._stem + "ae",  # puellae
                    "Naccpl": self._stem + "as",  # puellas\
                    "Ngenpl": self._stem + "arum",  # puellarum
                    "Ndatpl": self._stem + "is",  # puellis
                    "Nablpl": self._stem + "is",  # puellis
                }

            case 2:
                return {
                    "Nnomsg": self.nominative,  # servus
                    "Nvocsg": (
                        self.nominative  # puer
                        if self.nominative.endswith("er")
                        else self._stem + "e"  # serve
                    ),
                    "Naccsg": self._stem + "um",  # servum
                    "Ngensg": self.genitive,  # servi
                    "Ndatsg": self._stem + "o",  # servo
                    "Nablsg": self._stem + "o",  # servo
                    "Nnompl": self._stem + "i",  # servi
                    "Nvocpl": self._stem + "i",  # servi
                    "Naccpl": self._stem + "os",  # servos
                    "Ngenpl": self._stem + "orum",  # servorum
                    "Ndatpl": self._stem + "is",  # servis
                    "Nablpl": self._stem + "is",  # servis
                }

            case 3:
                return {
                    "Nnomsg": self.nominative,  # mercator
                    "Nvocsg": self.nominative,  # mercator
                    "Naccsg": self._stem + "em",  # mercatorem
                    "Ngensg": self.genitive,  # mercatoris
                    "Ndatsg": self._stem + "i",  # mercatori
                    "Nablsg": self._stem + "e",  # mercatore
                    "Nnompl": self._stem + "es",  # mercatores
                    "Nvocpl": self._stem + "es",  # mercatores
                    "Naccpl": self._stem + "es",  # mercatores
                    "Ngenpl": self._stem + "ium"  # montium
                    if self.i_stem
                    else self._stem + "um",  # mercatorum
                    "Ndatpl": self._stem + "ibus",  # mercatoribus
                    "Nablpl": self._stem + "ibus",  # mercatoribus
                }

            case 4:
                return {
                    "Nnomsg": self.nominative,  # manus
                    "Nvocsg": self.nominative,  # manus
                    "Naccsg": self._stem + "um",  # manum
                    "Ngensg": self._stem + "us",  # manus
                    "Ndatsg": self._stem + "ui",  # manui
                    "Nablsg": self._stem + "u",  # manu
                    "Nnompl": self._stem + "us",  # manus
                    "Nvocpl": self._stem + "us",  # manus
                    "Naccpl": self._stem + "us",  # manus
                    "Ngenpl": self._stem + "uum",  # manuum
                    "Ndatpl": self._stem + "ibus",  # manibus
                    "Nablpl": self._stem + "ibus",  # manibus
                }

            case _:
                return {
                    "Nnomsg": self.nominative,  # res
                    "Nvocsg": self.nominative,  # res
                    "Naccsg": self._stem + "em",  # rem
                    "Ngensg": self._stem + "ei",  # rei
                    "Ndatsg": self._stem + "ei",  # rei
                    "Nablsg": self._stem + "e",  # re
                    "Nnompl": self._stem + "es",  # res
                    "Nvocpl": self._stem + "es",  # res
                    "Naccpl": self._stem + "es",  # res
                    "Ngenpl": self._stem + "erum",  # rerum
                    "Ndatpl": self._stem + "ebus",  # rebus
                    "Nablpl": self._stem + "ebus",  # rebus
                }

    def _neuter_endings(self) -> None:
        self.endings["Nvocsg"] = self.nominative  # templum
        self.endings["Naccsg"] = self.nominative  # templum

        if self.declension == 3 and self.i_stem:
            self.endings["Nablsg"] = self._stem + "i"  # mari
            self.endings["Nnompl"] = self._stem + "ia"  # maria
            self.endings["Nvocpl"] = self._stem + "ia"  # maria
            self.endings["Naccpl"] = self._stem + "ia"  # maria
            self.endings["Ngenpl"] = self._stem + "ium"  # marium
            return

        if self.declension == 4:
            self.endings["Nnompl"] = self._stem + "ua"  # cornua
            self.endings["Nvocpl"] = self._stem + "ua"  # cornua
            self.endings["Naccpl"] = self._stem + "ua"  # cornua
            self.endings["Ndatsg"] = self._stem + "u"  # cornu
            return

        if self.declension == 5:
            raise InvalidInputError(
                "Fifth declension nouns cannot be neuter. "
                f"(noun '{self.nominative}' given)"
            )

        # For the other declensions
        self.endings["Nnompl"] = self._stem + "a"  # templa
        self.endings["Nvocpl"] = self._stem + "a"  # templa
        self.endings["Naccpl"] = self._stem + "a"  # templa

    def get(self, *, case: Case, number: Number) -> Ending | None:
        """Return the ending of the noun.

        The function returns ``None`` if no ending is found.

        Parameters
        ----------
        case : Case
            The case of the noun.
        number : Number
            The number of the noun.

        Returns
        -------
        Ending | None
            The ending found, or ``None`` if no ending is found.

        Examples
        --------
        >>> foo = Noun(
        ...     "ancilla", "ancillae", gender=Gender.FEMININE, meaning="slavegirl"
        ... )
        >>> foo.get(case=Case.NOMINATIVE, number=Number.SINGULAR)
        'ancilla'

        Note that all arguments of ``get()`` are keyword-only.
        """
        logger.debug("%s.get(%s, %s)", self._first, case, number)

        short_case = case.shorthand
        short_number = number.shorthand

        return self.endings.get(f"N{short_case}{short_number}")

    def create_components(self, key: str) -> EndingComponents:
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
                case=Case(key[1:4]), number=Number(value=key[4:6])
            )
        except (ValueError, IndexError) as e:
            raise InvalidInputError(f"Key '{key}' is invalid.") from e

        output.string = f"{output.case.regular} {output.number.regular}"
        if self.declension == 0:
            output.subtype = ComponentsSubtype.PRONOUN
        return output

    @deprecated("Use create_components instead")
    def create_components_instance(self, key: str) -> EndingComponents:
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
        return self.create_components(key)

    def __repr__(self) -> str:
        if self.declension == 0:
            return f"Noun({self.nominative}, meaning={self.meaning})"

        assert self.gender is not None

        return (
            f"Noun({', '.join(self.principal_parts)}, "
            f"gender={self.gender.regular}, meaning={self.meaning})"
        )

    def __str__(self) -> str:
        if self.declension == 0:
            return f"{self.meaning}: {self.nominative}, (irregular)"

        assert self.gender is not None

        return (
            f"{self.meaning}: {', '.join(self.principal_parts)}, "
            f"({self.gender.shorthand})"
        )

    def __add__(self, other: object) -> Noun:
        def _create_noun(
            nominative: str,
            genitive: str | None,
            gender: Gender | None,
            meaning: Meaning,
        ) -> Noun:
            if genitive is not None:  # implies `gender` is not None as well
                assert gender is not None

                return Noun(
                    nominative, genitive, gender=gender, meaning=meaning
                )

            return Noun(nominative, meaning=meaning)

        if not isinstance(other, Noun) or not (
            self.endings == other.endings
            and self.declension == other.declension
            and self.gender == other.gender
            and self.plurale_tantum == other.plurale_tantum
        ):
            return NotImplemented

        if self.meaning == other.meaning:
            return _create_noun(
                self.nominative, self.genitive, self.gender, self.meaning
            )

        if isinstance(self.meaning, MultipleMeanings) or isinstance(
            other.meaning, MultipleMeanings
        ):
            new_meaning = self.meaning + other.meaning
        else:
            new_meaning = MultipleMeanings((self.meaning, other.meaning))

        return _create_noun(
            self.nominative, self.genitive, self.gender, new_meaning
        )
