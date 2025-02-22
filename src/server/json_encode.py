"""Contains a custom encoder for converting some vocab-tester classes to JSON."""

from __future__ import annotations

from json import JSONEncoder
from typing import Any, Final, cast

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
        match obj:
            # NOTE: The tester tui currently uses the component string representation
            # case EndingComponents():
            #     ending_components_json = {}
            #     for key, value in obj.__dict__.items():
            #         if key in ENDING_COMPONENTS_ATTRS:
            #             if isinstance(value, _EndingComponentEnum):
            #                 ending_components_json[key] = value.regular
            #             elif isinstance(value, int):
            #                 ending_components_json[key] = PERSON_SHORTHAND[value]
            #             else:
            #                 ending_components_json[key] = value
            #     return ending_components_json

            case MultipleChoiceEngToLatQuestion():
                return {
                    "question_type": "MultipleChoiceEngToLatQuestion",
                    "prompt": obj.prompt,
                    "answer": obj.answer,
                    "choices": list(obj.choices),
                }

            case MultipleChoiceLatToEngQuestion():
                return {
                    "question_type": "MultipleChoiceLatToEngQuestion",
                    "prompt": obj.prompt,
                    "answer": obj.answer,
                    "choices": list(obj.choices),
                }

            case ParseWordCompToLatQuestion():
                return {
                    "question_type": "ParseWordCompToLatQuestion",
                    "prompt": obj.prompt,
                    "components": obj.components.string,
                    "main_answer": obj.main_answer,
                    "answers": sorted(obj.answers),
                }

            case ParseWordLatToCompQuestion():
                return {
                    "question_type": "ParseWordLatToCompQuestion",
                    "prompt": obj.prompt,
                    "dictionary_entry": obj.dictionary_entry,
                    "main_answer": obj.main_answer.string,
                    "answers": [
                        obj.main_answer.string for answer in obj.answers
                    ],
                    # "main_answer": self.default(obj.main_answer),
                    # "answers": [self.default(answer) for answer in obj.answers],
                }

            case PrincipalPartsQuestion():
                return {
                    "question_type": "PrincipalPartsQuestion",
                    "prompt": obj.prompt,
                    "principal_parts": list(obj.principal_parts),
                }

            case TypeInEngToLatQuestion():
                return {
                    "question_type": "TypeInEngToLatQuestion",
                    "prompt": obj.prompt,
                    "main_answer": obj.main_answer,
                    "answers": sorted(obj.answers),
                }

            case TypeInLatToEngQuestion():
                return {
                    "question_type": "TypeInLatToEngQuestion",
                    "prompt": obj.prompt,
                    "main_answer": obj.main_answer,
                    "answers": sorted(obj.answers),
                }

        # this actually throws error
        return cast("dict[str, Any]", super().default(obj))


QuestionClassEncoder.__doc__ = JSONEncoder.__doc__
QuestionClassEncoder.default.__doc__ = JSONEncoder.default.__doc__
