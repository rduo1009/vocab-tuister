from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

from ...utils import set_choice
from ..accido.endings import Adjective, Noun, Pronoun, Verb
from ..accido.misc import (
    Case,
    ComponentsSubtype,
    Gender,
    Mood,
    MultipleEndings,
    Number,
    Tense,
    Voice,
)
from ..transfero.words import find_inflection
from ._base import MultiAnswerQuestion
from ._utils import pick_ending, pick_ending_from_multipleendings

if TYPE_CHECKING:
    from ..accido.endings import _Word
    from ..accido.type_aliases import Ending, Endings


@dataclass
class TypeInEngToLatQuestion(MultiAnswerQuestion[str]):
    """A question that asks for the Latin translation of an English word.

    For example, "I search" (answer: "quaero")

    Attributes
    ----------
    prompt : str
        The prompt for the question (in English).
    main_answer : str
        The best answer to the question (in Latin).
    answers : set[str]
        The possible answers to the question (in Latin).
    """

    prompt: str


def generate_typein_engtolat(  # noqa: PLR0914, PLR0915
    chosen_word: _Word,
    filtered_endings: Endings,
    *,
    english_subjunctives: bool = False,
    english_verbal_nouns: bool = False,
) -> TypeInEngToLatQuestion | None:
    # Pick ending, getting the ending dict key to the ending as well
    ending_components_key, chosen_ending = pick_ending(filtered_endings)
    chosen_ending = pick_ending_from_multipleendings(chosen_ending)

    # Using the dict key, create an `EndingComponents`
    ending_components = chosen_word.create_components_instance(
        ending_components_key
    )

    # Unsupported endings
    # Subjunctives cannot be translated to English if the setting is not selected
    verb_subjunctive = (
        isinstance(chosen_word, Verb)
        and ending_components.mood == Mood.SUBJUNCTIVE
        and not english_subjunctives
    )

    # Gerundives translate weirdly (and too similar to present passive infinitive)
    verb_gerundive_flag = (
        isinstance(chosen_word, Verb)
        and ending_components.subtype == ComponentsSubtype.PARTICIPLE
        and ending_components.tense == Tense.FUTURE
        and ending_components.voice == Voice.PASSIVE
        and ending_components.mood == Mood.PARTICIPLE
    )

    verb_verbal_noun_flag = (
        isinstance(chosen_word, Verb)
        and ending_components.subtype == ComponentsSubtype.VERBAL_NOUN
        and not english_verbal_nouns
    )

    if verb_subjunctive or verb_gerundive_flag or verb_verbal_noun_flag:
        return None

    # Double-up endings
    noun_nom_acc_voc = isinstance(
        chosen_word, Noun
    ) and ending_components.case in {
        Case.NOMINATIVE,
        Case.ACCUSATIVE,
        Case.VOCATIVE,
    }

    adjective_not_adverb_flag = (
        isinstance(chosen_word, Adjective)
        and ending_components.subtype != ComponentsSubtype.ADVERB
    )

    participle_flag = (
        isinstance(chosen_word, Verb)
        and ending_components.subtype == ComponentsSubtype.PARTICIPLE
    )

    verb_second_person_flag = (
        isinstance(chosen_word, Verb)
        and ending_components.subtype
        not in {
            ComponentsSubtype.INFINITIVE,
            ComponentsSubtype.PARTICIPLE,
            ComponentsSubtype.VERBAL_NOUN,
        }
        and ending_components.person == 2  # noqa: PLR2004
    )

    pronoun_flag = isinstance(chosen_word, Pronoun)

    answers = {chosen_ending}

    # Nominative, vocative, accusative nouns translate the same way
    # NOTE: Might change later? Give accusative nouns a separate meaning
    if noun_nom_acc_voc:
        assert isinstance(chosen_word, Noun)

        endings_to_add = (
            chosen_word.get(
                case=Case.NOMINATIVE, number=ending_components.number
            ),
            chosen_word.get(
                case=Case.ACCUSATIVE, number=ending_components.number
            ),
            chosen_word.get(
                case=Case.VOCATIVE, number=ending_components.number
            ),
        )
        for ending in filter(None, endings_to_add):
            if isinstance(ending, str):
                answers.add(ending)
            else:
                assert isinstance(ending, MultipleEndings)
                answers.update(ending.get_all())

    # Adjectives all translate the same if they have the same degree
    elif adjective_not_adverb_flag:
        assert isinstance(chosen_word, Adjective)

        answers = {
            item
            for key, value in chosen_word.endings.items()
            if key.startswith("A")
            and key[1:4] == ending_components.degree.shorthand  # same degree
            for item in (  # unpack `MultipleEndings`
                value.get_all()
                if isinstance(value, MultipleEndings)
                else [value]
            )
        }

        chosen_ending = str(  # __str__ returns main ending
            chosen_word.get(
                case=Case.NOMINATIVE,
                number=Number.SINGULAR,
                gender=Gender.MASCULINE,
                degree=ending_components.degree,
            )
        )

    # All participles translate the same way
    elif participle_flag:
        assert isinstance(chosen_word, Verb)

        answers = {
            item
            for key, value in chosen_word.endings.items()
            if key[7:10] == Mood.PARTICIPLE.shorthand
            for item in (  # unpack `MultipleEndings`
                value.get_all()
                if isinstance(value, MultipleEndings)
                else [value]
            )
        }

        chosen_ending = str(  # __str__ returns main ending
            chosen_word.get(
                tense=ending_components.tense,
                voice=ending_components.voice,
                mood=Mood.PARTICIPLE,
                number=Number.SINGULAR,
                participle_case=Case.NOMINATIVE,
                participle_gender=Gender.MASCULINE,
            )
        )

    # English doesn't have 2nd person plural, so it's the same as singular
    elif verb_second_person_flag:
        assert isinstance(chosen_word, Verb)

        if second_person_plural := chosen_word.get(
            tense=ending_components.tense,
            voice=ending_components.voice,
            mood=ending_components.mood,
            number=Number.PLURAL,
            person=2,
        ):
            if isinstance(second_person_plural, MultipleEndings):
                temp_second_person_plural = tuple(
                    second_person_plural.get_all()
                )
            else:
                temp_second_person_plural = (second_person_plural,)

            answers = {
                chosen_ending,  # second person singular
                *temp_second_person_plural,
            }
        else:
            answers = {chosen_ending}

    # All pronouns translate the same way if same case and number
    elif pronoun_flag:
        assert isinstance(chosen_word, Pronoun)

        @overload
        def _convert_to_tuple(ending: Ending) -> tuple[str, ...]: ...
        @overload
        def _convert_to_tuple(ending: None) -> tuple[None]: ...

        def _convert_to_tuple(
            ending: Ending | None,
        ) -> tuple[str, ...] | tuple[None]:
            if ending is None:
                return ()

            if isinstance(ending, MultipleEndings):
                return tuple(ending.get_all())

            return (ending,)

        answers = {
            answer
            for gender in (Gender.MASCULINE, Gender.FEMININE, Gender.NEUTER)
            for answer in _convert_to_tuple(
                chosen_word.get(
                    case=ending_components.case,
                    number=ending_components.number,
                    gender=gender,
                )
            )
            if answer is not None
        }

        chosen_ending = str(
            chosen_word.get(
                case=ending_components.case,
                number=ending_components.number,
                gender=Gender.MASCULINE,
            )
        )

    # Determine meaning
    raw_meaning = str(chosen_word.meaning)  # __str__ returns main ending
    inflected_meaning = set_choice(
        find_inflection(raw_meaning, components=ending_components)
    )

    return TypeInEngToLatQuestion(
        prompt=inflected_meaning, main_answer=chosen_ending, answers=answers
    )
