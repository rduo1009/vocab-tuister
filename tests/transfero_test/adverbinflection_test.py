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


def test_adverb_inflection():
    word = "happily"
    assert find_adverb_inflections(word, EndingComponents(degree=Degree.POSITIVE)) == {"happily"}
    assert find_adverb_inflections(word, EndingComponents(degree=Degree.COMPARATIVE)) == {"more happily"}
    assert find_adverb_inflections(word, EndingComponents(degree=Degree.SUPERLATIVE)) == {"most happily", "very happily", "extremely happily", "rather happily", "too happily", "quite happily"}


def test_adverb_main_inflection():
    word = "happily"
    assert find_main_adverb_inflection(word, EndingComponents(degree=Degree.POSITIVE)) == "happily"
    assert find_main_adverb_inflection(word, EndingComponents(degree=Degree.COMPARATIVE)) == "more happily"
    assert find_main_adverb_inflection(word, EndingComponents(degree=Degree.SUPERLATIVE)) == "most happily"
