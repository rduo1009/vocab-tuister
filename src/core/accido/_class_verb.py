"""Representation of a Latin verb with endings."""

# pyright: reportImplicitOverride=false

import logging
from functools import total_ordering
from typing import TYPE_CHECKING, Literal, overload
from warnings import deprecated

from ...utils.dict_changes import apply_changes
from ._class_word import Word
from ._edge_cases import (
    ACTIVE_ONLY_VERBS,
    DEFECTIVE_VERBS,
    FUTURE_ACTIVE_PARTICIPLE_VERBS,
    IMPERSONAL_PASSIVE_VERBS,
    IMPERSONAL_VERBS,
    MISSING_FAP_VERBS,
    MISSING_FUTURE_VERBS,
    MISSING_GERUND_VERBS,
    MISSING_PERFECT_VERBS,
    MISSING_PPP_VERBS,
    find_derived_verb_changes,
    find_derived_verb_stems,
    find_irregular_verb_changes,
    find_irregular_verb_stems,
    get_derived_verb_conjugation,
    get_irregular_verb_conjugation,
    is_derived_verb,
    is_irregular_verb,
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
class Verb(Word):
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

    __slots__: tuple[str, ...] = (
        "_fap_stem",
        "_inf_stem",
        "_per_stem",
        "_ppp_stem",
        "_preptc_stem",
        "active_only",
        "conjugation",
        "deponent",
        "fap_fourthpp",
        "impersonal",
        "impersonal_passive",
        "infinitive",
        "no_fap",
        "no_future",
        "no_gerund",
        "no_perfect",
        "no_ppp",
        "no_supine",
        "perfect",
        "ppp",
        "present",
        "principal_parts",
        "semi_deponent",
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
            irregular or deponent. The supine can also be used here if a ppp
            form does not exist. Defaults to ``None`` if not applicable.
        meaning : Meaning

        Raises
        ------
        InvalidInputError
            If the input is invalid (incorrect `perfect`, `infinitive`
            or `ppp` values).
        """
        logger.debug(
            "Verb(%s, %s, %s, %s, meaning=%s)",
            present,
            infinitive,
            perfect,
            ppp,
            meaning,
        )

        super().__init__()

        self.present: str = present
        self.infinitive: str | None = infinitive
        self.perfect: str | None = perfect
        self.ppp: str | None = ppp
        self.meaning: Meaning = meaning

        self._first: str = self.present
        self.deponent: bool = False
        self.semi_deponent: bool = False
        self.no_ppp: bool = False
        self.fap_fourthpp: bool = False
        self.no_gerund: bool = False
        self.no_supine: bool = False
        self.no_perfect: bool = False
        self.no_future: bool = False
        self.no_fap: bool = False
        self.active_only: bool = False
        self.impersonal: bool = False
        self.impersonal_passive: bool = False

        self._ppp_stem: str | None = None
        self._fap_stem: str | None = None

        # ---------------------------------------------------------------------
        # IRREGULAR VERBS

        if irregular_endings := DEFECTIVE_VERBS.get(self.present):
            self.endings: Endings = irregular_endings
            self.conjugation: Conjugation = 0

            # HACK: Just letting `principal_parts` be the non-None forms
            # This is repeated later on in the function
            # Hopefully any issues are caught by the validation
            self.principal_parts: tuple[str, ...] = tuple(
                x
                for x in (
                    self.present,
                    self.infinitive,
                    self.perfect,
                    self.ppp,
                )
                if x is not None
            )

            return

        if self.infinitive is None:
            raise InvalidInputError(
                f"Verb '{self.present}' is not irregular, but no infinitive provided."
            )

        irregular_flag = is_irregular_verb(self.present) or is_derived_verb(
            self.present
        )

        # ---------------------------------------------------------------------
        # DEPONENT VERBS

        if self.present.endswith("or"):
            self.deponent = True

            # Verifying all arguments provided
            if self.perfect is None:  # no deponents that lack a perfect stem
                raise InvalidInputError(
                    f"Verb '{self.present}' is not irregular, but no perfect provided."
                )

            if self.ppp is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' is deponent, but ppp provided."
                )

            # Handle defective verbs
            if self.present in MISSING_PPP_VERBS:
                self.no_ppp = True
                self.no_supine = True
            else:
                if not self.perfect.endswith(" sum"):
                    raise InvalidInputError(
                        f"Invalid perfect form: '{self.perfect}' (must have 'sum')"
                    )

                self.ppp = self.perfect[:-4]
                self._ppp_stem = self.ppp[:-2]
                self._fap_stem = self.ppp[:-1] + "r"

            self.impersonal = self.present in IMPERSONAL_VERBS
            self.impersonal_passive = self.present in IMPERSONAL_PASSIVE_VERBS

            # Determine stems
            self._inf_stem: str
            self._preptc_stem: str
            if is_irregular_verb(self.present):
                self.conjugation = get_irregular_verb_conjugation(self.present)
                self._inf_stem, self._preptc_stem = find_irregular_verb_stems(
                    self.present
                )
            elif is_derived_verb(self.present):
                self.conjugation = get_derived_verb_conjugation(self.present)
                self._inf_stem, self._preptc_stem = find_derived_verb_stems(
                    self.present
                )
            elif self.infinitive.endswith("ari"):
                self.conjugation = 1
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2]
            elif self.infinitive.endswith("eri") and self.present.endswith("eor"):  # fmt: skip
                self.conjugation = 2
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2]
            elif self.infinitive.endswith("iri"):
                self.conjugation = 4
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2] + "e"
            elif self.infinitive.endswith("i") and self.present.endswith("ior"):  # fmt: skip
                self.conjugation = 5
                self._inf_stem = self.infinitive[:-1]
                self._preptc_stem = self.infinitive + "e"
            elif self.infinitive.endswith("i"):
                self.conjugation = 3
                self._inf_stem = self.infinitive[:-1]
                self._preptc_stem = self.infinitive[:-1] + "e"
            else:
                raise InvalidInputError(
                    f"Invalid infinitive form: '{self.infinitive}'"
                )

            self._per_stem: str | None = None

            # Determine endings
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
            self.endings |= self._verbal_nouns()

            # Override endings for irregular and defective verbs
            if is_irregular_verb(self.present):
                self.endings = apply_changes(
                    self.endings, find_irregular_verb_changes(self.present)
                )
            elif is_derived_verb(self.present):
                self.endings = apply_changes(
                    self.endings,
                    find_derived_verb_changes(
                        (self.present, self.infinitive, self.perfect, self.ppp)
                        if self.ppp
                        else (self.present, self.infinitive, self.perfect)
                    ),
                )

            # deponents are only passive
            if self.impersonal or self.impersonal_passive:
                self.endings = {
                    key: value
                    for key, value in self.endings.items()
                    if len(key) != 13
                    or key[10:13] == Number.SINGULAR.shorthand + "3"
                }

            self.principal_parts = (
                self.present,
                self.infinitive,
                self.perfect,
            )

            return

        # ---------------------------------------------------------------------
        # SEMI-DEPONENT VERBS

        if self.perfect is not None and self.perfect.endswith(" sum"):
            self.semi_deponent = True

            # Verifying all arguments provided
            if self.ppp is not None:  # ppp is derived from perfect
                raise InvalidInputError(
                    f"Verb '{self.present}' is semi-deponent, but ppp provided."
                )

            # Handle defective verbs
            if self.present in MISSING_PPP_VERBS:
                self.no_ppp = True
                self.no_supine = True
            else:
                self.ppp = self.perfect[:-4]  # remove " sum"
                self._ppp_stem = self.ppp[:-2]
                self._fap_stem = self.ppp[:-1] + "r"

            self.impersonal = self.present in IMPERSONAL_VERBS
            self.impersonal_passive = self.present in IMPERSONAL_PASSIVE_VERBS
            self.no_future = self.present in MISSING_FUTURE_VERBS

            if not self.present.endswith("o") and not irregular_flag:
                raise InvalidInputError(
                    f"Invalid present form: '{self.present}' (must end in '-o')"
                )

            # Determine stems
            if is_irregular_verb(self.present):
                self.conjugation = get_irregular_verb_conjugation(self.present)
                self._inf_stem, self._preptc_stem = find_irregular_verb_stems(
                    self.present
                )
            elif is_derived_verb(self.present):
                self.conjugation = get_derived_verb_conjugation(self.present)
                self._inf_stem, self._preptc_stem = find_derived_verb_stems(
                    self.present
                )
            elif self.infinitive.endswith("are"):
                self.conjugation = 1
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2]
            elif self.infinitive.endswith("ire"):
                self.conjugation = 4
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2] + "e"
            elif self.infinitive.endswith("ere"):
                if self.present.endswith("eo"):
                    self.conjugation = 2
                    self._inf_stem = self.infinitive[:-3]
                    self._preptc_stem = self.infinitive[:-2]
                elif self.present.endswith("io"):
                    self.conjugation = 5
                    self._inf_stem = self.infinitive[:-3]
                    self._preptc_stem = self.infinitive[:-3] + "ie"
                else:
                    self.conjugation = 3
                    self._inf_stem = self.infinitive[:-3]
                    self._preptc_stem = self.infinitive[:-2]
            else:
                raise InvalidInputError(
                    f"Invalid infinitive form for semi-deponent: '{self.infinitive}'"
                )

            self._per_stem = None

            # Determine endings
            match self.conjugation:
                case 1:
                    self.endings = self._first_conjugation()
                case 2:
                    self.endings = self._second_conjugation()
                case 3:
                    self.endings = self._third_conjugation()
                case 4:
                    self.endings = self._fourth_conjugation()
                case _:  # 5
                    self.endings = self._mixed_conjugation()

            self.endings |= self._participles()
            self.endings |= self._verbal_nouns()

            # Override endings for irregular and defective verbs
            if is_irregular_verb(self.present):
                self.endings = apply_changes(
                    self.endings, find_irregular_verb_changes(self.present)
                )
            elif is_derived_verb(self.present):
                self.endings = apply_changes(
                    self.endings,
                    find_derived_verb_changes(
                        (self.present, self.infinitive, self.perfect, self.ppp)
                        if self.ppp  # Should always be true unless MISSING_PPP_VERBS
                        else (self.present, self.infinitive, self.perfect)
                    ),
                )

            if self.impersonal or self.impersonal_passive:
                self.endings = {
                    key: value
                    for key, value in self.endings.items()
                    if len(key) != 13
                    or key[10:13] == Number.SINGULAR.shorthand + "3"
                }

            if self.no_future:
                self.endings = {
                    key: value
                    for key, value in self.endings.items()
                    if key[1:4]
                    not in {
                        Tense.FUTURE.shorthand,
                        Tense.FUTURE_PERFECT.shorthand,
                    }
                }

            self.principal_parts = (
                self.present,
                self.infinitive,
                self.perfect,
            )

            return

        # ---------------------------------------------------------------------
        # NON-DEPONENT VERBS (and not semi-deponent)

        # Handle defective verbs
        if self.present in MISSING_PERFECT_VERBS:
            # if only three args, then the form in `perfect` is actually the ppp
            if not self.ppp:
                self.ppp = self.perfect
                del self.perfect
            elif self.perfect is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' has no perfect, but perfect provided."
                )

            self.no_perfect = True
        else:
            if self.perfect is None:
                raise InvalidInputError(
                    f"Verb '{self.present}' is not irregular, but no perfect provided."
                )

            if not self.perfect.endswith("i") and not irregular_flag:
                raise InvalidInputError(
                    f"Invalid perfect form: '{self.perfect}' (must end in '-i')"
                )

            self._per_stem = self.perfect[:-1]

        if self.present in MISSING_PPP_VERBS:
            if self.ppp is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' has no ppp, but ppp provided."
                )

            self.no_ppp = True
            self.no_supine = True
        elif self.present in FUTURE_ACTIVE_PARTICIPLE_VERBS:
            if self.ppp is None:
                raise InvalidInputError(
                    f"Verb '{self.present}' does not have a future active participle provided."
                )

            if not self.ppp.endswith("urus"):
                raise InvalidInputError(
                    f"Invalid future active participle form: '{self.ppp}' (must end in '-urus')"
                )

            self.no_ppp = True
            self.no_supine = True
            self.fap_fourthpp = True

            self._fap_stem = self.ppp[:-2]
        else:
            if self.ppp is None:
                raise InvalidInputError(
                    f"Verb '{self.present}' is not irregular or deponent, but no ppp provided."
                )

            # HACK: convert supine into ppp, even if the ppp doesn't exist
            if self.ppp.endswith("um"):
                self.ppp = self.ppp[:-2] + "us"

            if not self.ppp.endswith("us"):
                raise InvalidInputError(
                    f"Invalid perfect passive participle form: '{self.ppp}' (must end in '-us')"
                )

            self._ppp_stem = self.ppp[:-2]
            self._fap_stem = self.ppp[:-1] + "r"

        self.no_gerund = self.present in MISSING_GERUND_VERBS
        self.no_fap = self.present in MISSING_FAP_VERBS
        self.active_only = self.present in ACTIVE_ONLY_VERBS
        self.impersonal = self.present in IMPERSONAL_VERBS
        self.impersonal_passive = self.present in IMPERSONAL_PASSIVE_VERBS

        if not self.present.endswith("o") and not irregular_flag:
            raise InvalidInputError(
                f"Invalid present form: '{self.present}' (must end in '-o')"
            )

        # Determine stems
        if is_irregular_verb(self.present):
            self.conjugation = get_irregular_verb_conjugation(self.present)
            self._inf_stem, self._preptc_stem = find_irregular_verb_stems(
                self.present
            )
        elif is_derived_verb(self.present):
            self.conjugation = get_derived_verb_conjugation(self.present)
            self._inf_stem, self._preptc_stem = find_derived_verb_stems(
                self.present
            )
        elif self.infinitive.endswith("are"):
            self.conjugation = 1
            self._inf_stem = self.infinitive[:-3]
            self._preptc_stem = self.infinitive[:-2]
        elif self.infinitive.endswith("ire"):
            self.conjugation = 4
            self._inf_stem = self.infinitive[:-3]
            self._preptc_stem = self.infinitive[:-2] + "e"
        elif self.infinitive.endswith("ere"):
            if self.present.endswith("eo"):
                self.conjugation = 2
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2]
            elif self.present.endswith("io"):
                self.conjugation = 5
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-3] + "ie"
            else:
                self.conjugation = 3
                self._inf_stem = self.infinitive[:-3]
                self._preptc_stem = self.infinitive[:-2]
        else:
            raise InvalidInputError(
                f"Invalid infinitive form: '{self.infinitive}'"
            )

        # Determine endings
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
        self.endings |= self._verbal_nouns()

        # Override endings for irregular and defective verbs
        if is_irregular_verb(self.present):
            self.endings = apply_changes(
                self.endings, find_irregular_verb_changes(self.present)
            )
        elif is_derived_verb(self.present):
            assert self.perfect is not None
            self.endings = apply_changes(
                self.endings,
                find_derived_verb_changes(
                    (self.present, self.infinitive, self.perfect, self.ppp)
                    if self.ppp
                    else (self.present, self.infinitive, self.perfect)
                ),
            )

        if self.active_only:
            self.endings = {
                key: value
                for key, value in self.endings.items()
                if key[4:7] != Voice.PASSIVE.shorthand
            }

        if self.impersonal:
            self.endings = {
                key: value
                for key, value in self.endings.items()
                if len(key) != 13
                or key[10:13] == Number.SINGULAR.shorthand + "3"
            }

        if self.impersonal_passive:
            self.endings = {
                key: value
                for key, value in self.endings.items()
                if len(key) != 13
                or (
                    key[10:13] == Number.SINGULAR.shorthand + "3"
                    or key[4:7] != Voice.PASSIVE.shorthand
                )
            }

        self.principal_parts = tuple(
            x
            for x in (self.present, self.infinitive, self.perfect, self.ppp)
            if x is not None
        )

    def _first_conjugation(self) -> Endings:
        assert self.infinitive is not None
        endings: Endings = {}

        # Passive forms
        if not self.semi_deponent:
            endings |= {
                "Vprepasindsg1": self._inf_stem + "or",  # portor
                "Vprepasindsg2": self._inf_stem + "aris",  # portaris
                "Vprepasindsg3": self._inf_stem + "atur",  # portatur
                "Vprepasindpl1": self._inf_stem + "amur",  # portamur
                "Vprepasindpl2": self._inf_stem + "amini",  # portamini
                "Vprepasindpl3": self._inf_stem + "antur",  # portantur
                "Vimppasindsg1": self._inf_stem + "abar",  # portabar
                "Vimppasindsg2": self._inf_stem + "abaris",  # portabaris
                "Vimppasindsg3": self._inf_stem + "abatur",  # portabatur
                "Vimppasindpl1": self._inf_stem + "abamur",  # portabamur
                "Vimppasindpl2": self._inf_stem + "abamini",  # portabamini
                "Vimppasindpl3": self._inf_stem + "abantur",  # portabantur
                "Vfutpasindsg1": self._inf_stem + "abor",  # portabor
                "Vfutpasindsg2": self._inf_stem + "aberis",  # portaberis
                "Vfutpasindsg3": self._inf_stem + "abitur",  # portabitur
                "Vfutpasindpl1": self._inf_stem + "abimur",  # portabimur
                "Vfutpasindpl2": self._inf_stem + "abimini",  # portabimini
                "Vfutpasindpl3": self._inf_stem + "abuntur",  # portabuntur
                "Vprepassbjsg1": self._inf_stem + "er",  # porter
                "Vprepassbjsg2": self._inf_stem + "eris",  # porteris
                "Vprepassbjsg3": self._inf_stem + "etur",  # portetur
                "Vprepassbjpl1": self._inf_stem + "emur",  # portemur
                "Vprepassbjpl2": self._inf_stem + "emini",  # portemini
                "Vprepassbjpl3": self._inf_stem + "entur",  # portentur
                "Vimppassbjsg1": self.infinitive + "r",  # portarer
                "Vimppassbjsg2": self.infinitive + "ris",  # portareris
                "Vimppassbjsg3": self.infinitive + "tur",  # portaretur
                "Vimppassbjpl1": self.infinitive + "mur",  # portaremur
                "Vimppassbjpl2": self.infinitive + "mini",  # portaremini
                "Vimppassbjpl3": self.infinitive + "ntur",  # portarentur
                "Vprepasipesg2": self._inf_stem + "are",  # portare
                "Vprepasipepl2": self._inf_stem + "amini",  # portamini
                "Vfutpasipesg2": self._inf_stem + "ator",  # portator
                "Vfutpasipesg3": self._inf_stem + "ator",  # portator
                "Vfutpasipepl3": self._inf_stem + "antor",  # portantor
                "Vprepasinf   ": self._inf_stem + "ari",  # portari
            }

        # Passive forms that use ppp
        if not self.no_ppp:
            assert self.ppp is not None
            endings |= {
                "Vperpasindsg1": self.ppp + " sum",  # portatus sum
                "Vperpasindsg2": self.ppp + " es",  # portatus es
                "Vperpasindsg3": self.ppp + " est",  # portatus est
                "Vperpasindpl1": self.ppp[:-2] + "i sumus",  # portati sumus
                "Vperpasindpl2": self.ppp[:-2] + "i estis",  # portati estis
                "Vperpasindpl3": self.ppp[:-2] + "i sunt",  # portati sunt
                "Vplppasindsg1": self.ppp + " eram",  # portatus eram
                "Vplppasindsg2": self.ppp + " eras",  # portatus eras
                "Vplppasindsg3": self.ppp + " erat",  # portatus erat
                "Vplppasindpl1": self.ppp[:-2] + "i eramus",  # portati eramus
                "Vplppasindpl2": self.ppp[:-2] + "i eratis",  # portati eratis
                "Vplppasindpl3": self.ppp[:-2] + "i erant",  # portati erant
                "Vfprpasindsg1": self.ppp + " ero",  # portatus ero
                "Vfprpasindsg2": self.ppp + " eris",  # portatus eris
                "Vfprpasindsg3": self.ppp + " erit",  # portatus erit
                "Vfprpasindpl1": self.ppp[:-2] + "i erimus",  # portati erimus
                "Vfprpasindpl2": self.ppp[:-2] + "i eritis",  # portati eritis
                "Vfprpasindpl3": self.ppp[:-2] + "i erunt",  # portati erunt
                "Vperpassbjsg1": self.ppp + " sim",  # portatus sim
                "Vperpassbjsg2": self.ppp + " sis",  # portatus sis
                "Vperpassbjsg3": self.ppp + " sit",  # portatus sit
                "Vperpassbjpl1": self.ppp[:-2] + "i simus",  # portati simus
                "Vperpassbjpl2": self.ppp[:-2] + "i sitis",  # portati sitis
                "Vperpassbjpl3": self.ppp[:-2] + "i sint",  # portati sint
                "Vplppassbjsg1": self.ppp + " essem",  # portatus essem
                "Vplppassbjsg2": self.ppp + " esses",  # portatus esses
                "Vplppassbjsg3": self.ppp + " esset",  # portatus esset
                "Vplppassbjpl1": self.ppp[:-2]
                + "i essemus",  # portati essemus
                "Vplppassbjpl2": self.ppp[:-2]
                + "i essetis",  # portati essetis
                "Vplppassbjpl3": self.ppp[:-2] + "i essent",  # portati essent
                "Vfutpasinf   ": self.ppp[:-2] + "um iri",  # portatum iri
                "Vperpasinf   ": self.ppp[:-2] + "us esse",  # portatus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect and not self.semi_deponent:
            assert self.perfect is not None
            assert self._per_stem is not None
            endings |= {
                "Vperactindsg1": self.perfect,  # portavi
                "Vperactindsg2": self._per_stem + "isti",  # portavisti
                "Vperactindsg3": self._per_stem + "it",  # portavit
                "Vperactindpl1": self._per_stem + "imus",  # portavimus
                "Vperactindpl2": self._per_stem + "istis",  # portavistis
                "Vperactindpl3": self._per_stem + "erunt",  # portaverunt
                "Vplpactindsg1": self._per_stem + "eram",  # portaveram
                "Vplpactindsg2": self._per_stem + "eras",  # portaveras
                "Vplpactindsg3": self._per_stem + "erat",  # portaverat
                "Vplpactindpl1": self._per_stem + "eramus",  # portaveramus
                "Vplpactindpl2": self._per_stem + "eratis",  # portaveratis
                "Vplpactindpl3": self._per_stem + "erant",  # portaverant
                "Vfpractindsg1": self._per_stem + "ero",  # portavero
                "Vfpractindsg2": self._per_stem + "eris",  # portaveris
                "Vfpractindsg3": self._per_stem + "erit",  # portaverit
                "Vfpractindpl1": self._per_stem + "erimus",  # portaverimus
                "Vfpractindpl2": self._per_stem + "eritis",  # portaveritis
                "Vfpractindpl3": self._per_stem + "erint",  # portaverint
                "Vperactsbjsg1": self._per_stem + "erim",  # portaverim
                "Vperactsbjsg2": self._per_stem + "eris",  # portaveris
                "Vperactsbjsg3": self._per_stem + "erit",  # portaverit
                "Vperactsbjpl1": self._per_stem + "erimus",  # portaverimus
                "Vperactsbjpl2": self._per_stem + "eritis",  # portaveritis
                "Vperactsbjpl3": self._per_stem + "erint",  # portaverint
                "Vplpactsbjsg1": self._per_stem + "issem",  # portavissem
                "Vplpactsbjsg2": self._per_stem + "isses",  # portavisses
                "Vplpactsbjsg3": self._per_stem + "isset",  # portavisset
                "Vplpactsbjpl1": self._per_stem + "issemus",  # portavissemus
                "Vplpactsbjpl2": self._per_stem + "issetis",  # portavissetis
                "Vplpactsbjpl3": self._per_stem + "issent",  # portavissent
                "Vperactinf   ": self._per_stem + "isse",  # portavisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            assert self._fap_stem is not None
            endings |= {
                "Vfutactinf   ": self._fap_stem + "us esse"  # portaturus esse
            }

        # Active forms
        endings |= {
            "Vpreactindsg1": self.present,  # porto
            "Vpreactindsg2": self._inf_stem + "as",  # portas
            "Vpreactindsg3": self._inf_stem + "at",  # portat
            "Vpreactindpl1": self._inf_stem + "amus",  # portamus
            "Vpreactindpl2": self._inf_stem + "atis",  # portatis
            "Vpreactindpl3": self._inf_stem + "ant",  # portant
            "Vimpactindsg1": self._inf_stem + "abam",  # portabam
            "Vimpactindsg2": self._inf_stem + "abas",  # portabas
            "Vimpactindsg3": self._inf_stem + "abat",  # portabat
            "Vimpactindpl1": self._inf_stem + "abamus",  # portabamus
            "Vimpactindpl2": self._inf_stem + "abatis",  # portabatis
            "Vimpactindpl3": self._inf_stem + "abant",  # portabant
            "Vfutactindsg1": self._inf_stem + "abo",  # portabo
            "Vfutactindsg2": self._inf_stem + "abis",  # portabis
            "Vfutactindsg3": self._inf_stem + "abit",  # portabit
            "Vfutactindpl1": self._inf_stem + "abimus",  # portabimus
            "Vfutactindpl2": self._inf_stem + "abitis",  # portabitis
            "Vfutactindpl3": self._inf_stem + "abunt",  # portabunt
            "Vpreactsbjsg1": self._inf_stem + "em",  # portem
            "Vpreactsbjsg2": self._inf_stem + "es",  # portes
            "Vpreactsbjsg3": self._inf_stem + "et",  # portet
            "Vpreactsbjpl1": self._inf_stem + "emus",  # portemus
            "Vpreactsbjpl2": self._inf_stem + "etis",  # portetis
            "Vpreactsbjpl3": self._inf_stem + "ent",  # portent
            "Vimpactsbjsg1": self.infinitive + "m",  # portarem
            "Vimpactsbjsg2": self.infinitive + "s",  # portares
            "Vimpactsbjsg3": self.infinitive + "t",  # portaret
            "Vimpactsbjpl1": self.infinitive + "mus",  # portaremus
            "Vimpactsbjpl2": self.infinitive + "tis",  # portaretis
            "Vimpactsbjpl3": self.infinitive + "nt",  # portarent
            "Vpreactipesg2": self._inf_stem + "a",  # porta
            "Vpreactipepl2": self._inf_stem + "ate",  # portate
            "Vfutactipesg2": self._inf_stem + "ato",  # portato
            "Vfutactipesg3": self._inf_stem + "ato",  # portato
            "Vfutactipepl2": self._inf_stem + "atote",  # portatote
            "Vfutactipepl3": self._inf_stem + "anto",  # portanto
            "Vpreactinf   ": self.infinitive,  # portare
        }

        if self.semi_deponent:
            return {
                key[:4] + "sdp" + key[7:]: value
                for key, value in endings.items()
            }

        return endings

    def _second_conjugation(self) -> Endings:
        assert self.infinitive is not None
        endings: Endings = {}

        # Passive forms
        if not self.semi_deponent:
            endings |= {
                "Vprepasindsg1": self._inf_stem + "eor",  # doceor
                "Vprepasindsg2": self._inf_stem + "eris",  # doceris
                "Vprepasindsg3": self._inf_stem + "etur",  # docetur
                "Vprepasindpl1": self._inf_stem + "emur",  # docemur
                "Vprepasindpl2": self._inf_stem + "emini",  # docemini
                "Vprepasindpl3": self._inf_stem + "entur",  # docentur
                "Vimppasindsg1": self._inf_stem + "ebar",  # docebar
                "Vimppasindsg2": self._inf_stem + "ebaris",  # docebaris
                "Vimppasindsg3": self._inf_stem + "ebatur",  # docebatur
                "Vimppasindpl1": self._inf_stem + "ebamur",  # docebamur
                "Vimppasindpl2": self._inf_stem + "ebamini",  # docebamini
                "Vimppasindpl3": self._inf_stem + "ebantur",  # docebantur
                "Vfutpasindsg1": self._inf_stem + "ebor",  # docebor
                "Vfutpasindsg2": self._inf_stem + "eberis",  # doceberis
                "Vfutpasindsg3": self._inf_stem + "ebitur",  # docebitur
                "Vfutpasindpl1": self._inf_stem + "ebimur",  # docebimur
                "Vfutpasindpl2": self._inf_stem + "ebimini",  # docebimini
                "Vfutpasindpl3": self._inf_stem + "ebuntur",  # docebuntur
                "Vprepassbjsg1": self._inf_stem + "ear",  # docear
                "Vprepassbjsg2": self._inf_stem + "earis",  # docearis
                "Vprepassbjsg3": self._inf_stem + "eatur",  # doceatur
                "Vprepassbjpl1": self._inf_stem + "eamur",  # doceamur
                "Vprepassbjpl2": self._inf_stem + "eamini",  # doceamini
                "Vprepassbjpl3": self._inf_stem + "eantur",  # doceantur
                "Vimppassbjsg1": self.infinitive + "r",  # docerer
                "Vimppassbjsg2": self.infinitive + "ris",  # docereris
                "Vimppassbjsg3": self.infinitive + "tur",  # doceretur
                "Vimppassbjpl1": self.infinitive + "mur",  # doceremur
                "Vimppassbjpl2": self.infinitive + "mini",  # doceremini
                "Vimppassbjpl3": self.infinitive + "ntur",  # docerentur
                "Vprepasipesg2": self._inf_stem + "ere",  # docere
                "Vprepasipepl2": self._inf_stem + "emini",  # docemini
                "Vfutpasipesg2": self._inf_stem + "etor",  # docetor
                "Vfutpasipesg3": self._inf_stem + "etor",  # docetor
                "Vfutpasipepl3": self._inf_stem + "entor",  # docentor
                "Vprepasinf   ": self._inf_stem + "eri",  # doceri
            }

        # Passive forms that use ppp
        if not self.no_ppp:
            assert self.ppp is not None
            endings |= {
                "Vperpasindsg1": self.ppp + " sum",  # doctus sum
                "Vperpasindsg2": self.ppp + " es",  # doctus es
                "Vperpasindsg3": self.ppp + " est",  # doctus est
                "Vperpasindpl1": self.ppp[:-2] + "i sumus",  # docti sumus
                "Vperpasindpl2": self.ppp[:-2] + "i estis",  # docti estis
                "Vperpasindpl3": self.ppp[:-2] + "i sunt",  # docti sunt
                "Vplppasindsg1": self.ppp + " eram",  # doctus eram
                "Vplppasindsg2": self.ppp + " eras",  # doctus eras
                "Vplppasindsg3": self.ppp + " erat",  # doctus erat
                "Vplppasindpl1": self.ppp[:-2] + "i eramus",  # docti eramus
                "Vplppasindpl2": self.ppp[:-2] + "i eratis",  # docti eratis
                "Vplppasindpl3": self.ppp[:-2] + "i erant",  # docti erant
                "Vfprpasindsg1": self.ppp + " ero",  # doctus ero
                "Vfprpasindsg2": self.ppp + " eris",  # doctus eris
                "Vfprpasindsg3": self.ppp + " erit",  # doctus erit
                "Vfprpasindpl1": self.ppp[:-2] + "i erimus",  # docti erimus
                "Vfprpasindpl2": self.ppp[:-2] + "i eritis",  # docti eritis
                "Vfprpasindpl3": self.ppp[:-2] + "i erunt",  # docti erunt
                "Vperpassbjsg1": self.ppp + " sim",  # doctus sim
                "Vperpassbjsg2": self.ppp + " sis",  # doctus sis
                "Vperpassbjsg3": self.ppp + " sit",  # doctus sit
                "Vperpassbjpl1": self.ppp[:-2] + "i simus",  # docti simus
                "Vperpassbjpl2": self.ppp[:-2] + "i sitis",  # docti sitis
                "Vperpassbjpl3": self.ppp[:-2] + "i sint",  # docti sint
                "Vplppassbjsg1": self.ppp + " essem",  # doctus essem
                "Vplppassbjsg2": self.ppp + " esses",  # doctus esses
                "Vplppassbjsg3": self.ppp + " esset",  # doctus esset
                "Vplppassbjpl1": self.ppp[:-2] + "i essemus",  # docti essemus
                "Vplppassbjpl2": self.ppp[:-2] + "i essetis",  # docti essetis
                "Vplppassbjpl3": self.ppp[:-2] + "i essent",  # docti essent
                "Vfutpasinf   ": self.ppp[:-2] + "um iri",  # doctum iri
                "Vperpasinf   ": self.ppp[:-2] + "us esse",  # doctus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect and not self.semi_deponent:
            assert self.perfect is not None
            assert self._per_stem is not None
            endings |= {
                "Vperactindsg1": self.perfect,  # docui
                "Vperactindsg2": self._per_stem + "isti",  # docuisit
                "Vperactindsg3": self._per_stem + "it",  # docuit
                "Vperactindpl1": self._per_stem + "imus",  # docuimus
                "Vperactindpl2": self._per_stem + "istis",  # docuistis
                "Vperactindpl3": self._per_stem + "erunt",  # docuerunt
                "Vplpactindsg1": self._per_stem + "eram",  # docueram
                "Vplpactindsg2": self._per_stem + "eras",  # docueras
                "Vplpactindsg3": self._per_stem + "erat",  # docuerat
                "Vplpactindpl1": self._per_stem + "eramus",  # docueramus
                "Vplpactindpl2": self._per_stem + "eratis",  # docueratis
                "Vplpactindpl3": self._per_stem + "erant",  # docuerant
                "Vfpractindsg1": self._per_stem + "ero",  # docuero
                "Vfpractindsg2": self._per_stem + "eris",  # docueris
                "Vfpractindsg3": self._per_stem + "erit",  # docuerit
                "Vfpractindpl1": self._per_stem + "erimus",  # docuerimus
                "Vfpractindpl2": self._per_stem + "eritis",  # docueritis
                "Vfpractindpl3": self._per_stem + "erint",  # docuerint
                "Vperactsbjsg1": self._per_stem + "erim",  # docuerim
                "Vperactsbjsg2": self._per_stem + "eris",  # docueris
                "Vperactsbjsg3": self._per_stem + "erit",  # docuerit
                "Vperactsbjpl1": self._per_stem + "erimus",  # docuerimus
                "Vperactsbjpl2": self._per_stem + "eritis",  # docueritis
                "Vperactsbjpl3": self._per_stem + "erint",  # docuerint
                "Vplpactsbjsg1": self._per_stem + "issem",  # docuissem
                "Vplpactsbjsg2": self._per_stem + "isses",  # docuisses
                "Vplpactsbjsg3": self._per_stem + "isset",  # docuisset
                "Vplpactsbjpl1": self._per_stem + "issemus",  # docuissmus
                "Vplpactsbjpl2": self._per_stem + "issetis",  # docuissetis
                "Vplpactsbjpl3": self._per_stem + "issent",  # docuissent
                "Vperactinf   ": self._per_stem + "isse",  # docuisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            assert self._fap_stem is not None
            endings |= {
                "Vfutactinf   ": self._fap_stem + "us esse"  # docturus esse
            }

        # Active forms
        endings |= {
            "Vpreactindsg1": self.present,  # doceo
            "Vpreactindsg2": self._inf_stem + "es",  # doces
            "Vpreactindsg3": self._inf_stem + "et",  # docet
            "Vpreactindpl1": self._inf_stem + "emus",  # docemus
            "Vpreactindpl2": self._inf_stem + "etis",  # docetis
            "Vpreactindpl3": self._inf_stem + "ent",  # docent
            "Vimpactindsg1": self._inf_stem + "ebam",  # docebam
            "Vimpactindsg2": self._inf_stem + "ebas",  # docebas
            "Vimpactindsg3": self._inf_stem + "ebat",  # docebat
            "Vimpactindpl1": self._inf_stem + "ebamus",  # docebamus
            "Vimpactindpl2": self._inf_stem + "ebatis",  # docebatis
            "Vimpactindpl3": self._inf_stem + "ebant",  # docebant
            "Vfutactindsg1": self._inf_stem + "ebo",  # docebo
            "Vfutactindsg2": self._inf_stem + "ebis",  # docebis
            "Vfutactindsg3": self._inf_stem + "ebit",  # docebit
            "Vfutactindpl1": self._inf_stem + "ebimus",  # docebimus
            "Vfutactindpl2": self._inf_stem + "ebitis",  # docebitis
            "Vfutactindpl3": self._inf_stem + "ebunt",  # docebunt
            "Vpreactsbjsg1": self._inf_stem + "eam",  # doceam
            "Vpreactsbjsg2": self._inf_stem + "eas",  # doceas
            "Vpreactsbjsg3": self._inf_stem + "eat",  # doceat
            "Vpreactsbjpl1": self._inf_stem + "eamus",  # doceamus
            "Vpreactsbjpl2": self._inf_stem + "eatis",  # doceatis
            "Vpreactsbjpl3": self._inf_stem + "eant",  # doceant
            "Vimpactsbjsg1": self.infinitive + "m",  # docerem
            "Vimpactsbjsg2": self.infinitive + "s",  # doceres
            "Vimpactsbjsg3": self.infinitive + "t",  # doceret
            "Vimpactsbjpl1": self.infinitive + "mus",  # doceremus
            "Vimpactsbjpl2": self.infinitive + "tis",  # doceretis
            "Vimpactsbjpl3": self.infinitive + "nt",  # docerent
            "Vpreactipesg2": self._inf_stem + "e",  # doce
            "Vpreactipepl2": self._inf_stem + "ete",  # docete
            "Vfutactipesg2": self._inf_stem + "eto",  # doceto
            "Vfutactipesg3": self._inf_stem + "eto",  # doceto
            "Vfutactipepl2": self._inf_stem + "etote",  # docetote
            "Vfutactipepl3": self._inf_stem + "ento",  # docento
            "Vpreactinf   ": self.infinitive,  # docere
        }

        if self.semi_deponent:
            return {
                key[:4] + "sdp" + key[7:]: value
                for key, value in endings.items()
            }

        return endings

    def _third_conjugation(self) -> Endings:
        assert self.infinitive is not None
        endings: Endings = {}

        # Passive forms
        if not self.semi_deponent:
            endings |= {
                "Vprepasindsg1": self._inf_stem + "or",  # trahor
                "Vprepasindsg2": self._inf_stem + "eris",  # traheris
                "Vprepasindsg3": self._inf_stem + "itur",  # trahitur
                "Vprepasindpl1": self._inf_stem + "imur",  # trahimur
                "Vprepasindpl2": self._inf_stem + "imini",  # trahimini
                "Vprepasindpl3": self._inf_stem + "untur",  # trahuntur
                "Vimppasindsg1": self._inf_stem + "ebar",  # trahebar
                "Vimppasindsg2": self._inf_stem + "ebaris",  # trahebaris
                "Vimppasindsg3": self._inf_stem + "ebatur",  # trahebatur
                "Vimppasindpl1": self._inf_stem + "ebamur",  # trahebamur
                "Vimppasindpl2": self._inf_stem + "ebamini",  # trahebamini
                "Vimppasindpl3": self._inf_stem + "ebantur",  # trahebantur
                "Vfutpasindsg1": self._inf_stem + "ar",  # trahar
                "Vfutpasindsg2": self._inf_stem + "eris",  # traheris
                "Vfutpasindsg3": self._inf_stem + "etur",  # trahetur
                "Vfutpasindpl1": self._inf_stem + "emur",  # trahemur
                "Vfutpasindpl2": self._inf_stem + "emini",  # trahemini
                "Vfutpasindpl3": self._inf_stem + "entur",  # trahentur
                "Vprepassbjsg1": self._inf_stem + "ar",  # trahar
                "Vprepassbjsg2": self._inf_stem + "aris",  # traharis
                "Vprepassbjsg3": self._inf_stem + "atur",  # trahatur
                "Vprepassbjpl1": self._inf_stem + "amur",  # trahamur
                "Vprepassbjpl2": self._inf_stem + "amini",  # trahamini
                "Vprepassbjpl3": self._inf_stem + "antur",  # trahantur
                "Vimppassbjsg1": self.infinitive + "r",  # traherer
                "Vimppassbjsg2": self.infinitive + "ris",  # trahereris
                "Vimppassbjsg3": self.infinitive + "tur",  # traheretur
                "Vimppassbjpl1": self.infinitive + "mur",  # traheremur
                "Vimppassbjpl2": self.infinitive + "mini",  # traheremini
                "Vimppassbjpl3": self.infinitive + "ntur",  # traherentur
                "Vprepasipesg2": self._inf_stem + "ere",  # trahere
                "Vprepasipepl2": self._inf_stem + "imini",  # trahimini
                "Vfutpasipesg2": self._inf_stem + "itor",  # trahitor
                "Vfutpasipesg3": self._inf_stem + "itor",  # trahitor
                "Vfutpasipepl3": self._inf_stem + "untor",  # trahuntor
                "Vprepasinf   ": self._inf_stem + "i",  # trahi
            }

        # Passive forms that use ppp
        if not self.no_ppp:
            assert self.ppp is not None
            endings |= {
                "Vperpasindsg1": self.ppp + " sum",  # tractus sum
                "Vperpasindsg2": self.ppp + " es",  # tractus es
                "Vperpasindsg3": self.ppp + " est",  # tractus est
                "Vperpasindpl1": self.ppp[:-2] + "i sumus",  # tracti sumus
                "Vperpasindpl2": self.ppp[:-2] + "i estis",  # tracti estis
                "Vperpasindpl3": self.ppp[:-2] + "i sunt",  # tracti sunt
                "Vplppasindsg1": self.ppp + " eram",  # tractus eram
                "Vplppasindsg2": self.ppp + " eras",  # tractus eras
                "Vplppasindsg3": self.ppp + " erat",  # tractus erat
                "Vplppasindpl1": self.ppp[:-2] + "i eramus",  # tracti eramus
                "Vplppasindpl2": self.ppp[:-2] + "i eratis",  # tracti eratis
                "Vplppasindpl3": self.ppp[:-2] + "i erant",  # tracti erant
                "Vfprpasindsg1": self.ppp + " ero",  # tractus ero
                "Vfprpasindsg2": self.ppp + " eris",  # tractus eris
                "Vfprpasindsg3": self.ppp + " erit",  # tractus erit
                "Vfprpasindpl1": self.ppp[:-2] + "i erimus",  # tracti erimus
                "Vfprpasindpl2": self.ppp[:-2] + "i eritis",  # tracti eritis
                "Vfprpasindpl3": self.ppp[:-2] + "i erunt",  # tracti erunt
                "Vperpassbjsg1": self.ppp + " sim",  # tractus sim
                "Vperpassbjsg2": self.ppp + " sis",  # tractus sis
                "Vperpassbjsg3": self.ppp + " sit",  # tractus sit
                "Vperpassbjpl1": self.ppp[:-2] + "i simus",  # tracti simus
                "Vperpassbjpl2": self.ppp[:-2] + "i sitis",  # tracti sitis
                "Vperpassbjpl3": self.ppp[:-2] + "i sint",  # tracti sint
                "Vplppassbjsg1": self.ppp + " essem",  # tractus essem
                "Vplppassbjsg2": self.ppp + " esses",  # tractus esses
                "Vplppassbjsg3": self.ppp + " esset",  # tractus esset
                "Vplppassbjpl1": self.ppp[:-2] + "i essemus",  # tracti essemus
                "Vplppassbjpl2": self.ppp[:-2] + "i essetis",  # tracti essetis
                "Vplppassbjpl3": self.ppp[:-2] + "i essent",  # tracti essent
                "Vfutpasinf   ": self.ppp[:-2] + "um iri",  # tractum iri
                "Vperpasinf   ": self.ppp[:-2] + "us esse",  # tractus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect and not self.semi_deponent:
            assert self.perfect is not None
            assert self._per_stem is not None
            endings |= {
                "Vperactindsg1": self.perfect,  # traxi
                "Vperactindsg2": self._per_stem + "isti",  # traxisti
                "Vperactindsg3": self._per_stem + "it",  # traxit
                "Vperactindpl1": self._per_stem + "imus",  # traximus
                "Vperactindpl2": self._per_stem + "istis",  # traxistis
                "Vperactindpl3": self._per_stem + "erunt",  # traxerunt
                "Vplpactindsg1": self._per_stem + "eram",  # traxeram
                "Vplpactindsg2": self._per_stem + "eras",  # traxeras
                "Vplpactindsg3": self._per_stem + "erat",  # traxerat
                "Vplpactindpl1": self._per_stem + "eramus",  # traxeramus
                "Vplpactindpl2": self._per_stem + "eratis",  # traxeratis
                "Vplpactindpl3": self._per_stem + "erant",  # traxerant
                "Vfpractindsg1": self._per_stem + "ero",  # traxero
                "Vfpractindsg2": self._per_stem + "eris",  # traxeris
                "Vfpractindsg3": self._per_stem + "erit",  # traxerit
                "Vfpractindpl1": self._per_stem + "erimus",  # traxerimus
                "Vfpractindpl2": self._per_stem + "eritis",  # traxeritis
                "Vfpractindpl3": self._per_stem + "erint",  # traxerint
                "Vperactsbjsg1": self._per_stem + "erim",  # traxerim
                "Vperactsbjsg2": self._per_stem + "eris",  # traxeris
                "Vperactsbjsg3": self._per_stem + "erit",  # traxerit
                "Vperactsbjpl1": self._per_stem + "erimus",  # traxerimus
                "Vperactsbjpl2": self._per_stem + "eritis",  # traxeritis
                "Vperactsbjpl3": self._per_stem + "erint",  # traxerint
                "Vplpactsbjsg1": self._per_stem + "issem",  # traxissem
                "Vplpactsbjsg2": self._per_stem + "isses",  # traxisses
                "Vplpactsbjsg3": self._per_stem + "isset",  # traxisset
                "Vplpactsbjpl1": self._per_stem + "issemus",  # traxissemus
                "Vplpactsbjpl2": self._per_stem + "issetis",  # traxissetis
                "Vplpactsbjpl3": self._per_stem + "issent",  # traxissent
                "Vperactinf   ": self._per_stem + "isse",  # traxisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            assert self._fap_stem is not None
            endings |= {
                "Vfutactinf   ": self._fap_stem + "us esse"  # tracturus esse
            }

        # Active forms
        endings |= {
            "Vpreactindsg1": self.present,  # traho
            "Vpreactindsg2": self._inf_stem + "is",  # trahis
            "Vpreactindsg3": self._inf_stem + "it",  # trahit
            "Vpreactindpl1": self._inf_stem + "imus",  # trahimus
            "Vpreactindpl2": self._inf_stem + "itis",  # trahitis
            "Vpreactindpl3": self._inf_stem + "unt",  # trahunt
            "Vimpactindsg1": self._inf_stem + "ebam",  # trahebam
            "Vimpactindsg2": self._inf_stem + "ebas",  # trahebas
            "Vimpactindsg3": self._inf_stem + "ebat",  # trahebat
            "Vimpactindpl1": self._inf_stem + "ebamus",  # trahebamus
            "Vimpactindpl2": self._inf_stem + "ebatis",  # trahebatis
            "Vimpactindpl3": self._inf_stem + "ebant",  # trahebant
            "Vfutactindsg1": self._inf_stem + "am",  # traham
            "Vfutactindsg2": self._inf_stem + "es",  # trahes
            "Vfutactindsg3": self._inf_stem + "et",  # trahet
            "Vfutactindpl1": self._inf_stem + "emus",  # trahemus
            "Vfutactindpl2": self._inf_stem + "etis",  # trahetis
            "Vfutactindpl3": self._inf_stem + "ent",  # trahent
            "Vpreactsbjsg1": self._inf_stem + "am",  # traham
            "Vpreactsbjsg2": self._inf_stem + "as",  # trahas
            "Vpreactsbjsg3": self._inf_stem + "at",  # trahat
            "Vpreactsbjpl1": self._inf_stem + "amus",  # trahamus
            "Vpreactsbjpl2": self._inf_stem + "atis",  # trahatis
            "Vpreactsbjpl3": self._inf_stem + "ant",  # trahant
            "Vimpactsbjsg1": self.infinitive + "m",  # traherem
            "Vimpactsbjsg2": self.infinitive + "s",  # traheres
            "Vimpactsbjsg3": self.infinitive + "t",  # traheret
            "Vimpactsbjpl1": self.infinitive + "mus",  # traheremus
            "Vimpactsbjpl2": self.infinitive + "tis",  # traheretis
            "Vimpactsbjpl3": self.infinitive + "nt",  # traherent
            "Vpreactipesg2": self._inf_stem + "e",  # trahe
            "Vpreactipepl2": self._inf_stem + "ite",  # trahite
            "Vfutactipesg2": self._inf_stem + "ito",  # trahito
            "Vfutactipesg3": self._inf_stem + "ito",  # trahito
            "Vfutactipepl2": self._inf_stem + "itote",  # trahitote
            "Vfutactipepl3": self._inf_stem + "unto",  # trahunto
            "Vpreactinf   ": self.infinitive,  # trahere
        }

        if self.semi_deponent:
            return {
                key[:4] + "sdp" + key[7:]: value
                for key, value in endings.items()
            }

        return endings

    def _fourth_conjugation(self) -> Endings:
        assert self.infinitive is not None
        endings: Endings = {}

        # Passive forms
        if not self.semi_deponent:
            endings |= {
                "Vprepasindsg1": self._inf_stem + "ior",  # audior
                "Vprepasindsg2": self._inf_stem + "iris",  # audiris
                "Vprepasindsg3": self._inf_stem + "itur",  # auditur
                "Vprepasindpl1": self._inf_stem + "imur",  # audimur
                "Vprepasindpl2": self._inf_stem + "imini",  # audimini
                "Vprepasindpl3": self._inf_stem + "iuntur",  # audiuntur
                "Vimppasindsg1": self._inf_stem + "iebar",  # audiebar
                "Vimppasindsg2": self._inf_stem + "iebaris",  # audiebaris
                "Vimppasindsg3": self._inf_stem + "iebatur",  # audiebatur
                "Vimppasindpl1": self._inf_stem + "iebamur",  # audiebamur
                "Vimppasindpl2": self._inf_stem + "iebamini",  # audiebamini
                "Vimppasindpl3": self._inf_stem + "iebantur",  # audiebantur
                "Vfutpasindsg1": self._inf_stem + "iar",  # audiar
                "Vfutpasindsg2": self._inf_stem + "ieris",  # audieris
                "Vfutpasindsg3": self._inf_stem + "ietur",  # audietur
                "Vfutpasindpl1": self._inf_stem + "iemur",  # audiemur
                "Vfutpasindpl2": self._inf_stem + "iemini",  # audiemini
                "Vfutpasindpl3": self._inf_stem + "ientur",  # audientur
                "Vprepassbjsg1": self._inf_stem + "iar",  # audiar
                "Vprepassbjsg2": self._inf_stem + "iaris",  # audiaris
                "Vprepassbjsg3": self._inf_stem + "iatur",  # audiatur
                "Vprepassbjpl1": self._inf_stem + "iamur",  # audiamur
                "Vprepassbjpl2": self._inf_stem + "iamini",  # audiamini
                "Vprepassbjpl3": self._inf_stem + "iantur",  # audiantur
                "Vimppassbjsg1": self.infinitive + "r",  # audirer
                "Vimppassbjsg2": self.infinitive + "ris",  # audireris
                "Vimppassbjsg3": self.infinitive + "tur",  # audiretur
                "Vimppassbjpl1": self.infinitive + "mur",  # audiremur
                "Vimppassbjpl2": self.infinitive + "mini",  # audiremini
                "Vimppassbjpl3": self.infinitive + "ntur",  # audirentur
                "Vprepasipesg2": self._inf_stem + "ire",  # audire
                "Vprepasipepl2": self._inf_stem + "imini",  # audimini
                "Vfutpasipesg2": self._inf_stem + "itor",  # auditor
                "Vfutpasipesg3": self._inf_stem + "itor",  # auditor
                "Vfutpasipepl3": self._inf_stem + "iuntor",  # audiuntor
                "Vprepasinf   ": self._inf_stem + "iri",  # audiri
            }

        # Passive forms that use ppp
        if not self.no_ppp:
            assert self.ppp is not None
            endings |= {
                "Vperpasindsg1": self.ppp + " sum",  # auditus sum
                "Vperpasindsg2": self.ppp + " es",  # auditus es
                "Vperpasindsg3": self.ppp + " est",  # auditus est
                "Vperpasindpl1": self.ppp[:-2] + "i sumus",  # auditi sumus
                "Vperpasindpl2": self.ppp[:-2] + "i estis",  # auditi estis
                "Vperpasindpl3": self.ppp[:-2] + "i sunt",  # auditi sunt
                "Vplppasindsg1": self.ppp + " eram",  # auditus eram
                "Vplppasindsg2": self.ppp + " eras",  # auditus eras
                "Vplppasindsg3": self.ppp + " erat",  # auditus erat
                "Vplppasindpl1": self.ppp[:-2] + "i eramus",  # auditi eramus
                "Vplppasindpl2": self.ppp[:-2] + "i eratis",  # auditi eratis
                "Vplppasindpl3": self.ppp[:-2] + "i erant",  # auditi erant
                "Vfprpasindsg1": self.ppp + " ero",  # auditus ero
                "Vfprpasindsg2": self.ppp + " eris",  # auditus eris
                "Vfprpasindsg3": self.ppp + " erit",  # auditus erit
                "Vfprpasindpl1": self.ppp[:-2] + "i erimus",  # auditi erimus
                "Vfprpasindpl2": self.ppp[:-2] + "i eritis",  # auditi eritis
                "Vfprpasindpl3": self.ppp[:-2] + "i erunt",  # auditi erunt
                "Vperpassbjsg1": self.ppp + " sim",  # auditus sim
                "Vperpassbjsg2": self.ppp + " sis",  # auditus sis
                "Vperpassbjsg3": self.ppp + " sit",  # auditus sit
                "Vperpassbjpl1": self.ppp[:-2] + "i simus",  # auditi simus
                "Vperpassbjpl2": self.ppp[:-2] + "i sitis",  # auditi sitis
                "Vperpassbjpl3": self.ppp[:-2] + "i sint",  # auditi sint
                "Vplppassbjsg1": self.ppp + " essem",  # auditus essem
                "Vplppassbjsg2": self.ppp + " esses",  # auditus esses
                "Vplppassbjsg3": self.ppp + " esset",  # auditus esset
                "Vplppassbjpl1": self.ppp[:-2] + "i essemus",  # auditi essemus
                "Vplppassbjpl2": self.ppp[:-2] + "i essetis",  # auditi essetis
                "Vplppassbjpl3": self.ppp[:-2] + "i essent",  # auditi essent
                "Vfutpasinf   ": self.ppp[:-2] + "um iri",  # auditum iri
                "Vperpasinf   ": self.ppp[:-2] + "us esse",  # auditus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect and not self.semi_deponent:
            assert self.perfect is not None
            assert self._per_stem is not None
            endings |= {
                "Vperactindsg1": self.perfect,  # audivi
                "Vperactindsg2": self._per_stem + "isti",  # audivisti
                "Vperactindsg3": self._per_stem + "it",  # audivit
                "Vperactindpl1": self._per_stem + "imus",  # audivimus
                "Vperactindpl2": self._per_stem + "istis",  # audivistis
                "Vperactindpl3": self._per_stem + "erunt",  # audiverunt
                "Vplpactindsg1": self._per_stem + "eram",  # audiveram
                "Vplpactindsg2": self._per_stem + "eras",  # audiveras
                "Vplpactindsg3": self._per_stem + "erat",  # audiverat
                "Vplpactindpl1": self._per_stem + "eramus",  # audiveramus
                "Vplpactindpl2": self._per_stem + "eratis",  # audiveratis
                "Vplpactindpl3": self._per_stem + "erant",  # audiverant
                "Vfpractindsg1": self._per_stem + "ero",  # audivero
                "Vfpractindsg2": self._per_stem + "eris",  # audiveris
                "Vfpractindsg3": self._per_stem + "erit",  # audiverit
                "Vfpractindpl1": self._per_stem + "erimus",  # audiverimus
                "Vfpractindpl2": self._per_stem + "eritis",  # audiveritis
                "Vfpractindpl3": self._per_stem + "erint",  # audiverint
                "Vperactsbjsg1": self._per_stem + "erim",  # audiverim
                "Vperactsbjsg2": self._per_stem + "eris",  # audiveris
                "Vperactsbjsg3": self._per_stem + "erit",  # audiverit
                "Vperactsbjpl1": self._per_stem + "erimus",  # audiverimus
                "Vperactsbjpl2": self._per_stem + "eritis",  # audiveritis
                "Vperactsbjpl3": self._per_stem + "erint",  # audiverint
                "Vplpactsbjsg1": self._per_stem + "issem",  # audivissem
                "Vplpactsbjsg2": self._per_stem + "isses",  # audivisses
                "Vplpactsbjsg3": self._per_stem + "isset",  # audivisset
                "Vplpactsbjpl1": self._per_stem + "issemus",  # audivissemus
                "Vplpactsbjpl2": self._per_stem + "issetis",  # audivissetis
                "Vplpactsbjpl3": self._per_stem + "issent",  # audivissent
                "Vperactinf   ": self._per_stem + "isse",  # audivisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            assert self._fap_stem is not None
            endings |= {
                "Vfutactinf   ": self._fap_stem + "us esse"  # auditurus esse
            }

        # Active forms
        endings |= {
            "Vpreactindsg1": self.present,  # audio
            "Vpreactindsg2": self._inf_stem + "is",  # audis
            "Vpreactindsg3": self._inf_stem + "it",  # audit
            "Vpreactindpl1": self._inf_stem + "imus",  # audimus
            "Vpreactindpl2": self._inf_stem + "itis",  # auditis
            "Vpreactindpl3": self._inf_stem + "iunt",  # audiunt
            "Vimpactindsg1": self._inf_stem + "iebam",  # audiebam
            "Vimpactindsg2": self._inf_stem + "iebas",  # audiebas
            "Vimpactindsg3": self._inf_stem + "iebat",  # audiebat
            "Vimpactindpl1": self._inf_stem + "iebamus",  # audiebamus
            "Vimpactindpl2": self._inf_stem + "iebatis",  # audiebatis
            "Vimpactindpl3": self._inf_stem + "iebant",  # audiebant
            "Vfutactindsg1": self._inf_stem + "iam",  # veniam
            "Vfutactindsg2": self._inf_stem + "ies",  # venies
            "Vfutactindsg3": self._inf_stem + "iet",  # veniet
            "Vfutactindpl1": self._inf_stem + "iemus",  # veniemus
            "Vfutactindpl2": self._inf_stem + "ietis",  # venietis
            "Vfutactindpl3": self._inf_stem + "ient",  # venient
            "Vpreactsbjsg1": self._inf_stem + "iam",  # audiam
            "Vpreactsbjsg2": self._inf_stem + "ias",  # audias
            "Vpreactsbjsg3": self._inf_stem + "iat",  # audiat
            "Vpreactsbjpl1": self._inf_stem + "iamus",  # audiamus
            "Vpreactsbjpl2": self._inf_stem + "iatis",  # audiatis
            "Vpreactsbjpl3": self._inf_stem + "iant",  # audiant
            "Vimpactsbjsg1": self.infinitive + "m",  # audirem
            "Vimpactsbjsg2": self.infinitive + "s",  # audires
            "Vimpactsbjsg3": self.infinitive + "t",  # audiret
            "Vimpactsbjpl1": self.infinitive + "mus",  # audiremus
            "Vimpactsbjpl2": self.infinitive + "tis",  # audiretis
            "Vimpactsbjpl3": self.infinitive + "nt",  # audirent
            "Vpreactipesg2": self._inf_stem + "i",  # audi
            "Vpreactipepl2": self._inf_stem + "ite",  # audite
            "Vfutactipesg2": self._inf_stem + "ito",  # audito
            "Vfutactipesg3": self._inf_stem + "ito",  # audito
            "Vfutactipepl2": self._inf_stem + "itote",  # auditote
            "Vfutactipepl3": self._inf_stem + "iunto",  # audiunto
            "Vpreactinf   ": self.infinitive,  # audire
        }

        if self.semi_deponent:
            return {
                key[:4] + "sdp" + key[7:]: value
                for key, value in endings.items()
            }

        return endings

    def _mixed_conjugation(self) -> Endings:
        assert self.infinitive is not None
        endings: Endings = {}

        # Passive forms
        if not self.semi_deponent:
            endings |= {
                "Vprepasindsg1": self._inf_stem + "ior",  # capior
                "Vprepasindsg2": self._inf_stem + "eris",  # caperis
                "Vprepasindsg3": self._inf_stem + "itur",  # capitur
                "Vprepasindpl1": self._inf_stem + "imur",  # capimur
                "Vprepasindpl2": self._inf_stem + "imini",  # capimini
                "Vprepasindpl3": self._inf_stem + "iuntur",  # capiuntur
                "Vimppasindsg1": self._inf_stem + "iebar",  # capiebar
                "Vimppasindsg2": self._inf_stem + "iebaris",  # capiebaris
                "Vimppasindsg3": self._inf_stem + "iebatur",  # capiebatur
                "Vimppasindpl1": self._inf_stem + "iebamur",  # capiebamur
                "Vimppasindpl2": self._inf_stem + "iebamini",  # capiebamini
                "Vimppasindpl3": self._inf_stem + "iebantur",  # capiebantur
                "Vfutpasindsg1": self._inf_stem + "iar",  # capiar
                "Vfutpasindsg2": self._inf_stem + "ieris",  # capieris
                "Vfutpasindsg3": self._inf_stem + "ietur",  # capietur
                "Vfutpasindpl1": self._inf_stem + "iemur",  # capiemur
                "Vfutpasindpl2": self._inf_stem + "iemini",  # capiemini
                "Vfutpasindpl3": self._inf_stem + "ientur",  # capientur
                "Vprepassbjsg1": self._inf_stem + "iar",  # capiar
                "Vprepassbjsg2": self._inf_stem + "iaris",  # capiaris
                "Vprepassbjsg3": self._inf_stem + "iatur",  # capiatur
                "Vprepassbjpl1": self._inf_stem + "iamur",  # capiamur
                "Vprepassbjpl2": self._inf_stem + "iamini",  # capiamini
                "Vprepassbjpl3": self._inf_stem + "iantur",  # capiantur
                "Vimppassbjsg1": self.infinitive + "r",  # caperer
                "Vimppassbjsg2": self.infinitive + "ris",  # capereris
                "Vimppassbjsg3": self.infinitive + "tur",  # caperetur
                "Vimppassbjpl1": self.infinitive + "mur",  # caperemur
                "Vimppassbjpl2": self.infinitive + "mini",  # caperemini
                "Vimppassbjpl3": self.infinitive + "ntur",  # caperentur
                "Vprepasipesg2": self._inf_stem + "ere",  # capere
                "Vprepasipepl2": self._inf_stem + "imini",  # capimini
                "Vfutpasipesg2": self._inf_stem + "itor",  # capitor
                "Vfutpasipesg3": self._inf_stem + "itor",  # capitor
                "Vfutpasipepl3": self._inf_stem + "iuntor",  # capiuntor
                "Vprepasinf   ": self._inf_stem + "i",  # capi
            }

        # Passive forms that use ppp
        if not self.no_ppp:
            assert self.ppp is not None
            endings |= {
                "Vperpasindsg1": self.ppp + " sum",  # captus sum
                "Vperpasindsg2": self.ppp + " es",  # captus es
                "Vperpasindsg3": self.ppp + " est",  # captus est
                "Vperpasindpl1": self.ppp[:-2] + "i sumus",  # capti sumus
                "Vperpasindpl2": self.ppp[:-2] + "i estis",  # capti estis
                "Vperpasindpl3": self.ppp[:-2] + "i sunt",  # capti sunt
                "Vplppasindsg1": self.ppp + " eram",  # captus eram
                "Vplppasindsg2": self.ppp + " eras",  # captus eras
                "Vplppasindsg3": self.ppp + " erat",  # captus erat
                "Vplppasindpl1": self.ppp[:-2] + "i eramus",  # capti eramus
                "Vplppasindpl2": self.ppp[:-2] + "i eratis",  # capti eratis
                "Vplppasindpl3": self.ppp[:-2] + "i erant",  # capti erant
                "Vfprpasindsg1": self.ppp + " ero",  # captus ero
                "Vfprpasindsg2": self.ppp + " eris",  # captus eris
                "Vfprpasindsg3": self.ppp + " erit",  # captus erit
                "Vfprpasindpl1": self.ppp[:-2] + "i erimus",  # capti erimus
                "Vfprpasindpl2": self.ppp[:-2] + "i eritis",  # capti eritis
                "Vfprpasindpl3": self.ppp[:-2] + "i erunt",  # capti erunt
                "Vperpassbjsg1": self.ppp + " sim",  # captus sim
                "Vperpassbjsg2": self.ppp + " sis",  # captus sis
                "Vperpassbjsg3": self.ppp + " sit",  # captus sit
                "Vperpassbjpl1": self.ppp[:-2] + "i simus",  # capti simus
                "Vperpassbjpl2": self.ppp[:-2] + "i sitis",  # capti sitis
                "Vperpassbjpl3": self.ppp[:-2] + "i sint",  # capti sint
                "Vplppassbjsg1": self.ppp + " essem",  # captus essem
                "Vplppassbjsg2": self.ppp + " esses",  # captus esses
                "Vplppassbjsg3": self.ppp + " esset",  # captus esset
                "Vplppassbjpl1": self.ppp[:-2] + "i essemus",  # capti essemus
                "Vplppassbjpl2": self.ppp[:-2] + "i essetis",  # capti essetis
                "Vplppassbjpl3": self.ppp[:-2] + "i essent",  # capti essent
                "Vfutpasinf   ": self.ppp[:-2] + "um iri",  # captum iri
                "Vperpasinf   ": self.ppp[:-2] + "us esse",  # captus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect and not self.semi_deponent:
            assert self.perfect is not None
            assert self._per_stem is not None
            endings |= {
                "Vperactindsg1": self.perfect,  # cepi
                "Vperactindsg2": self._per_stem + "isti",  # cepisti
                "Vperactindsg3": self._per_stem + "it",  # cepit
                "Vperactindpl1": self._per_stem + "imus",  # cepimus
                "Vperactindpl2": self._per_stem + "istis",  # cepistis
                "Vperactindpl3": self._per_stem + "erunt",  # ceperunt
                "Vplpactindsg1": self._per_stem + "eram",  # ceperam
                "Vplpactindsg2": self._per_stem + "eras",  # ceperas
                "Vplpactindsg3": self._per_stem + "erat",  # ceperat
                "Vplpactindpl1": self._per_stem + "eramus",  # ceperamus
                "Vplpactindpl2": self._per_stem + "eratis",  # ceperatis
                "Vplpactindpl3": self._per_stem + "erant",  # ceperant
                "Vfpractindsg1": self._per_stem + "ero",  # cepero
                "Vfpractindsg2": self._per_stem + "eris",  # ceperis
                "Vfpractindsg3": self._per_stem + "erit",  # ceperit
                "Vfpractindpl1": self._per_stem + "erimus",  # ceperimus
                "Vfpractindpl2": self._per_stem + "eritis",  # ceperitis
                "Vfpractindpl3": self._per_stem + "erint",  # ceperint
                "Vperactsbjsg1": self._per_stem + "erim",  # ceperim
                "Vperactsbjsg2": self._per_stem + "eris",  # ceperis
                "Vperactsbjsg3": self._per_stem + "erit",  # ceperit
                "Vperactsbjpl1": self._per_stem + "erimus",  # ceperimus
                "Vperactsbjpl2": self._per_stem + "eritis",  # ceperitis
                "Vperactsbjpl3": self._per_stem + "erint",  # ceperint
                "Vplpactsbjsg1": self._per_stem + "issem",  # cepissem
                "Vplpactsbjsg2": self._per_stem + "isses",  # cepisses
                "Vplpactsbjsg3": self._per_stem + "isset",  # cepisset
                "Vplpactsbjpl1": self._per_stem + "issemus",  # cepissemus
                "Vplpactsbjpl2": self._per_stem + "issetis",  # cepissetis
                "Vplpactsbjpl3": self._per_stem + "issent",  # cepissent
                "Vperactinf   ": self._per_stem + "isse",  # cepisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            assert self._fap_stem is not None
            endings |= {
                "Vfutactinf   ": self._fap_stem + "us esse"  # capturus esse
            }

        # Active forms
        endings |= {
            "Vpreactindsg1": self.present,  # capio
            "Vpreactindsg2": self._inf_stem + "is",  # capis
            "Vpreactindsg3": self._inf_stem + "it",  # capit
            "Vpreactindpl1": self._inf_stem + "imus",  # capimus
            "Vpreactindpl2": self._inf_stem + "itis",  # capitis
            "Vpreactindpl3": self._inf_stem + "iunt",  # capiunt
            "Vimpactindsg1": self._inf_stem + "iebam",  # capiebam
            "Vimpactindsg2": self._inf_stem + "iebas",  # capiebas
            "Vimpactindsg3": self._inf_stem + "iebat",  # capiebat
            "Vimpactindpl1": self._inf_stem + "iebamus",  # capiebamus
            "Vimpactindpl2": self._inf_stem + "iebatis",  # capiebatis
            "Vimpactindpl3": self._inf_stem + "iebant",  # capiebant
            "Vfutactindsg1": self._inf_stem + "iam",  # capiam
            "Vfutactindsg2": self._inf_stem + "ies",  # capies
            "Vfutactindsg3": self._inf_stem + "iet",  # capiet
            "Vfutactindpl1": self._inf_stem + "iemus",  # capiemus
            "Vfutactindpl2": self._inf_stem + "ietis",  # capietis
            "Vfutactindpl3": self._inf_stem + "ient",  # capient
            "Vpreactsbjsg1": self._inf_stem + "iam",  # capiam
            "Vpreactsbjsg2": self._inf_stem + "ias",  # capias
            "Vpreactsbjsg3": self._inf_stem + "iat",  # capiat
            "Vpreactsbjpl1": self._inf_stem + "iamus",  # capiamus
            "Vpreactsbjpl2": self._inf_stem + "iatis",  # capiatis
            "Vpreactsbjpl3": self._inf_stem + "iant",  # capiant
            "Vimpactsbjsg1": self.infinitive + "m",  # caperem
            "Vimpactsbjsg2": self.infinitive + "s",  # caperes
            "Vimpactsbjsg3": self.infinitive + "t",  # caperet
            "Vimpactsbjpl1": self.infinitive + "mus",  # caperemus
            "Vimpactsbjpl2": self.infinitive + "tis",  # caperetis
            "Vimpactsbjpl3": self.infinitive + "nt",  # caperent
            "Vpreactipesg2": self._inf_stem + "e",  # cape
            "Vpreactipepl2": self._inf_stem + "ite",  # capite
            "Vfutactipesg2": self._inf_stem + "ito",  # capito
            "Vfutactipesg3": self._inf_stem + "ito",  # capito
            "Vfutactipepl2": self._inf_stem + "itote",  # capitote
            "Vfutactipepl3": self._inf_stem + "iunto",  # capiunto
            "Vpreactinf   ": self.infinitive,  # capere
        }

        if self.semi_deponent:
            return {
                key[:4] + "sdp" + key[7:]: value
                for key, value in endings.items()
            }

        return endings

    def _participles(self) -> Endings:
        endings: Endings = {
            "Vpreactptcmnomsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcmvocsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcmaccsg": self._preptc_stem + "ntem",  # portantem
            "Vpreactptcmgensg": self._preptc_stem + "ntis",  # portantis
            "Vpreactptcmdatsg": self._preptc_stem + "nti",  # portanti
            "Vpreactptcmablsg": MultipleEndings(
                regular=self._preptc_stem + "nti",  # portanti
                absolute=self._preptc_stem + "nte",  # portante
            ),
            "Vpreactptcmnompl": self._preptc_stem + "ntes",  # portantes
            "Vpreactptcmvocpl": self._preptc_stem + "ntes",  # portantes
            "Vpreactptcmaccpl": self._preptc_stem + "ntes",  # portantes
            "Vpreactptcmgenpl": self._preptc_stem + "ntium",  # portantium
            "Vpreactptcmdatpl": self._preptc_stem + "ntibus",  # portantibus
            "Vpreactptcmablpl": self._preptc_stem + "ntibus",  # portantibus
            "Vpreactptcfnomsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcfvocsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcfaccsg": self._preptc_stem + "ntem",  # portantem
            "Vpreactptcfgensg": self._preptc_stem + "ntis",  # portantis
            "Vpreactptcfdatsg": self._preptc_stem + "nti",  # portanti
            "Vpreactptcfablsg": MultipleEndings(
                regular=self._preptc_stem + "nti",  # portanti
                absolute=self._preptc_stem + "nte",  # portante
            ),
            "Vpreactptcfnompl": self._preptc_stem + "ntes",  # portantes
            "Vpreactptcfvocpl": self._preptc_stem + "ntes",  # portantes
            "Vpreactptcfaccpl": self._preptc_stem + "ntes",  # portantes
            "Vpreactptcfgenpl": self._preptc_stem + "ntium",  # portantium
            "Vpreactptcfdatpl": self._preptc_stem + "ntibus",  # portantibus
            "Vpreactptcfablpl": self._preptc_stem + "ntibus",  # portantibus
            "Vpreactptcnnomsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcnvocsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcnaccsg": self._preptc_stem + "ns",  # portans
            "Vpreactptcngensg": self._preptc_stem + "ntis",  # portantis
            "Vpreactptcndatsg": self._preptc_stem + "nti",  # portanti
            "Vpreactptcnablsg": MultipleEndings(
                regular=self._preptc_stem + "nti",  # portanti
                absolute=self._preptc_stem + "nte",  # portante
            ),
            "Vpreactptcnnompl": self._preptc_stem + "ntia",  # portantia
            "Vpreactptcnvocpl": self._preptc_stem + "ntia",  # portantia
            "Vpreactptcnaccpl": self._preptc_stem + "ntia",  # portantia
            "Vpreactptcngenpl": self._preptc_stem + "ntium",  # portantium
            "Vpreactptcndatpl": self._preptc_stem + "ntibus",  # portantibus
            "Vpreactptcnablpl": self._preptc_stem + "ntibus",  # portantibus
        }

        if not self.no_fap:
            endings |= {
                "Vfutpasptcmnomsg": self._preptc_stem + "ndus",  # portandus
                "Vfutpasptcmvocsg": self._preptc_stem + "nde",  # portande
                "Vfutpasptcmaccsg": self._preptc_stem + "ndum",  # portandum
                "Vfutpasptcmgensg": self._preptc_stem + "ndi",  # portandi
                "Vfutpasptcmdatsg": self._preptc_stem + "ndo",  # portando
                "Vfutpasptcmablsg": self._preptc_stem + "ndo",  # portando
                "Vfutpasptcmnompl": self._preptc_stem + "ndi",  # portandi
                "Vfutpasptcmvocpl": self._preptc_stem + "ndi",  # portandi
                "Vfutpasptcmaccpl": self._preptc_stem + "ndos",  # portandos
                "Vfutpasptcmgenpl": self._preptc_stem
                + "ndorum",  # portandorum
                "Vfutpasptcmdatpl": self._preptc_stem + "ndis",  # portandis
                "Vfutpasptcmablpl": self._preptc_stem + "ndis",  # portandis
                "Vfutpasptcfnomsg": self._preptc_stem + "nda",  # portanda
                "Vfutpasptcfvocsg": self._preptc_stem + "nda",  # portanda
                "Vfutpasptcfaccsg": self._preptc_stem + "ndam",  # portandam
                "Vfutpasptcfgensg": self._preptc_stem + "ndae",  # portandae
                "Vfutpasptcfdatsg": self._preptc_stem + "ndae",  # portandae
                "Vfutpasptcfablsg": self._preptc_stem + "nda",  # portanda
                "Vfutpasptcfnompl": self._preptc_stem + "ndae",  # portandae
                "Vfutpasptcfvocpl": self._preptc_stem + "ndae",  # portandae
                "Vfutpasptcfaccpl": self._preptc_stem + "ndas",  # portandas
                "Vfutpasptcfgenpl": self._preptc_stem
                + "ndarum",  # portandarum
                "Vfutpasptcfdatpl": self._preptc_stem + "ndis",  # portandis
                "Vfutpasptcfablpl": self._preptc_stem + "ndis",  # portandis
                "Vfutpasptcnnomsg": self._preptc_stem + "ndum",  # portandum
                "Vfutpasptcnvocsg": self._preptc_stem + "ndum",  # portandum
                "Vfutpasptcnaccsg": self._preptc_stem + "ndum",  # portandum
                "Vfutpasptcngensg": self._preptc_stem + "ndi",  # portandi
                "Vfutpasptcndatsg": self._preptc_stem + "ndo",  # portando
                "Vfutpasptcnablsg": self._preptc_stem + "ndo",  # portando
                "Vfutpasptcnnompl": self._preptc_stem + "nda",  # portanda
                "Vfutpasptcnvocpl": self._preptc_stem + "nda",  # portanda
                "Vfutpasptcnaccpl": self._preptc_stem + "nda",  # portanda
                "Vfutpasptcngenpl": self._preptc_stem
                + "ndorum",  # portandorum
                "Vfutpasptcndatpl": self._preptc_stem + "ndis",  # portandis
                "Vfutpasptcnablpl": self._preptc_stem + "ndis",  # portandis
            }

        if (not self.no_ppp) or self.fap_fourthpp:
            if not self.no_fap:
                assert self._fap_stem is not None
                endings |= {
                    "Vfutactptcmnomsg": self._fap_stem + "us",  # portaturus
                    "Vfutactptcmvocsg": self._fap_stem + "e",  # portature
                    "Vfutactptcmaccsg": self._fap_stem + "um",  # portaturum
                    "Vfutactptcmgensg": self._fap_stem + "i",  # portaturi
                    "Vfutactptcmdatsg": self._fap_stem + "o",  # portaturo
                    "Vfutactptcmablsg": self._fap_stem + "o",  # portaturo
                    "Vfutactptcmnompl": self._fap_stem + "i",  # portaturi
                    "Vfutactptcmvocpl": self._fap_stem + "i",  # portaturi
                    "Vfutactptcmaccpl": self._fap_stem + "os",  # portaturos
                    "Vfutactptcmgenpl": self._fap_stem
                    + "orum",  # portaturorum
                    "Vfutactptcmdatpl": self._fap_stem + "is",  # portaturis
                    "Vfutactptcmablpl": self._fap_stem + "is",  # portaturis
                    "Vfutactptcfnomsg": self._fap_stem + "a",  # portatura
                    "Vfutactptcfvocsg": self._fap_stem + "a",  # portatura
                    "Vfutactptcfaccsg": self._fap_stem + "am",  # portaturam
                    "Vfutactptcfgensg": self._fap_stem + "ae",  # portaturae
                    "Vfutactptcfdatsg": self._fap_stem + "ae",  # portaturae
                    "Vfutactptcfablsg": self._fap_stem + "a",  # portatura
                    "Vfutactptcfnompl": self._fap_stem + "ae",  # portaturae
                    "Vfutactptcfvocpl": self._fap_stem + "ae",  # portaturae
                    "Vfutactptcfaccpl": self._fap_stem + "as",  # portaturas
                    "Vfutactptcfgenpl": self._fap_stem + "arum",  # portarum
                    "Vfutactptcfdatpl": self._fap_stem + "is",  # portaturis
                    "Vfutactptcfablpl": self._fap_stem + "is",  # portaturis
                    "Vfutactptcnnomsg": self._fap_stem + "um",  # portaturum
                    "Vfutactptcnvocsg": self._fap_stem + "um",  # portaturum
                    "Vfutactptcnaccsg": self._fap_stem + "um",  # portaturum
                    "Vfutactptcngensg": self._fap_stem + "i",  # portaturi
                    "Vfutactptcndatsg": self._fap_stem + "o",  # portaturo
                    "Vfutactptcnablsg": self._fap_stem + "o",  # portaturo
                    "Vfutactptcnnompl": self._fap_stem + "a",  # portatura
                    "Vfutactptcnvocpl": self._fap_stem + "a",  # portatura
                    "Vfutactptcnaccpl": self._fap_stem + "a",  # portatura
                    "Vfutactptcngenpl": self._fap_stem
                    + "orum",  # portaturorum
                    "Vfutactptcndatpl": self._fap_stem + "is",  # portaturis
                    "Vfutactptcnablpl": self._fap_stem + "is",  # portaturis
                }

            if not self.fap_fourthpp:
                assert self.ppp is not None
                assert self._ppp_stem is not None
                endings |= {
                    "Vperpasptcmnomsg": self.ppp,  # portatus
                    "Vperpasptcmvocsg": self._ppp_stem + "e",  # portate
                    "Vperpasptcmaccsg": self._ppp_stem + "um",  # portatum
                    "Vperpasptcmgensg": self._ppp_stem + "i",  # portati
                    "Vperpasptcmdatsg": self._ppp_stem + "o",  # portato
                    "Vperpasptcmablsg": self._ppp_stem + "o",  # portato
                    "Vperpasptcmnompl": self._ppp_stem + "i",  # portati
                    "Vperpasptcmvocpl": self._ppp_stem + "i",  # portati
                    "Vperpasptcmaccpl": self._ppp_stem + "os",  # portatos
                    "Vperpasptcmgenpl": self._ppp_stem + "orum",  # portatorum
                    "Vperpasptcmdatpl": self._ppp_stem + "is",  # portatis
                    "Vperpasptcmablpl": self._ppp_stem + "is",  # portatis
                    "Vperpasptcfnomsg": self._ppp_stem + "a",  # portata
                    "Vperpasptcfvocsg": self._ppp_stem + "a",  # portata
                    "Vperpasptcfaccsg": self._ppp_stem + "am",  # portatam
                    "Vperpasptcfgensg": self._ppp_stem + "ae",  # portatae
                    "Vperpasptcfdatsg": self._ppp_stem + "ae",  # portatae
                    "Vperpasptcfablsg": self._ppp_stem + "a",  # portata
                    "Vperpasptcfnompl": self._ppp_stem + "ae",  # portatae
                    "Vperpasptcfvocpl": self._ppp_stem + "ae",  # portatae
                    "Vperpasptcfaccpl": self._ppp_stem + "as",  # portatas
                    "Vperpasptcfgenpl": self._ppp_stem + "arum",  # portarum
                    "Vperpasptcfdatpl": self._ppp_stem + "is",  # portatis
                    "Vperpasptcfablpl": self._ppp_stem + "is",  # portatis
                    "Vperpasptcnnomsg": self._ppp_stem + "um",  # portatum
                    "Vperpasptcnvocsg": self._ppp_stem + "um",  # portatum
                    "Vperpasptcnaccsg": self._ppp_stem + "um",  # portatum
                    "Vperpasptcngensg": self._ppp_stem + "i",  # portati
                    "Vperpasptcndatsg": self._ppp_stem + "o",  # portato
                    "Vperpasptcnablsg": self._ppp_stem + "o",  # portato
                    "Vperpasptcnnompl": self._ppp_stem + "a",  # portata
                    "Vperpasptcnvocpl": self._ppp_stem + "a",  # portata
                    "Vperpasptcnaccpl": self._ppp_stem + "a",  # portata
                    "Vperpasptcngenpl": self._ppp_stem + "orum",  # portatorum
                    "Vperpasptcndatpl": self._ppp_stem + "is",  # portatis
                    "Vperpasptcnablpl": self._ppp_stem + "is",  # portatis
                }

        if self.deponent:
            return {
                (
                    key[:4] + "dep" + key[7:]
                    if key[4:7] == Voice.ACTIVE.shorthand
                    else key
                ): value
                for key, value in endings.items()
            }

        if self.semi_deponent:
            return {
                (
                    key[:4] + "sdp" + key[7:]
                    if not key.startswith("Vfutpasptc")
                    else key
                ): value
                for key, value in endings.items()
            }

        return endings

    def _verbal_nouns(self) -> Endings:
        endings: Endings = {}

        if not self.no_gerund:
            endings |= {
                "Vgeracc": self._preptc_stem + "ndum",  # portandum
                "Vgergen": self._preptc_stem + "ndi",  # portandi
                "Vgerdat": self._preptc_stem + "ndo",  # portando
                "Vgerabl": self._preptc_stem + "ndo",  # portando
            }

        if not self.no_supine:
            assert self._ppp_stem is not None
            endings |= {
                "Vsupacc": self._ppp_stem + "um",  # portatum
                "Vsupabl": self._ppp_stem + "u",  # portatu
            }

        return endings

    # fmt: off
    @overload
    def get(self, *, tense: Tense, voice: Voice, mood: Mood, person: Person, number: Number) -> Ending | None: ...
    @overload
    def get(self, *, tense: Tense, voice: Voice, mood: Literal[Mood.PARTICIPLE], number: Number, participle_gender: Gender, participle_case: Case) -> Ending | None: ...
    @overload
    def get(self, *, tense: Tense, voice: Voice, mood: Literal[Mood.INFINITIVE]) -> Ending | None: ...
    @overload
    def get(self, *, mood: Literal[Mood.GERUND, Mood.SUPINE], participle_case: Literal[Case.ACCUSATIVE, Case.GENITIVE, Case.DATIVE, Case.ABLATIVE]) -> Ending | None: ...
    # fmt: on

    def get(
        self,
        *,
        tense: Tense | None = None,
        voice: Voice | None = None,
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
        tense : Tense | None
            The tense of the ending, if applicable (not verbal noun).
        voice : Voice | None
            The voice of the ending, if applicable (not verbal noun).
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

        >>> foo.get(mood=Mood.GERUND, participle_case=Case.ACCUSATIVE)
        'celandum'

        Verbal nouns.
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

        if mood in {Mood.GERUND, Mood.SUPINE}:
            assert participle_case is not None

            short_mood = mood.shorthand
            short_case = participle_case.shorthand
            return self.endings.get(f"V{short_mood}{short_case}")

        assert tense is not None
        assert voice is not None

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
        short_number = number.shorthand if number else None

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

            if (output.tense, output.voice) == (Tense.FUTURE, Voice.PASSIVE):
                output.string = (
                    f"gerundive {output.gender.regular} {output.case.regular} "
                    f"{output.number.regular}"
                )
            else:
                output.string = (
                    f"{output.tense.regular} {output.voice.regular} participle "
                    f"{output.gender.regular} {output.case.regular} "
                    f"{output.number.regular}"
                )
            return output

        if len(key) == 7 and key[1:4] in {"ger", "sup"}:
            try:
                output = EndingComponents(
                    mood=Mood(key[1:4]), case=Case(key[4:7])
                )
            except ValueError as e:
                raise InvalidInputError(f"Key '{key}' is invalid.") from e

            output.string = f"{output.mood.regular} {output.case.regular}"
            return output

        raise InvalidInputError(f"Key '{key}' is invalid.")

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
        return (
            f"Verb({', '.join(self.principal_parts)}, meaning={self.meaning})"
        )

    def __str__(self) -> str:
        return f"{self.meaning}: {', '.join(self.principal_parts)}"

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
            and self.semi_deponent == other.semi_deponent
        ):
            return NotImplemented

        if self.meaning == other.meaning:
            return _create_verb(
                self.present,
                self.infinitive,
                self.perfect,
                self.ppp
                if not (self.deponent or self.semi_deponent)
                else None,
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
            self.ppp if not (self.deponent or self.semi_deponent) else None,
            meaning=new_meaning,
        )
