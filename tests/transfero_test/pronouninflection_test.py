# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportMissingParameterType=false

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.core.accido.misc import Case, Degree, EndingComponents, Gender, Number
from src.core.transfero.exceptions import InvalidComponentsError
from src.core.transfero.words import find_inflection


def test_invalid_type():
    with pytest.raises(InvalidComponentsError) as error:
        find_inflection("house", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER, degree=Degree.POSITIVE))
    assert str(error.value) == "Invalid type: 'adjective'"

    with pytest.raises(InvalidComponentsError) as error:
        find_inflection("house", EndingComponents(case=Case.NOMINATIVE, number=Number.SINGULAR, gender=Gender.NEUTER, degree=Degree.POSITIVE), main=True)
    assert str(error.value) == "Invalid type: 'adjective'"


PRONOUN_COMBINATIONS = (
    (Case.NOMINATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.VOCATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.ACCUSATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.GENITIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.DATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.ABLATIVE, Number.SINGULAR, Gender.MASCULINE),
    (Case.NOMINATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.VOCATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.ACCUSATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.GENITIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.DATIVE, Number.PLURAL, Gender.MASCULINE),
    (Case.ABLATIVE, Number.PLURAL, Gender.MASCULINE),
)


class TestPronounInflection:
    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"this"},
        {"this"},
        {"this"},
        {"of this"},
        {"for this", "to this"},
        {"by this", "by means of this", "with this", "this"},
        {"these"},
        {"these"},
        {"these"},
        {"of these"},
        {"for these", "to these"},
        {"by these", "by means of these", "with these", "these"},
    ])])  # fmt: skip
    def test_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("this", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "this", "this", "this", "of this", "for this", "by this",
        "these", "these", "these", "of these", "for these", "by these",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("this", EndingComponents(case=case, number=number, gender=gender), main=True) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"that"},
        {"that"},
        {"that"},
        {"of that"}, 
        {"for that", "to that"}, 
        {"by that", "by means of that", "with that", "that"},
        {"those"},
        {"those"},
        {"those"},
        {"of those"},
        {"for those", "to those"},
        {"by those", "by means of those", "with those", "those"},
    ])])  # fmt: skip
    def test_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("that", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "that", "that", "that", "of that", "for that", "by that",
        "those", "those", "those", "of those", "for those", "by those",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("that", EndingComponents(case=case, number=number, gender=gender), main=True) == expected


class TestNounlikePronounInflection:
    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"I"},
        {"I"},
        {"me"},
        {"of me", "my"},
        {"for me", "to me"},
        {"me", "with me", "by me", "by means of me"},
        {"we"},
        {"we"},
        {"us"},
        {"of us", "our"},
        {"for us", "to us"},
        {"us", "with us", "by us", "by means of us"},
    ])])  # fmt: skip
    def test_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("I", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "I", "I", "me", "of me", "for me", "by me",
        "we", "we", "us", "of us", "for us", "by us",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_1(self, case, number, gender, expected):
        assert find_inflection("I", EndingComponents(case=case, number=number, gender=gender), main=True) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        {"you"},
        {"you"},
        {"you"},
        {"of you", "your"},
        {"for you", "to you"},
        {"you", "with you", "by you", "by means of you"},
        {"you"},
        {"you"},
        {"you"},
        {"of you", "your"},
        {"for you", "to you"},
        {"you", "with you", "by you", "by means of you"},
    ])])  # fmt: skip
    def test_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("you", EndingComponents(case=case, number=number, gender=gender)) == expected

    @pytest.mark.parametrize(("case", "number", "gender", "expected"), [PRONOUN_COMBINATIONS[i] + (form,) for i, form in enumerate([
        "you", "you", "you", "of you", "for you", "by you",
        "you", "you", "you", "of you", "for you", "by you",
    ])])  # fmt: skip
    def test_main_pronoun_inflections_2(self, case, number, gender, expected):
        assert find_inflection("you", EndingComponents(case=case, number=number, gender=gender), main=True) == expected

    # NOTE: No nominative, so cannot parametrize probably
    def test_pronoun_inflections_3(self):
        word = "oneself"

        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.SINGULAR)) == {"oneself"}
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.SINGULAR)) == {"of the oneself", "oneself's"}
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.SINGULAR)) == {"to oneself", "for oneself"}
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.SINGULAR)) == {"by oneself", "with oneself", "from oneself", "in oneself", "on oneself"}
        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL)) == {"themselves"}
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.PLURAL)) == {"of the themselves", "themselves'"}
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.PLURAL)) == {"to themselves", "for themselves"}
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.PLURAL)) == {"by themselves", "with themselves", "from themselves", "in themselves", "on themselves"}

    def test_main_pronoun_inflections_3(self):
        word = "oneself"

        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.SINGULAR), main=True) == "oneself"
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.SINGULAR), main=True) == "of the oneself"
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.SINGULAR), main=True) == "to oneself"
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.SINGULAR), main=True) == "by oneself"
        assert find_inflection(word, EndingComponents(case=Case.ACCUSATIVE, number=Number.PLURAL), main=True) == "themselves"
        assert find_inflection(word, EndingComponents(case=Case.GENITIVE, number=Number.PLURAL), main=True) == "of the themselves"
        assert find_inflection(word, EndingComponents(case=Case.DATIVE, number=Number.PLURAL), main=True) == "to themselves"
        assert find_inflection(word, EndingComponents(case=Case.ABLATIVE, number=Number.PLURAL), main=True) == "by themselves"
