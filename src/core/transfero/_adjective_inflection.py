"""Contains functions that inflect English adjectives."""

from __future__ import annotations

from typing import TYPE_CHECKING

import lemminflect

from ..accido.misc import ComponentsType, Degree
from .edge_cases import NOT_COMPARABLE_ADJECTIVES
from .exceptions import InvalidComponentsError, InvalidWordError

if TYPE_CHECKING:
    from ..accido.misc import EndingComponents


def find_adjective_inflections(
    adjective: str, components: EndingComponents
) -> set[str]:
    """Inflect English adjectives using the degree.

    Parameters
    ----------
    adjective : str
        The adjective to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    set[str]
        The possible forms of the adjective.

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

    inflections: set[str] = set()
    for lemma in lemmas:
        inflections |= _inflect_lemma(lemma, components.degree)[1]

    return inflections


def find_main_adjective_inflection(
    adjective: str, components: EndingComponents
) -> str:
    """Find the main inflection of an English adjective.

    Parameters
    ----------
    adjective : str
        The adjective to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    str
        The main inflection of the adjective.

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
        lemma = lemminflect.getLemma(adjective, "ADJ")[0]
    except KeyError as e:
        raise InvalidWordError(
            f"Word '{adjective}' is not an adjective."
        ) from e

    return _inflect_lemma(lemma, components.degree)[0]


def _inflect_lemma(lemma: str, degree: Degree) -> tuple[str, set[str]]:
    not_comparable = lemma in NOT_COMPARABLE_ADJECTIVES

    match degree:
        case Degree.POSITIVE:
            return (lemma, {lemma})

        case Degree.COMPARATIVE:
            comparatives = lemminflect.getInflection(lemma, "RBR")
            return (
                f"more {lemma}" if not_comparable else comparatives[0],
                {*comparatives, f"more {lemma}"},
            )

        case _:
            superlatives = lemminflect.getInflection(lemma, "RBS")
            return (
                f"most {lemma}" if not_comparable else superlatives[0],
                {
                    *superlatives,
                    f"most {lemma}",
                    f"very {lemma}",
                    f"extremely {lemma}",
                    f"rather {lemma}",
                    f"too {lemma}",
                    f"quite {lemma}",
                },
            )
