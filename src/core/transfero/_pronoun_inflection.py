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
    "oneself": {
        (Case.ACCUSATIVE, Number.SINGULAR): ("oneself",),
        (Case.ACCUSATIVE, Number.PLURAL): ("themselves",),
        (Case.GENITIVE, Number.SINGULAR): ("of oneself", "one's"),
        (Case.GENITIVE, Number.PLURAL): ("of themselves", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for oneself", "to oneself"),
        (Case.DATIVE, Number.PLURAL): ("for themselves", "to themselves"),
        (Case.ABLATIVE, Number.SINGULAR): ("by oneself", "by means of oneself", "with oneself", "oneself"),
        (Case.ABLATIVE, Number.PLURAL): ("by themselves", "by means of themselves", "with themselves", "themselves"),
    },
    "himself": {
        (Case.ACCUSATIVE, Number.SINGULAR): ("himself",),
        (Case.ACCUSATIVE, Number.PLURAL): ("themselves",),
        (Case.GENITIVE, Number.SINGULAR): ("of himself", "his"),
        (Case.GENITIVE, Number.PLURAL): ("of themselves", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for himself", "to himself"),
        (Case.DATIVE, Number.PLURAL): ("for themselves", "to themselves"),
        (Case.ABLATIVE, Number.SINGULAR): ("by himself", "by means of himself", "with himself", "himself"),
        (Case.ABLATIVE, Number.PLURAL): ("by themselves", "by means of themselves", "with themselves", "themselves"),
    },
    "herself": {
        (Case.ACCUSATIVE, Number.SINGULAR): ("herself",),
        (Case.ACCUSATIVE, Number.PLURAL): ("themselves",),
        (Case.GENITIVE, Number.SINGULAR): ("of herself", "her"),
        (Case.GENITIVE, Number.PLURAL): ("of themselves", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for herself", "to herself"),
        (Case.DATIVE, Number.PLURAL): ("for themselves", "to themselves"),
        (Case.ABLATIVE, Number.SINGULAR): ("by herself", "by means of herself", "with herself", "herself"),
        (Case.ABLATIVE, Number.PLURAL): ("by themselves", "by means of themselves", "with themselves", "themselves"),
    },
    "itself": {
        (Case.ACCUSATIVE, Number.SINGULAR): ("itself",),
        (Case.ACCUSATIVE, Number.PLURAL): ("themselves",),
        (Case.GENITIVE, Number.SINGULAR): ("of itself", "its"),
        (Case.GENITIVE, Number.PLURAL): ("of themselves", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for itself", "to itself"),
        (Case.DATIVE, Number.PLURAL): ("for themselves", "to themselves"),
        (Case.ABLATIVE, Number.SINGULAR): ("by itself", "by means of itself", "with itself", "itself"),
        (Case.ABLATIVE, Number.PLURAL): ("by themselves", "by means of themselves", "with themselves", "themselves"),
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
    "someone": {
        (Case.NOMINATIVE, Number.SINGULAR): ("someone",),
        (Case.NOMINATIVE, Number.PLURAL): ("some people",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("someone",),
        (Case.ACCUSATIVE, Number.PLURAL): ("some people",),
        (Case.GENITIVE, Number.SINGULAR): ("of someone",),
        (Case.GENITIVE, Number.PLURAL): ("of some people",),
        (Case.DATIVE, Number.SINGULAR): ("for someone", "to someone"),
        (Case.DATIVE, Number.PLURAL): ("for some people", "to some people"),
        (Case.ABLATIVE, Number.SINGULAR): ("by someone", "by means of someone", "with someone", "someone"),
        (Case.ABLATIVE, Number.PLURAL): ("by some people", "by means of some people", "with some people", "some people"),
    },
    "something": {
        (Case.NOMINATIVE, Number.SINGULAR): ("something",),
        (Case.NOMINATIVE, Number.PLURAL): ("some things",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("something",),
        (Case.ACCUSATIVE, Number.PLURAL): ("some things",),
        (Case.GENITIVE, Number.SINGULAR): ("of something",),
        (Case.GENITIVE, Number.PLURAL): ("of some things",),
        (Case.DATIVE, Number.SINGULAR): ("for something", "to something"),
        (Case.DATIVE, Number.PLURAL): ("for some things", "to some things"),
        (Case.ABLATIVE, Number.SINGULAR): ("by something", "by means of something", "with something", "something"),
        (Case.ABLATIVE, Number.PLURAL): ("by some things", "by means of some things", "with some things", "some things"),
    },
    "he": {
        (Case.NOMINATIVE, Number.SINGULAR): ("he",),
        (Case.NOMINATIVE, Number.PLURAL): ("they",),
        (Case.VOCATIVE, Number.SINGULAR): ("he",),
        (Case.VOCATIVE, Number.PLURAL): ("they",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("him",),
        (Case.ACCUSATIVE, Number.PLURAL): ("them",),
        (Case.GENITIVE, Number.SINGULAR): ("of him", "his"),
        (Case.GENITIVE, Number.PLURAL): ("of them", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for him", "to him"),
        (Case.DATIVE, Number.PLURAL): ("for them", "to them"),
        (Case.ABLATIVE, Number.SINGULAR): ("by him", "by means of him", "with him", "him"),
        (Case.ABLATIVE, Number.PLURAL): ("by them", "by means of them", "with them", "them"),
    },
    "she": {
        (Case.NOMINATIVE, Number.SINGULAR): ("she",),
        (Case.NOMINATIVE, Number.PLURAL): ("they",),
        (Case.VOCATIVE, Number.SINGULAR): ("she",),
        (Case.VOCATIVE, Number.PLURAL): ("they",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("her",),
        (Case.ACCUSATIVE, Number.PLURAL): ("them",),
        (Case.GENITIVE, Number.SINGULAR): ("of her", "her"),
        (Case.GENITIVE, Number.PLURAL): ("of them", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for her", "to her"),
        (Case.DATIVE, Number.PLURAL): ("for them", "to them"),
        (Case.ABLATIVE, Number.SINGULAR): ("by her", "by means of her", "with her", "her"),
        (Case.ABLATIVE, Number.PLURAL): ("by them", "by means of them", "with them", "them"),
    },
    "it": {
        (Case.NOMINATIVE, Number.SINGULAR): ("it",),
        (Case.NOMINATIVE, Number.PLURAL): ("they",),
        (Case.VOCATIVE, Number.SINGULAR): ("it",),
        (Case.VOCATIVE, Number.PLURAL): ("they",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("it",),
        (Case.ACCUSATIVE, Number.PLURAL): ("them",),
        (Case.GENITIVE, Number.SINGULAR): ("of it", "its"),
        (Case.GENITIVE, Number.PLURAL): ("of them", "their"),
        (Case.DATIVE, Number.SINGULAR): ("for it", "to it"),
        (Case.DATIVE, Number.PLURAL): ("for them", "to them"),
        (Case.ABLATIVE, Number.SINGULAR): ("by it", "by means of it", "with it", "it"),
        (Case.ABLATIVE, Number.PLURAL): ("by them", "by means of them", "with them", "them"),
    },
}  # fmt: skip
