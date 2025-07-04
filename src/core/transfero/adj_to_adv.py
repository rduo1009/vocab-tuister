"""Contains a function that converts an adjective to an adverb.

Notes
-----
The code and json file is taken from https://github.com/gutfeeling/word_forms.
The original python package is not used as it has been unmaintained for a few
years now.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final, cast

from .exceptions import InvalidWordError

with (Path(__file__).parent.absolute() / "adj_to_adv.json").open(
    encoding="utf-8"
) as file:
    ADJECTIVE_TO_ADVERB: Final[dict[str, str]] = cast(
        "dict[str, str]", json.load(file)
    )


def adj_to_adv(adjective: str) -> str:
    """Convert an adjective to its corresponding adverb.

    Parameters
    ----------
    adjective : str
        The adjective to convert to an adverb.

    Returns
    -------
    str
        The adverb corresponding to the input adjective.

    Raises
    ------
    InvalidWordError
        If the input is not an adjective.

    Examples
    --------
    >>> adj_to_adv("happy")
    'happily'

    >>> adj_to_adv("sad")
    'sadly'
    """
    if adjective in ADJECTIVE_TO_ADVERB:
        return ADJECTIVE_TO_ADVERB[adjective]

    raise InvalidWordError(f"Word '{adjective}' is not an adjective.")
