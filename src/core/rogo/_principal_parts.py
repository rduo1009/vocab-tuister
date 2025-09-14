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
    # `RegularWord` is not supported (not principal parts)
    if isinstance(chosen_word, RegularWord):
        return None

    # Get principal parts
    principal_parts: tuple[str, ...]
    match chosen_word:
        case Verb():
            if chosen_word.conjugation == 0:  # irregular verb
                return None

            assert chosen_word.infinitive is not None
            assert chosen_word.perfect is not None

            if chosen_word.ppp:
                assert chosen_word.ppp is not None

                principal_parts = (
                    chosen_word.present,
                    chosen_word.infinitive,
                    chosen_word.perfect,
                    chosen_word.ppp,
                )
            else:
                principal_parts = (
                    chosen_word.present,
                    chosen_word.infinitive,
                    chosen_word.perfect,
                )

        case Noun():
            if chosen_word.declension == 0:  # irregular noun
                return None

            assert chosen_word.genitive is not None

            principal_parts = (chosen_word.nominative, chosen_word.genitive)

        case Adjective():
            match chosen_word.declension:
                case "212":
                    principal_parts = (
                        chosen_word.mascnom,
                        chosen_word.femnom,
                        chosen_word.neutnom,
                    )
                case "3":
                    match chosen_word.termination:
                        case 1:
                            principal_parts = (
                                chosen_word.mascnom,
                                chosen_word.mascgen,
                            )
                        case 2:
                            principal_parts = (
                                chosen_word.mascnom,
                                chosen_word.neutnom,
                            )
                        case 3:
                            principal_parts = (
                                chosen_word.mascnom,
                                chosen_word.femnom,
                                chosen_word.neutnom,
                            )
                        case _:
                            raise ValueError(
                                f"Termination '{chosen_word.termination}' not recognised."
                            )

        case Pronoun():
            principal_parts = (
                chosen_word.mascnom,
                chosen_word.femnom,
                chosen_word.neutnom,
            )

        case _:
            raise TypeError(f"Invalid type: {type(chosen_word)}")

    return PrincipalPartsQuestion(
        prompt=principal_parts[0], principal_parts=principal_parts
    )
