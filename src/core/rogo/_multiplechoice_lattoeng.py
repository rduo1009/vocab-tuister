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
    from ..accido.endings import _Word
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
    vocab_list: Vocab, chosen_word: _Word, number_multiplechoice_options: int
) -> MultipleChoiceLatToEngQuestion:
    prompt = chosen_word._first

    # Pick correct choice
    if isinstance(chosen_word.meaning, MultipleMeanings):
        chosen_word_meanings = tuple(chosen_word.meaning.meanings)
    else:
        chosen_word_meanings = (chosen_word.meaning,)

    # If the word is a verb, inflect the possible correct choices using priority components
    if isinstance(chosen_word, Verb):
        chosen_word_meanings = tuple(
            find_inflection(meaning, max(chosen_word.find(prompt)), main=True)
            for meaning in chosen_word_meanings
        )

    answer = random.choice(chosen_word_meanings)

    # Pick other possible choices
    possible_choices: list[str] = []
    for vocab in vocab_list:
        if isinstance(vocab, Verb):  # inflect other choices if verb as well
            if isinstance(vocab.meaning, str):
                current_meaning = find_inflection(
                    vocab.meaning, max(vocab.find(vocab._first)), main=True
                )
            else:
                current_meaning = MultipleMeanings(
                    tuple(
                        find_inflection(
                            meaning, max(vocab.find(vocab._first)), main=True
                        )
                        for meaning in vocab.meaning.meanings
                    )
                )
        else:
            current_meaning = vocab.meaning

        if isinstance(current_meaning, str):
            if current_meaning in chosen_word_meanings:
                continue
            possible_choices.append(current_meaning)
        else:
            possible_choices.extend(
                meaning
                for meaning in current_meaning.meanings
                if meaning not in chosen_word_meanings
            )

    # Put together choices
    choices = [
        answer,
        *random.sample(possible_choices, number_multiplechoice_options - 1),
    ]
    random.shuffle(choices)

    return MultipleChoiceLatToEngQuestion(
        prompt=prompt, answer=answer, choices=tuple(choices)
    )
