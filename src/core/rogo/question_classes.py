"""Contains representations of questions about Latin vocabulary."""

# pyright: reportAny=false, reportExplicitAny=false

from __future__ import annotations

from ._base import (
    MultiAnswerQuestion as MultiAnswerQuestion,
    MultipleChoiceQuestion as MultipleChoiceQuestion,
    Question as Question,
    QuestionClasses as QuestionClasses,
)
from ._multiplechoice_engtolat import (
    MultipleChoiceEngToLatQuestion as MultipleChoiceEngToLatQuestion,
)
from ._multiplechoice_lattoeng import (
    MultipleChoiceLatToEngQuestion as MultipleChoiceLatToEngQuestion,
)
from ._parseword_comptolat import (
    ParseWordCompToLatQuestion as ParseWordCompToLatQuestion,
)
from ._parseword_lattocomp import (
    ParseWordLatToCompQuestion as ParseWordLatToCompQuestion,
)
from ._principal_parts import PrincipalPartsQuestion as PrincipalPartsQuestion
from ._typein_engtolat import TypeInEngToLatQuestion as TypeInEngToLatQuestion
from ._typein_lattoeng import TypeInLatToEngQuestion as TypeInLatToEngQuestion
