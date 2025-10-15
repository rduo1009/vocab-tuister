# ruff: noqa: SLF001


import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..accido.endings import Verb
from ..transfero.words import find_inflection
from ._base import MultipleChoiceQuestion
from ._utils import pick_meaning_from_multiplemeanings

if TYPE_CHECKING:
    from ..accido.endings import Word
    from ..rogo.type_aliases import Vocab


@dataclass
class MultipleChoiceEngToLatQuestion(MultipleChoiceQuestion):
    """An English to Latin multiple choice question.

    Attributes
    ----------
    prompt : str
        The prompt of the question (in English).
    answer : str
        The answer of the question (in Latin).
    choices : tuple[str, ...]
        The choices of the question (including the answer).
    """


def generate_multiplechoice_engtolat(
    vocab_list: Vocab, chosen_word: Word, number_multiplechoice_options: int
) -> MultipleChoiceEngToLatQuestion:
    # Pick meaning
    meaning = pick_meaning_from_multiplemeanings(chosen_word.meaning)

    # Find answer and other choices
    answer = chosen_word._first
    other_choices = [
        w._first
        for w in random.sample(
            [w for w in vocab_list if w is not chosen_word],
            k=number_multiplechoice_options - 1,
        )
    ]

    # If the word is a verb, inflect the meaning using priority components
    if isinstance(chosen_word, Verb):
        meaning = find_inflection(
            meaning, max(chosen_word.find(answer)), main=True
        )

    # Put together choices
    choices = [answer, *other_choices]
    random.shuffle(choices)

    return MultipleChoiceEngToLatQuestion(
        prompt=meaning, answer=answer, choices=tuple(choices)
    )
