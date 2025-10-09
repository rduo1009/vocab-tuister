"""Contains functions that inflect English pronouns."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ..accido.misc import Case, ComponentsType, Number
from .exceptions import InvalidComponentsError

if TYPE_CHECKING:
    from ..accido.misc import EndingComponents


def find_pronoun_inflections(
    pronoun: str, components: EndingComponents
) -> tuple[str, ...]:
    """Inflect English pronouns using the case and number.

    Pronouns in Latin also have a gender, but this is not used in English.

    Parameters
    ----------
    pronoun : str
        The pronoun to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    tuple[str, ...]
        The possible forms of the pronoun (main form first).

    Raises
    ------
    NotImplementedError
        If `pronoun` is not a pronoun supported by ``transfero`` (or not
        a pronoun at all).
    InvalidComponentsError
        If `components` is invalid.
    """
    if components.type not in {ComponentsType.NOUN, ComponentsType.PRONOUN}:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    if pronoun not in PRONOUNS:
        raise NotImplementedError(
            f"Word {pronoun} has not been implemented as a pronoun."
        )

    try:
        return PRONOUNS[pronoun][components.case, components.number]
    except KeyError as e:
        raise InvalidComponentsError(
            f"No ending found for pronoun '{pronoun}' "
            f"({components.case.shorthand} {components.number.shorthand})"
        ) from e


type _Inflections = dict[  # pragma: no mutate
    tuple[Case, Number], tuple[str, ...]  # pragma: no mutate
]
PRONOUNS: Final[dict[str, _Inflections]] = {
    "this": {
        (Case.NOMINATIVE, Number.SINGULAR): ("this",),
        (Case.NOMINATIVE, Number.PLURAL): ("these",),
        (Case.VOCATIVE, Number.SINGULAR): ("this",),
        (Case.VOCATIVE, Number.PLURAL): ("these",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("this",),
        (Case.ACCUSATIVE, Number.PLURAL): ("these",),
        (Case.GENITIVE, Number.SINGULAR): ("of this",),
        (Case.GENITIVE, Number.PLURAL): ("of these",),
        (Case.DATIVE, Number.SINGULAR): ("for this", "to this"),
        (Case.DATIVE, Number.PLURAL): ("for these", "to these"),
        (Case.ABLATIVE, Number.SINGULAR): ("by this", "by means of this", "with this", "this"),
        (Case.ABLATIVE, Number.PLURAL): ("by these", "by means of these", "with these", "these"),
    },
    "that": {
        (Case.NOMINATIVE, Number.SINGULAR): ("that",),
        (Case.NOMINATIVE, Number.PLURAL): ("those",),
        (Case.VOCATIVE, Number.SINGULAR): ("that",),
        (Case.VOCATIVE, Number.PLURAL): ("those",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("that",),
        (Case.ACCUSATIVE, Number.PLURAL): ("those",),
        (Case.GENITIVE, Number.SINGULAR): ("of that",),
        (Case.GENITIVE, Number.PLURAL): ("of those",),
        (Case.DATIVE, Number.SINGULAR): ("for that", "to that"),
        (Case.DATIVE, Number.PLURAL): ("for those", "to those"),
        (Case.ABLATIVE, Number.SINGULAR): ("by that", "by means of that", "with that", "that"),
        (Case.ABLATIVE, Number.PLURAL): ("by those", "by means of those", "with those", "those"),
    },
    "I": {
        (Case.NOMINATIVE, Number.SINGULAR): ("I",),
        (Case.NOMINATIVE, Number.PLURAL): ("we",),
        (Case.VOCATIVE, Number.SINGULAR): ("I",),
        (Case.VOCATIVE, Number.PLURAL): ("we",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("me",),
        (Case.ACCUSATIVE, Number.PLURAL): ("us",),
        (Case.GENITIVE, Number.SINGULAR): ("of me", "my"),
        (Case.GENITIVE, Number.PLURAL): ("of us", "our"),
        (Case.DATIVE, Number.SINGULAR): ("for me", "to me"),
        (Case.DATIVE, Number.PLURAL): ("for us", "to us"),
        (Case.ABLATIVE, Number.SINGULAR): ("by me", "by means of me", "with me", "me"),
        (Case.ABLATIVE, Number.PLURAL): ("by us", "by means of us", "with us", "us"),
    },
    "we": {
        (Case.NOMINATIVE, Number.PLURAL): ("we",),
        (Case.VOCATIVE, Number.PLURAL): ("we",),
        (Case.ACCUSATIVE, Number.PLURAL): ("us",),
        (Case.GENITIVE, Number.PLURAL): ("of us", "our"),
        (Case.DATIVE, Number.PLURAL): ("for us", "to us"),
        (Case.ABLATIVE, Number.PLURAL): ("by us", "by means of us", "with us", "us"),
    },
    "you": {
        (Case.NOMINATIVE, Number.SINGULAR): ("you",),
        (Case.NOMINATIVE, Number.PLURAL): ("you all",),
        (Case.VOCATIVE, Number.SINGULAR): ("you",),
        (Case.VOCATIVE, Number.PLURAL): ("you all",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("you",),
        (Case.ACCUSATIVE, Number.PLURAL): ("you all",),
        (Case.GENITIVE, Number.SINGULAR): ("of you", "your"),
        (Case.GENITIVE, Number.PLURAL): ("of you all", "your"),
        (Case.DATIVE, Number.SINGULAR): ("for you", "to you"),
        (Case.DATIVE, Number.PLURAL): ("for you all", "to you all"),
        (Case.ABLATIVE, Number.SINGULAR): ("by you", "by means of you", "with you", "you"),
        (Case.ABLATIVE, Number.PLURAL): ("by you all", "by means of you all", "with you all", "you all"),
    },
    "you all": {
        (Case.NOMINATIVE, Number.PLURAL): ("you all",),
        (Case.VOCATIVE, Number.PLURAL): ("you all",),
        (Case.ACCUSATIVE, Number.PLURAL): ("you all",),
        (Case.GENITIVE, Number.PLURAL): ("of you all", "your"),
        (Case.DATIVE, Number.PLURAL): ("for you all", "to you"),
        (Case.ABLATIVE, Number.PLURAL): ("by you all", "by means of you all", "with you all", "you all"),
    },
    "oneself": { # XXX: should this be changed? only just 'oneself' here, then make the others secondary meanings?
        (Case.ACCUSATIVE, Number.SINGULAR): ("oneself", "himself", "herself", "itself"),
        (Case.ACCUSATIVE, Number.PLURAL): ("themselves",),
        (Case.GENITIVE, Number.SINGULAR): ("of oneself", "one's", "of himself", "his", "of herself", "her", "of itself", "its"),
        (Case.GENITIVE, Number.PLURAL): ("of themselves", "their"),
        (Case.DATIVE, Number.SINGULAR): (
            "for oneself", "for himself", "for herself", "for itself", "to oneself", "to himself", "to herself", "to itself",
        ),
        (Case.DATIVE, Number.PLURAL): ("for themselves", "to themselves"),
        (Case.ABLATIVE, Number.SINGULAR): (
            "by oneself", "by himself", "by herself", "by itself", "by means of oneself", "by means of himself",
            "by means of herself", "by means of itself", "with oneself", "with himself", "with herself", "with itself", "oneself",
            "himself", "herself", "itself",
        ),
        (Case.ABLATIVE, Number.PLURAL): (
            "by themselves", "by means of themselves", "with themselves", "themselves",
        ),
    },
    "anyone": {
        (Case.NOMINATIVE, Number.SINGULAR): ("anyone",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("anyone",),
        (Case.GENITIVE, Number.SINGULAR): ("of anyone", "anyone's"),
        (Case.DATIVE, Number.SINGULAR): ("for anyone", "to anyone"),
        (Case.ABLATIVE, Number.SINGULAR): ("by anyone", "by means of anyone", "with anyone", "anyone"),
    },
    "anything": {
        (Case.NOMINATIVE, Number.SINGULAR): ("anything",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("anything",),
        (Case.GENITIVE, Number.SINGULAR): ("of anything", "anything's"),
        (Case.DATIVE, Number.SINGULAR): ("for anything", "to anything"),
        (Case.ABLATIVE, Number.SINGULAR): ("by anything", "by means of anything", "with anything", "anything"),
    },
    "certain": {
        (Case.NOMINATIVE, Number.SINGULAR): ("certain", "a certain"),
        (Case.NOMINATIVE, Number.PLURAL): ("certain",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("certain", "a certain"),
        (Case.ACCUSATIVE, Number.PLURAL): ("certain",),
        (Case.GENITIVE, Number.SINGULAR): ("of certain", "of a certain"),
        (Case.GENITIVE, Number.PLURAL): ("of certain",),
        (Case.DATIVE, Number.SINGULAR): ("for certain", "to certain", "for a certain", "to a certain"),
        (Case.DATIVE, Number.PLURAL): ("for certain", "to certain"),
        (Case.ABLATIVE, Number.SINGULAR): (
            "by certain", "by means of certain", "with certain", "certain", "by a certain", "by means of a certain",
            "with a certain", "a certain",
        ),
        (Case.ABLATIVE, Number.PLURAL): ("by certain", "by means of certain", "with certain", "certain"),
    },
    "one": {
        (Case.NOMINATIVE, Number.SINGULAR): ("one",),
        (Case.NOMINATIVE, Number.PLURAL): ("one",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("one",),
        (Case.ACCUSATIVE, Number.PLURAL): ("one",),
        (Case.GENITIVE, Number.SINGULAR): ("of one",),
        (Case.GENITIVE, Number.PLURAL): ("of one",),
        (Case.DATIVE, Number.SINGULAR): ("for one", "to one"),
        (Case.DATIVE, Number.PLURAL): ("for one", "to one"),
        (Case.ABLATIVE, Number.SINGULAR): ("by one", "by means of one", "with one", "one"),
        (Case.ABLATIVE, Number.PLURAL): ("by one", "by means of one", "with one", "one"),
    },
}  # fmt: skip
