from typing import TYPE_CHECKING

from ...pb.vocab_tuister.v1 import PrincipalPartsQuestion
from ..accido.endings import Adjective, Noun, Pronoun, RegularWord, Verb

if TYPE_CHECKING:
    from ..accido.endings import Word


def generate_principal_parts(
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
        prompt=principal_parts[0],
        principal_parts=list(chosen_word.principal_parts),
    )
