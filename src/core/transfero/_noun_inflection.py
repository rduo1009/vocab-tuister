"""Contains functions that inflect English nouns."""

from __future__ import annotations

import sys as _sys
from typing import TYPE_CHECKING, Any, cast

import lemminflect

from ..accido.misc import Case, ComponentsType, Number
from .exceptions import InvalidComponentsError, InvalidWordError

if TYPE_CHECKING:
    from collections.abc import Callable

    from ..accido.misc import EndingComponents

# Frozen with PyInstaller
if (
    getattr(_sys, "frozen", False)
    and hasattr(_sys, "_MEIPASS")
    and not TYPE_CHECKING
):  # pragma: no cover

    def _typechecked(  # pyright: ignore[reportUnreachable]
        target: Callable[..., Any] | None = None,
        *args: Any,  # noqa: ARG001
        **kwargs: Any,  # noqa: ARG001
    ) -> Callable[..., Any]:
        if target is None:
            return lambda target: target
        return target

    class _TypeguardModule:
        typechecked = _typechecked

    # Monkeypatch typeguard, as not supported with pyinstaller
    _sys.modules["typeguard"] = cast("object", _TypeguardModule)

from ..._vendor.inflect import engine

# Distinguish from the lemminflect module
pluralinflect = engine()  # sourcery skip: avoid-global-variables
del engine


def _get_possessive(noun: str) -> str:
    return f"{noun}'" if noun.endswith("s") else f"{noun}'s"


def find_noun_inflections(noun: str, components: EndingComponents) -> set[str]:
    """Inflect English nouns using the case and number.

    This function can also be used to inflect pronouns that are treated
    like nouns in accido. For example, 'I', which is considered an
    irregular noun.

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
        If `noun` is not a valid English noun.
    InvalidComponentsError
        If `components` is invalid.
    """
    if components.type != ComponentsType.NOUN:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    try:
        lemmas = lemminflect.getLemma(noun, "NOUN")
    except KeyError as e:
        raise InvalidWordError(f"Word {noun} is not a noun.") from e

    inflections: set[str] = set()
    for lemma in lemmas:
        inflections |= _inflect_lemma(
            lemma, components.case, components.number
        )[1]

    return inflections


def find_main_noun_inflection(noun: str, components: EndingComponents) -> str:
    """Find the main inflection of an English noun.

    Parameters
    ----------
    noun : str
        The noun to inflect.
    components : EndingComponents
        The components of the ending.

    Returns
    -------
    str
        The main inflection of the noun.

    Raises
    ------
    InvalidWordError
        If `noun` is not a valid English noun.
    InvalidComponentsError
        If `components` is invalid.
    """
    if components.type != ComponentsType.NOUN:
        raise InvalidComponentsError(f"Invalid type: '{components.type}'")

    try:
        lemma = lemminflect.getLemma(noun, "NOUN")[0]
    except KeyError as e:
        raise InvalidWordError(f"Word {noun} is not a noun.") from e

    return _inflect_lemma(lemma, components.case, components.number)[0]


def _inflect_lemma(
    lemma: str, case: Case, number: Number
) -> tuple[str, set[str]]:
    base_forms: set[str] = set()

    if number == Number.SINGULAR:
        base_forms = {*lemminflect.getInflection(lemma, "NN")}
        best_form = lemminflect.getInflection(lemma, "NN")[0]
    else:
        normal_plural = pluralinflect.plural_noun(lemma)
        pluralinflect.classical(all=True)
        classical_plural = pluralinflect.plural_noun(lemma)
        pluralinflect.classical(all=False)
        base_forms.update({normal_plural, classical_plural})

        # If the noun has a classical plural form, then that is used,
        # but if it doesn't then classical_plural is just the normal
        # plural
        best_form = classical_plural

    match case:
        case Case.NOMINATIVE | Case.VOCATIVE | Case.ACCUSATIVE:
            return (best_form, base_forms)

        case Case.GENITIVE:
            possessive_genitive = {
                _get_possessive(base_form) for base_form in base_forms
            }
            if number == Number.SINGULAR:
                return (
                    f"of the {best_form}",
                    (
                        possessive_genitive
                        | {f"of the {base_form}" for base_form in base_forms}
                        | {
                            pluralinflect.inflect(f"of a('{base_form}')")
                            for base_form in base_forms
                        }
                    ),
                )
            return (
                f"of the {best_form}",
                possessive_genitive
                | {f"of the {base_form}" for base_form in base_forms},
            )

        case Case.DATIVE:
            if number == Number.SINGULAR:
                return (
                    f"for the {best_form}",
                    (
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
                    ),
                )

            return (
                f"for the {best_form}",
                (
                    {f"for the {base_form}" for base_form in base_forms}
                    | {f"for {base_form}" for base_form in base_forms}
                    | {f"to the {base_form}" for base_form in base_forms}
                    | {f"to {base_form}" for base_form in base_forms}
                ),
            )

        case _:
            if number == Number.SINGULAR:
                return (
                    f"by the {best_form}",
                    (
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
                            pluralinflect.inflect(
                                f"by means of a('{base_form}')"
                            )
                            for base_form in base_forms
                        }
                    ),
                )

            return (
                f"by the {best_form}",
                (
                    base_forms
                    | {f"with the {base_form}" for base_form in base_forms}
                    | {f"by the {base_form}" for base_form in base_forms}
                    | {
                        f"by means of the {base_form}"
                        for base_form in base_forms
                    }
                ),
            )
