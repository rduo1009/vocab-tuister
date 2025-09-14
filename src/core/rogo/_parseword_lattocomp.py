from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..accido.endings import RegularWord
from ..accido.misc import EndingComponents
from ._base import MultiAnswerQuestion
from ._utils import pick_ending, pick_ending_from_multipleendings

if TYPE_CHECKING:
    from ..accido.endings import Word
    from ..accido.type_aliases import Endings


@dataclass
class ParseWordLatToCompQuestion(MultiAnswerQuestion[EndingComponents]):
    """A question that asks for the grammatical components of a Latin
    word, given the word.

    For example:
    Parse "quaeratis" (hear: quaero, quaerere, quaesivi, quaesitus)
    (answer: "present active indicative 2nd person plural").

    Attributes
    ----------
    prompt : str
        The prompt for the question.
    dictionary_entry : str
        The dictionary entry for the word.
    main_answer : EndingComponents
        The best answer to the question.
    answers : set[EndingComponents]
        The possible answers to the question.
    """  # noqa: D205

    prompt: str
    dictionary_entry: str


def generate_parseword_lattocomp(
    chosen_word: Word, filtered_endings: Endings
) -> ParseWordLatToCompQuestion | None:
    # `RegularWord` is not supported (cannot be declined)
    if isinstance(chosen_word, RegularWord):
        return None

    # Pick ending
    _, chosen_ending = pick_ending(filtered_endings)
    chosen_ending = pick_ending_from_multipleendings(chosen_ending)

    # Find possible `EndingComponents`
    all_ending_components = set(chosen_word.find(chosen_ending))

    # Pick main ending components
    main_ending_components = max(all_ending_components)

    return ParseWordLatToCompQuestion(
        prompt=chosen_ending,
        main_answer=main_ending_components,
        answers=all_ending_components,
        dictionary_entry=str(chosen_word),  # __str__ returns dictionary entry
    )
