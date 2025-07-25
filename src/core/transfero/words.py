"""Contains functions that inflect English words."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Literal, overload

from ..accido.misc import ComponentsSubtype, ComponentsType
from ._adjective_inflection import (
    find_adjective_inflections,
    find_main_adjective_inflection,
)
from ._adverb_inflection import (
    find_adverb_inflections,
    find_main_adverb_inflection,
)
from ._noun_inflection import find_main_noun_inflection, find_noun_inflections
from ._pronoun_inflection import (
    find_main_pronoun_inflection,
    find_pronoun_inflections,
)
from ._verb_inflection import find_main_verb_inflection, find_verb_inflections
from .adj_to_adv import adj_to_adv

if TYPE_CHECKING:
    from ..accido.misc import EndingComponents

logger = logging.getLogger(__name__)


# fmt: off
@overload
def find_inflection(word: str, components: EndingComponents) -> set[str]: ...
@overload
def find_inflection(word: str, components: EndingComponents, *, main: Literal[True]) -> str: ...
# fmt: on


def find_inflection(
    word: str, components: EndingComponents, *, main: bool = False
) -> set[str] | str:
    """Find the inflections of an English word.

    Parameters
    ----------
    word : str
        The word to inflect.
    components : EndingComponents
        The components of the word.
    main : bool
        Whether to return the main inflection or all of the inflections.
        Default is ``False``.

    Returns
    -------
    set[str] | str
        The main inflection of the word or the inflections of the word.
    """
    logger.debug("find_inflection(%s, %s, main=%s)", word, components, main)

    match components.type:
        case ComponentsType.ADJECTIVE:
            if components.subtype == ComponentsSubtype.ADVERB:
                return (
                    find_main_adverb_inflection(adj_to_adv(word), components)
                    if main
                    else find_adverb_inflections(adj_to_adv(word), components)
                )
            return (
                find_main_adjective_inflection(word, components)
                if main
                else find_adjective_inflections(word, components)
            )

        case ComponentsType.NOUN:
            if components.subtype == ComponentsSubtype.PRONOUN:
                return (
                    find_main_pronoun_inflection(word, components)
                    if main
                    else find_pronoun_inflections(word, components)
                )
            return (
                find_main_noun_inflection(word, components)
                if main
                else find_noun_inflections(word, components)
            )

        case ComponentsType.VERB:
            return (
                find_main_verb_inflection(word, components)
                if main
                else find_verb_inflections(word, components)
            )

        case ComponentsType.PRONOUN:
            return (
                find_main_pronoun_inflection(word, components)
                if main
                else find_pronoun_inflections(word, components)
            )

        case _:
            return word if main else {word}
