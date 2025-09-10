# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import pytest
from src.core.accido.misc import Case, ComponentsSubtype, Degree, EndingComponents, Gender, Number
from src.core.transfero.exceptions import InvalidComponentsError
from src.core.transfero.words import find_adverb_inflections, find_inflection


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_adverb_inflections("happily", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER))
    assert str(error.value) == "Invalid type: 'pronoun'"


def test_invalid_subtype():
    a = EndingComponents(degree=Degree.POSITIVE)
    a.subtype = ComponentsSubtype.INFINITIVE

    with pytest.raises(InvalidComponentsError) as error:
        find_adverb_inflections("happy", a)
    assert str(error.value) == "Invalid subtype: 'infinitive'"


ADVERB_COMBINATIONS = (Degree.POSITIVE, Degree.COMPARATIVE, Degree.SUPERLATIVE)


class TestAdverbInflection:
    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        {"happily"},
        {"more happily"},
        {"most happily", "very happily", "extremely happily", "rather happily", "too happily", "quite happily"},
    ])])  # fmt: skip
    def test_adverb_inflection(self, degree, expected):
        word = "happy"
        assert find_inflection(word, EndingComponents(degree=degree)) == expected

    @pytest.mark.parametrize(("degree", "expected"), [(ADVERB_COMBINATIONS[i], form) for i, form in enumerate([
        "happily", "more happily", "most happily",
    ])])  # fmt: skip
    def test_adverb_main_inflection(self, degree, expected):
        word = "happy"
        assert find_inflection(word, EndingComponents(degree=degree), main=True) == expected
