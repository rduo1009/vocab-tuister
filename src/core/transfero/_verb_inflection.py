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
from .edge_cases import STATIVE_VERBS
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


def find_verb_inflections(verb: str, components: EndingComponents) -> set[str]:
    """Inflect English verbs using the ending components.

    If a participle is queried, ``find_participle_inflections`` is ran
    instead.

    Note that subjunctives are not supported as they do not have an exact
    translation in English.

    Parameters
    ----------
    verb : str
        The verb to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    set[str]
        The possible forms of the verb.

    Raises
    ------
    InvalidWordError
        If `verb` is not a valid English verb.
    InvalidComponentsError
        If `components` is invalid.
    """
    _verify_verb_inflections(components)

    if components.voice == Voice.DEPONENT:
        components.voice = Voice.ACTIVE

    if components.mood == Mood.PARTICIPLE:
        return _find_participle_inflections(verb, components)[1]

    try:
        lemmas = lemminflect.getLemma(verb, "VERB")
    except KeyError as e:
        raise InvalidWordError(f"Word {verb} is not a verb.") from e

    inflections: set[str] = set()
    if hasattr(components, "number") and hasattr(components, "person"):
        for lemma in lemmas:
            inflections |= _find_lemma(
                lemma,
                components.tense,
                components.voice,
                components.mood,
                components.number,
                components.person,
            )[1]
    else:
        for lemma in lemmas:
            inflections |= _find_lemma(
                lemma, components.tense, components.voice, components.mood
            )[1]

    return inflections


def find_main_verb_inflection(verb: str, components: EndingComponents) -> str:
    """Find the main inflection of an English verb.

    Parameters
    ----------
    verb : str
        The verb to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    str
        The main inflection of the verb.

    Raises
    ------
    InvalidWordError
        If `verb` is not a valid English verb.
    InvalidComponentsError
        If `components` is invalid.
    """
    _verify_verb_inflections(components)

    if components.voice == Voice.DEPONENT:
        components.voice = Voice.ACTIVE

    if components.mood == Mood.PARTICIPLE:
        return _find_participle_inflections(verb, components)[0]

    try:
        lemma = lemminflect.getLemma(verb, "VERB")[0]
    except KeyError as e:
        raise InvalidWordError(f"Word {verb} is not a verb.") from e

    if hasattr(components, "number") and hasattr(components, "person"):
        return _find_lemma(
            lemma,
            components.tense,
            components.voice,
            components.mood,
            components.number,
            components.person,
        )[0]

    return _find_lemma(
        lemma, components.tense, components.voice, components.mood
    )[0]


def _find_lemma(  # noqa: PLR0917
    lemma: str,
    tense: Tense,
    voice: Voice,
    mood: Mood,
    number: Number | None = None,
    person: Person | None = None,
) -> tuple[str, set[str]]:
    match (tense, voice, mood):
        case (Tense.PRESENT, Voice.ACTIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_preactind_inflections(lemma, number, person)

        case (Tense.IMPERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_impactind_inflections(lemma, number, person)

        case (Tense.FUTURE, Voice.ACTIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_futactind_inflections(lemma, number, person)

        case (Tense.PERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_peractind_inflections(lemma, number, person)

        case (Tense.PLUPERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_plpactind_inflections(lemma, number, person)

        case (Tense.FUTURE_PERFECT, Voice.ACTIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_fpractind_inflections(lemma, number, person)

        case (Tense.PRESENT, Voice.PASSIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_prepasind_inflections(lemma, number, person)

        case (Tense.IMPERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_imppasind_inflections(lemma, number, person)

        case (Tense.FUTURE, Voice.PASSIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_futpasind_inflections(lemma, number, person)

        case (Tense.PERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_perpasind_inflections(lemma, number, person)

        case (Tense.PLUPERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_plppasind_inflections(lemma, number, person)

        case (Tense.FUTURE_PERFECT, Voice.PASSIVE, Mood.INDICATIVE):
            assert number is not None
            assert person is not None

            return _find_fprpasind_inflections(lemma, number, person)

        case (Tense.PRESENT, Voice.ACTIVE, Mood.INFINITIVE):
            return _find_preactinf_inflections(lemma)

        case (Tense.PRESENT, Voice.PASSIVE, Mood.INFINITIVE):
            return _find_prepasinf_inflections(lemma)

        case (Tense.PRESENT, Voice.ACTIVE, Mood.IMPERATIVE):
            return _find_preipe_inflections(lemma)

        case _:
            raise NotImplementedError(
                f"The {tense.regular} {voice.regular} "
                f"{mood.regular} has not been implemented."
            )


def _find_preactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    present_nonthird = lemminflect.getInflection(lemma, "VBP")[0]
    present_third = lemminflect.getInflection(lemma, "VBZ")[0]
    present_participle = lemminflect.getInflection(lemma, "VBG")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I {present_nonthird}",
                {f"I {present_nonthird}", f"I am {present_participle}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we {present_nonthird}",
                {f"we {present_nonthird}", f"we are {present_participle}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you {present_nonthird}",
                {f"you {present_nonthird}", f"you are {present_participle}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he {present_third}",
                {
                    f"he {present_third}",
                    f"he is {present_participle}",
                    f"she {present_third}",
                    f"she is {present_participle}",
                    f"it {present_third}",
                    f"it is {present_participle}",
                },
            )

    return (
        f"they {present_nonthird}",
        {f"they {present_nonthird}", f"they are {present_participle}"},
    )


def _find_prepasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I am {past_participle}",
                {f"I am {past_participle}", f"I am being {past_participle}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we are {past_participle}",
                {
                    f"we are {past_participle}",
                    f"we are being {past_participle}",
                },
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you are {past_participle}",
                {
                    f"you are {past_participle}",
                    f"you are being {past_participle}",
                },
            )

        case (Number.SINGULAR, 3):
            return (
                f"he is {past_participle}",
                {
                    f"he is {past_participle}",
                    f"he is being {past_participle}",
                    f"she is {past_participle}",
                    f"she is being {past_participle}",
                    f"it is {past_participle}",
                    f"it is being {past_participle}",
                },
            )

    return (
        f"they are {past_participle}",
        {f"they are {past_participle}", f"they are being {past_participle}"},
    )


def _find_impactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    present_participle = lemminflect.getInflection(lemma, "VBG")[0]

    if lemma in STATIVE_VERBS:
        past = lemminflect.getInflection(lemma, "VBD")[0]

        match (number, person):
            case (Number.SINGULAR, 1):
                return (
                    f"I {past}",
                    {f"I {past}", f"I was {present_participle}"},
                )

            case (Number.PLURAL, 1):
                return (
                    f"we {past}",
                    {f"we {past}", f"we were {present_participle}"},
                )

            case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
                return (
                    f"you {past}",
                    {f"you {past}", f"you were {present_participle}"},
                )

            case (Number.SINGULAR, 3):
                return (
                    f"he {past}",
                    {
                        f"he {past}",
                        f"he was {present_participle}",
                        f"she {past}",
                        f"she was {present_participle}",
                        f"it {past}",
                        f"it was {present_participle}",
                    },
                )

        return (
            f"they {past}",
            {f"they {past}", f"they were {present_participle}"},
        )

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I was {present_participle}",
                {f"I was {present_participle}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we were {present_participle}",
                {f"we were {present_participle}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you were {present_participle}",
                {f"you were {present_participle}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he was {present_participle}",
                {
                    f"he was {present_participle}",
                    f"she was {present_participle}",
                    f"it was {present_participle}",
                },
            )

    return (
        f"they were {present_participle}",
        {f"they were {present_participle}"},
    )


def _find_imppasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past = lemminflect.getInflection(lemma, "VBD")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I was being {past}", {f"I was being {past}"})

        case (Number.PLURAL, 1):
            return (f"we were being {past}", {f"we were being {past}"})

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (f"you were being {past}", {f"you were being {past}"})

        case (Number.SINGULAR, 3):
            return (
                f"he was being {past}",
                {
                    f"he was being {past}",
                    f"she was being {past}",
                    f"it was being {past}",
                },
            )

    return (f"they were being {past}", {f"they were being {past}"})


def _find_futactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    present = lemminflect.getInflection(lemma, "VBP")[0]
    present_participle = lemminflect.getInflection(lemma, "VBG")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I will {present}",
                {
                    f"I will {present}",
                    f"I will be {present_participle}",
                    f"I shall {present}",
                    f"I shall be {present_participle}",
                },
            )

        case (Number.PLURAL, 1):
            return (
                f"we will {present}",
                {
                    f"we will {present}",
                    f"we will be {present_participle}",
                    f"we shall {present}",
                    f"we shall be {present_participle}",
                },
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you will {present}",
                {
                    f"you will {present}",
                    f"you will be {present_participle}",
                    f"you shall {present}",
                    f"you shall be {present_participle}",
                },
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will {present}",
                {
                    f"he will {present}",
                    f"he will be {present_participle}",
                    f"he shall {present}",
                    f"he shall be {present_participle}",
                    f"she will {present}",
                    f"she will be {present_participle}",
                    f"she shall {present}",
                    f"she shall be {present_participle}",
                    f"it will {present}",
                    f"it will be {present_participle}",
                    f"it shall {present}",
                    f"it shall be {present_participle}",
                },
            )

    return (
        f"they will {present}",
        {
            f"they will {present}",
            f"they will be {present_participle}",
            f"they shall {present}",
            f"they shall be {present_participle}",
        },
    )


def _find_futpasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past = lemminflect.getInflection(lemma, "VBD")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I will be {past}",
                {
                    f"I will be {past}",
                    f"I will be being {past}",
                    f"I shall be {past}",
                    f"I shall be being {past}",
                },
            )

        case (Number.PLURAL, 1):
            return (
                f"we will be {past}",
                {
                    f"we will be {past}",
                    f"we will be being {past}",
                    f"we shall be {past}",
                    f"we shall be being {past}",
                },
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you will be {past}",
                {
                    f"you will be {past}",
                    f"you will be being {past}",
                    f"you shall be {past}",
                    f"you shall be being {past}",
                },
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will be {past}",
                {
                    f"he will be {past}",
                    f"he will be being {past}",
                    f"he shall be {past}",
                    f"he shall be being {past}",
                    f"she will be {past}",
                    f"she will be being {past}",
                    f"she shall be {past}",
                    f"she shall be being {past}",
                    f"it will be {past}",
                    f"it will be being {past}",
                    f"it shall be {past}",
                    f"it shall be being {past}",
                },
            )

    return (
        f"they will be {past}",
        {
            f"they will be {past}",
            f"they will be being {past}",
            f"they shall be {past}",
            f"they shall be being {past}",
        },
    )


def _find_peractind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past = lemminflect.getInflection(lemma, "VBD")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I {past}",
                {f"I {past}", f"I have {past}", f"I did {lemma}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we {past}",
                {f"we {past}", f"we have {past}", f"we did {lemma}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you {past}",
                {f"you {past}", f"you have {past}", f"you did {lemma}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he {past}",
                {
                    f"he {past}",
                    f"he has {past}",
                    f"he did {lemma}",
                    f"she {past}",
                    f"she has {past}",
                    f"she did {lemma}",
                    f"it {past}",
                    f"it has {past}",
                    f"it did {lemma}",
                },
            )

    return (
        f"they {past}",
        {f"they {past}", f"they have {past}", f"they did {lemma}"},
    )


def _find_perpasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past = lemminflect.getInflection(lemma, "VBD")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I was {past}", {f"I was {past}", f"I have been {past}"})

        case (Number.PLURAL, 1):
            return (
                f"we were {past}",
                {f"we were {past}", f"we have been {past}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you were {past}",
                {f"you were {past}", f"you have been {past}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he was {past}",
                {
                    f"he was {past}",
                    f"he has been {past}",
                    f"she was {past}",
                    f"she has been {past}",
                    f"it was {past}",
                    f"it has been {past}",
                },
            )

    return (
        f"they were {past}",
        {f"they were {past}", f"they have been {past}"},
    )


def _find_plpactind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (f"I had {past_participle}", {f"I had {past_participle}"})

        case (Number.PLURAL, 1):
            return (f"we had {past_participle}", {f"we had {past_participle}"})

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you had {past_participle}",
                {f"you had {past_participle}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he had {past_participle}",
                {
                    f"he had {past_participle}",
                    f"she had {past_participle}",
                    f"it had {past_participle}",
                },
            )

    return (f"they had {past_participle}", {f"they had {past_participle}"})


def _find_plppasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I had been {past_participle}",
                {f"I had been {past_participle}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we had been {past_participle}",
                {f"we had been {past_participle}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you had been {past_participle}",
                {f"you had been {past_participle}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he had been {past_participle}",
                {
                    f"he had been {past_participle}",
                    f"she had been {past_participle}",
                    f"it had been {past_participle}",
                },
            )

    return (
        f"they had been {past_participle}",
        {f"they had been {past_participle}"},
    )


def _find_fpractind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I will have {past_participle}",
                {f"I will have {past_participle}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we will have {past_participle}",
                {f"we will have {past_participle}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you will have {past_participle}",
                {f"you will have {past_participle}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will have {past_participle}",
                {
                    f"he will have {past_participle}",
                    f"she will have {past_participle}",
                    f"it will have {past_participle}",
                },
            )

    return (
        f"they will have {past_participle}",
        {f"they will have {past_participle}"},
    )


def _find_fprpasind_inflections(
    lemma: str, number: Number, person: Person
) -> tuple[str, set[str]]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    match (number, person):
        case (Number.SINGULAR, 1):
            return (
                f"I will have been {past_participle}",
                {f"I will have been {past_participle}"},
            )

        case (Number.PLURAL, 1):
            return (
                f"we will have been {past_participle}",
                {f"we will have been {past_participle}"},
            )

        case (Number.SINGULAR, 2) | (Number.PLURAL, 2):
            return (
                f"you will have been {past_participle}",
                {f"you will have been {past_participle}"},
            )

        case (Number.SINGULAR, 3):
            return (
                f"he will have been {past_participle}",
                {
                    f"he will have been {past_participle}",
                    f"she will have been {past_participle}",
                    f"it will have been {past_participle}",
                },
            )

    return (
        f"they will have been {past_participle}",
        {f"they will have been {past_participle}"},
    )


def _find_preipe_inflections(lemma: str) -> tuple[str, set[str]]:
    return (lemma, {lemma})


def _find_preactinf_inflections(lemma: str) -> tuple[str, set[str]]:
    return (f"to {lemma}", {f"to {lemma}"})


def _find_prepasinf_inflections(lemma: str) -> tuple[str, set[str]]:
    past_participle = lemminflect.getInflection(lemma, "VBN")[0]

    return (f"to be {past_participle}", {f"to be {past_participle}"})


def _find_participle_inflections(
    verb: str, components: EndingComponents
) -> tuple[str, set[str]]:
    lemma = lemminflect.getLemma(verb, "NOUN")[0]

    match (components.tense, components.voice):
        case (Tense.PRESENT, Voice.ACTIVE):
            present_participle = lemminflect.getInflection(lemma, "VBG")[0]
            return (present_participle, {present_participle})

        case (Tense.PERFECT, Voice.ACTIVE):
            past_participle = lemminflect.getInflection(lemma, "VBN")[0]
            return (f"having {past_participle}", {f"having {past_participle}"})

        case (Tense.PERFECT, Voice.PASSIVE):
            past_participle = lemminflect.getInflection(lemma, "VBN")[0]
            return (
                f"having been {past_participle}",
                {f"having been {past_participle}", past_participle},
            )

        case (Tense.FUTURE, Voice.ACTIVE):
            return (f"about to {lemma}", {f"about to {lemma}"})

        case _:
            raise NotImplementedError(
                f"The {components.tense.regular} {components.voice.regular} "
                "participle has not been implemented."
            )
