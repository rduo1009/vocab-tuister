"""Contains functions that inflect English verbs."""

from __future__ import annotations

from typing import TYPE_CHECKING

import lemminflect

from ..accido.misc import (
    ComponentsSubtype,
    ComponentsType,
    Mood,
    Number,
    Tense,
    Voice,
)
from ._edge_cases import STATIVE_VERBS
from .exceptions import InvalidComponentsError, InvalidWordError

if TYPE_CHECKING:
    from ..accido.misc import EndingComponents
    from ..accido.type_aliases import Person


def _verify_verb_inflections(components: EndingComponents) -> None:
    if components.type is not ComponentsType.VERB:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    if (
        components.mood == Mood.PARTICIPLE
        and components.subtype != ComponentsSubtype.PARTICIPLE
    ):
        raise InvalidComponentsError(
            f"Invalid subtype: '{components.subtype}'"
        )

    if (
        components.mood == Mood.INFINITIVE
        and components.subtype != ComponentsSubtype.INFINITIVE
    ):
        raise InvalidComponentsError(
            f"Invalid subtype: '{components.subtype}'"
        )


def find_verb_inflections(
    verb: str, components: EndingComponents
) -> tuple[str, ...]:
    """Inflect English verbs using the ending components.

    If a participle is queried, ``find_participle_inflections`` is ran
    instead.

    Parameters
    ----------
    verb : str
        The verb to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    tuple[str, ...]
        The possible forms of the verb (main form first).

    Raises
    ------
    InvalidWordError
        If `verb` is not a valid English verb.
    InvalidComponentsError
        If `components` is invalid.
    """
    _verify_verb_inflections(components)

    if components.mood in {Mood.GERUND, Mood.SUPINE}:
        return _find_verbal_noun_inflections(verb, components)

    # For English inflection, deponent and semi-deponent verbs are treated based on context
    # Deponent: always active in meaning.
    # Semi-deponent: active in present system, passive (in form and meaning) in perfect system.
    if components.voice == Voice.DEPONENT:
        components.voice = Voice.ACTIVE
    elif components.voice == Voice.SEMI_DEPONENT:
        if components.tense in {
            Tense.PERFECT,
            Tense.PLUPERFECT,
            Tense.FUTURE_PERFECT,
        }:
            components.voice = Voice.PASSIVE  # Perfect system is passive
        else:
            components.voice = Voice.ACTIVE  # Present system is active

    if components.mood == Mood.PARTICIPLE:
        return _find_participle_inflections(verb, components)

    try:
        lemmas = lemminflect.getLemma(verb, "VERB")
    except KeyError as e:
        raise InvalidWordError(f"Word {verb} is not a verb.") from e

    inflections: list[str] = []
    if hasattr(components, "number") and hasattr(components, "person"):
        for lemma in lemmas:
            inflections.extend(
                _inflect_lemma(
                    lemma,
                    components.tense,
                    components.voice,
                    components.mood,
                    components.number,
                    components.person,
                )
            )
    else:
        for lemma in lemmas:
            inflections.extend(
                _inflect_lemma(
                    lemma, components.tense, components.voice, components.mood
                )
            )

    # dict.fromkeys() removes duplicates but keeps order
    return tuple(dict.fromkeys(inflections))


def _inflect_lemma(  # noqa: PLR0917
    lemma: str,
    tense: Tense,
    voice: Voice,
    mood: Mood,
    number: Number | None = None,
    person: Person | None = None,
) -> tuple[str, ...]:
    to_match = (tense, voice, mood)

    match to_match:
        case (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE):
            return _find_preactipe_inflections(lemma)

        case (Tense.PRESENT, Voice.PASSIVE, Mood.IMPERATIVE):
            return _find_prepasipe_inflections(lemma)

        case (Tense.PRESENT, Voice.ACTIVE, Mood.INFINITIVE):
            return _find_preactinf_inflections(lemma)

        case (Tense.FUTURE, Voice.ACTIVE, Mood.INFINITIVE):
            return _find_futactinf_inflections(lemma)

        case (Tense.PERFECT, Voice.ACTIVE, Mood.INFINITIVE):
            return _find_peractinf_inflections(lemma)

        case (Tense.PRESENT, Voice.PASSIVE, Mood.INFINITIVE):
            return _find_prepasinf_inflections(lemma)

        case (Tense.FUTURE, Voice.PASSIVE, Mood.INFINITIVE):
            return _find_futpasinf_inflections(lemma)

        case (Tense.PERFECT, Voice.PASSIVE, Mood.INFINITIVE):
            return _find_perpasinf_inflections(lemma)

        case _:
            pass

    assert number is not None
    assert person is not None

    match to_match:
        case (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE):
            return _find_preactind_inflections(lemma, number, person)

        case (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            return _find_impactind_inflections(lemma, number, person)

        case (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE):
            return _find_futactind_inflections(lemma, number, person)

        case (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            return _find_peractind_inflections(lemma, number, person)

        case (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            return _find_plpactind_inflections(lemma, number, person)

        case (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            return _find_fpractind_inflections(lemma, number, person)

        case (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE):
            return _find_prepasind_inflections(lemma, number, person)

        case (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            return _find_imppasind_inflections(lemma, number, person)

        case (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE):
            return _find_futpasind_inflections(lemma, number, person)

        case (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            return _find_perpasind_inflections(lemma, number, person)

        case (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            return _find_plppasind_inflections(lemma, number, person)

        case (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            return _find_fprpasind_inflections(lemma, number, person)

        case (Tense.PRESENT, Voice.ACTIVE, Mood.SUBJUNCTIVE):
            return _find_preactsbj_inflections(lemma, number, person)

        case (Tense.IMPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE):
            return _find_impactsbj_inflections(lemma, number, person)

        case (Tense.PERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE):
            return _find_peractsbj_inflections(lemma, number, person)

        case (Tense.PLUPERFECT, Voice.ACTIVE, Mood.SUBJUNCTIVE):
            return _find_plpactsbj_inflections(lemma, number, person)

        case (Tense.PRESENT, Voice.PASSIVE, Mood.SUBJUNCTIVE):
            return _find_prepassbj_inflections(lemma, number, person)

        case (Tense.IMPERFECT, Voice.PASSIVE, Mood.SUBJUNCTIVE):
            return _find_imppassbj_inflections(lemma, number, person)

        case (Tense.PERFECT, Voice.PASSIVE, Mood.SUBJUNCTIVE):
            return _find_perpassbj_inflections(lemma, number, person)

        case (Tense.PLUPERFECT, Voice.PASSIVE, Mood.SUBJUNCTIVE):
            return _find_plppassbj_inflections(lemma, number, person)

        case (Tense.FUTURE, Voice.ACTIVE, Mood.IMPERATIVE):
            return _find_futactipe_inflections(lemma, number, person)

        case (Tense.FUTURE, Voice.PASSIVE, Mood.IMPERATIVE):
            return _find_futpasipe_inflections(lemma, number, person)

        case _:
            pass

    raise NotImplementedError(
        f"The {tense.regular} {voice.regular} "
        f"{mood.regular} has not been implemented."
    )


def _find_preactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    present_nonthird = lemminflect.getInflection(lemma, "VBP")[0]
    present_third = lemminflect.getInflection(lemma, "VBZ")[0]
    present_participle = lemminflect.getInflection(lemma, "VBG")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I {present_nonthird}", f"I am {present_participle}")

        case (Number.PLURAL, 1):
            return (f"we {present_nonthird}", f"we are {present_participle}")

        case (Number.SINGULAR, 2):
            return (f"you {present_nonthird}", f"you are {present_participle}")

        case (Number.PLURAL, 2):
            return (
                f"you all {present_nonthird}",
                f"you all are {present_participle}",
                f"you {present_nonthird}",
                f"you are {present_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he {present_third}",
                f"he is {present_participle}",
                f"she {present_third}",
                f"she is {present_participle}",
                f"it {present_third}",
                f"it is {present_participle}",
            )

        case _:
            return (
                f"they {present_nonthird}",
                f"they are {present_participle}",
            )


def _find_prepasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I am {past_participle}", f"I am being {past_participle}")

        case (Number.PLURAL, 1):
            return (
                f"we are {past_participle}",
                f"we are being {past_participle}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you are {past_participle}",
                f"you are being {past_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all are {past_participle}",
                f"you all are being {past_participle}",
                f"you are {past_participle}",
                f"you are being {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he is {past_participle}",
                f"he is being {past_participle}",
                f"she is {past_participle}",
                f"she is being {past_participle}",
                f"it is {past_participle}",
                f"it is being {past_participle}",
            )

        case _:
            return (
                f"they are {past_participle}",
                f"they are being {past_participle}",
            )


def _find_impactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    present_participle = lemminflect.getInflection(lemma, "VBG")[0]

    if lemma in STATIVE_VERBS:
        past = lemminflect.getInflection(lemma, "VBD")[0]

        match (number, person):
            case (Number.SINGULAR, 1):
                return (
                    f"I {past}",
                    f"I was {present_participle}",
                    f"I used to {lemma}",
                    f"I began to {lemma}",
                    f"I kept {present_participle}",
                )

            case (Number.PLURAL, 1):
                return (
                    f"we {past}",
                    f"we were {present_participle}",
                    f"we used to {lemma}",
                    f"we began to {lemma}",
                    f"we kept {present_participle}",
                )

            case (Number.SINGULAR, 2):
                return (
                    f"you {past}",
                    f"you were {present_participle}",
                    f"you used to {lemma}",
                    f"you began to {lemma}",
                    f"you kept {present_participle}",
                )

            case (Number.PLURAL, 2):
                return (
                    f"you all {past}",
                    f"you all were {present_participle}",
                    f"you all used to {lemma}",
                    f"you all began to {lemma}",
                    f"you all kept {present_participle}",
                    f"you {past}",
                    f"you were {present_participle}",
                    f"you used to {lemma}",
                    f"you began to {lemma}",
                    f"you kept {present_participle}",
                )

            case (Number.SINGULAR, 3):
                return (
                    f"he {past}",
                    f"he was {present_participle}",
                    f"he used to {lemma}",
                    f"he began to {lemma}",
                    f"he kept {present_participle}",
                    f"she {past}",
                    f"she was {present_participle}",
                    f"she used to {lemma}",
                    f"she began to {lemma}",
                    f"she kept {present_participle}",
                    f"it {past}",
                    f"it was {present_participle}",
                    f"it used to {lemma}",
                    f"it began to {lemma}",
                    f"it kept {present_participle}",
                )

            case _:
                return (
                    f"they {past}",
                    f"they were {present_participle}",
                    f"they used to {lemma}",
                    f"they began to {lemma}",
                    f"they kept {present_participle}",
                )

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I was {present_participle}",
                f"I used to {lemma}",
                f"I began to {lemma}",
                f"I kept {present_participle}",
            )

        case (Number.PLURAL, 1):
            return (
                f"we were {present_participle}",
                f"we used to {lemma}",
                f"we began to {lemma}",
                f"we kept {present_participle}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you were {present_participle}",
                f"you used to {lemma}",
                f"you began to {lemma}",
                f"you kept {present_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all were {present_participle}",
                f"you all used to {lemma}",
                f"you all began to {lemma}",
                f"you all kept {present_participle}",
                f"you were {present_participle}",
                f"you used to {lemma}",
                f"you began to {lemma}",
                f"you kept {present_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he was {present_participle}",
                f"he used to {lemma}",
                f"he began to {lemma}",
                f"he kept {present_participle}",
                f"she was {present_participle}",
                f"she used to {lemma}",
                f"she began to {lemma}",
                f"she kept {present_participle}",
                f"it was {present_participle}",
                f"it used to {lemma}",
                f"it began to {lemma}",
                f"it kept {present_participle}",
            )

        case _:
            return (
                f"they were {present_participle}",
                f"they used to {lemma}",
                f"they began to {lemma}",
                f"they kept {present_participle}",
            )


def _find_imppasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I was {past_participle}",
                f"I was being {past_participle}",
                f"I used to be {past_participle}",
                f"I began to be {past_participle}",
                f"I kept being {past_participle}",
            )

        case (Number.PLURAL, 1):
            return (
                f"we were {past_participle}",
                f"we were being {past_participle}",
                f"we used to be {past_participle}",
                f"we began to be {past_participle}",
                f"we kept being {past_participle}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you were {past_participle}",
                f"you were being {past_participle}",
                f"you used to be {past_participle}",
                f"you began to be {past_participle}",
                f"you kept being {past_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all were {past_participle}",
                f"you all were being {past_participle}",
                f"you all used to be {past_participle}",
                f"you all began to be {past_participle}",
                f"you all kept being {past_participle}",
                f"you were {past_participle}",
                f"you were being {past_participle}",
                f"you used to be {past_participle}",
                f"you began to be {past_participle}",
                f"you kept being {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he was {past_participle}",
                f"he was being {past_participle}",
                f"he used to be {past_participle}",
                f"he began to be {past_participle}",
                f"he kept being {past_participle}",
                f"she was {past_participle}",
                f"she was being {past_participle}",
                f"she used to be {past_participle}",
                f"she began to be {past_participle}",
                f"she kept being {past_participle}",
                f"it was {past_participle}",
                f"it was being {past_participle}",
                f"it used to be {past_participle}",
                f"it began to be {past_participle}",
                f"it kept being {past_participle}",
            )

        case _:
            return (
                f"they were {past_participle}",
                f"they were being {past_participle}",
                f"they used to be {past_participle}",
                f"they began to be {past_participle}",
                f"they kept being {past_participle}",
            )


def _find_futactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    present_participle = lemminflect.getInflection(lemma, "VBG")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I will {lemma}",
                f"I will be {present_participle}",
                f"I shall {lemma}",
                f"I shall be {present_participle}",
            )

        case (Number.PLURAL, 1):
            return (
                f"we will {lemma}",
                f"we will be {present_participle}",
                f"we shall {lemma}",
                f"we shall be {present_participle}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you will {lemma}",
                f"you will be {present_participle}",
                f"you shall {lemma}",
                f"you shall be {present_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all will {lemma}",
                f"you all will be {present_participle}",
                f"you all shall {lemma}",
                f"you all shall be {present_participle}",
                f"you will {lemma}",
                f"you will be {present_participle}",
                f"you shall {lemma}",
                f"you shall be {present_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will {lemma}",
                f"he will be {present_participle}",
                f"he shall {lemma}",
                f"he shall be {present_participle}",
                f"she will {lemma}",
                f"she will be {present_participle}",
                f"she shall {lemma}",
                f"she shall be {present_participle}",
                f"it will {lemma}",
                f"it will be {present_participle}",
                f"it shall {lemma}",
                f"it shall be {present_participle}",
            )

        case _:
            return (
                f"they will {lemma}",
                f"they will be {present_participle}",
                f"they shall {lemma}",
                f"they shall be {present_participle}",
            )


def _find_futpasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I will be {past_participle}",
                f"I will be being {past_participle}",
                f"I shall be {past_participle}",
                f"I shall be being {past_participle}",
            )

        case (Number.PLURAL, 1):
            return (
                f"we will be {past_participle}",
                f"we will be being {past_participle}",
                f"we shall be {past_participle}",
                f"we shall be being {past_participle}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you will be {past_participle}",
                f"you will be being {past_participle}",
                f"you shall be {past_participle}",
                f"you shall be being {past_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all will be {past_participle}",
                f"you all will be being {past_participle}",
                f"you all shall be {past_participle}",
                f"you all shall be being {past_participle}",
                f"you will be {past_participle}",
                f"you will be being {past_participle}",
                f"you shall be {past_participle}",
                f"you shall be being {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will be {past_participle}",
                f"he will be being {past_participle}",
                f"he shall be {past_participle}",
                f"he shall be being {past_participle}",
                f"she will be {past_participle}",
                f"she will be being {past_participle}",
                f"she shall be {past_participle}",
                f"she shall be being {past_participle}",
                f"it will be {past_participle}",
                f"it will be being {past_participle}",
                f"it shall be {past_participle}",
                f"it shall be being {past_participle}",
            )

        case _:
            return (
                f"they will be {past_participle}",
                f"they will be being {past_participle}",
                f"they shall be {past_participle}",
                f"they shall be being {past_participle}",
            )


def _find_peractind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past = lemminflect.getInflection(lemma, "VBD")[0]
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I {past}", f"I have {past_participle}", f"I did {lemma}")

        case (Number.PLURAL, 1):
            return (
                f"we {past}",
                f"we have {past_participle}",
                f"we did {lemma}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you {past}",
                f"you have {past_participle}",
                f"you did {lemma}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all {past}",
                f"you all have {past_participle}",
                f"you all did {lemma}",
                f"you {past}",
                f"you have {past_participle}",
                f"you did {lemma}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he {past}",
                f"he has {past_participle}",
                f"he did {lemma}",
                f"she {past}",
                f"she has {past_participle}",
                f"she did {lemma}",
                f"it {past}",
                f"it has {past_participle}",
                f"it did {lemma}",
            )

        case _:
            return (
                f"they {past}",
                f"they have {past_participle}",
                f"they did {lemma}",
            )


def _find_perpasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I have been {past_participle}",
                f"I was {past_participle}",
            )

        case (Number.PLURAL, 1):
            return (
                f"we have been {past_participle}",
                f"we were {past_participle}",
            )

        case (Number.SINGULAR, 2):
            return (
                f"you have been {past_participle}",
                f"you were {past_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all have been {past_participle}",
                f"you all were {past_participle}",
                f"you have been {past_participle}",
                f"you were {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he has been {past_participle}",
                f"he was {past_participle}",
                f"she has been {past_participle}",
                f"she was {past_participle}",
                f"it has been {past_participle}",
                f"it was {past_participle}",
            )

        case _:
            return (
                f"they have been {past_participle}",
                f"they were {past_participle}",
            )


def _find_plpactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I had {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we had {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you had {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all had {past_participle}",
                f"you had {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he had {past_participle}",
                f"she had {past_participle}",
                f"it had {past_participle}",
            )

        case _:
            return (f"they had {past_participle}",)


def _find_plppasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I had been {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we had been {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you had been {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all had been {past_participle}",
                f"you had been {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he had been {past_participle}",
                f"she had been {past_participle}",
                f"it had been {past_participle}",
            )

        case _:
            return (f"they had been {past_participle}",)


def _find_fpractind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I will have {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we will have {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you will have {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all will have {past_participle}",
                f"you will have {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will have {past_participle}",
                f"she will have {past_participle}",
                f"it will have {past_participle}",
            )

        case _:
            return (f"they will have {past_participle}",)


def _find_fprpasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I will have been {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we will have been {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you will have been {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all will have been {past_participle}",
                f"you will have been {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will have been {past_participle}",
                f"she will have been {past_participle}",
                f"it will have been {past_participle}",
            )

        case _:
            return (f"they will have been {past_participle}",)


def _find_preactipe_inflections(lemma: str) -> tuple[str, ...]:
    return (lemminflect.getInflection(lemma, "VB")[0],)


def _find_prepasipe_inflections(lemma: str) -> tuple[str, ...]:
    return (f"be {lemminflect.getInflection(lemma, 'VBN')[0]}",)


def _find_futactipe_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    match (number, person):
        case (Number.SINGULAR, 2):
            return (f"you shall {lemma}", f"you will {lemma}")

        case (Number.SINGULAR, 3):
            return (f"let him {lemma}", f"let her {lemma}", f"let it {lemma}")

        case (Number.PLURAL, 2):
            return (
                f"you all shall {lemma}",
                f"you all will {lemma}",
                f"you shall {lemma}",
                f"you will {lemma}",
            )

        case (Number.PLURAL, 3):
            return (f"let them {lemma}",)

        case _:
            raise ValueError(
                f"Invalid number or person (given {number} {person})"
            )


def _find_futpasipe_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 2):
            return (
                f"you shall be {past_participle}",
                f"you will be {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"let him be {past_participle}",
                f"let her be {past_participle}",
                f"let it be {past_participle}",
            )

        case (Number.PLURAL, 2):
            return (
                f"you all shall be {past_participle}",
                f"you all will be {past_participle}",
                f"you shall be {past_participle}",
                f"you will be {past_participle}",
            )

        case (Number.PLURAL, 3):
            return (f"let them be {past_participle}",)

        case _:
            raise ValueError(
                f"Invalid number or person (given {number} {person})"
            )


def _find_preactinf_inflections(lemma: str) -> tuple[str, ...]:
    return (f"to {lemma}",)


def _find_futactinf_inflections(lemma: str) -> tuple[str, ...]:
    return (f"to be about to {lemma}",)


def _find_peractinf_inflections(lemma: str) -> tuple[str, ...]:
    return (f"to have {lemminflect.getInflection(lemma, 'VBN')[0]}",)


def _find_prepasinf_inflections(lemma: str) -> tuple[str, ...]:
    return (f"to be {lemminflect.getInflection(lemma, 'VBN')[0]}",)


def _find_futpasinf_inflections(lemma: str) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]
    return (f"to be about to be {past_participle}",)


def _find_perpasinf_inflections(lemma: str) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]
    return (f"to have been {past_participle}",)


def _find_preactsbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I may {lemma}",)

        case (Number.PLURAL, 1):
            return (f"we may {lemma}",)

        case (Number.SINGULAR, 2):
            return (f"you may {lemma}",)

        case (Number.PLURAL, 2):
            return (f"you all may {lemma}", f"you may {lemma}")

        case (Number.SINGULAR, 3):
            return (f"he may {lemma}", f"she may {lemma}", f"it may {lemma}")

        case _:
            return (f"they may {lemma}",)


def _find_impactsbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I might {lemma}",)

        case (Number.PLURAL, 1):
            return (f"we might {lemma}",)

        case (Number.SINGULAR, 2):
            return (f"you might {lemma}",)

        case (Number.PLURAL, 2):
            return (f"you all might {lemma}", f"you might {lemma}")

        case (Number.SINGULAR, 3):
            return (
                f"he might {lemma}",
                f"she might {lemma}",
                f"it might {lemma}",
            )

        case _:
            return (f"they might {lemma}",)


def _find_peractsbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I may have {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we may have {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you may have {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all may have {past_participle}",
                f"you may have {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he may have {past_participle}",
                f"she may have {past_participle}",
                f"it may have {past_participle}",
            )

        case _:
            return (f"they may have {past_participle}",)


def _find_plpactsbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I might have {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we might have {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you might have {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all might have {past_participle}",
                f"you might have {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he might have {past_participle}",
                f"she might have {past_participle}",
                f"it might have {past_participle}",
            )

        case _:
            return (f"they might have {past_participle}",)


def _find_prepassbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I may be {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we may be {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you may be {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all may be {past_participle}",
                f"you may be {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he may be {past_participle}",
                f"she may be {past_participle}",
                f"it may be {past_participle}",
            )

        case _:
            return (f"they may be {past_participle}",)


def _find_imppassbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I might be {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we might be {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you might be {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all might be {past_participle}",
                f"you might be {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he might be {past_participle}",
                f"she might be {past_participle}",
                f"it might be {past_participle}",
            )

        case _:
            return (f"they might be {past_participle}",)


def _find_perpassbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I may have been {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we may have been {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you may have been {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all may have been {past_participle}",
                f"you may have been {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he may have been {past_participle}",
                f"she may have been {past_participle}",
                f"it may have been {past_participle}",
            )

        case _:
            return (f"they may have been {past_participle}",)


def _find_plppassbj_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, ...]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I might have been {past_participle}",)

        case (Number.PLURAL, 1):
            return (f"we might have been {past_participle}",)

        case (Number.SINGULAR, 2):
            return (f"you might have been {past_participle}",)

        case (Number.PLURAL, 2):
            return (
                f"you all might have been {past_participle}",
                f"you might have been {past_participle}",
            )

        case (Number.SINGULAR, 3):
            return (
                f"he might have been {past_participle}",
                f"she might have been {past_participle}",
                f"it might have been {past_participle}",
            )

        case _:
            return (f"they might have been {past_participle}",)


def _find_participle_inflections(
    verb: str, components: EndingComponents
) -> tuple[str, ...]:
    lemma = lemminflect.getLemma(verb, "VERB")[0]

    match (components.tense, components.voice):
        case (Tense.PRESENT, Voice.ACTIVE):
            present_participle = lemminflect.getInflection(lemma, "VBG")[0]
            return (present_participle,)

        case (Tense.PERFECT, Voice.ACTIVE):
            past_participle = lemminflect.getInflection(lemma, "VBN")[0]
            return (f"having {past_participle}",)

        case (Tense.PERFECT, Voice.PASSIVE):
            past_participle = lemminflect.getInflection(lemma, "VBN")[0]
            return (f"having been {past_participle}", past_participle)

        case (Tense.FUTURE, Voice.ACTIVE):
            return (f"about to {lemma}",)

        case (Tense.FUTURE, Voice.PASSIVE):
            past_participle = lemminflect.getInflection(lemma, "VBN")[0]
            return (
                f"requiring to be {past_participle}",
                f"to be {past_participle}",
            )

        case _:
            raise NotImplementedError(
                f"The {components.tense.regular} {components.voice.regular} "
                "participle has not been implemented."
            )


def _find_verbal_noun_inflections(
    verb: str, components: EndingComponents
) -> tuple[str, ...]:
    lemma = lemminflect.getLemma(verb, "VERB")[0]

    match components.mood:
        case Mood.GERUND:
            return (lemminflect.getInflection(lemma, "VBG")[0],)

        case Mood.SUPINE:
            return (f"to {lemma}",)

        case _:
            raise NotImplementedError(
                f"The {components.mood.regular} has not been implemented."
            )
