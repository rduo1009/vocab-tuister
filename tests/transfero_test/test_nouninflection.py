# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import pytest
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, Number
from src.core.transfero.exceptions import InvalidComponentsError
from src.core.transfero.words import find_inflection, find_noun_inflections


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_noun_inflections("house", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER, degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid type: 'adjective'"


NOUN_COMBINATIONS = (
    (Case.NOMINATIVE, Number.SINGULAR),
    (Case.VOCATIVE, Number.SINGULAR),
    (Case.ACCUSATIVE, Number.SINGULAR),
    (Case.GENITIVE, Number.SINGULAR),
    (Case.DATIVE, Number.SINGULAR),
    (Case.ABLATIVE, Number.SINGULAR),
    (Case.NOMINATIVE, Number.PLURAL),
    (Case.VOCATIVE, Number.PLURAL),
    (Case.ACCUSATIVE, Number.PLURAL),
    (Case.GENITIVE, Number.PLURAL),
    (Case.DATIVE, Number.PLURAL),
    (Case.ABLATIVE, Number.PLURAL),
)


class TestNounInflection:
    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"house"},
        {"house"},
        {"house"},
        {"of the house", "house's", "of a house"},
        {"for the house", "to the house", "for a house", "to a house"},
        {"house", "with the house", "with a house", "by the house", "by a house", "by means of the house", "by means of a house"},
        {"houses"},
        {"houses"},
        {"houses"},
        {"of the houses", "houses'"},
        {"for the houses", "for houses", "to the houses", "to houses"},
        {"houses", "with the houses", "by the houses", "by means of the houses"},
    ])])  # fmt: skip
    def test_noun_inflections_1(self, case, number, expected):
        word = "house"
        assert find_inflection(word, EndingComponents(case=case, number=number)) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"cactus"},
        {"cactus"},
        {"cactus"},
        {"of the cactus", "cactus'", "of a cactus"},
        {"for the cactus", "to the cactus", "for a cactus", "to a cactus"},
        {"cactus", "with the cactus", "with a cactus", "by the cactus", "by a cactus", "by means of the cactus", "by means of a cactus"},
        {"cacti", "cactuses"},
        {"cacti", "cactuses"},
        {"cacti", "cactuses"},
        {"of the cacti", "cacti's", "of the cactuses", "cactuses'"},
        {"for the cacti", "for cacti", "to the cacti", "to cacti", "for the cactuses", "for cactuses", "to the cactuses", "to cactuses"},
        {"cacti", "with the cacti", "by the cacti", "by means of the cacti", "cactuses", "with the cactuses", "by the cactuses", "by means of the cactuses"},
    ])])  # fmt: skip
    def test_noun_inflections_2(self, case, number, expected):
        word = "cactus"
        assert find_inflection(word, EndingComponents(case=case, number=number)) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"apple"},
        {"apple"},
        {"apple"},
        {"of the apple", "apple's", "of an apple"},
        {"for the apple", "to the apple", "for an apple", "to an apple"},
        {"apple", "with the apple", "with an apple", "by the apple", "by an apple", "by means of the apple", "by means of an apple"},
        {"apples"},
        {"apples"},
        {"apples"},        
        {"of the apples", "apples'"},
        {"for the apples", "for apples", "to the apples", "to apples"},
        {"apples", "with the apples", "by the apples", "by means of the apples"},
    ])])  # fmt: skip
    def test_noun_inflections_3(self, case, number, expected):
        word = "apple"
        assert find_inflection(word, EndingComponents(case=case, number=number)) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "house", "house", "house", "of the house", "for the house", "by the house",
        "houses", "houses", "houses", "of the houses", "for the houses", "by the houses",
    ])])  # fmt: skip
    def test_main_noun_inflections_1(self, case, number, expected):
        word = "house"
        assert find_inflection(word, EndingComponents(case=case, number=number), main=True) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "cactus", "cactus", "cactus", "of the cactus", "for the cactus", "by the cactus",
        "cacti", "cacti", "cacti", "of the cacti", "for the cacti", "by the cacti",
    ])])  # fmt: skip
    def test_main_noun_inflections_2(self, case, number, expected):
        word = "cactus"
        assert find_inflection(word, EndingComponents(case=case, number=number), main=True) == expected

    @pytest.mark.parametrize(("case", "number", "expected"), [NOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "apple", "apple", "apple", "of the apple", "for the apple", "by the apple",
        "apples", "apples", "apples", "of the apples", "for the apples", "by the apples",
    ])])  # fmt: skip
    def test_main_noun_inflections_3(self, case, number, expected):
        word = "apple"
        assert find_inflection(word, EndingComponents(case=case, number=number), main=True) == expected
