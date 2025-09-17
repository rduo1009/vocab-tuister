from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils import set_choice
from ..accido._class_pronoun import Pronoun
from ..accido.endings import Verb
from ..accido.misc import ComponentsSubtype, Mood
from ..transfero.exceptions import InvalidWordError
from ..transfero.synonyms import find_synonyms
from ..transfero.words import find_inflection
from ._base import MultiAnswerQuestion
from ._utils import (
    normalise_to_multiplemeanings,
    pick_ending,
    pick_ending_from_multipleendings,
)

if TYPE_CHECKING:
    from ..accido.endings import Word
    from ..accido.type_aliases import Endings


@dataclass
class TypeInLatToEngQuestion(MultiAnswerQuestion[str]):
    """A question that asks for the English translation of a Latin word.

    For example, "quaero" (answer: "I search")

    Attributes
    ----------
    prompt : str
        The prompt for the question (in Latin).
    main_answer : str
        The best answer to the question (in English).
    answers : set[str]
        The possible answers to the question (in English).
    """

    prompt: str


def generate_typein_lattoeng(
    chosen_word: Word,
    filtered_endings: Endings,
    *,
    english_subjunctives: bool = False,
    english_verbal_nouns: bool = False,
    synonyms: bool = False,
    similar_words: bool = False,
) -> TypeInLatToEngQuestion | None:
    # Pick ending
    _, chosen_ending = pick_ending(filtered_endings)
    chosen_ending = pick_ending_from_multipleendings(chosen_ending)

    # Find all possible `EndingComponents` for the ending
    all_ending_components = chosen_word.find(chosen_ending)
    possible_main_answers: set[str] = set()
    inflected_meanings: set[str] = set()

    for ending_components in all_ending_components:
        verb_subjunctive = (
            isinstance(chosen_word, Verb)
            and ending_components.mood == Mood.SUBJUNCTIVE
            and not english_subjunctives
        )

        verb_verbal_noun_flag = (
            isinstance(chosen_word, Verb)
            and ending_components.subtype == ComponentsSubtype.VERBAL_NOUN
            and not english_verbal_nouns
        )

        # Subjunctives cannot be translated to English if the setting is not selected
        if verb_subjunctive or verb_verbal_noun_flag:
            continue

        meanings = normalise_to_multiplemeanings(chosen_word.meaning)

        # Inflect meanings
        for meaning in meanings.meanings:
            inflected_meanings.update(
                find_inflection(meaning, components=ending_components)
            )

        # Add synonyms if requested
        if synonyms and not (
            isinstance(chosen_word, Pronoun)
            or ending_components.subtype == ComponentsSubtype.PRONOUN
        ):
            for meaning in find_synonyms(
                str(meanings),
                pos=type(chosen_word),
                known_synonyms=meanings.meanings[1:],
                include_similar_words=similar_words,
            ):
                # HACK: `find_inflection` currently doesn't support inflecting multi-word phrases
                # TODO: deal with this later
                if " " in meaning:
                    continue

                # Skip errors to make this part more resilient
                try:
                    inflected_meanings.update(
                        find_inflection(meaning, components=ending_components)
                    )
                except (IndexError, InvalidWordError):
                    continue

        # Inflect the main meaning (__str__ returns the main meaning)
        possible_main_answers.add(
            find_inflection(
                str(meanings), components=ending_components, main=True
            )
        )

    # If the loop went to `continue` every time (i.e. the ending was subjunctive)
    if not possible_main_answers:
        return None

    # Pick a main answer
    main_answer = set_choice(possible_main_answers)

    return TypeInLatToEngQuestion(
        prompt=chosen_ending,
        main_answer=main_answer,
        answers=inflected_meanings,
    )
