# ruff: noqa: SLF001


import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..accido.endings import Verb
from ..accido.misc import MultipleMeanings
from ..transfero.words import find_inflection
from ._base import MultipleChoiceQuestion
from ._utils import (
    normalise_to_multiplemeanings,
    pick_meaning_from_multiplemeanings,
)

if TYPE_CHECKING:
    from ..accido.endings import Word
    from .type_aliases import Vocab


@dataclass
class MultipleChoiceLatToEngQuestion(MultipleChoiceQuestion):
    """A Latin to English multiple choice question.

    Attributes
    ----------
    prompt : str
        The prompt of the question (in Latin).
    answer : str
        The answer of the question (in English).
    choices : tuple[str, ...]
        The choices of the question (including the answer).
    """


def generate_multiplechoice_lattoeng(
    vocab_list: Vocab, chosen_word: Word, number_multiplechoice_options: int
) -> MultipleChoiceLatToEngQuestion:
    prompt = chosen_word._first

    # Pick meaning
    answer = pick_meaning_from_multiplemeanings(chosen_word.meaning)

    # If the word is a verb, inflect the choice using priority components
    if isinstance(chosen_word, Verb):
        answer = find_inflection(
            answer, max(chosen_word.find(prompt)), main=True
        )

    # Pick other possible choices
    candidate_words = random.sample(
        [w for w in vocab_list if w is not chosen_word],
        k=number_multiplechoice_options - 1,
    )

    other_choices: list[str] = []
    for vocab in candidate_words:
        if len(other_choices) >= number_multiplechoice_options - 1:
            break

        current_meaning = normalise_to_multiplemeanings(vocab.meaning)

        if isinstance(vocab, Verb):  # inflect other choices if verb as well
            current_meaning = MultipleMeanings(
                tuple(
                    find_inflection(
                        meaning, max(vocab.find(vocab._first)), main=True
                    )
                    for meaning in current_meaning.meanings
                )
            )

        meaning = random.choice(current_meaning.meanings)
        if meaning != answer and meaning not in other_choices:
            other_choices.append(meaning)

    # Put together choices
    choices = [answer, *other_choices]
    random.shuffle(choices)

    return MultipleChoiceLatToEngQuestion(
        prompt=prompt, answer=answer, choices=tuple(choices)
    )
