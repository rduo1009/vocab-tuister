from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb

if TYPE_CHECKING:
    from ..accido.endings import Word


@dataclass
class PrincipalPartsQuestion:
    """A question that asks for the principal parts of a Latin verb.

    Attributes
    ----------
    prompt : str
        The prompt of the question.
    principal_parts : tuple[str, ...]
        The answer of the question (the principal parts).
    """

    prompt: str
    principal_parts: tuple[str, ...]

    def check(self, response: tuple[str, ...]) -> bool:
        """Check if the given principal parts are correct.

        Parameters
        ----------
        response : tuple[str, ...]
            The principal parts to check.

        Returns
        -------
        bool
            ``True`` if the given principal parts are correct,
            ``False`` otherwise.
        """
        return response == self.principal_parts


# FIXME: Rename function
def generate_principal_parts_question(
    chosen_word: Word,
) -> PrincipalPartsQuestion | None:
    # `RegularWord` is not supported (no principal parts)
    if isinstance(chosen_word, RegularWord):
        return None

    # Irregular words are not supported
    if (isinstance(chosen_word, Verb) and chosen_word.conjugation == 0) or (
        isinstance(chosen_word, Noun) and chosen_word.declension == 0
    ):
        return None

    # Get principal parts
    assert isinstance(chosen_word, (Noun, Verb, Adjective, Pronoun))
    principal_parts = chosen_word.principal_parts

    return PrincipalPartsQuestion(
        prompt=principal_parts[0], principal_parts=chosen_word.principal_parts
    )
