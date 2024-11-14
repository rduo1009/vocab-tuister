"""Contains a custom encoder for converting some vocab-tester classes to JSON."""

from __future__ import annotations

from json import JSONEncoder
from typing import Any, Final, cast

from ..core.accido.misc import EndingComponents, _EndingComponentEnum
from ..core.rogo.question_classes import (
    MultipleChoiceEngToLatQuestion,
    MultipleChoiceLatToEngQuestion,
    ParseWordCompToLatQuestion,
    ParseWordLatToCompQuestion,
    PrincipalPartsQuestion,
    TypeInEngToLatQuestion,
    TypeInLatToEngQuestion,
)

ENDING_COMPONENTS_ATTRS: Final[set[str]] = {
    "case",
    "number",
    "gender",
    "tense",
    "voice",
    "mood",
    "person",
    "degree",
}


class QuestionClassEncoder(JSONEncoder):  # noqa: D101
    def default(self, obj: object) -> dict[str, Any]:  # noqa: D102
        if isinstance(obj, EndingComponents):
            ending_components_json = {}
            for key, value in obj.__dict__.items():
                if key in ENDING_COMPONENTS_ATTRS:
                    ending_components_json[key] = (
                        value.regular
                        if isinstance(value, _EndingComponentEnum)
                        else value
                    )
            return ending_components_json

        if isinstance(obj, MultipleChoiceEngToLatQuestion):
            return {
                "question_type": "MultipleChoiceEngToLatQuestion",
                "prompt": obj.prompt,
                "answer": obj.answer,
                "choices": list(obj.choices),
            }

        if isinstance(obj, MultipleChoiceLatToEngQuestion):
            return {
                "question_type": "MultipleChoiceLatToEngQuestion",
                "prompt": obj.prompt,
                "answer": obj.answer,
                "choices": list(obj.choices),
            }

        if isinstance(obj, ParseWordCompToLatQuestion):
            return {
                "question_type": "ParseWordCompToLatQuestion",
                "prompt": obj.prompt,
                "components": obj.components.string,
                "main_answer": obj.main_answer,
                "answers": list(obj.answers),
            }

        if isinstance(obj, ParseWordLatToCompQuestion):
            return {
                "question_type": "ParseWordLatToCompQuestion",
                "prompt": obj.prompt,
                "dictionary_entry": obj.dictionary_entry,
                "main_answer": self.default(obj.main_answer),
                "answers": [self.default(answer) for answer in obj.answers],
            }

        if isinstance(obj, PrincipalPartsQuestion):
            return {
                "question_type": "PrincipalPartsQuestion",
                "prompt": obj.prompt,
                "principal_parts": list(obj.principal_parts),
            }

        if isinstance(obj, TypeInEngToLatQuestion):
            return {
                "question_type": "TypeInEngToLatQuestion",
                "prompt": obj.prompt,
                "main_answer": obj.main_answer,
                "answers": list(obj.answers),
            }

        if isinstance(obj, TypeInLatToEngQuestion):
            return {
                "question_type": "TypeInLatToEngQuestion",
                "prompt": obj.prompt,
                "main_answer": obj.main_answer,
                "answers": list(obj.answers),
            }

        # this actually throws error
        return cast(dict[str, Any], super().default(obj))


QuestionClassEncoder.__doc__ = JSONEncoder.__doc__
QuestionClassEncoder.default.__doc__ = JSONEncoder.default.__doc__
