# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, Number
from src.core.transfero._adverb_inflection import find_adverb_inflections, find_main_adverb_inflection
from src.core.transfero.exceptions import InvalidComponentsError


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_adverb_inflections("happily", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER))
    assert str(error.value) == "Invalid type: 'pronoun'"

    with pytest.raises(InvalidComponentsError) as error:
        find_main_adverb_inflection("happily", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER))
    assert str(error.value) == "Invalid type: 'pronoun'"


def test_invalid_subtype():
    with pytest.raises(InvalidComponentsError) as error:
        find_adverb_inflections("happily", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER, degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid subtype: 'None'"

    with pytest.raises(InvalidComponentsError) as error:
        find_main_adverb_inflection("happily", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER, degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid subtype: 'None'"


ADVERB_COMBINATIONS = (Degree.POSITIVE, Degree.COMPARATIVE, Degree.SUPERLATIVE)


class TestAdverbInflection:
    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        {"happily"},
        {"more happily"},
        {"most happily", "very happily", "extremely happily", "rather happily", "too happily", "quite happily"},
    ])])  # fmt: skip
    def test_adverb_inflection(self, degree, expected):
        word = "happily"
        assert find_adverb_inflections(word, EndingComponents(degree=degree)) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "happily", "more happily", "most happily",
    ])])  # fmt: skip
    def test_adverb_main_inflection(self, degree, expected):
        word = "happily"
        assert find_main_adverb_inflection(word, EndingComponents(degree=degree)) == expected
