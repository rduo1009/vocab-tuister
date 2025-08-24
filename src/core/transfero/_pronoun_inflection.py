"""Contains functions that inflect English pronouns."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ..accido.misc import Case, ComponentsType, Gender, Number
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

    gender = getattr(components, "gender", None)
    if pronoun in GENDERED_PRONOUNS:
        if gender is None:
            raise InvalidComponentsError(
                f"Pronoun '{pronoun}' is gendered but gender was not provided."
            )

        return GENDERED_PRONOUNS[pronoun][
            components.case, components.number, gender
        ]

    try:
        return NON_GENDERED_PRONOUNS[pronoun][
            components.case, components.number
        ]
    except KeyError as e:
        raise NotImplementedError(
            f"Word {pronoun} has not been implemented as a pronoun."
        ) from e


type _NonGenderedInflections = dict[  # pragma: no mutate
    tuple[Case, Number], tuple[str, ...]  # pragma: no mutate
]
NON_GENDERED_PRONOUNS: Final[dict[str, _NonGenderedInflections]] = {
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
    "you": {
        (Case.NOMINATIVE, Number.SINGULAR): ("you",),
        (Case.NOMINATIVE, Number.PLURAL): ("you",),
        (Case.VOCATIVE, Number.SINGULAR): ("you",),
        (Case.VOCATIVE, Number.PLURAL): ("you",),
        (Case.ACCUSATIVE, Number.SINGULAR): ("you",),
        (Case.ACCUSATIVE, Number.PLURAL): ("you",),
        (Case.GENITIVE, Number.SINGULAR): ("of you", "your"),
        (Case.GENITIVE, Number.PLURAL): ("of you", "your"),
        (Case.DATIVE, Number.SINGULAR): ("for you", "to you"),
        (Case.DATIVE, Number.PLURAL): ("for you", "to you"),
        (Case.ABLATIVE, Number.SINGULAR): ("by you", "by means of you", "with you", "you"),
        (Case.ABLATIVE, Number.PLURAL): ("by you", "by means of you", "with you", "you"),
    },
}  # fmt: skip

type _GenderedInflections = dict[  # pragma: no mutate
    tuple[Case, Number, Gender | None], tuple[str, ...]  # pragma: no mutate
]
GENDERED_PRONOUNS: Final[dict[str, _GenderedInflections]] = {
    "oneself": {
        (Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE): ("himself", "itself", "oneself"),
        (Case.ACCUSATIVE, Number.SINGULAR, Gender.FEMININE): ("herself", "itself", "oneself"),
        (Case.ACCUSATIVE, Number.SINGULAR, Gender.NEUTER): ("itself", "oneself"),
        (Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE): ("themselves",),
        (Case.ACCUSATIVE, Number.PLURAL, Gender.FEMININE): ("themselves",),
        (Case.ACCUSATIVE, Number.PLURAL, Gender.NEUTER): ("themselves",),
        (Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE): ("of himself", "of itself", "of oneself"),
        (Case.GENITIVE, Number.SINGULAR, Gender.FEMININE): ("of herself", "of itself", "of oneself"),
        (Case.GENITIVE, Number.SINGULAR, Gender.NEUTER): ("of itself", "of oneself"),
        (Case.GENITIVE, Number.PLURAL, Gender.MASCULINE): ("of themselves",),
        (Case.GENITIVE, Number.PLURAL, Gender.FEMININE): ("of themselves",),
        (Case.GENITIVE, Number.PLURAL, Gender.NEUTER): ("of themselves",),
        (Case.DATIVE, Number.SINGULAR, Gender.MASCULINE): (
            "for himself", "to himself", "for itself", "to itself", "for oneself", "to oneself"
        ),
        (Case.DATIVE, Number.SINGULAR, Gender.FEMININE): (
            "for herself", "to herself", "for itself", "to itself", "for oneself", "to oneself",
        ),
        (Case.DATIVE, Number.SINGULAR, Gender.NEUTER): ("for itself", "to itself", "for oneself", "to oneself"),
        (Case.DATIVE, Number.PLURAL, Gender.MASCULINE): ("for themselves", "to themselves"),
        (Case.DATIVE, Number.PLURAL, Gender.FEMININE): ("for themselves", "to themselves"),
        (Case.DATIVE, Number.PLURAL, Gender.NEUTER): ("for themselves", "to themselves"),
        (Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE): (
            "by himself", "by means of himself", "with himself", "himself", "by itself", "by means of itself", "with itself",
            "itself", "by oneself", "by means of oneself", "with oneself", "oneself",
        ),
        (Case.ABLATIVE, Number.SINGULAR, Gender.FEMININE): (
            "by herself", "by means of herself", "with herself", "herself", "by itself", "by means of itself", "with itself",
            "itself", "by oneself", "by means of oneself", "with oneself", "oneself",
        ),
        (Case.ABLATIVE, Number.SINGULAR, Gender.NEUTER): (
            "by itself", "by means of itself", "with itself", "itself", "by oneself", "by means of oneself", "with oneself",
            "oneself",
        ),
        (Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE): (
            "by themselves", "by means of themselves", "with themselves", "themselves",
        ),
        (Case.ABLATIVE, Number.PLURAL, Gender.FEMININE): (
            "by themselves", "by means of themselves", "with themselves", "themselves",
        ),
        (Case.ABLATIVE, Number.PLURAL, Gender.NEUTER): (
            "by themselves", "by means of themselves", "with themselves", "themselves",
        ),
    }
}  # fmt: skip
