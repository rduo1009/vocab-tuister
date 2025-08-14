"""Contains functions that inflect English adverbs."""

from __future__ import annotations

from typing import TYPE_CHECKING

import lemminflect

from ..accido.misc import ComponentsSubtype, ComponentsType, Degree
from .exceptions import InvalidComponentsError, InvalidWordError

if TYPE_CHECKING:
    from ..accido.misc import EndingComponents


def find_adverb_inflections(
    adverb: str, components: EndingComponents
) -> set[str]:
    """Inflect English adverbs using the degree.

    Parameters
    ----------
    adverb : str
        The adverb to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    set[str]
        The possible forms of the adverb.

    Raises
    ------
    InvalidWordError
        If `adverb` is not a valid English adverb.
    InvalidComponentsError
        If `components` is invalid.
    """
    if components.type != ComponentsType.ADJECTIVE:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    if components.subtype != ComponentsSubtype.ADVERB:
        raise InvalidComponentsError(
            f"Invalid subtype: '{components.subtype}'"
        )

    try:
        lemmas = lemminflect.getLemma(adverb, "ADV")
    except KeyError as e:
        raise InvalidWordError(f"Word '{adverb}' is not an adverb.") from e

    inflections: set[str] = set()
    for lemma in lemmas:
        inflections.update(_inflect_lemma(lemma, components.degree))

    return inflections


def find_main_adverb_inflection(
    adverb: str, components: EndingComponents
) -> str:
    """Find the main inflection of an English adverb.

    Parameters
    ----------
    adverb : str
        The adverb to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    str
        The main inflection of the adverb.

    Raises
    ------
    InvalidWordError
        If `adverb` is not a valid English adverb.
    InvalidComponentsError
        If `components` is invalid.
    """
    if components.type is not ComponentsType.ADJECTIVE:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    if components.subtype != ComponentsSubtype.ADVERB:
        raise InvalidComponentsError(
            f"Invalid subtype: '{components.subtype}'"
        )

    try:
        lemma = lemminflect.getLemma(adverb, "ADV")[0]
    except KeyError as e:
        raise InvalidWordError(f"Word '{adverb}' is not an adverb.") from e

    return _inflect_lemma(lemma, components.degree)[0]


def _inflect_lemma(lemma: str, degree: Degree) -> tuple[str, ...]:
    match degree:
        case Degree.POSITIVE:
            return (lemma,)

        case Degree.COMPARATIVE:
            return (f"more {lemma}",)

        case _:
            all_forms = {
                f"most {lemma}",
                f"very {lemma}",
                f"extremely {lemma}",
                f"rather {lemma}",
                f"too {lemma}",
                f"quite {lemma}",
            }
            return (f"most {lemma}", *sorted(all_forms - {f"most {lemma}"}))
