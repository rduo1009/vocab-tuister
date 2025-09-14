from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from ..accido.endings import RegularWord
from ..accido.misc import MultipleEndings
from ._base import MultiAnswerQuestion
from ._utils import pick_ending

if TYPE_CHECKING:
    from ..accido.endings import Word
    from ..accido.misc import EndingComponents
    from ..accido.type_aliases import Endings


@dataclass
class ParseWordCompToLatQuestion(MultiAnswerQuestion[str]):
    """A question that asks for a Latin word given the grammatical
    components of the word.

    For example:
    present active indicative 2nd person plural of "quaero"
    (answer: "quaeratis").

    Attributes
    ----------
    prompt : str
        The prompt for the question (the dictionary entry).
    components : EndingComponents
        The grammatical components of the word.
    main_answer : str
        The best answer to the question.
    answers : set[str]
        The possible answers to the question.
    """  # noqa: D205

    prompt: str
    components: EndingComponents


# FIXME: Rename function
def generate_inflect(
    chosen_word: Word, filtered_endings: Endings
) -> ParseWordCompToLatQuestion | None:
    # `RegularWord` is not supported (cannot be declined)
    if isinstance(chosen_word, RegularWord):
        return None

    # Pick ending, getting the ending dict key to the ending as well
    ending_components_key, chosen_ending = pick_ending(filtered_endings)

    # Find `EndingComponents` from dict key
    ending_components = chosen_word.create_components_instance(
        ending_components_key
    )

    # Convert `chosen_ending` to string if necessary
    if isinstance(chosen_ending, MultipleEndings):
        # If the `MutipleEndings` has a `regular` attribute then use that
        if hasattr(chosen_ending, "regular"):
            main_answer = cast("str", chosen_ending.regular)
        else:
            main_answer = random.choice(chosen_ending.get_all())
        answers = set(chosen_ending.get_all())
    else:
        main_answer = chosen_ending
        answers = {chosen_ending}

    return ParseWordCompToLatQuestion(
        prompt=str(chosen_word),  # __str__ returns dictionary entry
        components=ending_components,
        main_answer=main_answer,
        answers=answers,
    )
