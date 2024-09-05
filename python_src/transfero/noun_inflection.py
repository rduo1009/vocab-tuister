#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains functions that inflect English nouns."""

from __future__ import annotations

import lemminflect
from inflect import engine

from .. import accido
from .exceptions import InvalidWordError

# Distinguish from the lemminflect module
pluralinflect = engine()  # sourcery skip: avoid-global-variables
del engine


def _get_possessive(noun: str) -> str:
    return f"{noun}'" if noun.endswith("s") else f"{noun}'s"


def find_noun_inflections(
    noun: str, components: accido.misc.EndingComponents
) -> set[str]:
    """Inflect English nouns using the case and number.

    Parameters
    ----------
    noun : str
        The noun to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    set[str]
        The possible forms of the noun.

    Raises
    ------
    InvalidWordError
        If the word is not a valid English noun.
    ValueError
        If the input (other than the word itself) is invalid.
    """

    if not hasattr(components, "case"):
        raise ValueError("Case must be specified")

    if not hasattr(components, "number"):
        raise ValueError("Number must be specified")

    try:
        lemma: str = lemminflect.getLemma(noun, "NOUN")[0]
    except KeyError as e:
        raise InvalidWordError(f"Word {noun} is not a noun") from e

    base_forms: set[str] = set()

    match components.number:
        case "singular":
            base_forms = {lemminflect.getInflection(lemma, "NN")[0]}

        case "plural":
            base_forms.add(pluralinflect.plural_noun(lemma))
            pluralinflect.classical(all=True)
            base_forms.add(pluralinflect.plural_noun(lemma))
            pluralinflect.classical(all=False)

        case _:
            raise ValueError(f"Invalid number: '{components.number}'")

    match components.case:
        case "nominative" | "vocative" | "accusative":
            return base_forms

        case "genitive":
            possessive_genitive: set[str] = {
                _get_possessive(base_form) for base_form in base_forms
            }

            if components.number == "singular":
                return (
                    possessive_genitive
                    | {f"of the {base_form}" for base_form in base_forms}
                    | {
                        pluralinflect.inflect(f"of a('{base_form}')")
                        for base_form in base_forms
                    }
                )

            return possessive_genitive | {
                f"of the {base_form}" for base_form in base_forms
            }

        case "dative":
            if components.number == "singular":
                return (
                    {f"for the {base_form}" for base_form in base_forms}
                    | {
                        pluralinflect.inflect(f"for a('{base_form}')")
                        for base_form in base_forms
                    }
                    | {f"to the {base_form}" for base_form in base_forms}
                    | {
                        pluralinflect.inflect(f"to a('{base_form}')")
                        for base_form in base_forms
                    }
                )

            return (
                {f"for the {base_form}" for base_form in base_forms}
                | {f"for {base_form}" for base_form in base_forms}
                | {f"to the {base_form}" for base_form in base_forms}
                | {f"to {base_form}" for base_form in base_forms}
            )

        case "ablative":
            if components.number == "singular":
                return (
                    base_forms
                    | {f"with the {base_form}" for base_form in base_forms}
                    | {
                        pluralinflect.inflect(f"with a('{base_form}')")
                        for base_form in base_forms
                    }
                    | {f"by the {base_form}" for base_form in base_forms}
                    | {
                        pluralinflect.inflect(f"by a('{base_form}')")
                        for base_form in base_forms
                    }
                    | {
                        f"by means of the {base_form}"
                        for base_form in base_forms
                    }
                    | {
                        pluralinflect.inflect(f"by means of a('{base_form}')")
                        for base_form in base_forms
                    }
                )

            return (
                base_forms
                | {f"with the {base_form}" for base_form in base_forms}
                | {f"by the {base_form}" for base_form in base_forms}
                | {f"by means of the {base_form}" for base_form in base_forms}
            )

        case _:
            raise ValueError(f"Invalid case: '{components.case}'")