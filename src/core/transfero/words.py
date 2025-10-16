"""Contains functions that inflect English words."""

import logging
from typing import TYPE_CHECKING, Literal, overload

from ..accido.misc import ComponentsSubtype, ComponentsType
from ._adj_to_adv import adj_to_adv
from ._adjective_inflection import find_adjective_inflections
from ._adverb_inflection import find_adverb_inflections
from ._noun_inflection import find_noun_inflections
from ._pronoun_inflection import find_pronoun_inflections
from ._verb_inflection import find_verb_inflections

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

    def pick(result: tuple[str, ...]) -> str | set[str]:
        if main:
            return result[0]
        return set(result)

    logger.debug("find_inflection(%s, %s, main=%s)", word, components, main)

    match components.type:
        case ComponentsType.ADJECTIVE:
            if components.subtype == ComponentsSubtype.ADVERB:
                return pick(
                    find_adverb_inflections(adj_to_adv(word), components)
                )
            return pick(find_adjective_inflections(word, components))

        case ComponentsType.NOUN:
            if components.subtype == ComponentsSubtype.PRONOUN:
                return pick(find_pronoun_inflections(word, components))
            return pick(find_noun_inflections(word, components))

        case ComponentsType.VERB:
            return pick(find_verb_inflections(word, components))

        case ComponentsType.PRONOUN:
            return pick(find_pronoun_inflections(word, components))

        case _:
            return word if main else {word}
