"""Representation of a Latin adjective with endings."""

from __future__ import annotations

import logging
import warnings
from functools import total_ordering
from typing import TYPE_CHECKING, Any, Literal, overload
from warnings import deprecated

from ._class_word import Word
from ._edge_cases import (
    IRREGULAR_ADJECTIVES,
    IRREGULAR_PP_ADJECTIVES,
    IRREGULAR_STEM_ADJECTIVES,
    LIS_ADJECTIVES,
    REAL_ADVERB_ADJECTIVES,
    UNCOMPARABLE_ADVERBS,
)
from .exceptions import InvalidInputError
from .misc import (
    Case,
    Degree,
    EndingComponents,
    Gender,
    MultipleMeanings,
    Number,
)

if TYPE_CHECKING:
    from .type_aliases import (
        AdjectiveDeclension,
        Ending,
        Endings,
        Meaning,
        Termination,
    )

logger = logging.getLogger(__name__)


@total_ordering
class Adjective(Word):
    """Representation of a Latin adjective with endings.

    Attributes
    ----------
    meaning : Meaning
    endings : Endings
    declension : AdjectiveDeclension
        The declension of the adjective. 212 represents a 2-1-2
        adjective, while 3 represents a third declension adjective.
    termination : Termination | None
        The termination of the adjective if applicable (only third
        declension adjectives).
    irregular_flag : bool

    Examples
    --------
    >>> foo = Adjective(
    ...     "laetus", "laeta", "laetum", declension="212", meaning="happy"
    ... )
    >>> foo["Aposmnomsg"]
    'laetus'

    Note that the declension and meaning arguments of ``Adjective``s are
    keyword-only.

    >>> bar = Adjective(
    ...     "egens", "egentis", termination=1, declension="3", meaning="poor"
    ... )
    >>> bar["Aposmnomsg"]
    'egens'

    The same can be said with the termination argument for third declension
    adjectives.
    """

    __slots__: tuple[str, ...] = (
        "_cmp_stem",
        "_irregular_cmpadv",
        "_irregular_posadv",
        "_irregular_spradv",
        "_pos_stem",
        "_principal_parts",
        "_spr_stem",
        "adverb_flag",
        "declension",
        "femnom",
        "irregular_flag",
        "mascgen",
        "mascnom",
        "neutnom",
        "plurale_tantum",
        "principal_parts",
        "termination",
    )

    # fmt: off
    @overload
    def __init__(self, *principal_parts: str, declension: Literal["212"], meaning: Meaning) -> None: ...
    @overload
    def __init__(self, *principal_parts: str, termination: Termination, declension: Literal["3"], meaning: Meaning) -> None: ...
    # fmt: on

    def __init__(
        self,
        *principal_parts: str,
        termination: Termination | None = None,
        declension: AdjectiveDeclension,
        meaning: Meaning,
    ) -> None:
        """Initialise ``Adjective`` and determine the endings.

        Parameters
        ----------
        *principal_parts : str
            The principal parts of the adjective.
        termination : Termination | None, default = None
            The termination of the adjective if applicable (only third
            declension adjectives).
        declension : AdjectiveDeclension
            The declension of the adjective. 212 represents a 2-1-2
            adjective, while 3 represents a third declension adjective.
        meaning : Meaning
        """
        logger.debug(
            "Adjective(%s, termination=%s, declension=%s, meaning=%s)",
            ", ".join(principal_parts),
            termination,
            declension,
            meaning,
        )

        super().__init__()

        self.principal_parts: tuple[str, ...] = principal_parts
        self._principal_parts: tuple[str, ...] = self.principal_parts
        self.mascnom: str = self.principal_parts[0]

        self._first: str = self.principal_parts[0]
        self.meaning: Meaning = meaning
        self.declension: AdjectiveDeclension = declension
        self.termination: Termination | None = termination
        self.irregular_flag: bool = False
        self.adverb_flag: bool = self.mascnom in REAL_ADVERB_ADJECTIVES
        self.plurale_tantum: bool = False

        if self.mascnom in IRREGULAR_ADJECTIVES:
            self.endings = IRREGULAR_ADJECTIVES[self.mascnom]
            return

        if self.mascnom in IRREGULAR_STEM_ADJECTIVES:
            self.irregular_flag = True
            irregular_data = IRREGULAR_STEM_ADJECTIVES[self.mascnom]

            self._cmp_stem: str = irregular_data[0]
            self._spr_stem: Ending = irregular_data[1]

            if None not in irregular_data[2:]:
                assert irregular_data[2] is not None
                assert irregular_data[3] is not None
                assert irregular_data[4] is not None

                self._irregular_posadv: str = irregular_data[2]
                self._irregular_cmpadv: str = irregular_data[3]
                self._irregular_spradv: str = irregular_data[4]
            else:
                self.adverb_flag = False

        if self.declension == "212":
            self.endings: Endings = self._212_endings()
            return

        self._pos_stem: str
        self.femnom: str
        self.mascgen: str
        self.neutnom: str

        match self.termination:
            case 1:
                self.endings = self._31_endings()

            case 2:
                self.endings = self._32_endings()

            case _:
                self.endings = self._33_endings()

    def _212_endings(self) -> Endings:
        if len(self.principal_parts) != 3:
            raise InvalidInputError(
                "2-1-2 adjectives must have 3 principal parts. "
                f"(adjective '{self._first}' given)"
            )

        self.femnom = self.principal_parts[1]
        self.neutnom = self.principal_parts[2]

        if (
            self.mascnom.endswith("i")
            and self.femnom.endswith("ae")
            and self.neutnom.endswith("a")
        ):
            self.plurale_tantum = True
            self._pos_stem = self.femnom[:-2]  # nonnullae -> nonnull-
        else:
            if self.mascnom not in IRREGULAR_PP_ADJECTIVES:
                if not (self.mascnom.endswith(("us", "er"))):
                    raise InvalidInputError(
                        f"Invalid masculine form: '{self.mascnom}' (must end in '-us' or '-er')"
                    )
                if not self.femnom.endswith("a"):
                    raise InvalidInputError(
                        f"Invalid feminine form: '{self.femnom}' (must end in '-a')"
                    )
                if not self.neutnom.endswith("um"):
                    raise InvalidInputError(
                        f"Invalid neuter form: '{self.neutnom}' (must end in '-um')"
                    )
            self._pos_stem = self.femnom[:-1]  # cara -> car-

        if self.mascnom not in IRREGULAR_STEM_ADJECTIVES:
            self._cmp_stem = self._pos_stem + "ior"  # car- -> carior-
            if self.mascnom.endswith("er"):
                self._spr_stem = self.mascnom + "rim"  # miser- -> miserrim-
            elif self.mascnom in LIS_ADJECTIVES:
                self._spr_stem = self._pos_stem + "lim"  # facil- -> facillim-
            else:
                self._spr_stem = self._pos_stem + "issim"  # car- -> carissim-

        endings: Endings = {
            "Aposmnomsg": self.mascnom,  # carus
            "Aposmvocsg": self.mascnom  # miser
            if self.mascnom.endswith("er")
            else self._pos_stem + "e",  # care
            "Aposmaccsg": self._pos_stem + "um",  # carum
            "Aposmgensg": self._pos_stem + "i",  # cari
            "Aposmdatsg": self._pos_stem + "o",  # caro
            "Aposmablsg": self._pos_stem + "o",  # caro
            "Aposmnompl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "i",  # cari
            "Aposmvocpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "i",  # cari
            "Aposmaccpl": self._pos_stem + "os",  # caros
            "Aposmgenpl": self._pos_stem + "orum",  # carorum
            "Aposmdatpl": self._pos_stem + "is",  # caris
            "Aposmablpl": self._pos_stem + "is",  # caris
            "Aposfnomsg": self.femnom,  # cara
            "Aposfvocsg": self.femnom,  # cara
            "Aposfaccsg": self._pos_stem + "am",  # caram
            "Aposfgensg": self._pos_stem + "ae",  # carae
            "Aposfdatsg": self._pos_stem + "ae",  # carae
            "Aposfablsg": self._pos_stem + "a",  # cara
            "Aposfnompl": self._pos_stem
            + "ae",  # carae # even if plural only, _pos_stem is derived from the feminine anyway
            "Aposfvocpl": self._pos_stem + "ae",  # carae
            "Aposfaccpl": self._pos_stem + "as",  # caras
            "Aposfgenpl": self._pos_stem + "arum",  # cararum
            "Aposfdatpl": self._pos_stem + "is",  # caris
            "Aposfablpl": self._pos_stem + "is",  # caris
            "Aposnnomsg": self.neutnom,  # carum
            "Aposnvocsg": self.neutnom,  # carum
            "Aposnaccsg": self.neutnom,  # carum
            "Aposngensg": self._pos_stem + "i",  # cari
            "Aposndatsg": self._pos_stem + "o",  # caro
            "Aposnablsg": self._pos_stem + "o",  # caro
            "Aposnnompl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "a",  # cara
            "Aposnvocpl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "a",  # cara
            "Aposnaccpl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "a",  # cara
            "Aposngenpl": self._pos_stem + "orum",  # carorum
            "Aposndatpl": self._pos_stem + "is",  # caris
            "Aposnablpl": self._pos_stem + "is",  # caris
            "Acmpmnomsg": self._cmp_stem,  # carior
            "Acmpmvocsg": self._cmp_stem,  # carior
            "Acmpmaccsg": self._cmp_stem + "em",  # cariorem
            "Acmpmgensg": self._cmp_stem + "is",  # carioris
            "Acmpmdatsg": self._cmp_stem + "i",  # cariori
            "Acmpmablsg": self._cmp_stem + "e",  # cariore
            "Acmpmnompl": self._cmp_stem + "es",  # cariores
            "Acmpmvocpl": self._cmp_stem + "es",  # cariores
            "Acmpmaccpl": self._cmp_stem + "es",  # cariores
            "Acmpmgenpl": self._cmp_stem + "um",  # cariorum
            "Acmpmdatpl": self._cmp_stem + "ibus",  # carioribus
            "Acmpmablpl": self._cmp_stem + "ibus",  # carioribus
            "Acmpfnomsg": self._cmp_stem,  # carior
            "Acmpfvocsg": self._cmp_stem,  # carior
            "Acmpfaccsg": self._cmp_stem + "em",  # cariorem
            "Acmpfgensg": self._cmp_stem + "is",  # carioris
            "Acmpfdatsg": self._cmp_stem + "i",  # cariori
            "Acmpfablsg": self._cmp_stem + "e",  # cariore
            "Acmpfnompl": self._cmp_stem + "es",  # cariores
            "Acmpfvocpl": self._cmp_stem + "es",  # cariores
            "Acmpfaccpl": self._cmp_stem + "es",  # cariores
            "Acmpfgenpl": self._cmp_stem + "um",  # cariorum
            "Acmpfdatpl": self._cmp_stem + "ibus",  # carioribus
            "Acmpfablpl": self._cmp_stem + "ibus",  # carioribus
            "Acmpnnomsg": self._cmp_stem[:-3] + "ius",  # carius
            "Acmpnvocsg": self._cmp_stem[:-3] + "ius",  # carius
            "Acmpnaccsg": self._cmp_stem[:-3] + "ius",  # carius
            "Acmpngensg": self._cmp_stem + "is",  # carioris
            "Acmpndatsg": self._cmp_stem + "i",  # cariori
            "Acmpnablsg": self._cmp_stem + "e",  # cariore
            "Acmpnnompl": self._cmp_stem + "a",  # cariora
            "Acmpnvocpl": self._cmp_stem + "a",  # cariora
            "Acmpnaccpl": self._cmp_stem + "a",  # cariora
            "Acmpngenpl": self._cmp_stem + "um",  # cariorum
            "Acmpndatpl": self._cmp_stem + "ibus",  # carioribus
            "Acmpnablpl": self._cmp_stem + "ibus",  # carioribus
            "Asprmnomsg": self._spr_stem + "us",  # carrissimus
            "Asprmvocsg": self._spr_stem + "e",  # carrissime
            "Asprmaccsg": self._spr_stem + "um",  # carrissimum
            "Asprmgensg": self._spr_stem + "i",  # carrissimi
            "Asprmdatsg": self._spr_stem + "o",  # carrissimo
            "Asprmablsg": self._spr_stem + "o",  # carrissimo
            "Asprmnompl": self._spr_stem + "i",  # carrissimi
            "Asprmvocpl": self._spr_stem + "i",  # carrissimi
            "Asprmaccpl": self._spr_stem + "os",  # carrissimos
            "Asprmgenpl": self._spr_stem + "orum",  # carrissimorum
            "Asprmdatpl": self._spr_stem + "is",  # carrissimis
            "Asprmablpl": self._spr_stem + "is",  # carrissimis
            "Asprfnomsg": self._spr_stem + "a",  # carrissima
            "Asprfvocsg": self._spr_stem + "a",  # carrissima
            "Asprfaccsg": self._spr_stem + "am",  # carrissimam
            "Asprfgensg": self._spr_stem + "ae",  # carrissimae
            "Asprfdatsg": self._spr_stem + "ae",  # crrissimae
            "Asprfablsg": self._spr_stem + "a",  # carrissima
            "Asprfnompl": self._spr_stem + "ae",  # carrissimae
            "Asprfvocpl": self._spr_stem + "ae",  # carrissimae
            "Asprfaccpl": self._spr_stem + "as",  # carrissimas
            "Asprfgenpl": self._spr_stem + "arum",  # carrissimarum
            "Asprfdatpl": self._spr_stem + "is",  # carrissimis
            "Asprfablpl": self._spr_stem + "is",  # carrissimis
            "Asprnnomsg": self._spr_stem + "um",  # carrissimum
            "Asprnvocsg": self._spr_stem + "um",  # carrissimum
            "Asprnaccsg": self._spr_stem + "um",  # carrissimum
            "Asprngensg": self._spr_stem + "i",  # carrissimi
            "Asprndatsg": self._spr_stem + "o",  # carrissimo
            "Asprnablsg": self._spr_stem + "o",  # carrissimo
            "Asprnnompl": self._spr_stem + "a",  # carrissima
            "Asprnvocpl": self._spr_stem + "a",  # carrissima
            "Asprnaccpl": self._spr_stem + "a",  # carrissima
            "Asprngenpl": self._spr_stem + "orum",  # carrissimorum
            "Asprndatpl": self._spr_stem + "is",  # carrissimis
            "Asprnablpl": self._spr_stem + "is",  # carrissimis
        }

        if self.adverb_flag:
            endings |= {
                "Dpos": (
                    self._irregular_posadv
                    if self.irregular_flag
                    else self._pos_stem + "e"
                )  # laete
            }

            if endings["Dpos"] not in UNCOMPARABLE_ADVERBS:
                endings |= {
                    "Dcmp": (
                        self._irregular_cmpadv
                        if self.irregular_flag
                        else self._pos_stem + "ius"
                    ),  # laetius
                    "Dspr": (
                        self._irregular_spradv
                        if self.irregular_flag
                        else self._spr_stem + "e"
                    ),  # laetissime
                }

        if self.plurale_tantum:
            endings = {
                k: v for k, v in endings.items() if not k.endswith("sg")
            }

        return endings

    def _31_endings(self) -> Endings:
        if len(self.principal_parts) != 2:
            raise InvalidInputError(
                "First-termination adjectives must have 2 principal parts. "
                f"(adjective '{self._first}' given)"
            )

        self.mascgen = self.principal_parts[1]

        if self.mascnom.endswith("es") and self.mascgen.endswith("ium"):
            self.plurale_tantum = True
            self._pos_stem = self.mascgen[:-3]  # novensidium -> novensid-
        elif (
            self.mascnom not in IRREGULAR_PP_ADJECTIVES
            and not self.mascgen.endswith("is")
        ):
            raise InvalidInputError(
                f"Invalid genitive form: '{self.mascgen}' (must end in '-is')"
            )
        else:
            self._pos_stem = self.mascgen[:-2]  # ingentis -> ingent-

        if not self.irregular_flag:
            self._cmp_stem = self._pos_stem + "ior"  # ingent- > ingentior-
            if self.mascnom.endswith("er"):
                self._spr_stem = self.mascnom + "rim"  # miser- -> miserrim-
            elif self.mascnom in LIS_ADJECTIVES:
                self._spr_stem = self._pos_stem + "lim"  # facil- -> facillim-
            else:
                self._spr_stem = (
                    self._pos_stem + "issim"  # ingent- -> ingentissim-
                )

        endings: Endings = {
            "Aposmnomsg": self.mascnom,  # ingens
            "Aposmvocsg": self.mascnom,  # ingens
            "Aposmaccsg": self._pos_stem + "em",  # ingentem
            "Aposmgensg": self.mascgen,  # ingentis
            "Aposmdatsg": self._pos_stem + "i",  # ingenti
            "Aposmablsg": self._pos_stem + "i",  # ingenti
            "Aposmnompl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # ingentes
            "Aposmvocpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # ingentes
            "Aposmaccpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # ingentes
            "Aposmgenpl": self._pos_stem
            + "ium",  # ingentium # even if plural only, _pos_stem is derived from the genitive anyway
            "Aposmdatpl": self._pos_stem + "ibus",  # ingentibus
            "Aposmablpl": self._pos_stem + "ibus",  # ingentibus
            "Aposfnomsg": self.mascnom,  # ingens
            "Aposfvocsg": self.mascnom,  # ingens
            "Aposfaccsg": self._pos_stem + "em",  # ingentem
            "Aposfgensg": self.mascgen,  # ingentis
            "Aposfdatsg": self._pos_stem + "i",  # ingenti
            "Aposfablsg": self._pos_stem + "i",  # ingenti
            "Aposfnompl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # ingentes
            "Aposfvocpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # ingentes
            "Aposfaccpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # ingentes
            "Aposfgenpl": self._pos_stem + "ium",  # ingentium
            "Aposfdatpl": self._pos_stem + "ibus",  # ingentibus
            "Aposfablpl": self._pos_stem + "ibus",  # ingentibus
            "Aposnnomsg": self.mascnom,  # ingens
            "Aposnvocsg": self.mascnom,  # ingens
            "Aposnaccsg": self.mascnom,  # ingens
            "Aposngensg": self.mascgen,  # ingentis
            "Aposndatsg": self._pos_stem + "i",  # ingenti
            "Aposnablsg": self._pos_stem + "i",  # ingenti
            "Aposnnompl": self._pos_stem + "ia",  # ingentia
            "Aposnvocpl": self._pos_stem + "ia",  # ingentia
            "Aposnaccpl": self._pos_stem + "ia",  # ingentia
            "Aposngenpl": self._pos_stem + "ium",  # ingentium
            "Aposndatpl": self._pos_stem + "ibus",  # ingentibus
            "Aposnablpl": self._pos_stem + "ibus",  # ingentibus
            "Acmpmnomsg": self._cmp_stem,  # ingentior
            "Acmpmvocsg": self._cmp_stem,  # ingentior
            "Acmpmaccsg": self._cmp_stem + "em",  # ingentiorem
            "Acmpmgensg": self._cmp_stem + "is",  # ingentioris
            "Acmpmdatsg": self._cmp_stem + "i",  # ingentiori
            "Acmpmablsg": self._cmp_stem + "e",  # ingentiore
            "Acmpmnompl": self._cmp_stem + "es",  # ingentiores
            "Acmpmvocpl": self._cmp_stem + "es",  # ingentiores
            "Acmpmaccpl": self._cmp_stem + "es",  # ingentiores
            "Acmpmgenpl": self._cmp_stem + "um",  # ingentiorum
            "Acmpmdatpl": self._cmp_stem + "ibus",  # ingentioribus
            "Acmpmablpl": self._cmp_stem + "ibus",  # ingentioribus
            "Acmpfnomsg": self._cmp_stem,  # ingentior
            "Acmpfvocsg": self._cmp_stem,  # ingentior
            "Acmpfaccsg": self._cmp_stem + "em",  # ingentiorem
            "Acmpfgensg": self._cmp_stem + "is",  # ingentioris
            "Acmpfdatsg": self._cmp_stem + "i",  # ingentiori
            "Acmpfablsg": self._cmp_stem + "e",  # ingentiore
            "Acmpfnompl": self._cmp_stem + "es",  # ingentiores
            "Acmpfvocpl": self._cmp_stem + "es",  # ingentiores
            "Acmpfaccpl": self._cmp_stem + "es",  # ingentiores
            "Acmpfgenpl": self._cmp_stem + "um",  # ingentiorum
            "Acmpfdatpl": self._cmp_stem + "ibus",  # ingentioribus
            "Acmpfablpl": self._cmp_stem + "ibus",  # ingentioribus
            "Acmpnnomsg": self._cmp_stem[:-3] + "ius",  # ingentius
            "Acmpnvocsg": self._cmp_stem[:-3] + "ius",  # ingentius
            "Acmpnaccsg": self._cmp_stem[:-3] + "ius",  # ingentius
            "Acmpngensg": self._cmp_stem + "is",  # ingentioris
            "Acmpndatsg": self._cmp_stem + "i",  # ingentiori
            "Acmpnablsg": self._cmp_stem + "e",  # ingentiore
            "Acmpnnompl": self._cmp_stem + "a",  # ingentiora
            "Acmpnvocpl": self._cmp_stem + "a",  # ingentiora
            "Acmpnaccpl": self._cmp_stem + "a",  # ingentiora
            "Acmpngenpl": self._cmp_stem + "um",  # ingentiorum
            "Acmpndatpl": self._cmp_stem + "ibus",  # ingentioribus
            "Acmpnablpl": self._cmp_stem + "ibus",  # ingentioribus
            "Asprmnomsg": self._spr_stem + "us",  # ingentissimus
            "Asprmvocsg": self._spr_stem + "e",  # ingentissime
            "Asprmaccsg": self._spr_stem + "um",  # ingentissimum
            "Asprmgensg": self._spr_stem + "i",  # ingentissimi
            "Asprmdatsg": self._spr_stem + "o",  # ingentissimo
            "Asprmablsg": self._spr_stem + "o",  # ingentissimo
            "Asprmnompl": self._spr_stem + "i",  # ingentissimi
            "Asprmvocpl": self._spr_stem + "i",  # ingentissimi
            "Asprmaccpl": self._spr_stem + "os",  # ingentissimos
            "Asprmgenpl": self._spr_stem + "orum",  # ingentissimorum
            "Asprmdatpl": self._spr_stem + "is",  # ingentissimis
            "Asprmablpl": self._spr_stem + "is",  # ingentissimis
            "Asprfnomsg": self._spr_stem + "a",  # ingentissima
            "Asprfvocsg": self._spr_stem + "a",  # ingentissima
            "Asprfaccsg": self._spr_stem + "am",  # ingentissimam
            "Asprfgensg": self._spr_stem + "ae",  # ingentissimae
            "Asprfdatsg": self._spr_stem + "ae",  # ingentissimae
            "Asprfablsg": self._spr_stem + "a",  # ingentissima
            "Asprfnompl": self._spr_stem + "ae",  # ingentissimae
            "Asprfvocpl": self._spr_stem + "ae",  # ingentissimae
            "Asprfaccpl": self._spr_stem + "as",  # ingentissimas
            "Asprfgenpl": self._spr_stem + "arum",  # ingentissimarum
            "Asprfdatpl": self._spr_stem + "is",  # ingentissimis
            "Asprfablpl": self._spr_stem + "is",  # ingentissimis
            "Asprnnomsg": self._spr_stem + "um",  # ingentissimum
            "Asprnvocsg": self._spr_stem + "um",  # ingentissimum
            "Asprnaccsg": self._spr_stem + "um",  # ingentissimum
            "Asprngensg": self._spr_stem + "i",  # ingentissimi
            "Asprndatsg": self._spr_stem + "o",  # ingentissimo
            "Asprnablsg": self._spr_stem + "o",  # ingentissimo
            "Asprnnompl": self._spr_stem + "a",  # ingentissima
            "Asprnvocpl": self._spr_stem + "a",  # ingentissima
            "Asprnaccpl": self._spr_stem + "a",  # ingentissima
            "Asprngenpl": self._spr_stem + "orum",  # ingentissimorum
            "Asprndatpl": self._spr_stem + "is",  # ingentissimis
            "Asprnablpl": self._spr_stem + "is",  # ingentissimis
        }

        if self.adverb_flag:
            endings |= {
                "Dpos": (
                    self._irregular_posadv
                    if self.irregular_flag
                    else self._pos_stem + "er"
                )  # atrociter
            }

            if endings["Dpos"] not in UNCOMPARABLE_ADVERBS:
                endings |= {
                    "Dcmp": (
                        self._irregular_cmpadv
                        if self.irregular_flag
                        else self._pos_stem + "ius"
                    ),  # atrocius
                    "Dspr": (
                        self._irregular_spradv
                        if self.irregular_flag
                        else self._spr_stem + "e"
                    ),  # atrocissime
                }

        if self.plurale_tantum:
            endings = {
                k: v for k, v in endings.items() if not k.endswith("sg")
            }

        return endings

    def _32_endings(self) -> Endings:
        if len(self.principal_parts) != 2:
            raise InvalidInputError(
                "Second-termination adjectives must have 2 principal parts. "
                f"(adjective '{self._first}' given)"
            )

        self.neutnom = self.principal_parts[1]

        if self.mascnom.endswith("es") and self.neutnom.endswith("a"):
            # same _pos_stem (remove last 2 chars from nominative)
            self.plurale_tantum = True
        elif self.mascnom not in IRREGULAR_PP_ADJECTIVES:
            if not self.mascnom.endswith("is"):
                raise InvalidInputError(
                    f"Invalid masculine form: '{self.mascnom}' (must end in '-is')"
                )
            if not self.neutnom.endswith("e"):
                raise InvalidInputError(
                    f"Invalid neuter form: '{self.neutnom}' (must end in '-e')"
                )

        self._pos_stem = self.mascnom[:-2]  # fortis -> fort-
        if not self.irregular_flag:
            self._cmp_stem = self._pos_stem + "ior"  # fort- -> fortior-
            if self.mascnom.endswith("er"):
                self._spr_stem = self.mascnom + "rim"  # miser- -> miserrim-
            elif self.mascnom in LIS_ADJECTIVES:
                self._spr_stem = self._pos_stem + "lim"  # facil- -> facillim-
            else:
                self._spr_stem = (
                    self._pos_stem + "issim"  # fort- -> fortissim-
                )

        endings: Endings = {
            "Aposmnomsg": self.mascnom,  # fortis
            "Aposmvocsg": self.mascnom,  # fortis
            "Aposmaccsg": self._pos_stem + "em",  # fortem
            "Aposmgensg": self._pos_stem + "is",  # fortis
            "Aposmdatsg": self._pos_stem + "i",  # forti
            "Aposmablsg": self._pos_stem + "i",  # forti
            "Aposmnompl": self._pos_stem
            + "es",  # fortes # even if plural only, _pos_stem is derived from the masculine anyway
            "Aposmvocpl": self._pos_stem + "es",  # fortes
            "Aposmaccpl": self._pos_stem + "es",  # fortes
            "Aposmgenpl": self._pos_stem + "ium",  # fortium
            "Aposmdatpl": self._pos_stem + "ibus",  # fortibus
            "Aposmablpl": self._pos_stem + "ibus",  # fortibus
            "Aposfnomsg": self.mascnom,  # fortis
            "Aposfvocsg": self.mascnom,  # fortis
            "Aposfaccsg": self._pos_stem + "em",  # fortem
            "Aposfgensg": self._pos_stem + "is",  # fortis
            "Aposfdatsg": self._pos_stem + "i",  # forti
            "Aposfablsg": self._pos_stem + "i",  # forti
            "Aposfnompl": self._pos_stem + "es",  # fortes
            "Aposfvocpl": self._pos_stem + "es",  # fortes
            "Aposfaccpl": self._pos_stem + "es",  # fortes
            "Aposfgenpl": self._pos_stem + "ium",  # fortium
            "Aposfdatpl": self._pos_stem + "ibus",  # fortibus
            "Aposfablpl": self._pos_stem + "ibus",  # fortibus
            "Aposnnomsg": self.neutnom,  # forte
            "Aposnvocsg": self.neutnom,  # forte
            "Aposnaccsg": self.neutnom,  # forte
            "Aposngensg": self._pos_stem + "is",  # fortis
            "Aposndatsg": self._pos_stem + "i",  # fortibus
            "Aposnablsg": self._pos_stem + "i",  # fortibus
            "Aposnnompl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "ia",  # fortia
            "Aposnvocpl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "ia",  # fortia
            "Aposnaccpl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "ia",  # fortia
            "Aposngenpl": self._pos_stem + "ium",  # fortium
            "Aposndatpl": self._pos_stem + "ibus",  # fortibus
            "Aposnablpl": self._pos_stem + "ibus",  # fortibus
            "Acmpmnomsg": self._cmp_stem,  # fortior
            "Acmpmvocsg": self._cmp_stem,  # fortior
            "Acmpmaccsg": self._cmp_stem + "em",  # fortiorem
            "Acmpmgensg": self._cmp_stem + "is",  # fortioris
            "Acmpmdatsg": self._cmp_stem + "i",  # fortiori
            "Acmpmablsg": self._cmp_stem + "e",  # fortiore
            "Acmpmnompl": self._cmp_stem + "es",  # fortiores
            "Acmpmvocpl": self._cmp_stem + "es",  # fortiores
            "Acmpmaccpl": self._cmp_stem + "es",  # fortiores
            "Acmpmgenpl": self._cmp_stem + "um",  # fortiorum
            "Acmpmdatpl": self._cmp_stem + "ibus",  # fortioribus
            "Acmpmablpl": self._cmp_stem + "ibus",  # fortioribus
            "Acmpfnomsg": self._cmp_stem,  # fortior
            "Acmpfvocsg": self._cmp_stem,  # fortior
            "Acmpfaccsg": self._cmp_stem + "em",  # fortiorem
            "Acmpfgensg": self._cmp_stem + "is",  # fortioris
            "Acmpfdatsg": self._cmp_stem + "i",  # fortiori
            "Acmpfablsg": self._cmp_stem + "e",  # fortiore
            "Acmpfnompl": self._cmp_stem + "es",  # fortiores
            "Acmpfvocpl": self._cmp_stem + "es",  # fortiores
            "Acmpfaccpl": self._cmp_stem + "es",  # fortiores
            "Acmpfgenpl": self._cmp_stem + "um",  # fortiorum
            "Acmpfdatpl": self._cmp_stem + "ibus",  # fortioribus
            "Acmpfablpl": self._cmp_stem + "ibus",  # fortioribus
            "Acmpnnomsg": self._cmp_stem[:-3] + "ius",  # fortius
            "Acmpnvocsg": self._cmp_stem[:-3] + "ius",  # fortius
            "Acmpnaccsg": self._cmp_stem[:-3] + "ius",  # fortius
            "Acmpngensg": self._cmp_stem + "is",  # fortioris
            "Acmpndatsg": self._cmp_stem + "i",  # fortiori
            "Acmpnablsg": self._cmp_stem + "e",  # fortiore
            "Acmpnnompl": self._cmp_stem + "a",  # fortiora
            "Acmpnvocpl": self._cmp_stem + "a",  # fortiora
            "Acmpnaccpl": self._cmp_stem + "a",  # fortiora
            "Acmpngenpl": self._cmp_stem + "um",  # fortiorum
            "Acmpndatpl": self._cmp_stem + "ibus",  # fortioribus
            "Acmpnablpl": self._cmp_stem + "ibus",  # fortioribus
            "Asprmnomsg": self._spr_stem + "us",  # fortissimus
            "Asprmvocsg": self._spr_stem + "e",  # fortissime
            "Asprmaccsg": self._spr_stem + "um",  # fortissimum
            "Asprmgensg": self._spr_stem + "i",  # fortissimi
            "Asprmdatsg": self._spr_stem + "o",  # fortissimo
            "Asprmablsg": self._spr_stem + "o",  # fortissimo
            "Asprmnompl": self._spr_stem + "i",  # fortissimi
            "Asprmvocpl": self._spr_stem + "i",  # fortissimi
            "Asprmaccpl": self._spr_stem + "os",  # fortissimi
            "Asprmgenpl": self._spr_stem + "orum",  # fortissimorum
            "Asprmdatpl": self._spr_stem + "is",  # fortissimis
            "Asprmablpl": self._spr_stem + "is",  # fortissimis
            "Asprfnomsg": self._spr_stem + "a",  # fortissima
            "Asprfvocsg": self._spr_stem + "a",  # fortissima
            "Asprfaccsg": self._spr_stem + "am",  # fortissimam
            "Asprfgensg": self._spr_stem + "ae",  # fortissimae
            "Asprfdatsg": self._spr_stem + "ae",  # fortissimae
            "Asprfablsg": self._spr_stem + "a",  # fortissima
            "Asprfnompl": self._spr_stem + "ae",  # fortissimae
            "Asprfvocpl": self._spr_stem + "ae",  # fortissimae
            "Asprfaccpl": self._spr_stem + "as",  # fortissimas
            "Asprfgenpl": self._spr_stem + "arum",  # fortissimarum
            "Asprfdatpl": self._spr_stem + "is",  # fortissimis
            "Asprfablpl": self._spr_stem + "is",  # fortissimis
            "Asprnnomsg": self._spr_stem + "um",  # fortissimum
            "Asprnvocsg": self._spr_stem + "um",  # fortissimum
            "Asprnaccsg": self._spr_stem + "um",  # fortissimum
            "Asprngensg": self._spr_stem + "i",  # fortissimi
            "Asprndatsg": self._spr_stem + "o",  # fortissimo
            "Asprnablsg": self._spr_stem + "o",  # fortissimo
            "Asprnnompl": self._spr_stem + "a",  # fortissima
            "Asprnvocpl": self._spr_stem + "a",  # fortissima
            "Asprnaccpl": self._spr_stem + "a",  # fortissima
            "Asprngenpl": self._spr_stem + "orum",  # fortissimorum
            "Asprndatpl": self._spr_stem + "is",  # fortissimis
            "Asprnablpl": self._spr_stem + "is",  # fortissimis
        }

        if self.adverb_flag:
            endings |= {
                "Dpos": (
                    self._irregular_posadv
                    if self.irregular_flag
                    else self._pos_stem + "iter"
                )  # fortiter
            }

            if endings["Dpos"] not in UNCOMPARABLE_ADVERBS:
                endings |= {
                    "Dcmp": (
                        self._irregular_cmpadv
                        if self.irregular_flag
                        else self._pos_stem + "ius"
                    ),  # fortius
                    "Dspr": (
                        self._irregular_spradv
                        if self.irregular_flag
                        else self._spr_stem + "e"
                    ),  # fortissime
                }

        if self.plurale_tantum:
            endings = {
                k: v for k, v in endings.items() if not k.endswith("sg")
            }

        return endings

    def _33_endings(self) -> Endings:
        if len(self.principal_parts) != 3:
            raise InvalidInputError(
                "Third-termination adjectives must have 3 principal parts. "
                f"(adjective '{self._first}' given)"
            )

        self.mascnom = self.principal_parts[0]
        self.femnom = self.principal_parts[1]
        self.neutnom = self.principal_parts[2]

        if (
            self.mascnom.endswith("es")
            and self.femnom.endswith("es")
            and self.neutnom.endswith("a")
        ):
            # same _pos_stem (remove last 2 chars from feminine)
            self.plurale_tantum = True

        elif self.mascnom not in IRREGULAR_PP_ADJECTIVES:
            if not self.mascnom.endswith("er"):
                raise InvalidInputError(
                    f"Invalid masculine form: '{self.mascnom}' (must end in '-er')"
                )
            if not self.femnom.endswith("is"):
                raise InvalidInputError(
                    f"Invalid feminine form: '{self.femnom}' (must end in '-is')"
                )
            if not self.neutnom.endswith("e"):
                raise InvalidInputError(
                    f"Invalid neuter form: '{self.neutnom}' (must end in '-e')"
                )

        self._pos_stem = self.femnom[:-2]  # acris -> acr-
        if not self.irregular_flag:
            self._cmp_stem = self._pos_stem + "ior"  # acr- -> acrior-
            if self.mascnom.endswith("er"):
                self._spr_stem = self.mascnom + "rim"  # acer- -> acerrim-
            elif self.mascnom in LIS_ADJECTIVES:
                self._spr_stem = self._pos_stem + "lim"  # facil- -> facillim-
            else:
                self._spr_stem = self._pos_stem + "issim"  # levis -> levissim-

        endings: Endings = {
            "Aposmnomsg": self.mascnom,  # acer
            "Aposmvocsg": self.mascnom,  # acer
            "Aposmaccsg": self._pos_stem + "em",  # acrem
            "Aposmgensg": self._pos_stem + "is",  # acris
            "Aposmdatsg": self._pos_stem + "i",  # acri
            "Aposmablsg": self._pos_stem + "i",  # acri
            "Aposmnompl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # acres
            "Aposmvocpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # acres
            "Aposmaccpl": self.mascnom
            if self.plurale_tantum
            else self._pos_stem + "es",  # acres
            "Aposmgenpl": self._pos_stem + "ium",  # acrium
            "Aposmdatpl": self._pos_stem + "ibus",  # acribus
            "Aposmablpl": self._pos_stem + "ibus",  # acribus
            "Aposfnomsg": self.femnom,  # acris
            "Aposfvocsg": self.femnom,  # acris
            "Aposfaccsg": self._pos_stem + "em",  # acrem
            "Aposfgensg": self._pos_stem + "is",  # acris
            "Aposfdatsg": self._pos_stem + "i",  # acri
            "Aposfablsg": self._pos_stem + "i",  # acri
            "Aposfnompl": self._pos_stem
            + "es",  # acres # even if plural only, _pos_stem is derived from the feminine anyway
            "Aposfvocpl": self._pos_stem + "es",  # acres
            "Aposfaccpl": self._pos_stem + "es",  # acres
            "Aposfgenpl": self._pos_stem + "ium",  # acrium
            "Aposfdatpl": self._pos_stem + "ibus",  # acribus
            "Aposfablpl": self._pos_stem + "ibus",  # acribus
            "Aposnnomsg": self.neutnom,  # acre
            "Aposnvocsg": self.neutnom,  # acre
            "Aposnaccsg": self.neutnom,  # acre
            "Aposngensg": self._pos_stem + "is",  # acris
            "Aposndatsg": self._pos_stem + "i",  # acri
            "Aposnablsg": self._pos_stem + "i",  # acri
            "Aposnnompl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "ia",  # acria
            "Aposnvocpl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "ia",  # acria
            "Aposnaccpl": self.neutnom
            if self.plurale_tantum
            else self._pos_stem + "ia",  # acria
            "Aposngenpl": self._pos_stem + "ium",  # acrium
            "Aposndatpl": self._pos_stem + "ibus",  # acribus
            "Aposnablpl": self._pos_stem + "ibus",  # acribus
            "Acmpmnomsg": self._cmp_stem,  # acrior
            "Acmpmvocsg": self._cmp_stem,  # acrior
            "Acmpmaccsg": self._cmp_stem + "em",  # acriorem
            "Acmpmgensg": self._cmp_stem + "is",  # acrioris
            "Acmpmdatsg": self._cmp_stem + "i",  # acriori
            "Acmpmablsg": self._cmp_stem + "e",  # acriore
            "Acmpmnompl": self._cmp_stem + "es",  # acriores
            "Acmpmvocpl": self._cmp_stem + "es",  # acriores
            "Acmpmaccpl": self._cmp_stem + "es",  # acriores
            "Acmpmgenpl": self._cmp_stem + "um",  # acriorum
            "Acmpmdatpl": self._cmp_stem + "ibus",  # acrioribus
            "Acmpmablpl": self._cmp_stem + "ibus",  # acrioribus
            "Acmpfnomsg": self._cmp_stem,  # acrior
            "Acmpfvocsg": self._cmp_stem,  # acrior
            "Acmpfaccsg": self._cmp_stem + "em",  # acriorem
            "Acmpfgensg": self._cmp_stem + "is",  # acrioris
            "Acmpfdatsg": self._cmp_stem + "i",  # acriori
            "Acmpfablsg": self._cmp_stem + "e",  # acriore
            "Acmpfnompl": self._cmp_stem + "es",  # acriores
            "Acmpfvocpl": self._cmp_stem + "es",  # acriores
            "Acmpfaccpl": self._cmp_stem + "es",  # acriores
            "Acmpfgenpl": self._cmp_stem + "um",  # acriorum
            "Acmpfdatpl": self._cmp_stem + "ibus",  # acrioribus
            "Acmpfablpl": self._cmp_stem + "ibus",  # acrioribus
            "Acmpnnomsg": self._cmp_stem[:-3] + "ius",  # acrius
            "Acmpnvocsg": self._cmp_stem[:-3] + "ius",  # acrius
            "Acmpnaccsg": self._cmp_stem[:-3] + "ius",  # acrius
            "Acmpngensg": self._cmp_stem + "is",  # acrioris
            "Acmpndatsg": self._cmp_stem + "i",  # acriori
            "Acmpnablsg": self._cmp_stem + "e",  # acriore
            "Acmpnnompl": self._cmp_stem + "a",  # acriora
            "Acmpnvocpl": self._cmp_stem + "a",  # acriora
            "Acmpnaccpl": self._cmp_stem + "a",  # acriora
            "Acmpngenpl": self._cmp_stem + "um",  # acriorum
            "Acmpndatpl": self._cmp_stem + "ibus",  # acrioribus
            "Acmpnablpl": self._cmp_stem + "ibus",  # acrioribus
            "Asprmnomsg": self._spr_stem + "us",  # acerrimus
            "Asprmvocsg": self._spr_stem + "e",  # acerrime
            "Asprmaccsg": self._spr_stem + "um",  # acerrimum
            "Asprmgensg": self._spr_stem + "i",  # acerrimi
            "Asprmdatsg": self._spr_stem + "o",  # acerrimo
            "Asprmablsg": self._spr_stem + "o",  # acerrimo
            "Asprmnompl": self._spr_stem + "i",  # acerrimi
            "Asprmvocpl": self._spr_stem + "i",  # acerrimi
            "Asprmaccpl": self._spr_stem + "os",  # acerrimos
            "Asprmgenpl": self._spr_stem + "orum",  # acerrimorum
            "Asprmdatpl": self._spr_stem + "is",  # acerrimis
            "Asprmablpl": self._spr_stem + "is",  # acerrimis
            "Asprfnomsg": self._spr_stem + "a",  # acerrima
            "Asprfvocsg": self._spr_stem + "a",  # acerrima
            "Asprfaccsg": self._spr_stem + "am",  # acerrimam
            "Asprfgensg": self._spr_stem + "ae",  # acerrimae
            "Asprfdatsg": self._spr_stem + "ae",  # crrissimae
            "Asprfablsg": self._spr_stem + "a",  # acerrima
            "Asprfnompl": self._spr_stem + "ae",  # acerrimae
            "Asprfvocpl": self._spr_stem + "ae",  # acerrimae
            "Asprfaccpl": self._spr_stem + "as",  # acerrimas
            "Asprfgenpl": self._spr_stem + "arum",  # acerrimarum
            "Asprfdatpl": self._spr_stem + "is",  # acerrimis
            "Asprfablpl": self._spr_stem + "is",  # acerrimis
            "Asprnnomsg": self._spr_stem + "um",  # acerrimum
            "Asprnvocsg": self._spr_stem + "um",  # acerrimum
            "Asprnaccsg": self._spr_stem + "um",  # acerrimum
            "Asprngensg": self._spr_stem + "i",  # acerrimi
            "Asprndatsg": self._spr_stem + "o",  # acerrimo
            "Asprnablsg": self._spr_stem + "o",  # acerrimo
            "Asprnnompl": self._spr_stem + "a",  # acerrima
            "Asprnvocpl": self._spr_stem + "a",  # acerrima
            "Asprnaccpl": self._spr_stem + "a",  # acerrima
            "Asprngenpl": self._spr_stem + "orum",  # acerrimorum
            "Asprndatpl": self._spr_stem + "is",  # acerrimis
            "Asprnablpl": self._spr_stem + "is",  # acerrimis
        }

        if self.adverb_flag:
            endings |= {
                "Dpos": (
                    self._irregular_posadv
                    if self.irregular_flag
                    else self._pos_stem + "iter"
                )  # acriter
            }

            if endings["Dpos"] not in UNCOMPARABLE_ADVERBS:
                endings |= {
                    "Dcmp": (
                        self._irregular_cmpadv
                        if self.irregular_flag
                        else self._pos_stem + "ius"
                    ),  # acrius
                    "Dspr": (
                        self._irregular_spradv
                        if self.irregular_flag
                        else self._spr_stem + "e"
                    ),  # acerrime
                }

        if self.plurale_tantum:
            endings = {
                k: v for k, v in endings.items() if not k.endswith("sg")
            }

        return endings

    # fmt: off
    @overload
    def get(self, *, degree: Degree, adverb: Literal[True]) -> Ending | None: ...
    @overload
    def get(self, *, degree: Degree, gender: Gender, case: Case, number: Number, adverb: Literal[False] = False) -> Ending | None: ...
    # fmt: on

    def get(
        self,
        *,
        degree: Degree,
        case: Case | None = None,
        number: Number | None = None,
        gender: Gender | None = None,
        adverb: bool = False,
    ) -> Ending | None:
        """Return the ending of the adjective from the grammatical components.

        The function returns ``None`` if no ending is found.

        Parameters
        ----------
        degree : Degree
            The degree of the adjective.
        case : Case | None
            The case of the ending, if applicable (not an adverb).
            Default is None.
        number : Number | None
            The number of the ending, if applicable (not an adverb).
            Default is None.
        gender : Gender | None
            The gender of the ending, if applicable (not an adverb).
            Default is None.
        adverb : bool
            Whether the queried ending is an adverb or not. Defaults to
            False.

        Returns
        -------
        Ending | None
            The ending found, or ``None`` if no ending is found.

        Examples
        --------
        >>> foo = Adjective(
        ...     "egens", "egentis", termination=1, declension="3", meaning="poor"
        ... )
        >>> foo.get(
        ...     degree=Degree.POSITIVE,
        ...     case=Case.NOMINATIVE,
        ...     number=Number.SINGULAR,
        ...     gender=Gender.MASCULINE,
        ... )
        'egens'

        Note that the arguments of ``get()`` are keyword-only.
        """
        logger.debug(
            "%s.get(%s, %s, %s, %s, adverb=%s)",
            self._first,
            degree,
            gender,
            case,
            number,
            adverb,
        )

        if adverb:
            short_degree = degree.shorthand
            return self.endings.get(f"D{short_degree}")

        assert gender is not None
        assert case is not None
        assert number is not None

        short_degree = degree.shorthand
        short_gender = gender.shorthand
        short_case = case.shorthand
        short_number = number.shorthand

        return self.endings.get(
            f"A{short_degree}{short_gender}{short_case}{short_number}"
        )

    def create_components(self, key: str) -> EndingComponents:  # noqa: PLR6301
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
        if key[0] == "A":
            try:
                output = EndingComponents(
                    degree=Degree(key[1:4]),
                    gender=Gender(key[4]),
                    case=Case(key[5:8]),
                    number=Number(key[8:10]),
                )
            except (ValueError, IndexError) as e:
                raise InvalidInputError(f"Key '{key}' is invalid.") from e

            output.string = (
                f"{output.degree.regular} {output.case.regular} "
                f"{output.number.regular} {output.gender.regular}"
            )

        else:
            output = EndingComponents(degree=Degree(key[1:4]))
            output.string = f"{output.degree.regular} (adverb)"

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

    def __str__(self) -> str:
        if self.declension == "3":
            return (
                f"{self.meaning}: {', '.join(self.principal_parts)}, "
                f"({self.declension}-{self.termination})"
            )

        return f"{self.meaning}: {', '.join(self.principal_parts)}, (2-1-2)"

    def __repr__(self) -> str:
        return (
            f"Adjective({', '.join(self.principal_parts)}, "
            f"termination={self.termination}, "
            f"declension={self.declension}, meaning={self.meaning})"
        )

    def __add__(self, other: object) -> Adjective:
        def _create_adjective(
            principal_parts: tuple[str, ...],
            declension: AdjectiveDeclension,
            termination: Termination | None,
            meaning: Meaning,
        ) -> Adjective:
            if declension == "212":
                return Adjective(
                    *principal_parts, declension="212", meaning=meaning
                )

            assert termination is not None

            return Adjective(
                *principal_parts,
                termination=termination,
                declension="3",
                meaning=meaning,
            )

        if not isinstance(other, Adjective) or not (
            self.endings == other.endings
            and self.termination == other.termination
            and self.irregular_flag == other.irregular_flag
            and self.declension == other.declension
            and self.principal_parts == other.principal_parts
            and self.plurale_tantum == other.plurale_tantum
        ):
            return NotImplemented

        if self.meaning == other.meaning:
            return _create_adjective(
                self.principal_parts,
                self.declension,
                self.termination,
                self.meaning,
            )

        if isinstance(self.meaning, MultipleMeanings) or isinstance(
            other.meaning, MultipleMeanings
        ):
            new_meaning = self.meaning + other.meaning
        else:
            new_meaning = MultipleMeanings((self.meaning, other.meaning))

        return _create_adjective(
            self.principal_parts,
            self.declension,
            self.termination,
            new_meaning,
        )

    def __getattribute__(self, name: str) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        if name == "_principal_parts":
            warnings.warn(
                "_principal_parts is deprecated, use principal_parts instead",
                category=DeprecationWarning,
                stacklevel=2,
            )
        return super().__getattribute__(name)  # pyright: ignore[reportAny]

    def __setattr__(self, name: str, value: Any) -> None:  # pyright: ignore[reportExplicitAny, reportAny]
        if name == "_principal_parts":
            warnings.warn(
                "_principal_parts is deprecated, use principal_parts instead",
                category=DeprecationWarning,
                stacklevel=2,
            )
            # keep in sync with principal_parts
            super().__setattr__("principal_parts", value)
        super().__setattr__(name, value)
