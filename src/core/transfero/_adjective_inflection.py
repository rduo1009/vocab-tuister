"""Contains functions that inflect English adjectives."""

from __future__ import annotations

from typing import TYPE_CHECKING

import lemminflect

from ..accido.misc import ComponentsType, Degree
from ._edge_cases import NOT_COMPARABLE_ADJECTIVES
from .exceptions import InvalidComponentsError, InvalidWordError

if TYPE_CHECKING:
    from ..accido.misc import EndingComponents


def find_adjective_inflections(
    adjective: str, components: EndingComponents
) -> tuple[str, ...]:
    """Inflect English adjectives using the degree.

    Parameters
    ----------
    adjective : str
        The adjective to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    tuple[str, ...]
        The possible forms of the adjective (main form first).

    Raises
    ------
    InvalidWordError
        If `adjective` is not a valid English adjective.
    InvalidComponentsError
        If `components` is invalid.
    """
    if components.type != ComponentsType.ADJECTIVE:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    if components.subtype is not None:
        raise InvalidComponentsError(
            f"Invalid subtype: '{components.subtype}'"
        )

    try:
        lemmas = lemminflect.getLemma(adjective, "ADJ")
    except KeyError as e:
        raise InvalidWordError(
            f"Word '{adjective}' is not an adjective."
        ) from e

    inflections_list: list[str] = []
    for lemma in lemmas:
        inflections_list.extend(_inflect_lemma(lemma, components.degree))

    # dict.fromkeys() removes duplicates but keeps order
    return tuple(dict.fromkeys(inflections_list))


def _inflect_lemma(lemma: str, degree: Degree) -> tuple[str, ...]:
    not_comparable = lemma in NOT_COMPARABLE_ADJECTIVES

    match degree:
        case Degree.POSITIVE:
            return (lemma,)

        case Degree.COMPARATIVE:
            comparatives = lemminflect.getInflection(lemma, "JJR")
            main = f"more {lemma}" if not_comparable else comparatives[0]
            all_forms = {*comparatives, f"more {lemma}"}
            # The main form must be first.
            return (main, *sorted(all_forms - {main}))

        case _:
            superlatives = lemminflect.getInflection(lemma, "JJS")
            main = f"most {lemma}" if not_comparable else superlatives[0]
            all_forms = {
                *superlatives,
                f"most {lemma}",
                f"very {lemma}",
                f"extremely {lemma}",
                f"rather {lemma}",
                f"too {lemma}",
                f"quite {lemma}",
            }
            # The main form must be first.
            return (main, *sorted(all_forms - {main}))
