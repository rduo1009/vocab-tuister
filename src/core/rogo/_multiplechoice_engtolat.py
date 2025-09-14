# ruff: noqa: SLF001

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..accido.endings import Verb
from ..accido.misc import MultipleMeanings
from ..transfero.words import find_inflection
from ._base import MultipleChoiceQuestion

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
    # Remove `chosen_word` from copy of `vocab_list`
    vocab_list = vocab_list.copy()  # sourcery skip: name-type-suffix
    vocab_list.remove(chosen_word)

    # Get a single meaning if it is `MultipleMeanings`
    meaning = chosen_word.meaning
    if isinstance(meaning, MultipleMeanings):
        meaning = random.choice(meaning.meanings)

    # Find answer and other choices
    answer = chosen_word._first
    other_choices = (
        vocab._first
        for vocab in random.sample(
            vocab_list,
            # minus one as the chosen word is already in the question
            number_multiplechoice_options - 1,
        )
    )

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
