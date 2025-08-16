"""Contains a custom encoder for converting some vocab-tester classes to JSON."""

# pyright: reportExplicitAny=false

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


class QuestionClassEncoder(JSONEncoder):
    def default(self, o: object) -> dict[str, Any]:
        match o:
            # NOTE: The tester tui currently uses the component string representation
            # case EndingComponents():
            #     ending_components_json = {}
            #     for key, value in o.__dict__.items():
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
                    "prompt": o.prompt,
                    "answer": o.answer,
                    "choices": list(o.choices),
                }

            case MultipleChoiceLatToEngQuestion():
                return {
                    "question_type": "MultipleChoiceLatToEngQuestion",
                    "prompt": o.prompt,
                    "answer": o.answer,
                    "choices": list(o.choices),
                }

            case ParseWordCompToLatQuestion():
                return {
                    "question_type": "ParseWordCompToLatQuestion",
                    "prompt": o.prompt,
                    "components": o.components.string,
                    "main_answer": o.main_answer,
                    "answers": sorted(o.answers),
                }

            case ParseWordLatToCompQuestion():
                return {
                    "question_type": "ParseWordLatToCompQuestion",
                    "prompt": o.prompt,
                    "dictionary_entry": o.dictionary_entry,
                    "main_answer": o.main_answer.string,
                    "answers": sorted([answer.string for answer in o.answers]),
                    # "main_answer": self.default(obj.main_answer),
                    # "answers": [self.default(answer) for answer in obj.answers],
                }

            case PrincipalPartsQuestion():
                return {
                    "question_type": "PrincipalPartsQuestion",
                    "prompt": o.prompt,
                    "principal_parts": list(o.principal_parts),
                }

            case TypeInEngToLatQuestion():
                return {
                    "question_type": "TypeInEngToLatQuestion",
                    "prompt": o.prompt,
                    "main_answer": o.main_answer,
                    "answers": sorted(o.answers),
                }

            case TypeInLatToEngQuestion():
                return {
                    "question_type": "TypeInLatToEngQuestion",
                    "prompt": o.prompt,
                    "main_answer": o.main_answer,
                    "answers": sorted(o.answers),
                }

            case _:
                pass

        # this actually throws error
        return cast("dict[str, Any]", super().default(o))


QuestionClassEncoder.__doc__ = JSONEncoder.__doc__
QuestionClassEncoder.default.__doc__ = JSONEncoder.default.__doc__
