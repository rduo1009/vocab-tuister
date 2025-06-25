"""Representation of a Latin verb with endings."""

# pyright: reportImplicitOverride=false

from __future__ import annotations

import logging
from functools import total_ordering
from typing import TYPE_CHECKING, Literal, overload
from warnings import deprecated

from ...utils.dict_changes import apply_changes
from ._class_word import _Word
from .edge_cases import (
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
            return

        if self.infinitive is None:
            raise InvalidInputError(
                f"Verb '{self.present}' is not irregular, but no infinitive provided."
            )

        irregular_flag = is_irregular_verb(self.present) or is_derived_verb(
            self.present
        )

        # ---------------------------------------------------------------------
        # SEMI-DEPONENT VERBS

        # Check for semi-deponent verbs before deponent verbs
        # Semi-deponents have active present system, passive perfect system
        # e.g. audeo, audere, ausus sum
        # Crucially, their present does not end in "or"
        if (
            self.perfect is not None
            and self.perfect.endswith(" sum")
            and not self.present.endswith("or")
        ):
            self.semi_deponent = True

            if self.ppp is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' is semi-deponent, but ppp ('{self.ppp}') was provided. "
                    "The perfect form already implies the ppp."
                )
            if not self.present.endswith("o") and not irregular_flag:
                raise InvalidInputError(
                    f"Invalid present form for semi-deponent verb: '{self.present}' (must end in '-o')"
                )

            # Stems are derived similarly to non-deponent verbs, but perfect active forms use the 'ppp'
            # and perfect passive forms are standard.
            # The 'ppp' for a semi-deponent is effectively the perfect stem part before 'sum'
            self.ppp = self.perfect[:-4]  # e.g., "ausus" from "ausus sum"
            self._ppp_stem = self.ppp[:-2]  # e.g., "aus" from "ausus"
            self._fap_stem = self.ppp[:-1] + "r"  # e.g., "ausur" from "ausus"
            # Perfect stem for active perfect system forms (which don't exist for true semi-deponents but code structure might expect it)
            # For semi-deponents, perfect system is passive in form.
            # However, the logic for _first_conjugation etc. might generate active perfect forms.
            # We will use the PPP stem as the _per_stem for generation of perfect passive forms.
            self._per_stem = self.ppp  # Use the "ppp" (e.g. ausus) as the base for perfect system endings

            # Other flags
            self.no_ppp = (
                False  # It effectively has one, derived from the perfect
            )
            self.impersonal = self.present in IMPERSONAL_VERBS
            self.impersonal_passive = self.present in IMPERSONAL_PASSIVE_VERBS
            self.no_gerund = (
                self.present in MISSING_GERUND_VERBS
            )  # audeo has gerund
            self.no_supine = False  # audeo has supine
            self.no_perfect = False  # Has a perfect system
            self.no_future = (
                self.present in MISSING_FUTURE_VERBS
            )  # For 'soleo'
            self.no_fap = (
                self.present in MISSING_FAP_VERBS
            )  # audeo has FAP (ausurus)
            if self.no_future: # If no future tense, usually no FAP or Gerundive either for semi-deponents
                self.no_fap = True
            self.active_only = False  # Has passive forms in perfect system

            # Determine stems (similar to non-deponent)
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
                if self.present.endswith("eo"):  # e.g. audeo, not soleo here
                    self.conjugation = 2
                    self._inf_stem = self.infinitive[:-3]
                    self._preptc_stem = self.infinitive[:-2]
                # Mixed conjugation semi-deponents are rare/non-existent with this PPP pattern?
                # else if self.present.endswith("io"):
                #     self.conjugation = 5
                #     self._inf_stem = self.infinitive[:-3]
                #     self._preptc_stem = self.infinitive[:-3] + "ie"
                else:  # Default to 3rd if not clearly 2nd or mixed
                    self.conjugation = 3
                    self._inf_stem = self.infinitive[:-3]
                    self._preptc_stem = self.infinitive[:-2]
            else:
                raise InvalidInputError(
                    f"Invalid infinitive form for semi-deponent: '{self.infinitive}'"
                )

            # Determine endings (base from conjugation, then adjust)
            match self.conjugation:
                case 1:
                    self.endings = self._first_conjugation()
                case 2:
                    self.endings = self._second_conjugation()
                case 3:
                    self.endings = self._third_conjugation()
                case 4:
                    self.endings = self._fourth_conjugation()
                case _:  # 5 (mixed)
                    self.endings = self._mixed_conjugation()

            # Crucially, add participles and verbal nouns before filtering for semi-deponents
            self.endings |= self._participles()
            self.endings |= self._verbal_nouns()

            # Semi-deponents: Active present system, Passive perfect system
            # Keep active forms for present, imperfect, future indicative/subjunctive/imperative/infinitive
            # Keep passive forms for perfect, pluperfect, future perfect indicative/subjunctive/infinitive
            # Participles: Present Active, Perfect Passive, Future Active
            # Verbal Nouns: Gerund (active), Supine (active forms from ppp)

            # --- DEBUG PRINT ---
            # print(f"DEBUG: Initial endings for {self.present}: {sorted(list(self.endings.keys()))}")
            # --- END DEBUG PRINT ---

            new_active_keys = set()
            for k_loop_active in self.endings:
                # Standard Active Tenses (Indicative, Subjunctive, Imperative)
                # Ensure not to grab participles here if mood check is not precise enough
                if (
                    k_loop_active.startswith(("Vpreact", "Vimpact", "Vfutact"))
                ) and k_loop_active[7:10] in {
                    Mood.INDICATIVE.shorthand,
                    Mood.SUBJUNCTIVE.shorthand,
                    Mood.IMPERATIVE.shorthand,
                }:
                    new_active_keys.add(k_loop_active)

                # Present Active Participle (all forms)
                if k_loop_active.startswith("Vpreactptc"):
                    new_active_keys.add(k_loop_active)

                # Present Active Infinitive
                if k_loop_active == "Vpreactinf   ":  # Exact key with spaces
                    new_active_keys.add(k_loop_active)

                # Gerunds & Supines
                if k_loop_active.startswith((
                    "V" + Mood.GERUND.shorthand,
                    "V" + Mood.SUPINE.shorthand,
                )):
                    new_active_keys.add(k_loop_active)

            # Future Active Participle & Future Active Infinitive (if applicable)
            if not self.no_fap:  # self.no_fap is specific to the verb
                for k_loop_fap in self.endings:
                    # Future Active Participle (all forms)
                    if k_loop_fap.startswith("Vfutactptc"):
                        new_active_keys.add(k_loop_fap)
                    # Future Active Infinitive
                    if k_loop_fap == "Vfutactinf   ":  # Exact key with spaces
                        new_active_keys.add(k_loop_fap)

            active_present_system_keys = new_active_keys

            # --- DEBUG PRINT ---
            # print(f"DEBUG: Active present system keys for {self.present}: {sorted(list(active_present_system_keys))}")
            # --- END DEBUG PRINT ---

            # Perfect system passive forms (using self.ppp which is derived from "perfect ... sum")
            # The conjugation methods already generate these based on self.ppp and self._ppp_stem
            passive_perfect_system_keys = {
                k
                for k, v in self.endings.items()
                if k.startswith((
                    "Vperp",
                    "Vplpp",
                    "Vfprp",
                    "Vperpasptc",
                    "Vfutpasptc",
                ))  # future passive participle (gerundive)
            }
            # NOTE: The redundant block that updated active_present_system_keys again has been removed.

            # Combine the desired keys
            final_endings = {}
            for key in active_present_system_keys:
                if key in self.endings:
                    final_endings[key] = self.endings[key]
            for key_loop_passive in passive_perfect_system_keys:
                if key_loop_passive in self.endings:
                    # For participles, retain their original "passive" voice key.
                    # For other perfect system forms (indicative, subjunctive, infinitive),
                    # change voice to SEMI_DEPONENT.
                    if key_loop_passive[7:10] == Mood.PARTICIPLE.shorthand or (
                        key_loop_passive[4:7] == Voice.PASSIVE.shorthand
                        and key_loop_passive.startswith("Vfutpasptc")
                    ):  # Gerundive is futpasptc
                        final_endings[key_loop_passive] = self.endings[
                            key_loop_passive
                        ]
                    else:
                        # V per pas ind sg 1 -> V per sdp ind sg 1
                        new_key = (
                            key_loop_passive[:4]
                            + Voice.SEMI_DEPONENT.shorthand
                            + key_loop_passive[7:]
                        )
                        final_endings[new_key] = self.endings[key_loop_passive]

            self.endings = final_endings

            # Add participles and verbal nouns (some might have been missed or need specific handling)
            # self.endings |= self._participles() # Already partially done by selecting keys
            # self.endings |= self._verbal_nouns() # Already partially done

            # Apply irregular changes if any
            if is_irregular_verb(self.present):
                self.endings = apply_changes(
                    self.endings, find_irregular_verb_changes(self.present)
                )
            elif is_derived_verb(self.present):
                self.endings = apply_changes(
                    self.endings,
                    find_derived_verb_changes((
                        self.present,
                        self.infinitive,
                        self.perfect,
                        self.ppp,
                    )),  # ppp is now guaranteed for semi-dep
                )

            # Handle impersonal flags
            if self.impersonal or self.impersonal_passive:
                self.endings = {
                    key: value
                    for key, value in self.endings.items()
                    if len(key) != 13  # TODO: check this logic for sdp
                    or key[10:13] == Number.SINGULAR.shorthand + "3"
                }

            # Handle no_future specifically for 'soleo' (if it's semi-deponent)
            # The FIXME for 'soleo' and MISSING_FUTURE_VERBS
            # This check needs to be after irregular/derived changes are applied
            if self.present in MISSING_FUTURE_VERBS and self.semi_deponent:
                current_endings = self.endings.copy()
                for key in list(
                    current_endings.keys()
                ):  # list() to allow modification
                    tense_shorthand = key[1:4]
                    if tense_shorthand in {
                        Tense.FUTURE.shorthand,
                        Tense.FUTURE_PERFECT.shorthand,
                    }:
                        del current_endings[key]
                self.endings = current_endings

            return  # Finished processing for semi-deponent

        # ---------------------------------------------------------------------
        # DEPONENT VERBS

        if self.present.endswith(
            "or"
        ):  # `elif` ensures semi-deponents are not also treated as deponents
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
            if is_irregular_verb(self.present):
                self.conjugation = get_irregular_verb_conjugation(self.present)
                self._preptc_stem: str
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
            elif self.infinitive.endswith("eri"):
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

            return

        # ---------------------------------------------------------------------
        # NON-DEPONENT VERBS (if not semi-deponent or deponent)
        # Handle defective verbs
        if self.present in MISSING_PERFECT_VERBS:
            # if only three args, then the form in `perfect` is actually the ppp
            if not self.ppp:
                self.ppp = self.perfect
                del self.perfect  # type: ignore[attr-defined]
            elif self.perfect is not None:
                raise InvalidInputError(
                    f"Verb '{self.present}' has no perfect, but perfect provided."
                )

            self.no_perfect = True
        else:
            if (
                self.perfect is None
            ):  # Should have been caught if not irregular
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
            if self.ppp is None:  # This ppp is actually the FAP stem source
                raise InvalidInputError(
                    f"Verb '{self.present}' does not have a future active participle provided."
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
            if self.ppp.endswith(
                "um"
            ):  # Make sure it's a supine ending, not already a ppp
                self.ppp = (
                    self.ppp[:-2] + "us"
                )  # Convert to masculine nominative singular ppp

            self._ppp_stem = self.ppp[:-2]
            self._fap_stem = self.ppp[:-1] + "r"

        self.no_gerund = self.present in MISSING_GERUND_VERBS
        self.no_fap = self.present in MISSING_FAP_VERBS
        self.active_only = self.present in ACTIVE_ONLY_VERBS
        self.impersonal = self.present in IMPERSONAL_VERBS
        self.impersonal_passive = self.present in IMPERSONAL_PASSIVE_VERBS

        # Original FIXME for no_future was here. It's now handled in semi-deponent block if applicable.
        # If a non-semi-deponent verb is in MISSING_FUTURE_VERBS, it will be handled later.
        self.no_future = self.present in MISSING_FUTURE_VERBS

        if not self.present.endswith("o") and not irregular_flag:
            raise InvalidInputError(
                f"Invalid present form: '{self.present}' (must end in '-o')"
            )

        # Determine stems for non-deponent, non-semi-deponent
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

        # Determine endings for non-deponent, non-semi-deponent
        match self.conjugation:
            case 1:
                self.endings = self._first_conjugation()
            case 2:
                self.endings = self._second_conjugation()
            case 3:
                self.endings = self._third_conjugation()
            case 4:
                self.endings = self._fourth_conjugation()
            case _:  # 5 (mixed)
                self.endings = self._mixed_conjugation()

        self.endings |= self._participles()
        self.endings |= self._verbal_nouns()

        # Override endings for irregular and defective verbs
        if is_irregular_verb(self.present):
            self.endings = apply_changes(
                self.endings, find_irregular_verb_changes(self.present)
            )
        elif is_derived_verb(self.present):
            assert (
                self.perfect is not None
            )  # Should be true for derived if not no_perfect
            self.endings = apply_changes(
                self.endings,
                find_derived_verb_changes(
                    (self.present, self.infinitive, self.perfect, self.ppp)
                    if self.ppp
                    and not self.no_ppp  # Only pass ppp if it exists
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

        # General no_future handling if not semi-deponent
        if self.no_future and not self.semi_deponent:
            self.endings = {
                key: value
                for key, value in self.endings.items()
                if key[1:4]
                not in {Tense.FUTURE.shorthand, Tense.FUTURE_PERFECT.shorthand}
            }

    def _first_conjugation(self) -> Endings:
        assert self.infinitive is not None

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
            "Vprepassbjsg1": f"{self._inf_stem}er",  # porter
            "Vprepassbjsg2": f"{self._inf_stem}eris",  # porteris
            "Vprepassbjsg3": f"{self._inf_stem}etur",  # portetur
            "Vprepassbjpl1": f"{self._inf_stem}emur",  # portemur
            "Vprepassbjpl2": f"{self._inf_stem}emini",  # portemini
            "Vprepassbjpl3": f"{self._inf_stem}entur",  # portentur
            "Vimppassbjsg1": f"{self.infinitive}r",  # portarer
            "Vimppassbjsg2": f"{self.infinitive}ris",  # portareris
            "Vimppassbjsg3": f"{self.infinitive}tur",  # portaretur
            "Vimppassbjpl1": f"{self.infinitive}mur",  # portaremur
            "Vimppassbjpl2": f"{self.infinitive}mini",  # portaremini
            "Vimppassbjpl3": f"{self.infinitive}ntur",  # portarentur
            "Vprepasipesg2": f"{self._inf_stem}are",  # portare
            "Vprepasipepl2": f"{self._inf_stem}amini",  # portamini
            "Vfutpasipesg2": f"{self._inf_stem}ator",  # portator
            "Vfutpasipesg3": f"{self._inf_stem}ator",  # portator
            "Vfutpasipepl3": f"{self._inf_stem}antor",  # portantor
            "Vprepasinf   ": f"{self._inf_stem}ari",  # portari
        }

        # Passive forms that use ppp
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
                "Vperpassbjsg1": f"{self.ppp} sim",  # portatus sim
                "Vperpassbjsg2": f"{self.ppp} sis",  # portatus sis
                "Vperpassbjsg3": f"{self.ppp} sit",  # portatus sit
                "Vperpassbjpl1": f"{self.ppp[:-2]}i simus",  # portati simus
                "Vperpassbjpl2": f"{self.ppp[:-2]}i sitis",  # portati sitis
                "Vperpassbjpl3": f"{self.ppp[:-2]}i sint",  # portati sint
                "Vplppassbjsg1": f"{self.ppp} essem",  # portatus essem
                "Vplppassbjsg2": f"{self.ppp} esses",  # portatus esses
                "Vplppassbjsg3": f"{self.ppp} esset",  # portatus esset
                "Vplppassbjpl1": f"{self.ppp[:-2]}i essemus",  # portati essemus
                "Vplppassbjpl2": f"{self.ppp[:-2]}i essetis",  # portati essetis
                "Vplppassbjpl3": f"{self.ppp[:-2]}i essent",  # portati essent
                "Vfutpasinf   ": f"{self.ppp[:-2]}um iri",  # portatum iri
                "Vperpasinf   ": f"{self.ppp[:-2]}us esse",  # portatus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect:
            assert self.perfect is not None
            endings |= {
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
                "Vperactsbjsg1": f"{self._per_stem}erim",  # portaverim
                "Vperactsbjsg2": f"{self._per_stem}eris",  # portaveris
                "Vperactsbjsg3": f"{self._per_stem}erit",  # portaverit
                "Vperactsbjpl1": f"{self._per_stem}erimus",  # portaverimus
                "Vperactsbjpl2": f"{self._per_stem}eritis",  # portaveritis
                "Vperactsbjpl3": f"{self._per_stem}erint",  # portaverint
                "Vplpactsbjsg1": f"{self._per_stem}issem",  # portavissem
                "Vplpactsbjsg2": f"{self._per_stem}isses",  # portavisses
                "Vplpactsbjsg3": f"{self._per_stem}isset",  # portavisset
                "Vplpactsbjpl1": f"{self._per_stem}issemus",  # portavissemus
                "Vplpactsbjpl2": f"{self._per_stem}issetis",  # portavissetis
                "Vplpactsbjpl3": f"{self._per_stem}issent",  # portavissent
                "Vperactinf   ": f"{self._per_stem}isse",  # portavisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            endings |= {
                "Vfutactinf   ": f"{self._fap_stem}us esse"  # portaturus esse
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
            "Vpreactsbjsg1": f"{self._inf_stem}em",  # portem
            "Vpreactsbjsg2": f"{self._inf_stem}es",  # portes
            "Vpreactsbjsg3": f"{self._inf_stem}et",  # portet
            "Vpreactsbjpl1": f"{self._inf_stem}emus",  # portemus
            "Vpreactsbjpl2": f"{self._inf_stem}etis",  # portetis
            "Vpreactsbjpl3": f"{self._inf_stem}ent",  # portent
            "Vimpactsbjsg1": f"{self.infinitive}m",  # portarem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # portares
            "Vimpactsbjsg3": f"{self.infinitive}t",  # portaret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # portaremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # portaretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # portarent
            "Vpreactipesg2": f"{self._inf_stem}a",  # porta
            "Vpreactipepl2": f"{self._inf_stem}ate",  # portate
            "Vfutactipesg2": f"{self._inf_stem}ato",  # portato
            "Vfutactipesg3": f"{self._inf_stem}ato",  # portato
            "Vfutactipepl2": f"{self._inf_stem}atote",  # portatote
            "Vfutactipepl3": f"{self._inf_stem}anto",  # portanto
            "Vpreactinf   ": self.infinitive,  # portare
        }

    def _second_conjugation(self) -> Endings:
        assert self.infinitive is not None

        # Passive forms
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
            "Vprepassbjsg1": f"{self._inf_stem}ear",  # docear
            "Vprepassbjsg2": f"{self._inf_stem}earis",  # docearis
            "Vprepassbjsg3": f"{self._inf_stem}eatur",  # doceatur
            "Vprepassbjpl1": f"{self._inf_stem}eamur",  # doceamur
            "Vprepassbjpl2": f"{self._inf_stem}eamini",  # doceamini
            "Vprepassbjpl3": f"{self._inf_stem}eantur",  # doceantur
            "Vimppassbjsg1": f"{self.infinitive}r",  # docerer
            "Vimppassbjsg2": f"{self.infinitive}ris",  # docereris
            "Vimppassbjsg3": f"{self.infinitive}tur",  # doceretur
            "Vimppassbjpl1": f"{self.infinitive}mur",  # doceremur
            "Vimppassbjpl2": f"{self.infinitive}mini",  # doceremini
            "Vimppassbjpl3": f"{self.infinitive}ntur",  # docerentur
            "Vprepasipesg2": f"{self._inf_stem}ere",  # docere
            "Vprepasipepl2": f"{self._inf_stem}emini",  # docemini
            "Vfutpasipesg2": f"{self._inf_stem}etor",  # docetor
            "Vfutpasipesg3": f"{self._inf_stem}etor",  # docetor
            "Vfutpasipepl3": f"{self._inf_stem}entor",  # docentor
            "Vprepasinf   ": f"{self._inf_stem}eri",  # doceri
        }

        # Passive forms that use ppp
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
                "Vperpassbjsg1": f"{self.ppp} sim",  # doctus sim
                "Vperpassbjsg2": f"{self.ppp} sis",  # doctus sis
                "Vperpassbjsg3": f"{self.ppp} sit",  # doctus sit
                "Vperpassbjpl1": f"{self.ppp[:-2]}i simus",  # docti simus
                "Vperpassbjpl2": f"{self.ppp[:-2]}i sitis",  # docti sitis
                "Vperpassbjpl3": f"{self.ppp[:-2]}i sint",  # docti sint
                "Vplppassbjsg1": f"{self.ppp} essem",  # doctus essem
                "Vplppassbjsg2": f"{self.ppp} esses",  # doctus esses
                "Vplppassbjsg3": f"{self.ppp} esset",  # doctus esset
                "Vplppassbjpl1": f"{self.ppp[:-2]}i essemus",  # docti essemus
                "Vplppassbjpl2": f"{self.ppp[:-2]}i essetis",  # docti essetis
                "Vplppassbjpl3": f"{self.ppp[:-2]}i essent",  # docti essent
                "Vfutpasinf   ": f"{self.ppp[:-2]}um iri",  # doctum iri
                "Vperpasinf   ": f"{self.ppp[:-2]}us esse",  # doctus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect:
            assert self.perfect is not None
            endings |= {
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
                "Vperactsbjsg1": f"{self._per_stem}erim",  # docuerim
                "Vperactsbjsg2": f"{self._per_stem}eris",  # docueris
                "Vperactsbjsg3": f"{self._per_stem}erit",  # docuerit
                "Vperactsbjpl1": f"{self._per_stem}erimus",  # docuerimus
                "Vperactsbjpl2": f"{self._per_stem}eritis",  # docueritis
                "Vperactsbjpl3": f"{self._per_stem}erint",  # docuerint
                "Vplpactsbjsg1": f"{self._per_stem}issem",  # docuissem
                "Vplpactsbjsg2": f"{self._per_stem}isses",  # docuisses
                "Vplpactsbjsg3": f"{self._per_stem}isset",  # docuisset
                "Vplpactsbjpl1": f"{self._per_stem}issemus",  # docuissmus
                "Vplpactsbjpl2": f"{self._per_stem}issetis",  # docuissetis
                "Vplpactsbjpl3": f"{self._per_stem}issent",  # docuissent
                "Vperactinf   ": f"{self._per_stem}isse",  # docuisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            endings |= {
                "Vfutactinf   ": f"{self._fap_stem}us esse"  # docturus esse
            }

        # Active forms
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
            "Vpreactsbjsg1": f"{self._inf_stem}eam",  # doceam
            "Vpreactsbjsg2": f"{self._inf_stem}eas",  # doceas
            "Vpreactsbjsg3": f"{self._inf_stem}eat",  # doceat
            "Vpreactsbjpl1": f"{self._inf_stem}eamus",  # doceamus
            "Vpreactsbjpl2": f"{self._inf_stem}eatis",  # doceatis
            "Vpreactsbjpl3": f"{self._inf_stem}eant",  # doceant
            "Vimpactsbjsg1": f"{self.infinitive}m",  # docerem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # doceres
            "Vimpactsbjsg3": f"{self.infinitive}t",  # doceret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # doceremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # doceretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # docerent
            "Vpreactipesg2": f"{self._inf_stem}e",  # doce
            "Vpreactipepl2": f"{self._inf_stem}ete",  # docete
            "Vfutactipesg2": f"{self._inf_stem}eto",  # doceto
            "Vfutactipesg3": f"{self._inf_stem}eto",  # doceto
            "Vfutactipepl2": f"{self._inf_stem}etote",  # docetote
            "Vfutactipepl3": f"{self._inf_stem}ento",  # docento
            "Vpreactinf   ": self.infinitive,  # docere
        }

    def _third_conjugation(self) -> Endings:
        assert self.infinitive is not None

        # Passive forms
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
            "Vprepassbjsg1": f"{self._inf_stem}ar",  # trahar
            "Vprepassbjsg2": f"{self._inf_stem}aris",  # traharis
            "Vprepassbjsg3": f"{self._inf_stem}atur",  # trahatur
            "Vprepassbjpl1": f"{self._inf_stem}amur",  # trahamur
            "Vprepassbjpl2": f"{self._inf_stem}amini",  # trahamini
            "Vprepassbjpl3": f"{self._inf_stem}antur",  # trahantur
            "Vimppassbjsg1": f"{self.infinitive}r",  # traherer
            "Vimppassbjsg2": f"{self.infinitive}ris",  # trahereris
            "Vimppassbjsg3": f"{self.infinitive}tur",  # traheretur
            "Vimppassbjpl1": f"{self.infinitive}mur",  # traheremur
            "Vimppassbjpl2": f"{self.infinitive}mini",  # traheremini
            "Vimppassbjpl3": f"{self.infinitive}ntur",  # traherentur
            "Vprepasipesg2": f"{self._inf_stem}ere",  # trahere
            "Vprepasipepl2": f"{self._inf_stem}imini",  # trahimini
            "Vfutpasipesg2": f"{self._inf_stem}itor",  # trahitor
            "Vfutpasipesg3": f"{self._inf_stem}itor",  # trahitor
            "Vfutpasipepl3": f"{self._inf_stem}untor",  # trahuntor
            "Vprepasinf   ": f"{self._inf_stem}i",  # trahi
        }

        # Passive forms that use ppp
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
                "Vperpassbjsg1": f"{self.ppp} sim",  # tractus sim
                "Vperpassbjsg2": f"{self.ppp} sis",  # tractus sis
                "Vperpassbjsg3": f"{self.ppp} sit",  # tractus sit
                "Vperpassbjpl1": f"{self.ppp[:-2]}i simus",  # tracti simus
                "Vperpassbjpl2": f"{self.ppp[:-2]}i sitis",  # tracti sitis
                "Vperpassbjpl3": f"{self.ppp[:-2]}i sint",  # tracti sint
                "Vplppassbjsg1": f"{self.ppp} essem",  # tractus essem
                "Vplppassbjsg2": f"{self.ppp} esses",  # tractus esses
                "Vplppassbjsg3": f"{self.ppp} esset",  # tractus esset
                "Vplppassbjpl1": f"{self.ppp[:-2]}i essemus",  # tracti essemus
                "Vplppassbjpl2": f"{self.ppp[:-2]}i essetis",  # tracti essetis
                "Vplppassbjpl3": f"{self.ppp[:-2]}i essent",  # tracti essent
                "Vfutpasinf   ": f"{self.ppp[:-2]}um iri",  # tractum iri
                "Vperpasinf   ": f"{self.ppp[:-2]}us esse",  # tractus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect:
            assert self.perfect is not None
            endings |= {
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
                "Vperactsbjsg1": f"{self._per_stem}erim",  # traxerim
                "Vperactsbjsg2": f"{self._per_stem}eris",  # traxeris
                "Vperactsbjsg3": f"{self._per_stem}erit",  # traxerit
                "Vperactsbjpl1": f"{self._per_stem}erimus",  # traxerimus
                "Vperactsbjpl2": f"{self._per_stem}eritis",  # traxeritis
                "Vperactsbjpl3": f"{self._per_stem}erint",  # traxerint
                "Vplpactsbjsg1": f"{self._per_stem}issem",  # traxissem
                "Vplpactsbjsg2": f"{self._per_stem}isses",  # traxisses
                "Vplpactsbjsg3": f"{self._per_stem}isset",  # traxisset
                "Vplpactsbjpl1": f"{self._per_stem}issemus",  # traxissemus
                "Vplpactsbjpl2": f"{self._per_stem}issetis",  # traxissetis
                "Vplpactsbjpl3": f"{self._per_stem}issent",  # traxissent
                "Vperactinf   ": f"{self._per_stem}isse",  # traxisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            endings |= {
                "Vfutactinf   ": f"{self._fap_stem}us esse"  # tracturus esse
            }

        # Active forms
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
            "Vpreactsbjsg1": f"{self._inf_stem}am",  # traham
            "Vpreactsbjsg2": f"{self._inf_stem}as",  # trahas
            "Vpreactsbjsg3": f"{self._inf_stem}at",  # trahat
            "Vpreactsbjpl1": f"{self._inf_stem}amus",  # trahamus
            "Vpreactsbjpl2": f"{self._inf_stem}atis",  # trahatis
            "Vpreactsbjpl3": f"{self._inf_stem}ant",  # trahant
            "Vimpactsbjsg1": f"{self.infinitive}m",  # traherem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # traheres
            "Vimpactsbjsg3": f"{self.infinitive}t",  # traheret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # traheremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # traheretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # traherent
            "Vpreactipesg2": f"{self._inf_stem}e",  # trahe
            "Vpreactipepl2": f"{self._inf_stem}ite",  # trahite
            "Vfutactipesg2": f"{self._inf_stem}ito",  # trahito
            "Vfutactipesg3": f"{self._inf_stem}ito",  # trahito
            "Vfutactipepl2": f"{self._inf_stem}itote",  # trahitote
            "Vfutactipepl3": f"{self._inf_stem}unto",  # trahunto
            "Vpreactinf   ": self.infinitive,  # trahere
        }

    def _fourth_conjugation(self) -> Endings:
        assert self.infinitive is not None

        # Passive forms
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
            "Vprepassbjsg1": f"{self._inf_stem}iar",  # audiar
            "Vprepassbjsg2": f"{self._inf_stem}iaris",  # audiaris
            "Vprepassbjsg3": f"{self._inf_stem}iatur",  # audiatur
            "Vprepassbjpl1": f"{self._inf_stem}iamur",  # audiamur
            "Vprepassbjpl2": f"{self._inf_stem}iamini",  # audiamini
            "Vprepassbjpl3": f"{self._inf_stem}iantur",  # audiantur
            "Vimppassbjsg1": f"{self.infinitive}r",  # audirer
            "Vimppassbjsg2": f"{self.infinitive}ris",  # audireris
            "Vimppassbjsg3": f"{self.infinitive}tur",  # audiretur
            "Vimppassbjpl1": f"{self.infinitive}mur",  # audiremur
            "Vimppassbjpl2": f"{self.infinitive}mini",  # audiremini
            "Vimppassbjpl3": f"{self.infinitive}ntur",  # audirentur
            "Vprepasipesg2": f"{self._inf_stem}ire",  # audire
            "Vprepasipepl2": f"{self._inf_stem}imini",  # audimini
            "Vfutpasipesg2": f"{self._inf_stem}itor",  # auditor
            "Vfutpasipesg3": f"{self._inf_stem}itor",  # auditor
            "Vfutpasipepl3": f"{self._inf_stem}iuntor",  # audiuntor
            "Vprepasinf   ": f"{self._inf_stem}iri",  # audiri
        }

        # Passive forms that use ppp
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
                "Vperpassbjsg1": f"{self.ppp} sim",  # auditus sim
                "Vperpassbjsg2": f"{self.ppp} sis",  # auditus sis
                "Vperpassbjsg3": f"{self.ppp} sit",  # auditus sit
                "Vperpassbjpl1": f"{self.ppp[:-2]}i simus",  # auditi simus
                "Vperpassbjpl2": f"{self.ppp[:-2]}i sitis",  # auditi sitis
                "Vperpassbjpl3": f"{self.ppp[:-2]}i sint",  # auditi sint
                "Vplppassbjsg1": f"{self.ppp} essem",  # auditus essem
                "Vplppassbjsg2": f"{self.ppp} esses",  # auditus esses
                "Vplppassbjsg3": f"{self.ppp} esset",  # auditus esset
                "Vplppassbjpl1": f"{self.ppp[:-2]}i essemus",  # auditi essemus
                "Vplppassbjpl2": f"{self.ppp[:-2]}i essetis",  # auditi essetis
                "Vplppassbjpl3": f"{self.ppp[:-2]}i essent",  # auditi essent
                "Vfutpasinf   ": f"{self.ppp[:-2]}um iri",  # auditum iri
                "Vperpasinf   ": f"{self.ppp[:-2]}us esse",  # auditus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect:
            assert self.perfect is not None
            endings |= {
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
                "Vperactsbjsg1": f"{self._per_stem}erim",  # audiverim
                "Vperactsbjsg2": f"{self._per_stem}eris",  # audiveris
                "Vperactsbjsg3": f"{self._per_stem}erit",  # audiverit
                "Vperactsbjpl1": f"{self._per_stem}erimus",  # audiverimus
                "Vperactsbjpl2": f"{self._per_stem}eritis",  # audiveritis
                "Vperactsbjpl3": f"{self._per_stem}erint",  # audiverint
                "Vplpactsbjsg1": f"{self._per_stem}issem",  # audivissem
                "Vplpactsbjsg2": f"{self._per_stem}isses",  # audivisses
                "Vplpactsbjsg3": f"{self._per_stem}isset",  # audivisset
                "Vplpactsbjpl1": f"{self._per_stem}issemus",  # audivissemus
                "Vplpactsbjpl2": f"{self._per_stem}issetis",  # audivissetis
                "Vplpactsbjpl3": f"{self._per_stem}issent",  # audivissent
                "Vperactinf   ": f"{self._per_stem}isse",  # audivisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            endings |= {
                "Vfutactinf   ": f"{self._fap_stem}us esse"  # auditurus esse
            }

        # Active forms
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
            "Vpreactsbjsg1": f"{self._inf_stem}iam",  # audiam
            "Vpreactsbjsg2": f"{self._inf_stem}ias",  # audias
            "Vpreactsbjsg3": f"{self._inf_stem}iat",  # audiat
            "Vpreactsbjpl1": f"{self._inf_stem}iamus",  # audiamus
            "Vpreactsbjpl2": f"{self._inf_stem}iatis",  # audiatis
            "Vpreactsbjpl3": f"{self._inf_stem}iant",  # audiant
            "Vimpactsbjsg1": f"{self.infinitive}m",  # audirem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # audires
            "Vimpactsbjsg3": f"{self.infinitive}t",  # audiret
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # audiremus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # audiretis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # audirent
            "Vpreactipesg2": f"{self._inf_stem}i",  # audi
            "Vpreactipepl2": f"{self._inf_stem}ite",  # audite
            "Vfutactipesg2": f"{self._inf_stem}ito",  # audito
            "Vfutactipesg3": f"{self._inf_stem}ito",  # audito
            "Vfutactipepl2": f"{self._inf_stem}itote",  # auditote
            "Vfutactipepl3": f"{self._inf_stem}iunto",  # audiunto
            "Vpreactinf   ": self.infinitive,  # audire
        }

    def _mixed_conjugation(self) -> Endings:
        assert self.infinitive is not None

        # Passive forms
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
            "Vprepassbjsg1": f"{self._inf_stem}iar",  # capiar
            "Vprepassbjsg2": f"{self._inf_stem}iaris",  # capiaris
            "Vprepassbjsg3": f"{self._inf_stem}iatur",  # capiatur
            "Vprepassbjpl1": f"{self._inf_stem}iamur",  # capiamur
            "Vprepassbjpl2": f"{self._inf_stem}iamini",  # capiamini
            "Vprepassbjpl3": f"{self._inf_stem}iantur",  # capiantur
            "Vimppassbjsg1": f"{self.infinitive}r",  # caperer
            "Vimppassbjsg2": f"{self.infinitive}ris",  # capereris
            "Vimppassbjsg3": f"{self.infinitive}tur",  # caperetur
            "Vimppassbjpl1": f"{self.infinitive}mur",  # caperemur
            "Vimppassbjpl2": f"{self.infinitive}mini",  # caperemini
            "Vimppassbjpl3": f"{self.infinitive}ntur",  # caperentur
            "Vprepasipesg2": f"{self._inf_stem}ere",  # capere
            "Vprepasipepl2": f"{self._inf_stem}imini",  # capimini
            "Vfutpasipesg2": f"{self._inf_stem}itor",  # capitor
            "Vfutpasipesg3": f"{self._inf_stem}itor",  # capitor
            "Vfutpasipepl3": f"{self._inf_stem}iuntor",  # capiuntor
            "Vprepasinf   ": f"{self._inf_stem}i",  # capi
        }

        # Passive forms that use ppp
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
                "Vperpassbjsg1": f"{self.ppp} sim",  # captus sim
                "Vperpassbjsg2": f"{self.ppp} sis",  # captus sis
                "Vperpassbjsg3": f"{self.ppp} sit",  # captus sit
                "Vperpassbjpl1": f"{self.ppp[:-2]}i simus",  # capti simus
                "Vperpassbjpl2": f"{self.ppp[:-2]}i sitis",  # capti sitis
                "Vperpassbjpl3": f"{self.ppp[:-2]}i sint",  # capti sint
                "Vplppassbjsg1": f"{self.ppp} essem",  # captus essem
                "Vplppassbjsg2": f"{self.ppp} esses",  # captus esses
                "Vplppassbjsg3": f"{self.ppp} esset",  # captus esset
                "Vplppassbjpl1": f"{self.ppp[:-2]}i essemus",  # capti essemus
                "Vplppassbjpl2": f"{self.ppp[:-2]}i essetis",  # capti essetis
                "Vplppassbjpl3": f"{self.ppp[:-2]}i essent",  # capti essent
                "Vfutpasinf   ": f"{self.ppp[:-2]}um iri",  # captum iri
                "Vperpasinf   ": f"{self.ppp[:-2]}us esse",  # captus esse
            }

        if self.deponent:
            return {
                key[:4] + "dep" + key[7:]: value
                for key, value in endings.items()
            }

        # Active forms that use perfect stem
        if not self.no_perfect:
            assert self.perfect is not None
            endings |= {
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
                "Vperactsbjsg1": f"{self._per_stem}erim",  # ceperim
                "Vperactsbjsg2": f"{self._per_stem}eris",  # ceperis
                "Vperactsbjsg3": f"{self._per_stem}erit",  # ceperit
                "Vperactsbjpl1": f"{self._per_stem}erimus",  # ceperimus
                "Vperactsbjpl2": f"{self._per_stem}eritis",  # ceperitis
                "Vperactsbjpl3": f"{self._per_stem}erint",  # ceperint
                "Vplpactsbjsg1": f"{self._per_stem}issem",  # cepissem
                "Vplpactsbjsg2": f"{self._per_stem}isses",  # cepisses
                "Vplpactsbjsg3": f"{self._per_stem}isset",  # cepisset
                "Vplpactsbjpl1": f"{self._per_stem}issemus",  # cepissemus
                "Vplpactsbjpl2": f"{self._per_stem}issetis",  # cepissetis
                "Vplpactsbjpl3": f"{self._per_stem}issent",  # cepissent
                "Vperactinf   ": f"{self._per_stem}isse",  # cepisse
            }

        # Active forms that use future active participle stem
        if ((not self.no_ppp) or self.fap_fourthpp) and (not self.no_fap):
            endings |= {
                "Vfutactinf   ": f"{self._fap_stem}us esse"  # capturus esse
            }

        # Active forms
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
            "Vpreactsbjsg1": f"{self._inf_stem}iam",  # capiam
            "Vpreactsbjsg2": f"{self._inf_stem}ias",  # capias
            "Vpreactsbjsg3": f"{self._inf_stem}iat",  # capiat
            "Vpreactsbjpl1": f"{self._inf_stem}iamus",  # capiamus
            "Vpreactsbjpl2": f"{self._inf_stem}iatis",  # capiatis
            "Vpreactsbjpl3": f"{self._inf_stem}iant",  # capiant
            "Vimpactsbjsg1": f"{self.infinitive}m",  # caperem
            "Vimpactsbjsg2": f"{self.infinitive}s",  # caperes
            "Vimpactsbjsg3": f"{self.infinitive}t",  # caperet
            "Vimpactsbjpl1": f"{self.infinitive}mus",  # caperemus
            "Vimpactsbjpl2": f"{self.infinitive}tis",  # caperetis
            "Vimpactsbjpl3": f"{self.infinitive}nt",  # caperent
            "Vpreactipesg2": f"{self._inf_stem}e",  # cape
            "Vpreactipepl2": f"{self._inf_stem}ite",  # capite
            "Vfutactipesg2": f"{self._inf_stem}ito",  # capito
            "Vfutactipesg3": f"{self._inf_stem}ito",  # capito
            "Vfutactipepl2": f"{self._inf_stem}itote",  # capitote
            "Vfutactipepl3": f"{self._inf_stem}iunto",  # capiunto
            "Vpreactinf   ": self.infinitive,  # capere
        }

    def _participles(self) -> Endings:
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

        if not self.no_fap:
            endings |= {
                "Vfutpasptcmnomsg": f"{self._preptc_stem}ndus",  # portandus
                "Vfutpasptcmvocsg": f"{self._preptc_stem}nde",  # portande
                "Vfutpasptcmaccsg": f"{self._preptc_stem}ndum",  # portandum
                "Vfutpasptcmgensg": f"{self._preptc_stem}ndi",  # portandi
                "Vfutpasptcmdatsg": f"{self._preptc_stem}ndo",  # portando
                "Vfutpasptcmablsg": f"{self._preptc_stem}ndo",  # portando
                "Vfutpasptcmnompl": f"{self._preptc_stem}ndi",  # portandi
                "Vfutpasptcmvocpl": f"{self._preptc_stem}ndi",  # portandi
                "Vfutpasptcmaccpl": f"{self._preptc_stem}ndos",  # portandos
                "Vfutpasptcmgenpl": f"{self._preptc_stem}ndorum",  # portandorum
                "Vfutpasptcmdatpl": f"{self._preptc_stem}ndis",  # portandis
                "Vfutpasptcmablpl": f"{self._preptc_stem}ndis",  # portandis
                "Vfutpasptcfnomsg": f"{self._preptc_stem}nda",  # portanda
                "Vfutpasptcfvocsg": f"{self._preptc_stem}nda",  # portanda
                "Vfutpasptcfaccsg": f"{self._preptc_stem}ndam",  # portandam
                "Vfutpasptcfgensg": f"{self._preptc_stem}ndae",  # portandae
                "Vfutpasptcfdatsg": f"{self._preptc_stem}ndae",  # portandae
                "Vfutpasptcfablsg": f"{self._preptc_stem}nda",  # portanda
                "Vfutpasptcfnompl": f"{self._preptc_stem}ndae",  # portandae
                "Vfutpasptcfvocpl": f"{self._preptc_stem}ndae",  # portandae
                "Vfutpasptcfaccpl": f"{self._preptc_stem}ndas",  # portandas
                "Vfutpasptcfgenpl": f"{self._preptc_stem}ndarum",  # portandarum
                "Vfutpasptcfdatpl": f"{self._preptc_stem}ndis",  # portandis
                "Vfutpasptcfablpl": f"{self._preptc_stem}ndis",  # portandis
                "Vfutpasptcnnomsg": f"{self._preptc_stem}ndum",  # portandum
                "Vfutpasptcnvocsg": f"{self._preptc_stem}ndum",  # portandum
                "Vfutpasptcnaccsg": f"{self._preptc_stem}ndum",  # portandum
                "Vfutpasptcngensg": f"{self._preptc_stem}ndi",  # portandi
                "Vfutpasptcndatsg": f"{self._preptc_stem}ndo",  # portando
                "Vfutpasptcnablsg": f"{self._preptc_stem}ndo",  # portando
                "Vfutpasptcnnompl": f"{self._preptc_stem}nda",  # portanda
                "Vfutpasptcnvocpl": f"{self._preptc_stem}nda",  # portanda
                "Vfutpasptcnaccpl": f"{self._preptc_stem}nda",  # portanda
                "Vfutpasptcngenpl": f"{self._preptc_stem}ndorum",  # portandorum
                "Vfutpasptcndatpl": f"{self._preptc_stem}ndis",  # portandis
                "Vfutpasptcnablpl": f"{self._preptc_stem}ndis",  # portandis
            }

        if (not self.no_ppp) or self.fap_fourthpp:
            if not self.no_fap:
                endings |= {
                    "Vfutactptcmnomsg": f"{self._fap_stem}us",  # portaturus
                    "Vfutactptcmvocsg": f"{self._fap_stem}e",  # portature
                    "Vfutactptcmaccsg": f"{self._fap_stem}um",  # portaturum
                    "Vfutactptcmgensg": f"{self._fap_stem}i",  # portaturi
                    "Vfutactptcmdatsg": f"{self._fap_stem}o",  # portaturo
                    "Vfutactptcmablsg": f"{self._fap_stem}o",  # portaturo
                    "Vfutactptcmnompl": f"{self._fap_stem}i",  # portaturi
                    "Vfutactptcmvocpl": f"{self._fap_stem}i",  # portaturi
                    "Vfutactptcmaccpl": f"{self._fap_stem}os",  # portaturos
                    "Vfutactptcmgenpl": f"{self._fap_stem}orum",  # portaturorum
                    "Vfutactptcmdatpl": f"{self._fap_stem}is",  # portaturis
                    "Vfutactptcmablpl": f"{self._fap_stem}is",  # portaturis
                    "Vfutactptcfnomsg": f"{self._fap_stem}a",  # portatura
                    "Vfutactptcfvocsg": f"{self._fap_stem}a",  # portatura
                    "Vfutactptcfaccsg": f"{self._fap_stem}am",  # portaturam
                    "Vfutactptcfgensg": f"{self._fap_stem}ae",  # portaturae
                    "Vfutactptcfdatsg": f"{self._fap_stem}ae",  # portaturae
                    "Vfutactptcfablsg": f"{self._fap_stem}a",  # portatura
                    "Vfutactptcfnompl": f"{self._fap_stem}ae",  # portaturae
                    "Vfutactptcfvocpl": f"{self._fap_stem}ae",  # portaturae
                    "Vfutactptcfaccpl": f"{self._fap_stem}as",  # portaturas
                    "Vfutactptcfgenpl": f"{self._fap_stem}arum",  # portarum
                    "Vfutactptcfdatpl": f"{self._fap_stem}is",  # portaturis
                    "Vfutactptcfablpl": f"{self._fap_stem}is",  # portaturis
                    "Vfutactptcnnomsg": f"{self._fap_stem}um",  # portaturum
                    "Vfutactptcnvocsg": f"{self._fap_stem}um",  # portaturum
                    "Vfutactptcnaccsg": f"{self._fap_stem}um",  # portaturum
                    "Vfutactptcngensg": f"{self._fap_stem}i",  # portaturi
                    "Vfutactptcndatsg": f"{self._fap_stem}o",  # portaturo
                    "Vfutactptcnablsg": f"{self._fap_stem}o",  # portaturo
                    "Vfutactptcnnompl": f"{self._fap_stem}a",  # portatura
                    "Vfutactptcnvocpl": f"{self._fap_stem}a",  # portatura
                    "Vfutactptcnaccpl": f"{self._fap_stem}a",  # portatura
                    "Vfutactptcngenpl": f"{self._fap_stem}orum",  # portaturorum
                    "Vfutactptcndatpl": f"{self._fap_stem}is",  # portaturis
                    "Vfutactptcnablpl": f"{self._fap_stem}is",  # portaturis
                }

            if not self.fap_fourthpp:
                assert self.ppp is not None
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

        if self.deponent:
            return {
                (
                    key[:4] + "dep" + key[7:]
                    if key[4:7] == Voice.ACTIVE.shorthand
                    else key
                ): value
                for key, value in endings.items()
            }

        return endings

    def _verbal_nouns(self) -> Endings:
        endings: Endings = {}

        if not self.no_gerund:
            endings |= {
                "Vgeracc": f"{self._preptc_stem}ndum",  # portandum
                "Vgergen": f"{self._preptc_stem}ndi",  # portandi
                "Vgerdat": f"{self._preptc_stem}ndo",  # portando
                "Vgerabl": f"{self._preptc_stem}ndo",  # portando
            }

        if not self.no_supine:
            endings |= {
                "Vsupacc": f"{self._ppp_stem}um",  # portatum
                "Vsupabl": f"{self._ppp_stem}u",  # portatu
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

    def create_components_instance(self, key: str) -> EndingComponents:  # noqa: PLR6301
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

    @deprecated(
        "A regular method was favoured over a staticmethod. Use `create_components_instance` instead."
    )
    @staticmethod
    def create_components(key: str) -> EndingComponents:
        """Generate an ``EndingComponents`` object based on endings keys.

        Deprecated in favour of ``create_components_instance`` instead.
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
        return Verb.create_components_instance(placeholder_verb, key)

    def __repr__(self) -> str:
        if self.conjugation == 0:
            return f"Verb({self.present}, meaning={self.meaning})"

        if self.deponent or self.semi_deponent:
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

        if self.deponent or self.semi_deponent:
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
            and self.semi_deponent
            == other.semi_deponent  # Add semi_deponent check
        ):
            return NotImplemented

        # For deponent and semi-deponent, ppp is None in the constructor call,
        # as it's derived from the perfect form.
        ppp_arg = None
        if not self.deponent and not self.semi_deponent:
            ppp_arg = self.ppp

        if self.meaning == other.meaning:
            return _create_verb(
                self.present,
                self.infinitive,
                self.perfect,
                ppp_arg,
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
            ppp_arg,
            meaning=new_meaning,
        )
