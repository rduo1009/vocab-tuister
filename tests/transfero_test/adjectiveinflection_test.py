import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, Number
from src.core.transfero._adjective_inflection import find_adjective_inflections, find_main_adjective_inflection
from src.core.transfero.exceptions import InvalidComponentsError


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_adjective_inflections("happy", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER))
    assert str(error.value) == "Invalid type: 'pronoun'"

    with pytest.raises(InvalidComponentsError) as error:
        find_main_adjective_inflection("happy", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER))
    assert str(error.value) == "Invalid type: 'pronoun'"


def test_invalid_subtype():
    with pytest.raises(InvalidComponentsError) as error:
        find_adjective_inflections("happy", EndingComponents(degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid subtype: 'adverb'"

    with pytest.raises(InvalidComponentsError) as error:
        find_main_adjective_inflection("happy", EndingComponents(degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid subtype: 'adverb'"


ADJECTIVE_COMBINATIONS = (Degree.POSITIVE, Degree.COMPARATIVE, Degree.SUPERLATIVE)


@pytest.mark.parametrize(("degree", "expected"), [(ADJECTIVE_COMBINATIONS[i], form) for i, form in enumerate([
    {"happy"},
    {"happier", "more happy"},
    {"happiest", "most happy", "very happy", "extremely happy", "rather happy", "too happy", "quite happy"},
])])  # fmt: skip
def test_adjective_inflection(degree, expected):
    assert find_adjective_inflections("happy", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE, degree=degree)) == expected


@pytest.mark.parametrize(("degree", "expected"), [(ADJECTIVE_COMBINATIONS[i], form) for i, form in enumerate([
    "happy", "happier", "happiest",
])])  # fmt: skip
def test_adjective_main_inflection(degree, expected):
    assert find_main_adjective_inflection("happy", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE, degree=degree)) == expected


@pytest.mark.parametrize(("degree", "expected"), [(ADJECTIVE_COMBINATIONS[i], form) for i, form in enumerate([
    {"far"},
    {"farther", "further", "more far"},
    {"farthest", "furthest", "most far", "very far", "extremely far", "rather far", "too far", "quite far"},
])])  # fmt: skip
def test_adjective_inflection_multiple_superlatives(degree, expected):
    assert find_adjective_inflections("far", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE, degree=degree)) == expected


@pytest.mark.parametrize(("degree", "expected"), [(ADJECTIVE_COMBINATIONS[i], form) for i, form in enumerate([
    "interesting",
    "more interesting",
    "most interesting",
])])  # fmt: skip
def test_adjective_main_inflection_irregular(degree, expected):
    assert find_main_adjective_inflection("interesting", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.MASCULINE, degree=degree)) == expected
