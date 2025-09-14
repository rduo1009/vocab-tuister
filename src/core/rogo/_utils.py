from __future__ import annotations

import itertools
import random
from typing import TYPE_CHECKING

from ..accido.misc import MultipleEndings, MultipleMeanings

if TYPE_CHECKING:
    from ..accido.type_aliases import Ending, Endings, Meaning


def pick_ending(endings: Endings) -> tuple[str, Ending]:
    i = random.randrange(len(endings))
    key = next(itertools.islice(endings, i, None))
    return key, endings[key]


def pick_ending_from_multipleendings(ending: Ending) -> str:
    return (
        random.choice(ending.get_all())
        if isinstance(ending, MultipleEndings)
        else ending
    )


def normalise_to_multipleendings(
    ending: str | MultipleEndings,
) -> MultipleEndings:
    return (
        MultipleEndings(regular=ending) if isinstance(ending, str) else ending
    )


def pick_meaning_from_multiplemeanings(meaning: Meaning) -> str:
    return (
        random.choice(meaning.meanings)
        if isinstance(meaning, MultipleMeanings)
        else meaning
    )


def normalise_to_multiplemeanings(meaning: Meaning) -> MultipleMeanings:
    return (
        MultipleMeanings((meaning,)) if isinstance(meaning, str) else meaning
    )
