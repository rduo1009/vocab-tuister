from __future__ import annotations

import random
from typing import TYPE_CHECKING

from ..accido.misc import MultipleEndings

if TYPE_CHECKING:
    from ..accido.type_aliases import Ending, Endings


def pick_ending(endings: Endings) -> tuple[str, Ending]:
    return random.choice(list(endings.items()))


def pick_ending_from_multipleendings(ending: Ending) -> str:
    if isinstance(ending, MultipleEndings):
        return random.choice(ending.get_all())

    return ending
