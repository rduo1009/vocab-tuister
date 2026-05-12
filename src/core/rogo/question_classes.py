"""Contains representations of questions about Latin vocabulary."""

# pyright: reportAny=false, reportExplicitAny=false

from __future__ import annotations

from enum import Enum
from functools import total_ordering

from ...pb.vocab_tuister.v1 import (
    MultipleChoiceEngToLatQuestion,
    MultipleChoiceLatToEngQuestion,
    ParseWordCompToLatQuestion,
    ParseWordLatToCompQuestion,
    PrincipalPartsQuestion,
    TypeInEngToLatQuestion,
    TypeInLatToEngQuestion,
)


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


type Question = (
    MultipleChoiceEngToLatQuestion
    | MultipleChoiceLatToEngQuestion
    | ParseWordCompToLatQuestion
    | ParseWordLatToCompQuestion
    | PrincipalPartsQuestion
    | TypeInEngToLatQuestion
    | TypeInLatToEngQuestion
)
