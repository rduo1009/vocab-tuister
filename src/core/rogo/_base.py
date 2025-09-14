# pyright: reportAny=false, reportExplicitAny=false

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Any, Protocol


@total_ordering
class QuestionClasses(Enum):
    """The classes of questions that can be asked."""

    TYPEIN_ENGTOLAT = "TypeInEngToLatQuestion"
    TYPEIN_LATTOENG = "TypeInLatToEngQuestion"
    PARSEWORD_LATTOCOMP = "ParseWordLatToCompQuestion"
    PARSEWORD_COMPTOLAT = "ParseWordCompToLatQuestion"
    PRINCIPAL_PARTS = "PrincipalPartsQuestion"
    MULTIPLECHOICE_ENGTOLAT = "MultipleChoiceEngToLatQuestion"
    MULTIPLECHOICE_LATTOENG = "MultipleChoiceLatToEngQuestion"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, QuestionClasses):
            return NotImplemented
        return self.value < other.value


class Question(Protocol):
    """A protocol for questions."""

    prompt: Any

    def check(self, response: Any) -> bool:
        """Check if the response is correct."""
        ...


@dataclass
class MultiAnswerQuestion[T]:
    """Generic class for questions."""

    main_answer: T
    answers: set[T]

    def check(self, response: T) -> bool:
        """Check if the response is correct.

        Parameters
        ----------
        response : T
            The response to the question.

        Returns
        -------
        bool
            ``True`` if the response is correct, ``False`` otherwise.
        """
        return response in self.answers


@dataclass
class MultipleChoiceQuestion:
    """Generic class for multiple choice questions."""

    prompt: str
    answer: str
    choices: tuple[str, ...]

    def check(self, response: str) -> bool:
        """Check if the given answer is correct.

        Parameters
        ----------
        response : str
            The answer to check.

        Returns
        -------
        bool
            ``True`` if the given answer is correct, ``False`` otherwise.
        """
        return response == self.answer
