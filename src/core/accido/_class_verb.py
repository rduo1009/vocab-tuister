"""Representation of a Latin verb with endings."""

from __future__ import annotations

import logging
from functools import total_ordering
from typing import TYPE_CHECKING, Literal, overload
from warnings import deprecated

from ._class_word import _Word
from .edge_cases import (
    MISSING_PPP_VERBS,
    check_mixed_conjugation_verb,
    find_irregular_endings,
)
from .exceptions import InvalidInputError
from .misc import (
    PERSON_SHORTHAND,
    Case,
    EndingComponents,
    Gender,
    Mood,
    MultipleEndings,
    MultipleMeanings,
    Number,
    Tense,
    Voice,
)
from .type_aliases import is_person

if TYPE_CHECKING:
    from .type_aliases import Conjugation, Ending, Endings, Meaning, Person

logger = logging.getLogger(__name__)


@total_ordering
class Verb(_Word):
    """Representation of a Latin verb with endings.

    Attributes
    ----------
    present : str
    infinitive : str
    perfect : str
        The infinitive and perfect forms, if the verb is not irregular.
        ``None`` if not applicable.
    ppp : str | None
        The perfect passive participle form, if the verb is not
        irregular or deponent. ``None`` if not applicable.
    meaning : Meaning
    conjugation : Conjugation
        The conjugation of the verb. The value 5 represents mixed
        conjugation verbs, and the value 0 represents an irregular
        conjugation.
    endings : Endings

    Examples
    --------
    >>> foo = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
    >>> foo["Vpreactindsg1"]
    'celo'

    Note that all arguments of ``Verb`` are keyword-only.
    """

    __slots__ = (
        "_inf_stem",
        "_per_stem",
        "_ppp_stem",
        "_pre_stem",
        "_preptc_stem",
        "conjugation",
        "deponent",
        "infinitive",
        "no_ppp",
        "perfect",
        "ppp",
        "present",
    )

    # fmt: off
    @overload
    def __init__(self, present: str, *, meaning: Meaning) -> None: ...
    @overload
    def __init__(self, present: str, infinitive: str, *, meaning: Meaning) -> None: ...
    @overload
    def __init__(self, present: str, infinitive: str, perfect: str, *, meaning: Meaning) -> None: ...
    @overload
    def __init__(self, present: str, infinitive: str, perfect: str, ppp: str, *, meaning: Meaning) -> None: ...
    # fmt: on

    def __init__(  # noqa: PLR0915
        self,
        present: str,
        infinitive: str | None = None,
        perfect: str | None = None,
        ppp: str | None = None,
        *,
        meaning: Meaning,
    ) -> None:
        """Initialise ``Verb`` and determine the conjugation and endings.

        Parameters
        ----------
        present : str
        infinitive : str | None
        perfect : str | None
            The infinitive and perfect forms, if the verb is not irregular.
            Defaults to ``None`` if not applicable.
        ppp : str | None
            The perfect passive participle form, if the verb is not
            irregular or deponent. The supine can also be used here, but
            is not supported. Defaults to ``None`` if not applicable.
        meaning : Meaning

        Raises
        ------
        InvalidInputError
            If the input is invalid (incorrect `perfect`, `infinitive`
            or `ppp` values).
        """
        logger.debug(
            "RegularWord(%s, %s, %s, %s, meaning=%s)",
            present,
            infinitive,
            perfect,
            ppp,
            meaning,
        )

        super().__init__()

        (
            self.present,
            self.infinitive,
            self.perfect,
            self.ppp,
            self.meaning,
        ) = (present, infinitive, perfect, ppp, meaning)

        self._first = self.present
        self.deponent = False
        self.no_ppp = False

        # ---------------------------------------------------------------------
        # IRREGULAR VERBS

        if irregular_endings := find_irregular_endings(self.present):
            self.endings = irregular_endings
            self.conjugation: Conjugation = 0
            return

        if self.infinitive is None:
            raise InvalidInputError(
                f"Verb '{self.present}' is not irregular, but no infinitive provided."
            )

        if self.perfect is None:
            raise InvalidInputError(
                f"Verb '{self.present}' is not irregular, but no perfect provided."
            )

        # ---------------------------------------------------------------------
        # DEPONENT VERBS

        if self.present.endswith("or"):
            if self.ppp is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' is deponent, but ppp provided."
                )

            self.deponent = True

            self._inf_stem = self.infinitive[:-3]
            if check_mixed_conjugation_verb(self.present):
                self._inf_stem = self.infinitive[:-1]
                self.conjugation = 5
            elif self.infinitive.endswith("ari"):
                self.conjugation = 1
            elif self.infinitive.endswith("eri"):
                self.conjugation = 2
            elif self.infinitive.endswith("iri"):
                self.conjugation = 4
            elif self.infinitive.endswith("i"):
                self._inf_stem = self.infinitive[:-1]
                self.conjugation = 3
            else:
                raise InvalidInputError(
                    f"Invalid infinitive form: '{self.infinitive}'"
                )

            if self.present in MISSING_PPP_VERBS:
                self.no_ppp = True

                if self.perfect is not None:
                    raise InvalidInputError(
                        f"Verb '{self.present}' has no ppp, but perfect provided."
                    )
            else:
                if not self.perfect.endswith(" sum"):
                    raise InvalidInputError(
                        f"Invalid perfect form: '{self.perfect}' (must have 'sum')"
                    )

                self.ppp = self.perfect[:-4]

            self._pre_stem = self.present[:-2]
            self._per_stem = None

            match self.conjugation:
                case 1:
                    self.endings = self._first_conjugation()

                case 2:
                    self.endings = self._second_conjugation()

                case 3:
                    self.endings = self._third_conjugation()

                case 4:
                    self.endings = self._fourth_conjugation()

                case _:
                    self.endings = self._mixed_conjugation()

            self.endings |= self._participles()

            return

        # ---------------------------------------------------------------------
        # NON-DEPONENT VERBS

        if check_mixed_conjugation_verb(self.present):
            self.conjugation = 5
        elif self.infinitive.endswith("are"):
            self.conjugation = 1
        elif self.infinitive.endswith("ire"):
            self.conjugation = 4
        elif self.infinitive.endswith("ere"):
            self.conjugation = 2 if self.present.endswith("eo") else 3
        else:
            raise InvalidInputError(
                f"Invalid infinitive form: '{self.infinitive}'"
            )

        if not self.present.endswith("o"):
            raise InvalidInputError(
                f"Invalid present form: '{self.present}' (must end in '-o')"
            )

        if not self.perfect.endswith("i"):
            raise InvalidInputError(
                f"Invalid perfect form: '{self.perfect}' (must end in '-i')"
            )

        self._pre_stem = self.present[:-2]
        self._inf_stem = self.infinitive[:-3]
        self._per_stem = self.perfect[:-1]

        if self.present in MISSING_PPP_VERBS:
            self.no_ppp = True

            if self.ppp is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' has no ppp, but ppp provided."
                )
        else:
            if self.ppp is None:
                raise InvalidInputError(
                    f"Verb '{self.present}' is not irregular or deponent, but no ppp provided."
                )

            # HACK: convert supine into ppp, even if the ppp doesn't really
            # exist
            if self.ppp.endswith("um"):
                self.ppp = self.ppp[:-2] + "um"

        match self.conjugation:
            case 1:
                self.endings = self._first_conjugation()

            case 2:
                self.endings = self._second_conjugation()

            case 3:
                self.endings = self._third_conjugation()

            case 4:
                self.endings = self._fourth_conjugation()

            case _:
                self.endings = self._mixed_conjugation()

        self.endings |= self._participles()

    def _first_conjugation(self) -> Endings:
        assert self.infinitive is not None
        assert self.perfect is not None

        # Passive forms
        endings: Endings = {
            "Vprepasindsg1": f"{self._inf_stem}or",  # portor
            "Vprepasindsg2": f"{self._inf_stem}aris",  # portaris
            "Vprepasindsg3": f"{self._inf_stem}atur",  # portatur
            "Vprepasindpl1": f"{self._inf_stem}amur",  # portamur
            "Vprepasindpl2": f"{self._inf_stem}amini",  # portamini
            "Vprepasindpl3": f"{self._inf_stem}antur",  # portantur
            "Vimppasindsg1": f"{self._inf_stem}abar",  # portabar
            "Vimppasindsg2": f"{self._inf_stem}abaris",  # portabaris
            "Vimppasindsg3": f"{self._inf_stem}abatur",  # portabatur
            "Vimppasindpl1": f"{self._inf_stem}abamur",  # portabamur
            "Vimppasindpl2": f"{self._inf_stem}abamini",  # portabamini
            "Vimppasindpl3": f"{self._inf_stem}abantur",  # portabantur
            "Vfutpasindsg1": f"{self._inf_stem}abor",  # portabor
            "Vfutpasindsg2": f"{self._inf_stem}aberis",  # portaberis
            "Vfutpasindsg3": f"{self._inf_stem}abitur",  # portabitur
            "Vfutpasindpl1": f"{self._inf_stem}abimur",  # portabimur
            "Vfutpasindpl2": f"{self._inf_stem}abimini",  # portabimini
            "Vfutpasindpl3": f"{self._inf_stem}abuntur",  # portabuntur
            "Vprepasinf   ": f"{self._inf_stem}ari",  # portari
        }

        if not self.no_ppp:
            assert self.ppp is not None

            endings |= {
                "Vperpasindsg1": f"{self.ppp} sum",  # portatus sum
                "Vperpasindsg2": f"{self.ppp} es",  # portatus es
                "Vperpasindsg3": f"{self.ppp} est",  # portatus est
                "Vperpasindpl1": f"{self.ppp[:-2]}i sumus",  # portati sumus
                "Vperpasindpl2": f"{self.ppp[:-2]}i estis",  # portati estis
                "Vperpasindpl3": f"{self.ppp[:-2]}i sunt",  # portati sunt
                "Vplppasindsg1": f"{self.ppp} eram",  # portatus eram
                "Vplppasindsg2": f"{self.ppp} eras",  # portatus eras
                "Vplppasindsg3": f"{self.ppp} erat",  # portatus erat
                "Vplppasindpl1": f"{self.ppp[:-2]}i eramus",  # portati eramus
                "Vplppasindpl2": f"{self.ppp[:-2]}i eratis",  # portati eratis
                "Vplppasindpl3": f"{self.ppp[:-2]}i erant",  # portati erant
                "Vfprpasindsg1": f"{self.ppp} ero",  # portatus ero
                "Vfprpasindsg2": f"{self.ppp} eris",  # portatus eris
                "Vfprpasindsg3": f"{self.ppp} erit",  # portatus erit
                "Vfprpasindpl1": f"{self.ppp[:-2]}i erimus",  # portati erimus
                "Vfprpasindpl2": f"{self.ppp[:-2]}i eritis",  # portati eritis
                "Vfprpasindpl3": f"{self.ppp[:-2]}i erunt",  # portati erunt
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms
        return endings | {
            "Vpreactindsg1": self.present,  # porto
            "Vpreactindsg2": f"{self._inf_stem}as",  # portas
            "Vpreactindsg3": f"{self._inf_stem}at",  # portat
            "Vpreactindpl1": f"{self._inf_stem}amus",  # portamus
            "Vpreactindpl2": f"{self._inf_stem}atis",  # portatis
            "Vpreactindpl3": f"{self._inf_stem}ant",  # portant
            "Vimpactindsg1": f"{self._inf_stem}abam",  # portabam
            "Vimpactindsg2": f"{self._inf_stem}abas",  # portabas
            "Vimpactindsg3": f"{self._inf_stem}abat",  # portabat
            "Vimpactindpl1": f"{self._inf_stem}abamus",  # portabamus
            "Vimpactindpl2": f"{self._inf_stem}abatis",  # portabatis
            "Vimpactindpl3": f"{self._inf_stem}abant",  # portabant
            "Vfutactindsg1": f"{self._inf_stem}abo",  # portabo
            "Vfutactindsg2": f"{self._inf_stem}abis",  # portabis
            "Vfutactindsg3": f"{self._inf_stem}abit",  # portabit
            "Vfutactindpl1": f"{self._inf_stem}abimus",  # portabimus
            "Vfutactindpl2": f"{self._inf_stem}abitis",  # portabitis
            "Vfutactindpl3": f"{self._inf_stem}abunt",  # portabunt
            "Vperactindsg1": self.perfect,  # portavi
            "Vperactindsg2": f"{self._per_stem}isti",  # portavisti
            "Vperactindsg3": f"{self._per_stem}it",  # portavit
            "Vperactindpl1": f"{self._per_stem}imus",  # portavimus
            "Vperactindpl2": f"{self._per_stem}istis",  # portavistis
            "Vperactindpl3": f"{self._per_stem}erunt",  # portaverunt
            "Vplpactindsg1": f"{self._per_stem}eram",  # portaveram
            "Vplpactindsg2": f"{self._per_stem}eras",  # portaveras
            "Vplpactindsg3": f"{self._per_stem}erat",  # portaverat
            "Vplpactindpl1": f"{self._per_stem}eramus",  # portaveramus
            "Vplpactindpl2": f"{self._per_stem}eratis",  # portaveratis
            "Vplpactindpl3": f"{self._per_stem}erant",  # portaverant
            "Vfpractindsg1": f"{self._per_stem}ero",  # portavero
            "Vfpractindsg2": f"{self._per_stem}eris",  # portaveris
            "Vfpractindsg3": f"{self._per_stem}erit",  # portaverit
            "Vfpractindpl1": f"{self._per_stem}erimus",  # portaverimus
            "Vfpractindpl2": f"{self._per_stem}eritis",  # portaveritis
            "Vfpractindpl3": f"{self._per_stem}erint",  # portaverint
            "Vimpactsbjsg1": f"{self.infinitive}m",  # portarem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # portares
            "Vimpactsbjsg3": f"{self.infinitive}t",  # portaret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # portaremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # portaretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # portarent
            "Vplpactsbjsg1": f"{self._per_stem}issem",  # portavissem
            "Vplpactsbjsg2": f"{self._per_stem}isses",  # portavisses
            "Vplpactsbjsg3": f"{self._per_stem}isset",  # portavisset
            "Vplpactsbjpl1": f"{self._per_stem}issemus",  # portavissemus
            "Vplpactsbjpl2": f"{self._per_stem}issetis",  # portavissetis
            "Vplpactsbjpl3": f"{self._per_stem}issent",  # portavissent
            "Vpreactipesg2": f"{self._inf_stem}a",  # porta
            "Vpreactipepl2": f"{self._inf_stem}ate",  # portate
            "Vpreactinf   ": self.infinitive,  # portare
        }

    def _second_conjugation(self) -> Endings:
        assert self.infinitive is not None
        assert self.perfect is not None

        endings: Endings = {
            "Vprepasindsg1": f"{self._inf_stem}eor",  # doceor
            "Vprepasindsg2": f"{self._inf_stem}eris",  # doceris
            "Vprepasindsg3": f"{self._inf_stem}etur",  # docetur
            "Vprepasindpl1": f"{self._inf_stem}emur",  # docemur
            "Vprepasindpl2": f"{self._inf_stem}emini",  # docemini
            "Vprepasindpl3": f"{self._inf_stem}entur",  # docentur
            "Vimppasindsg1": f"{self._inf_stem}ebar",  # docebar
            "Vimppasindsg2": f"{self._inf_stem}ebaris",  # docebaris
            "Vimppasindsg3": f"{self._inf_stem}ebatur",  # docebatur
            "Vimppasindpl1": f"{self._inf_stem}ebamur",  # docebamur
            "Vimppasindpl2": f"{self._inf_stem}ebamini",  # docebamini
            "Vimppasindpl3": f"{self._inf_stem}ebantur",  # docebantur
            "Vfutpasindsg1": f"{self._inf_stem}ebor",  # docebor
            "Vfutpasindsg2": f"{self._inf_stem}eberis",  # doceberis
            "Vfutpasindsg3": f"{self._inf_stem}ebitur",  # docebitur
            "Vfutpasindpl1": f"{self._inf_stem}ebimur",  # docebimur
            "Vfutpasindpl2": f"{self._inf_stem}ebimini",  # docebimini
            "Vfutpasindpl3": f"{self._inf_stem}ebuntur",  # docebuntur
            "Vprepasinf   ": f"{self._inf_stem}eri",  # doceri
        }

        if not self.no_ppp:
            assert self.ppp is not None

            endings |= {
                "Vperpasindsg1": f"{self.ppp} sum",  # doctus sum
                "Vperpasindsg2": f"{self.ppp} es",  # doctus es
                "Vperpasindsg3": f"{self.ppp} est",  # doctus est
                "Vperpasindpl1": f"{self.ppp[:-2]}i sumus",  # docti sumus
                "Vperpasindpl2": f"{self.ppp[:-2]}i estis",  # docti estis
                "Vperpasindpl3": f"{self.ppp[:-2]}i sunt",  # docti sunt
                "Vplppasindsg1": f"{self.ppp} eram",  # doctus eram
                "Vplppasindsg2": f"{self.ppp} eras",  # doctus eras
                "Vplppasindsg3": f"{self.ppp} erat",  # doctus erat
                "Vplppasindpl1": f"{self.ppp[:-2]}i eramus",  # docti eramus
                "Vplppasindpl2": f"{self.ppp[:-2]}i eratis",  # docti eratis
                "Vplppasindpl3": f"{self.ppp[:-2]}i erant",  # docti erant
                "Vfprpasindsg1": f"{self.ppp} ero",  # doctus ero
                "Vfprpasindsg2": f"{self.ppp} eris",  # doctus eris
                "Vfprpasindsg3": f"{self.ppp} erit",  # doctus erit
                "Vfprpasindpl1": f"{self.ppp[:-2]}i erimus",  # docti erimus
                "Vfprpasindpl2": f"{self.ppp[:-2]}i eritis",  # docti eritis
                "Vfprpasindpl3": f"{self.ppp[:-2]}i erunt",  # docti erunt
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        return endings | {
            "Vpreactindsg1": self.present,  # doceo
            "Vpreactindsg2": f"{self._inf_stem}es",  # doces
            "Vpreactindsg3": f"{self._inf_stem}et",  # docet
            "Vpreactindpl1": f"{self._inf_stem}emus",  # docemus
            "Vpreactindpl2": f"{self._inf_stem}etis",  # docetis
            "Vpreactindpl3": f"{self._inf_stem}ent",  # docent
            "Vimpactindsg1": f"{self._inf_stem}ebam",  # docebam
            "Vimpactindsg2": f"{self._inf_stem}ebas",  # docebas
            "Vimpactindsg3": f"{self._inf_stem}ebat",  # docebat
            "Vimpactindpl1": f"{self._inf_stem}ebamus",  # docebamus
            "Vimpactindpl2": f"{self._inf_stem}ebatis",  # docebatis
            "Vimpactindpl3": f"{self._inf_stem}ebant",  # docebant
            "Vfutactindsg1": f"{self._inf_stem}ebo",  # docebo
            "Vfutactindsg2": f"{self._inf_stem}ebis",  # docebis
            "Vfutactindsg3": f"{self._inf_stem}ebit",  # docebit
            "Vfutactindpl1": f"{self._inf_stem}ebimus",  # docebimus
            "Vfutactindpl2": f"{self._inf_stem}ebitis",  # docebitis
            "Vfutactindpl3": f"{self._inf_stem}ebunt",  # docebunt
            "Vperactindsg1": self.perfect,  # docui
            "Vperactindsg2": f"{self._per_stem}isti",  # docuisit
            "Vperactindsg3": f"{self._per_stem}it",  # docuit
            "Vperactindpl1": f"{self._per_stem}imus",  # docuimus
            "Vperactindpl2": f"{self._per_stem}istis",  # docuistis
            "Vperactindpl3": f"{self._per_stem}erunt",  # docuerunt
            "Vplpactindsg1": f"{self._per_stem}eram",  # docueram
            "Vplpactindsg2": f"{self._per_stem}eras",  # docueras
            "Vplpactindsg3": f"{self._per_stem}erat",  # docuerat
            "Vplpactindpl1": f"{self._per_stem}eramus",  # docueramus
            "Vplpactindpl2": f"{self._per_stem}eratis",  # docueratis
            "Vplpactindpl3": f"{self._per_stem}erant",  # docuerant
            "Vfpractindsg1": f"{self._per_stem}ero",  # docuero
            "Vfpractindsg2": f"{self._per_stem}eris",  # docueris
            "Vfpractindsg3": f"{self._per_stem}erit",  # docuerit
            "Vfpractindpl1": f"{self._per_stem}erimus",  # docuerimus
            "Vfpractindpl2": f"{self._per_stem}eritis",  # docueritis
            "Vfpractindpl3": f"{self._per_stem}erint",  # docuerint
            "Vimpactsbjsg1": f"{self.infinitive}m",  # docerem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # doceres
            "Vimpactsbjsg3": f"{self.infinitive}t",  # doceret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # doceremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # doceretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # docerent
            "Vplpactsbjsg1": f"{self._per_stem}issem",  # docuissem
            "Vplpactsbjsg2": f"{self._per_stem}isses",  # docuisses
            "Vplpactsbjsg3": f"{self._per_stem}isset",  # docuisset
            "Vplpactsbjpl1": f"{self._per_stem}issemus",  # docuissmus
            "Vplpactsbjpl2": f"{self._per_stem}issetis",  # docuissetis
            "Vplpactsbjpl3": f"{self._per_stem}issent",  # docuissent
            "Vpreactipesg2": f"{self._inf_stem}e",  # doce
            "Vpreactipepl2": f"{self._inf_stem}ete",  # docete
            "Vpreactinf   ": self.infinitive,  # docere
        }

    def _third_conjugation(self) -> Endings:
        assert self.infinitive is not None
        assert self.perfect is not None

        endings: Endings = {
            "Vprepasindsg1": f"{self._inf_stem}or",  # trahor
            "Vprepasindsg2": f"{self._inf_stem}eris",  # traheris
            "Vprepasindsg3": f"{self._inf_stem}itur",  # trahitur
            "Vprepasindpl1": f"{self._inf_stem}imur",  # trahimur
            "Vprepasindpl2": f"{self._inf_stem}imini",  # trahimini
            "Vprepasindpl3": f"{self._inf_stem}untur",  # trahuntur
            "Vimppasindsg1": f"{self._inf_stem}ebar",  # trahebar
            "Vimppasindsg2": f"{self._inf_stem}ebaris",  # trahebaris
            "Vimppasindsg3": f"{self._inf_stem}ebatur",  # trahebatur
            "Vimppasindpl1": f"{self._inf_stem}ebamur",  # trahebamur
            "Vimppasindpl2": f"{self._inf_stem}ebamini",  # trahebamini
            "Vimppasindpl3": f"{self._inf_stem}ebantur",  # trahebantur
            "Vfutpasindsg1": f"{self._inf_stem}ar",  # trahar
            "Vfutpasindsg2": f"{self._inf_stem}eris",  # traheris
            "Vfutpasindsg3": f"{self._inf_stem}etur",  # trahetur
            "Vfutpasindpl1": f"{self._inf_stem}emur",  # trahemur
            "Vfutpasindpl2": f"{self._inf_stem}emini",  # trahemini
            "Vfutpasindpl3": f"{self._inf_stem}entur",  # trahentur
            "Vprepasinf   ": f"{self._inf_stem}i",  # trahi
        }

        if not self.no_ppp:
            assert self.ppp is not None

            endings |= {
                "Vperpasindsg1": f"{self.ppp} sum",  # tractus sum
                "Vperpasindsg2": f"{self.ppp} es",  # tractus es
                "Vperpasindsg3": f"{self.ppp} est",  # tractus est
                "Vperpasindpl1": f"{self.ppp[:-2]}i sumus",  # tracti sumus
                "Vperpasindpl2": f"{self.ppp[:-2]}i estis",  # tracti estis
                "Vperpasindpl3": f"{self.ppp[:-2]}i sunt",  # tracti sunt
                "Vplppasindsg1": f"{self.ppp} eram",  # tractus eram
                "Vplppasindsg2": f"{self.ppp} eras",  # tractus eras
                "Vplppasindsg3": f"{self.ppp} erat",  # tractus erat
                "Vplppasindpl1": f"{self.ppp[:-2]}i eramus",  # tracti eramus
                "Vplppasindpl2": f"{self.ppp[:-2]}i eratis",  # tracti eratis
                "Vplppasindpl3": f"{self.ppp[:-2]}i erant",  # tracti erant
                "Vfprpasindsg1": f"{self.ppp} ero",  # tractus ero
                "Vfprpasindsg2": f"{self.ppp} eris",  # tractus eris
                "Vfprpasindsg3": f"{self.ppp} erit",  # tractus erit
                "Vfprpasindpl1": f"{self.ppp[:-2]}i erimus",  # tracti erimus
                "Vfprpasindpl2": f"{self.ppp[:-2]}i eritis",  # tracti eritis
                "Vfprpasindpl3": f"{self.ppp[:-2]}i erunt",  # tracti erunt
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        return endings | {
            "Vpreactindsg1": self.present,  # traho
            "Vpreactindsg2": f"{self._inf_stem}is",  # trahis
            "Vpreactindsg3": f"{self._inf_stem}it",  # trahit
            "Vpreactindpl1": f"{self._inf_stem}imus",  # trahimus
            "Vpreactindpl2": f"{self._inf_stem}itis",  # trahitis
            "Vpreactindpl3": f"{self._inf_stem}unt",  # trahunt
            "Vimpactindsg1": f"{self._inf_stem}ebam",  # trahebam
            "Vimpactindsg2": f"{self._inf_stem}ebas",  # trahebas
            "Vimpactindsg3": f"{self._inf_stem}ebat",  # trahebat
            "Vimpactindpl1": f"{self._inf_stem}ebamus",  # trahebamus
            "Vimpactindpl2": f"{self._inf_stem}ebatis",  # trahebatis
            "Vimpactindpl3": f"{self._inf_stem}ebant",  # trahebant
            "Vfutactindsg1": f"{self._inf_stem}am",  # traham
            "Vfutactindsg2": f"{self._inf_stem}es",  # trahes
            "Vfutactindsg3": f"{self._inf_stem}et",  # trahet
            "Vfutactindpl1": f"{self._inf_stem}emus",  # trahemus
            "Vfutactindpl2": f"{self._inf_stem}etis",  # trahetis
            "Vfutactindpl3": f"{self._inf_stem}ent",  # trahent
            "Vperactindsg1": self.perfect,  # traxi
            "Vperactindsg2": f"{self._per_stem}isti",  # traxisti
            "Vperactindsg3": f"{self._per_stem}it",  # traxit
            "Vperactindpl1": f"{self._per_stem}imus",  # traximus
            "Vperactindpl2": f"{self._per_stem}istis",  # traxistis
            "Vperactindpl3": f"{self._per_stem}erunt",  # traxerunt
            "Vplpactindsg1": f"{self._per_stem}eram",  # traxeram
            "Vplpactindsg2": f"{self._per_stem}eras",  # traxeras
            "Vplpactindsg3": f"{self._per_stem}erat",  # traxerat
            "Vplpactindpl1": f"{self._per_stem}eramus",  # traxeramus
            "Vplpactindpl2": f"{self._per_stem}eratis",  # traxeratis
            "Vplpactindpl3": f"{self._per_stem}erant",  # traxerant
            "Vfpractindsg1": f"{self._per_stem}ero",  # traxero
            "Vfpractindsg2": f"{self._per_stem}eris",  # traxeris
            "Vfpractindsg3": f"{self._per_stem}erit",  # traxerit
            "Vfpractindpl1": f"{self._per_stem}erimus",  # traxerimus
            "Vfpractindpl2": f"{self._per_stem}eritis",  # traxeritis
            "Vfpractindpl3": f"{self._per_stem}erint",  # traxerint
            "Vimpactsbjsg1": f"{self.infinitive}m",  # traherem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # traheres
            "Vimpactsbjsg3": f"{self.infinitive}t",  # traheret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # traheremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # traheretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # traherent
            "Vplpactsbjsg1": f"{self._per_stem}issem",  # traxissem
            "Vplpactsbjsg2": f"{self._per_stem}isses",  # traxisses
            "Vplpactsbjsg3": f"{self._per_stem}isset",  # traxisset
            "Vplpactsbjpl1": f"{self._per_stem}issemus",  # traxissemus
            "Vplpactsbjpl2": f"{self._per_stem}issetis",  # traxissetis
            "Vplpactsbjpl3": f"{self._per_stem}issent",  # traxissent
            "Vpreactipesg2": f"{self._inf_stem}e",  # trahe
            "Vpreactipepl2": f"{self._inf_stem}ite",  # trahite
            "Vpreactinf   ": self.infinitive,  # trahere
        }

    def _fourth_conjugation(self) -> Endings:
        assert self.infinitive is not None
        assert self.perfect is not None

        endings: Endings = {
            "Vprepasindsg1": f"{self._inf_stem}ior",  # audior
            "Vprepasindsg2": f"{self._inf_stem}iris",  # audiris
            "Vprepasindsg3": f"{self._inf_stem}itur",  # auditur
            "Vprepasindpl1": f"{self._inf_stem}imur",  # audimur
            "Vprepasindpl2": f"{self._inf_stem}imini",  # audimini
            "Vprepasindpl3": f"{self._inf_stem}iuntur",  # audiuntur
            "Vimppasindsg1": f"{self._inf_stem}iebar",  # audiebar
            "Vimppasindsg2": f"{self._inf_stem}iebaris",  # audiebaris
            "Vimppasindsg3": f"{self._inf_stem}iebatur",  # audiebatur
            "Vimppasindpl1": f"{self._inf_stem}iebamur",  # audiebamur
            "Vimppasindpl2": f"{self._inf_stem}iebamini",  # audiebamini
            "Vimppasindpl3": f"{self._inf_stem}iebantur",  # audiebantur
            "Vfutpasindsg1": f"{self._inf_stem}iar",  # audiar
            "Vfutpasindsg2": f"{self._inf_stem}ieris",  # audieris
            "Vfutpasindsg3": f"{self._inf_stem}ietur",  # audietur
            "Vfutpasindpl1": f"{self._inf_stem}iemur",  # audiemur
            "Vfutpasindpl2": f"{self._inf_stem}iemini",  # audiemini
            "Vfutpasindpl3": f"{self._inf_stem}ientur",  # audientur
            "Vprepasinf   ": f"{self._inf_stem}iri",  # audiri
        }

        if not self.no_ppp:
            assert self.ppp is not None

            endings |= {
                "Vperpasindsg1": f"{self.ppp} sum",  # auditus sum
                "Vperpasindsg2": f"{self.ppp} es",  # auditus es
                "Vperpasindsg3": f"{self.ppp} est",  # auditus est
                "Vperpasindpl1": f"{self.ppp[:-2]}i sumus",  # auditi sumus
                "Vperpasindpl2": f"{self.ppp[:-2]}i estis",  # auditi estis
                "Vperpasindpl3": f"{self.ppp[:-2]}i sunt",  # auditi sunt
                "Vplppasindsg1": f"{self.ppp} eram",  # auditus eram
                "Vplppasindsg2": f"{self.ppp} eras",  # auditus eras
                "Vplppasindsg3": f"{self.ppp} erat",  # auditus erat
                "Vplppasindpl1": f"{self.ppp[:-2]}i eramus",  # auditi eramus
                "Vplppasindpl2": f"{self.ppp[:-2]}i eratis",  # auditi eratis
                "Vplppasindpl3": f"{self.ppp[:-2]}i erant",  # auditi erant
                "Vfprpasindsg1": f"{self.ppp} ero",  # auditus ero
                "Vfprpasindsg2": f"{self.ppp} eris",  # auditus eris
                "Vfprpasindsg3": f"{self.ppp} erit",  # auditus erit
                "Vfprpasindpl1": f"{self.ppp[:-2]}i erimus",  # auditi erimus
                "Vfprpasindpl2": f"{self.ppp[:-2]}i eritis",  # auditi eritis
                "Vfprpasindpl3": f"{self.ppp[:-2]}i erunt",  # auditi erunt
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        return endings | {
            "Vpreactindsg1": self.present,  # audio
            "Vpreactindsg2": f"{self._inf_stem}is",  # audis
            "Vpreactindsg3": f"{self._inf_stem}it",  # audit
            "Vpreactindpl1": f"{self._inf_stem}imus",  # audimus
            "Vpreactindpl2": f"{self._inf_stem}itis",  # auditis
            "Vpreactindpl3": f"{self._inf_stem}iunt",  # audiunt
            "Vimpactindsg1": f"{self._inf_stem}iebam",  # audiebam
            "Vimpactindsg2": f"{self._inf_stem}iebas",  # audiebas
            "Vimpactindsg3": f"{self._inf_stem}iebat",  # audiebat
            "Vimpactindpl1": f"{self._inf_stem}iebamus",  # audiebamus
            "Vimpactindpl2": f"{self._inf_stem}iebatis",  # audiebatis
            "Vimpactindpl3": f"{self._inf_stem}iebant",  # audiebant
            "Vfutactindsg1": f"{self._inf_stem}iam",  # veniam
            "Vfutactindsg2": f"{self._inf_stem}ies",  # venies
            "Vfutactindsg3": f"{self._inf_stem}iet",  # veniet
            "Vfutactindpl1": f"{self._inf_stem}iemus",  # veniemus
            "Vfutactindpl2": f"{self._inf_stem}ietis",  # venietis
            "Vfutactindpl3": f"{self._inf_stem}ient",  # venient
            "Vperactindsg1": self.perfect,  # audivi
            "Vperactindsg2": f"{self._per_stem}isti",  # audivisti
            "Vperactindsg3": f"{self._per_stem}it",  # audivit
            "Vperactindpl1": f"{self._per_stem}imus",  # audivimus
            "Vperactindpl2": f"{self._per_stem}istis",  # audivistis
            "Vperactindpl3": f"{self._per_stem}erunt",  # audiverunt
            "Vplpactindsg1": f"{self._per_stem}eram",  # audiveram
            "Vplpactindsg2": f"{self._per_stem}eras",  # audiveras
            "Vplpactindsg3": f"{self._per_stem}erat",  # audiverat
            "Vplpactindpl1": f"{self._per_stem}eramus",  # audiveramus
            "Vplpactindpl2": f"{self._per_stem}eratis",  # audiveratis
            "Vplpactindpl3": f"{self._per_stem}erant",  # audiverant
            "Vfpractindsg1": f"{self._per_stem}ero",  # audivero
            "Vfpractindsg2": f"{self._per_stem}eris",  # audiveris
            "Vfpractindsg3": f"{self._per_stem}erit",  # audiverit
            "Vfpractindpl1": f"{self._per_stem}erimus",  # audiverimus
            "Vfpractindpl2": f"{self._per_stem}eritis",  # audiveritis
            "Vfpractindpl3": f"{self._per_stem}erint",  # audiverint
            "Vimpactsbjsg1": f"{self.infinitive}m",  # audirem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # audires
            "Vimpactsbjsg3": f"{self.infinitive}t",  # audiret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # audiremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # audiretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # audirent
            "Vplpactsbjsg1": f"{self._per_stem}issem",  # audivissem
            "Vplpactsbjsg2": f"{self._per_stem}isses",  # audivisses
            "Vplpactsbjsg3": f"{self._per_stem}isset",  # audivisset
            "Vplpactsbjpl1": f"{self._per_stem}issemus",  # audivissemus
            "Vplpactsbjpl2": f"{self._per_stem}issetis",  # audivissetis
            "Vplpactsbjpl3": f"{self._per_stem}issent",  # audivissent
            "Vpreactipesg2": f"{self._inf_stem}i",  # audi
            "Vpreactipepl2": f"{self._inf_stem}ite",  # audite
            "Vpreactinf   ": self.infinitive,  # audire
        }

    def _mixed_conjugation(self) -> Endings:
        assert self.infinitive is not None
        assert self.perfect is not None

        endings: Endings = {
            "Vprepasindsg1": f"{self._inf_stem}ior",  # capior
            "Vprepasindsg2": f"{self._inf_stem}eris",  # caperis
            "Vprepasindsg3": f"{self._inf_stem}itur",  # capitur
            "Vprepasindpl1": f"{self._inf_stem}imur",  # capimur
            "Vprepasindpl2": f"{self._inf_stem}imini",  # capimini
            "Vprepasindpl3": f"{self._inf_stem}iuntur",  # capiuntur
            "Vimppasindsg1": f"{self._inf_stem}iebar",  # capiebar
            "Vimppasindsg2": f"{self._inf_stem}iebaris",  # capiebaris
            "Vimppasindsg3": f"{self._inf_stem}iebatur",  # capiebatur
            "Vimppasindpl1": f"{self._inf_stem}iebamur",  # capiebamur
            "Vimppasindpl2": f"{self._inf_stem}iebamini",  # capiebamini
            "Vimppasindpl3": f"{self._inf_stem}iebantur",  # capiebantur
            "Vfutpasindsg1": f"{self._inf_stem}iar",  # capiar
            "Vfutpasindsg2": f"{self._inf_stem}ieris",  # capieris
            "Vfutpasindsg3": f"{self._inf_stem}ietur",  # capietur
            "Vfutpasindpl1": f"{self._inf_stem}iemur",  # capiemur
            "Vfutpasindpl2": f"{self._inf_stem}iemini",  # capiemini
            "Vfutpasindpl3": f"{self._inf_stem}ientur",  # capientur
            "Vprepasinf   ": f"{self._inf_stem}i",  # capi
        }

        if not self.no_ppp:
            assert self.ppp is not None

            endings |= {
                "Vperpasindsg1": f"{self.ppp} sum",  # captus sum
                "Vperpasindsg2": f"{self.ppp} es",  # captus es
                "Vperpasindsg3": f"{self.ppp} est",  # captus est
                "Vperpasindpl1": f"{self.ppp[:-2]}i sumus",  # capti sumus
                "Vperpasindpl2": f"{self.ppp[:-2]}i estis",  # capti estis
                "Vperpasindpl3": f"{self.ppp[:-2]}i sunt",  # capti sunt
                "Vplppasindsg1": f"{self.ppp} eram",  # captus eram
                "Vplppasindsg2": f"{self.ppp} eras",  # captus eras
                "Vplppasindsg3": f"{self.ppp} erat",  # captus erat
                "Vplppasindpl1": f"{self.ppp[:-2]}i eramus",  # capti eramus
                "Vplppasindpl2": f"{self.ppp[:-2]}i eratis",  # capti eratis
                "Vplppasindpl3": f"{self.ppp[:-2]}i erant",  # capti erant
                "Vfprpasindsg1": f"{self.ppp} ero",  # captus ero
                "Vfprpasindsg2": f"{self.ppp} eris",  # captus eris
                "Vfprpasindsg3": f"{self.ppp} erit",  # captus erit
                "Vfprpasindpl1": f"{self.ppp[:-2]}i erimus",  # capti erimus
                "Vfprpasindpl2": f"{self.ppp[:-2]}i eritis",  # capti eritis
                "Vfprpasindpl3": f"{self.ppp[:-2]}i erunt",  # capti erunt
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        return endings | {
            "Vpreactindsg1": self.present,  # capio
            "Vpreactindsg2": f"{self._inf_stem}is",  # capis
            "Vpreactindsg3": f"{self._inf_stem}it",  # capit
            "Vpreactindpl1": f"{self._inf_stem}imus",  # capimus
            "Vpreactindpl2": f"{self._inf_stem}itis",  # capitis
            "Vpreactindpl3": f"{self._inf_stem}iunt",  # capiunt
            "Vimpactindsg1": f"{self._inf_stem}iebam",  # capiebam
            "Vimpactindsg2": f"{self._inf_stem}iebas",  # capiebas
            "Vimpactindsg3": f"{self._inf_stem}iebat",  # capiebat
            "Vimpactindpl1": f"{self._inf_stem}iebamus",  # capiebamus
            "Vimpactindpl2": f"{self._inf_stem}iebatis",  # capiebatis
            "Vimpactindpl3": f"{self._inf_stem}iebant",  # capiebant
            "Vfutactindsg1": f"{self._inf_stem}iam",  # capiam
            "Vfutactindsg2": f"{self._inf_stem}ies",  # capies
            "Vfutactindsg3": f"{self._inf_stem}iet",  # capiet
            "Vfutactindpl1": f"{self._inf_stem}iemus",  # capiemus
            "Vfutactindpl2": f"{self._inf_stem}ietis",  # capietis
            "Vfutactindpl3": f"{self._inf_stem}ient",  # capient
            "Vperactindsg1": self.perfect,  # cepi
            "Vperactindsg2": f"{self._per_stem}isti",  # cepisti
            "Vperactindsg3": f"{self._per_stem}it",  # cepit
            "Vperactindpl1": f"{self._per_stem}imus",  # cepimus
            "Vperactindpl2": f"{self._per_stem}istis",  # cepistis
            "Vperactindpl3": f"{self._per_stem}erunt",  # ceperunt
            "Vplpactindsg1": f"{self._per_stem}eram",  # ceperam
            "Vplpactindsg2": f"{self._per_stem}eras",  # ceperas
            "Vplpactindsg3": f"{self._per_stem}erat",  # ceperat
            "Vplpactindpl1": f"{self._per_stem}eramus",  # ceperamus
            "Vplpactindpl2": f"{self._per_stem}eratis",  # ceperatis
            "Vplpactindpl3": f"{self._per_stem}erant",  # ceperant
            "Vfpractindsg1": f"{self._per_stem}ero",  # cepero
            "Vfpractindsg2": f"{self._per_stem}eris",  # ceperis
            "Vfpractindsg3": f"{self._per_stem}erit",  # ceperit
            "Vfpractindpl1": f"{self._per_stem}erimus",  # ceperimus
            "Vfpractindpl2": f"{self._per_stem}eritis",  # ceperitis
            "Vfpractindpl3": f"{self._per_stem}erint",  # ceperint
            "Vimpactsbjsg1": f"{self.infinitive}m",  # caperem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # caperes
            "Vimpactsbjsg3": f"{self.infinitive}t",  # caperet
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # caperemus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # caperetis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # caperent
            "Vplpactsbjsg1": f"{self._per_stem}issem",  # cepissem
            "Vplpactsbjsg2": f"{self._per_stem}isses",  # cepisses
            "Vplpactsbjsg3": f"{self._per_stem}isset",  # cepisset
            "Vplpactsbjpl1": f"{self._per_stem}issemus",  # cepissemus
            "Vplpactsbjpl2": f"{self._per_stem}issetis",  # cepissetis
            "Vplpactsbjpl3": f"{self._per_stem}issent",  # cepissent
            "Vpreactipesg2": f"{self._inf_stem}e",  # cape
            "Vpreactipepl2": f"{self._inf_stem}ite",  # capite
            "Vpreactinf   ": self.infinitive,  # capere
        }

    def _participles(self) -> Endings:
        assert self.infinitive is not None
        assert self.perfect is not None

        self._preptc_stem = self.infinitive[:-2]
        if self.conjugation == 4:
            self._preptc_stem += "e"
        if self.conjugation == 5:
            self._preptc_stem = self.infinitive[:-3]
            self._preptc_stem += "ie"

        endings: Endings = {
            "Vpreactptcmnomsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcmvocsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcmaccsg": f"{self._preptc_stem}ntem",  # portantem
            "Vpreactptcmgensg": f"{self._preptc_stem}ntis",  # portantis
            "Vpreactptcmdatsg": f"{self._preptc_stem}nti",  # portanti
            "Vpreactptcmablsg": MultipleEndings(
                regular=f"{self._preptc_stem}nti",  # portanti
                absolute=f"{self._preptc_stem}nte",  # portante
            ),
            "Vpreactptcmnompl": f"{self._preptc_stem}ntes",  # portantes
            "Vpreactptcmvocpl": f"{self._preptc_stem}ntes",  # portantes
            "Vpreactptcmaccpl": f"{self._preptc_stem}ntes",  # portantes
            "Vpreactptcmgenpl": f"{self._preptc_stem}ntium",  # portantium
            "Vpreactptcmdatpl": f"{self._preptc_stem}ntibus",  # portantibus
            "Vpreactptcmablpl": f"{self._preptc_stem}ntibus",  # portantibus
            "Vpreactptcfnomsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcfvocsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcfaccsg": f"{self._preptc_stem}ntem",  # portantem
            "Vpreactptcfgensg": f"{self._preptc_stem}ntis",  # portantis
            "Vpreactptcfdatsg": f"{self._preptc_stem}nti",  # portanti
            "Vpreactptcfablsg": MultipleEndings(
                regular=f"{self._preptc_stem}nti",  # portanti
                absolute=f"{self._preptc_stem}nte",  # portante
            ),
            "Vpreactptcfnompl": f"{self._preptc_stem}ntes",  # portantes
            "Vpreactptcfvocpl": f"{self._preptc_stem}ntes",  # portantes
            "Vpreactptcfaccpl": f"{self._preptc_stem}ntes",  # portantes
            "Vpreactptcfgenpl": f"{self._preptc_stem}ntium",  # portantium
            "Vpreactptcfdatpl": f"{self._preptc_stem}ntibus",  # portantibus
            "Vpreactptcfablpl": f"{self._preptc_stem}ntibus",  # portantibus
            "Vpreactptcnnomsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcnvocsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcnaccsg": f"{self._preptc_stem}ns",  # portans
            "Vpreactptcngensg": f"{self._preptc_stem}ntis",  # portantis
            "Vpreactptcndatsg": f"{self._preptc_stem}nti",  # portanti
            "Vpreactptcnablsg": MultipleEndings(
                regular=f"{self._preptc_stem}nti",  # portanti
                absolute=f"{self._preptc_stem}nte",  # portante
            ),
            "Vpreactptcnnompl": f"{self._preptc_stem}ntia",  # portantia
            "Vpreactptcnvocpl": f"{self._preptc_stem}ntia",  # portantia
            "Vpreactptcnaccpl": f"{self._preptc_stem}ntia",  # portantia
            "Vpreactptcngenpl": f"{self._preptc_stem}ntium",  # portantium
            "Vpreactptcndatpl": f"{self._preptc_stem}ntibus",  # portantibus
            "Vpreactptcnablpl": f"{self._preptc_stem}ntibus",  # portantibus
        }

        if not self.no_ppp:
            assert self.ppp is not None
            self._ppp_stem = self.ppp[:-2]

            endings |= {
                "Vperpasptcmnomsg": self.ppp,  # portatus
                "Vperpasptcmvocsg": f"{self._ppp_stem}e",  # portate
                "Vperpasptcmaccsg": f"{self._ppp_stem}um",  # portatum
                "Vperpasptcmgensg": f"{self._ppp_stem}i",  # portati
                "Vperpasptcmdatsg": f"{self._ppp_stem}o",  # portato
                "Vperpasptcmablsg": f"{self._ppp_stem}o",  # portato
                "Vperpasptcmnompl": f"{self._ppp_stem}i",  # portati
                "Vperpasptcmvocpl": f"{self._ppp_stem}i",  # portati
                "Vperpasptcmaccpl": f"{self._ppp_stem}os",  # portatos
                "Vperpasptcmgenpl": f"{self._ppp_stem}orum",  # portatorum
                "Vperpasptcmdatpl": f"{self._ppp_stem}is",  # portatis
                "Vperpasptcmablpl": f"{self._ppp_stem}is",  # portatis
                "Vperpasptcfnomsg": f"{self._ppp_stem}a",  # portata
                "Vperpasptcfvocsg": f"{self._ppp_stem}a",  # portata
                "Vperpasptcfaccsg": f"{self._ppp_stem}am",  # portatam
                "Vperpasptcfgensg": f"{self._ppp_stem}ae",  # portatae
                "Vperpasptcfdatsg": f"{self._ppp_stem}ae",  # portatae
                "Vperpasptcfablsg": f"{self._ppp_stem}a",  # portata
                "Vperpasptcfnompl": f"{self._ppp_stem}ae",  # portatae
                "Vperpasptcfvocpl": f"{self._ppp_stem}ae",  # portatae
                "Vperpasptcfaccpl": f"{self._ppp_stem}as",  # portatas
                "Vperpasptcfgenpl": f"{self._ppp_stem}arum",  # portarum
                "Vperpasptcfdatpl": f"{self._ppp_stem}is",  # portatis
                "Vperpasptcfablpl": f"{self._ppp_stem}is",  # portatis
                "Vperpasptcnnomsg": f"{self._ppp_stem}um",  # portatum
                "Vperpasptcnvocsg": f"{self._ppp_stem}um",  # portatum
                "Vperpasptcnaccsg": f"{self._ppp_stem}um",  # portatum
                "Vperpasptcngensg": f"{self._ppp_stem}i",  # portati
                "Vperpasptcndatsg": f"{self._ppp_stem}o",  # portato
                "Vperpasptcnablsg": f"{self._ppp_stem}o",  # portato
                "Vperpasptcnnompl": f"{self._ppp_stem}a",  # portata
                "Vperpasptcnvocpl": f"{self._ppp_stem}a",  # portata
                "Vperpasptcnaccpl": f"{self._ppp_stem}a",  # portata
                "Vperpasptcngenpl": f"{self._ppp_stem}orum",  # portatorum
                "Vperpasptcndatpl": f"{self._ppp_stem}is",  # portatis
                "Vperpasptcnablpl": f"{self._ppp_stem}is",  # portatis
            }

        return endings

    # fmt: off
    @overload
    def get(self, *, tense: Tense, voice: Voice, mood: Mood, person: Person, number: Number) -> Ending | None: ...
    @overload
    def get(self, *, tense: Tense, voice: Voice, mood: Literal[Mood.PARTICIPLE], number: Number, participle_gender: Gender, participle_case: Case) -> Ending | None: ...
    @overload
    def get(self, *, tense: Tense, voice: Voice, mood: Literal[Mood.INFINITIVE]) -> Ending | None: ...
    # fmt: on

    def get(
        self,
        *,
        tense: Tense,
        voice: Voice,
        mood: Mood,
        person: Person | None = None,
        number: Number | None = None,
        participle_gender: Gender | None = None,
        participle_case: Case | None = None,
    ) -> Ending | None:
        """Return the ending of the verb.

        The function returns ``None`` if no ending is found.

        Parameters
        ----------
        tense : Tense
            The tense of the ending.
        voice : Voice
            The voice of the ending.
        mood : Mood
            The mood of the ending.
        person : Person | None
            The person of the ending, if applicable (not participle).
        number : Number | None
            The number of the ending, if applicable (not participle).
        participle_gender : Gender | None
            The gender of the participle, if applicable.
        participle_case : Case | None
            The case of the participle, if applicable.

        Returns
        -------
        Ending | None
            The ending found, or ``None`` if no ending is found

        Examples
        --------
        >>> foo = Verb("celo", "celare", "celavi", "celatus", meaning="hide")
        >>> foo.get(
        ...     tense=Tense.PRESENT,
        ...     voice=Voice.ACTIVE,
        ...     mood=Mood.INDICATIVE,
        ...     person=1,
        ...     number=Number.SINGULAR,
        ... )
        'celo'

        Note that all arguments of ``get()`` are keyword-only.

        >>> foo.get(
        ...     tense=Tense.PERFECT,
        ...     voice=Voice.PASSIVE,
        ...     mood=Mood.PARTICIPLE,
        ...     participle_case=Case.NOMINATIVE,
        ...     number=Number.SINGULAR,
        ...     participle_gender=Gender.MASCULINE,
        ... )
        'celatus'

        Similar with participle endings.

        >>> foo.get(tense=Tense.PRESENT, voice=Voice.ACTIVE, mood=Mood.INFINITIVE)
        'celare'

        Infinitives.
        """
        logger.debug(
            "RegularWord(%s, %s, %s, %s, %s, %s, %s)",
            mood,
            tense,
            voice,
            participle_gender,
            participle_case,
            number,
            person,
        )

        if mood == Mood.PARTICIPLE:
            assert number is not None
            assert participle_gender is not None
            assert participle_case is not None

            return self._get_participle(
                tense=tense,
                voice=voice,
                number=number,
                participle_gender=participle_gender,
                participle_case=participle_case,
            )

        short_tense = tense.shorthand
        short_voice = voice.shorthand
        if number:
            short_number = number.shorthand

        if mood == Mood.INFINITIVE:
            return self.endings.get(f"V{short_tense}{short_voice}inf   ")

        short_mood = mood.shorthand
        return self.endings.get(
            f"V{short_tense}{short_voice}{short_mood}{short_number}{person}"
        )

    def _get_participle(
        self,
        *,
        tense: Tense,
        voice: Voice,
        number: Number,
        participle_gender: Gender,
        participle_case: Case,
    ) -> Ending | None:
        short_tense = tense.shorthand
        short_voice = voice.shorthand
        short_number = number.shorthand
        short_gender = participle_gender.shorthand
        short_case = participle_case.shorthand

        return self.endings.get(
            f"V{short_tense}{short_voice}ptc{short_gender}{short_case}{short_number}"
        )

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
        if len(key) == 13 and key[7:10] == "inf":
            try:
                output = EndingComponents(
                    tense=Tense(key[1:4]),
                    voice=Voice(key[4:7]),
                    mood=Mood(key[7:10]),
                )
            except ValueError as e:
                raise InvalidInputError(f"Key '{key}' is invalid.") from e

            output.string = (
                f"{output.tense.regular} {output.voice.regular} "
                f"{output.mood.regular}"
            )
            return output

        if len(key) == 13:
            person_value = int(key[12])
            assert is_person(person_value)

            try:
                output = EndingComponents(
                    tense=Tense(key[1:4]),
                    voice=Voice(key[4:7]),
                    mood=Mood(key[7:10]),
                    number=Number(key[10:12]),
                    person=person_value,
                )
            except ValueError as e:
                raise InvalidInputError(f"Key '{key}' is invalid.") from e

            output.string = (
                f"{output.tense.regular} {output.voice.regular} "
                f"{output.mood.regular} {output.number.regular} "
                f"{PERSON_SHORTHAND[int(key[12])]}"
            )
            return output

        if len(key) == 16 and key[7:10] == "ptc":
            try:
                output = EndingComponents(
                    tense=Tense(key[1:4]),
                    voice=Voice(key[4:7]),
                    mood=Mood.PARTICIPLE,
                    gender=Gender(key[10]),
                    case=Case(key[11:14]),
                    number=Number(key[14:16]),
                )
            except ValueError as e:
                raise InvalidInputError(f"Key '{key}' is invalid.") from e

            output.string = (
                f"{output.tense.regular} {output.voice.regular} participle "
                f"{output.gender.regular} {output.case.regular} "
                f"{output.number.regular}"
            )
            return output

        raise InvalidInputError(f"Key '{key}' is invalid.")

    @deprecated(
        "A regular method was favoured over a staticmethod. Use `create_components_normalmeth` instead."
    )
    @staticmethod
    def create_components(key: str) -> EndingComponents:
        """Generate an ``EndingComponents`` object based on endings keys.

        Deprecated in favour of ``create_components_normalmeth`` instead.
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
        placeholder_verb = Verb(
            "celo", "celare", "celavi", "celatus", meaning="hide"
        )
        return Verb.create_components_normalmeth(placeholder_verb, key)

    def __repr__(self) -> str:
        if self.conjugation == 0:
            return f"Verb({self.present}, meaning={self.meaning})"

        if self.deponent:
            return (
                f"Verb({self.present}, {self.infinitive}, {self.perfect}, "
                f"meaning={self.meaning})"
            )

        return (
            f"Verb({self.present}, {self.infinitive}, {self.perfect}, "
            f"{self.ppp}, meaning={self.meaning})"
        )

    def __str__(self) -> str:
        if self.conjugation == 0:
            return f"{self.meaning}: {self.present}"

        if self.deponent:
            return (
                f"{self.meaning}: {self.present}, "
                f"{self.infinitive}, {self.perfect}"
            )

        return (
            f"{self.meaning}: {self.present}, {self.infinitive}, "
            f"{self.perfect}, {self.ppp}"
        )

    def __add__(self, other: object) -> Verb:
        def _create_verb(
            present: str,
            infinitive: str | None,
            perfect: str | None,
            ppp: str | None,
            meaning: Meaning,
        ) -> Verb:
            if infinitive is not None:
                assert perfect is not None

                if ppp is None:
                    return Verb(present, infinitive, perfect, meaning=meaning)

                return Verb(present, infinitive, perfect, ppp, meaning=meaning)

            return Verb(present, meaning=meaning)

        if not isinstance(other, Verb) or not (
            self.endings == other.endings
            and self.conjugation == other.conjugation
            and self.deponent == other.deponent
        ):
            return NotImplemented

        if self.meaning == other.meaning:
            _create_verb(
                self.present,
                self.infinitive,
                self.perfect,
                self.ppp if not self.deponent else None,
                meaning=self.meaning,
            )

        if isinstance(self.meaning, MultipleMeanings) or isinstance(
            other.meaning, MultipleMeanings
        ):
            new_meaning = self.meaning + other.meaning
        else:
            new_meaning = MultipleMeanings((self.meaning, other.meaning))

        return _create_verb(
            self.present,
            self.infinitive,
            self.perfect,
            self.ppp if not self.deponent else None,
            meaning=new_meaning,
        )
